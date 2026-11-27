#!/usr/bin/env python3
"""W0's local broker and shared, versioned coordination store."""

import argparse
import json
import sqlite3
import subprocess
import time
import uuid
from pathlib import Path

WORKERS = tuple(f"W{i}" for i in range(9))
TYPES = {"assignment", "ack", "question", "answer", "review", "request", "escalation"}
STATES = {"planned", "drafting", "review", "revision", "verified", "integrated", "blocked"}
BRANCHES = {"utp/integration": "W0", **{f"utp/{w}": w for w in WORKERS[1:]}}
SCHEMA = """
CREATE TABLE IF NOT EXISTS messages(
 message_id TEXT PRIMARY KEY, sender TEXT NOT NULL, recipient TEXT NOT NULL,
 type TEXT NOT NULL, correlation_id TEXT NOT NULL, timestamp INTEGER NOT NULL,
 payload TEXT NOT NULL, reply_to TEXT REFERENCES messages(message_id),
 state TEXT NOT NULL DEFAULT 'queued', attempts INTEGER NOT NULL DEFAULT 0,
 delivered INTEGER, acknowledged INTEGER
);
CREATE TABLE IF NOT EXISTS revisions(
 revision INTEGER PRIMARY KEY, key TEXT NOT NULL, owner TEXT NOT NULL,
 timestamp INTEGER NOT NULL, value TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS revision_key ON revisions(key, revision DESC);
"""


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def dump(value):
    print(json.dumps(value, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    for command in ("route", "inbox", "ledger", "state"):
        commands.add_parser(command)
    send = commands.add_parser("send")
    send.add_argument("recipient", choices=WORKERS)
    send.add_argument("type", choices=sorted(TYPES - {"ack"}))
    send.add_argument("payload")
    send.add_argument("--reply-to")
    ack = commands.add_parser("ack")
    ack.add_argument("message_id")
    retry = commands.add_parser("requeue")
    retry.add_argument("message_id")
    publish = commands.add_parser("publish")
    publish.add_argument("key")
    publish.add_argument("json_value", help="JSON string, or @path to a JSON file")
    publish.add_argument("--expect", type=int, default=0, help="last revision; 0 for new key")
    history = commands.add_parser("history")
    history.add_argument("key")
    args = parser.parse_args()

    actor = BRANCHES.get(git("branch", "--show-current"))
    if actor is None:
        parser.error("run in your assigned worktree")
    if args.action in {"route", "ledger", "requeue"} and actor != "W0":
        parser.error("only W0 can perform this operation")
    db_path = Path(git("rev-parse", "--path-format=absolute", "--git-common-dir")) / "utp-coordination.sqlite3"
    db = sqlite3.connect(db_path, timeout=30)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    db.executescript(SCHEMA)
    now = int(time.time())
    with db:
        db.execute("BEGIN IMMEDIATE")
        if args.action in {"send", "ack"}:
            reply = args.reply_to if args.action == "send" else args.message_id
            parent = db.execute("SELECT * FROM messages WHERE message_id=?", (reply,)).fetchone()
            if reply and (not parent or parent["recipient"] != actor or parent["state"] not in {"delivered", "acknowledged"}):
                parser.error("reply must refer to a message delivered to your inbox")
            if args.action == "ack":
                if parent["acknowledged"] is not None:
                    return
                recipient, kind, payload = parent["sender"], "ack", "Received"
                db.execute("UPDATE messages SET state='acknowledged', acknowledged=? WHERE message_id=?", (now, reply))
            else:
                recipient, kind, payload = args.recipient, args.type, args.payload
            if recipient == actor or (parent and recipient != parent["sender"]):
                parser.error("invalid destination for this message")
            identity = uuid.uuid4().hex
            correlation = parent["correlation_id"] if parent else identity
            db.execute(
                "INSERT INTO messages(message_id,sender,recipient,type,correlation_id,timestamp,payload,reply_to) "
                "VALUES (?,?,?,?,?,?,?,?)", (identity, actor, recipient, kind, correlation, now, payload, reply)
            )
            print(identity)
        elif args.action == "route":
            # Retrying changes delivery metadata, never creates a second envelope.
            db.execute("UPDATE messages SET state='timeout' WHERE state='delivered' AND attempts>=3 AND delivered<=?", (now-900,))
            changed = db.execute(
                "UPDATE messages SET state=CASE WHEN type='ack' THEN 'acknowledged' ELSE 'delivered' END, "
                "delivered=?, attempts=attempts+1 WHERE state='queued' OR (state='delivered' AND delivered<=?)",
                (now, now-900),
            )
            print(f"Routed or retried {changed.rowcount} messages")
        elif args.action == "requeue":
            changed = db.execute(
                "UPDATE messages SET state='queued', attempts=0, delivered=NULL WHERE message_id=? AND state='timeout'",
                (args.message_id,),
            )
            if not changed.rowcount:
                parser.error("only a timed-out envelope can be requeued")
        elif args.action == "inbox":
            rows = db.execute(
                "SELECT * FROM messages WHERE recipient=? AND state IN ('delivered','acknowledged') ORDER BY timestamp,rowid",
                (actor,),
            )
            dump([dict(row) for row in rows])
        elif args.action == "ledger":
            dump([dict(row) for row in db.execute("SELECT * FROM messages ORDER BY timestamp,rowid")])
        elif args.action == "publish":
            if not args.key or (actor != "W0" and not args.key.startswith(actor + "/")):
                parser.error("workers publish only below their own Wn/ namespace")
            data = json.loads(Path(args.json_value[1:]).read_text() if args.json_value.startswith("@") else args.json_value)
            prior = db.execute("SELECT max(revision) FROM revisions WHERE key=?", (args.key,)).fetchone()[0] or 0
            if args.expect != prior:
                parser.error(f"revision conflict; current revision is {prior}")
            if args.key.endswith("/progress") and (
                not isinstance(data, dict) or data.get("state") not in STATES
                or not isinstance(data.get("artifacts"), list) or not isinstance(data.get("blockers"), list)
            ):
                parser.error("progress requires state, artifacts list, and blockers list")
            cursor = db.execute(
                "INSERT INTO revisions(key,owner,timestamp,value) VALUES (?,?,?,?)",
                (args.key, actor, now, json.dumps(data)),
            )
            print(cursor.lastrowid)
        elif args.action in {"state", "history"}:
            if args.action == "state":
                rows = db.execute("SELECT * FROM revisions WHERE revision IN (SELECT max(revision) FROM revisions GROUP BY key) ORDER BY key")
            else:
                rows = db.execute("SELECT * FROM revisions WHERE key=? ORDER BY revision", (args.key,))
            dump([dict(row) | {"value": json.loads(row["value"])} for row in rows])


if __name__ == "__main__":
    main()
