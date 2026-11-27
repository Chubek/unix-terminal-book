# Chapter 44 — Make the Terminal Accessible

- Linux 6.18.52 on EndeavourOS, GNU grep 3.12-modified and coreutils:
  confirmed initial line count, numbered matches, bounded rereads and
  explicit no-match message. Verified separate missing-file diagnostic,
  done line, and cleanup under Bash 5.3.15, its POSIX `/bin/sh` mode,
  and Zsh 5.9.2.
- Injected a failing `mktemp` under each tested shell: the separate setup
  block returned one with no output and never called `cd`.
- Plan for reader trials is intentionally application-specific. No real
  screen reader, braille device, macOS/BSD terminal, or desktop
  preference changes tested. Apple and Orca documentation links are for
  readers; prose does not assert feature parity or access compliance.
- Reproduce offline checks with
  `TMPDIR=/mnt/nvme python3 editorial/evidence/check-w8-offline.py`.
