# Chapter 43 — Customize a Session Safely

- Linux 6.18.52 on EndeavourOS: Bash 5.3.15 interactive with startup
  bypass; confirmed same-shell alias expansion, removal of the alias,
  child inheritance after export and one-command assignment. POSIX-mode
  Bash (`/bin/sh`) syntax-checked the candidate.
- Zsh 5.9.2 with `-f -i -s`: verified the alias with the candidate and
  invocation on separate input lines. Zsh `-ic` parsing is not equivalent
  to entering those lines separately. Local `zsh(1)` documents global
  zshenv and user startup ordering.
- No personal startup files modified. Fish, macOS, FreeBSD, OpenBSD,
  NetBSD and site-managed startup behavior not runtime-tested.
- Reproducible example checks: `TMPDIR=/mnt/nvme python3 editorial/evidence/check-w8-offline.py`.
  This harness checks the candidate and export examples, not a real
  change to login settings or GUI launch options.
