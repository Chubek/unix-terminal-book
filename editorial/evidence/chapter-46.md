# Chapter 46 — Build a Daily Terminal Routine

- Linux 6.18.52, GNU grep 3.12-modified, GNU diffutils 3.12, C locale.
  Confirmed case-insensitive literal match, numbered source lines,
  no match, same-file zero and unified-diff difference status one,
  quoted phrase input, and a deliberately missing input stopping the
  routine (exit two without attempting the comparison). The harness
  ran the fixtures under Bash 5.3.15, its `/bin/sh` POSIX mode,
  and Zsh 5.9.2. The supplied script itself was invoked via `sh`.
- A simulated `mktemp` failure returned one and did not call `cd`; the
  notes and handoff writes are in separate blocks.
- Header timestamp fields vary. No macOS/BSD systems or non-C locale
  semantics tested; non-ASCII case matching is flagged as locale-sensitive.
- Reproduce offline checks with
  `TMPDIR=/mnt/nvme python3 editorial/evidence/check-w8-offline.py`.
