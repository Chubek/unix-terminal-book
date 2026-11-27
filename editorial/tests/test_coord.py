"""Exercise the broker in a throwaway repository, not the live queue."""

import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "editorial/coord.py"


class BrokerTest(unittest.TestCase):
    def setUp(self):
        build = ROOT / "build"
        build.mkdir(exist_ok=True)
        temp = tempfile.TemporaryDirectory(dir=build, prefix="broker-")
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        self.broker, self.one, self.two = (root / name for name in ("main", "one", "two"))
        self.broker.mkdir()
        self.git("init", "-b", "utp/integration")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null",
                 "commit", "--allow-empty", "-m", "Fixture")
        self.git("worktree", "add", "-b", "utp/W1", str(self.one))
        self.git("worktree", "add", "-b", "utp/W2", str(self.two))

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.broker, check=True, capture_output=True)

    def call(self, where, *args, ok=True):
        proc = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=where, text=True, capture_output=True)
        self.assertEqual(proc.returncode == 0, ok, proc.stderr)
        return proc.stdout.strip()

    def rows(self, where, *args):
        return json.loads(self.call(where, *args))

    def test_routing_and_correlation(self):
        identity = self.call(self.one, "send", "W2", "question", "Fixture?")
        self.assertEqual(self.rows(self.two, "inbox"), [])
        self.call(self.two, "route", ok=False)
        self.call(self.broker, "route")
        self.assertEqual(self.rows(self.one, "inbox"), [])
        first, = self.rows(self.two, "inbox")
        self.assertEqual((first["message_id"], first["sender"], first["recipient"]), (identity, "W1", "W2"))
        self.call(self.one, "ack", identity, ok=False)
        self.call(self.two, "ack", identity)
        self.assertEqual(self.call(self.two, "ack", identity), "")
        self.call(self.two, "send", "W0", "answer", "Wrong route", "--reply-to", identity, ok=False)
        self.call(self.two, "send", "W1", "answer", "Yes.", "--reply-to", identity)
        self.call(self.broker, "route")
        ack, reply = self.rows(self.one, "inbox")
        self.assertEqual(ack["type"], "ack")
        self.assertEqual((reply["correlation_id"], reply["reply_to"], reply["payload"]), (identity, identity, "Yes."))

    def test_checkpoint_ownership_and_cas(self):
        key = "W1/progress"
        word = '{"state":"drafting","artifacts":[],"blockers":[]}'
        rev = self.call(self.one, "publish", key, word)
        self.call(self.two, "publish", key, word, "--expect", rev, ok=False)
        self.call(self.one, "publish", key, word, ok=False)
        self.call(self.one, "publish", key, word.replace("drafting", "review"), "--expect", rev)
        self.assertEqual([r["value"]["state"] for r in self.rows(self.two, "history", key)], ["drafting", "review"])

    def test_retry_keeps_identity(self):
        identity = self.call(self.broker, "send", "W1", "assignment", "Fixture")
        self.call(self.broker, "route")
        db_file = self.broker / ".git/utp-coordination.sqlite3"
        # Backdate delivery in this test database to exercise timeout promptly.
        for _ in range(3):
            with sqlite3.connect(db_file) as db:
                db.execute("UPDATE messages SET delivered=0 WHERE message_id=?", (identity,))
            self.call(self.broker, "route")
        row, = self.rows(self.broker, "ledger")
        self.assertEqual((row["message_id"], row["attempts"], row["state"]), (identity, 3, "timeout"))
        self.call(self.broker, "requeue", identity)
        self.call(self.broker, "route")
        row, = self.rows(self.one, "inbox")
        self.assertEqual((row["message_id"], row["attempts"], row["state"]), (identity, 1, "delivered"))


if __name__ == "__main__":
    unittest.main()
