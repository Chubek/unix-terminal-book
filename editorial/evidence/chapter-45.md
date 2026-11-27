# Chapter 45 — Troubleshoot One Layer at a Time

- Linux 6.18.52, Bash 5.3.15, Bash as `/bin/sh`, Zsh 5.9.2:
  reproduced explicit command lookup miss, direct execution of the
  toy helper, wrong-directory read failure, corrected paths, access
  check, separate captured diagnostic, and cleanup. `stty -a` inspected
  only a disposable pseudo-terminal. Terminal flow-control and
  `stty sane` recovery notes are conditional; no actual terminal modes
  were changed. See local `stty(1)`.
- No remote connections, host-key failures, app-specific shortcut
  behavior, or macOS/BSD systems tested. No credentials were used.
- Reproduce offline checks with
  `TMPDIR=/mnt/nvme python3 editorial/evidence/check-w8-offline.py`.
