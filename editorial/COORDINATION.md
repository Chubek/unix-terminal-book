# Coordination and handoff

W0 is the parent runtime session, on `utp/integration`. Eight child
runtime sessions work on branches `utp/W1`–`utp/W8`, in the corresponding
worktrees under `/mnt/nvme/my-books/.utp-workers/`. Only W0 edits shared
integration files. Each author commits only their assigned chapter
fragments and associated assets, listings and test evidence. Keep `master`
untouched. Do not publish to a remote.

## Common state and directed messages

`python3 editorial/coord.py state` reads the common store. The SQLite
database is `utp-coordination.sqlite3` in Git's common directory, shared
by the worktrees and outside the manuscript. An SQLite transaction
serializes changes, `publish --expect REVISION` prevents stale overwrites,
and `history KEY` reads checkpoints. Branch identity binds the local
client to its worker role; this is cooperative local IPC, not a security
boundary against someone with write access to the shared Git directory.

Use `publish Wn/progress '{"state":"drafting","artifacts":[],"blockers":[]}'`
for the first checkpoint; use `--expect` for subsequent updates. Put
public requests for pairing in `Wn/open-requests`, and publication-ready
asset and label inventories in `Wn/assets` and `Wn/xrefs`. W0 owns the
aggregated registries and announces reviewer pairings there. Do not put
the content of a private request or review in the common store.

`send W7 question '…'` submits an envelope to W0, not to W7 directly.
Only W0 runs `route`. From the delivery inbox, `ack MESSAGE_ID` confirms
receipt, and `send W5 answer '…' --reply-to MESSAGE_ID` sends a correlated
substantive reply when W5 was the sender. Acknowledging and replying are
separate operations. W0 inspects the `ledger` at handoff boundaries and
routes pending work before waking its intended recipient. An unacknowledged
delivery gets up to three attempts, at 15-minute intervals when W0
services the route. The same envelope ID is kept across attempts. W0
investigates a timeout and can `requeue MESSAGE_ID` after resolving it.

## Peer review and release

W0 sends the reviewer named in `chapters/MANIFEST.json` a chapter number,
author commit, and requested checks. Reviewers read the commit without
checking out or editing an author's worktree. They return concrete issues
or an explicit approval via the broker, and include test limitations.
W0 sends substantive issues back to the owner for revision and asks the
reviewer to check the new commit. W0 writes the durable review receipt in
`editorial/reviews/chapter-N.md` with reviewer, reviewed commit, findings
and outcome. A chapter may enter `verified` only after that review and
its own evidence record pass, then `integrated` after the W0 import.

If a worker stops before delivery, preserve their branch and checkpoint.
Review the common progress state and directed messages for unresolved
dependencies. Resume the same runtime session where possible. If work needs
reassignment, W0 records the old owner, new owner, reason and exact branch
tip before granting write ownership. Cannot resolve a dependency? Mark
the affected chapter `blocked` rather than fabricating a review or skipping
the release check.
