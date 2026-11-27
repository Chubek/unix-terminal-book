#!/usr/bin/env python3
"""Write pending chapter receipts from W0-selected, delivered broker replies."""

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("selection", type=Path, help="TSV: chapter, integrated source, message ID, disposition summary")
    args = parser.parse_args()
    data = json.loads((ROOT / "chapters/MANIFEST.json").read_text())
    messages = json.loads(subprocess.check_output(
        ["python3", "editorial/coord.py", "ledger"], cwd=ROOT, text=True
    ))
    replies = {x["message_id"]: x for x in messages if (
        x["type"] == "answer" and x["recipient"] == "W0" and x["state"] == "acknowledged"
        or x["type"] == "answer" and x["recipient"] == "W0" and x["state"] == "delivered"
    )}
    selections = []
    for line in args.selection.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        n, commit, msg_id, summary = line.split("\t", maxsplit=3)
        c = data["chapters"][int(n) - 1]
        reply = replies[msg_id]
        if c["reviewer"] != reply["sender"] or c["owner"] == reply["sender"]:
            raise SystemExit(f"Chapter {n}: receipt must come from the assigned non-author reviewer")
        if c["status"] not in {"review", "revision", "verified"}:
            raise SystemExit(f"Chapter {n}: not awaiting review import")
        if not any(word in reply["payload"].lower() for word in ("approve", "pass")):
            raise SystemExit(f"Chapter {n}: review reply does not cite approval or passing outcome")
        revision = subprocess.check_output(
            ["git", "rev-parse", "--verify", commit + "^{commit}"], cwd=ROOT, text=True
        ).strip()
        selections.append((n, revision, msg_id, summary, c))
    for n, rev, msg_id, summary, c in selections:
        target = ROOT / "editorial/reviews" / f"chapter-{n}.md"
        with target.open("x") as f:
            f.write(f"# Chapter {n} — approved\n\n"
                    f"- Author: {c['owner']}; non-author reviewer: {c['reviewer']}.\n"
                    f"- Integrated source: `{rev}`.\n"
                    f"- Broker reply: `{msg_id}`.\n\n"
                    f"{summary}\n")


if __name__ == "__main__":
    main()
