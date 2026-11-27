# Chapter 47 — Capstone: Organize Photos and Their Catalog

- Linux 6.18.52, Python 3.14.7, Bash 5.3.15 (including `/bin/sh`
  mode), and Zsh 5.9.2. Checked JSON field values and planned paths from
  the quoted CSV; invalid album exits one from the converter; both staged
  copies match; a deliberately wrong pair differs; the canal checksums
  agree; explicit cleanup leaves no fixture files.
- No real photographs or arbitrary media opened; no metadata removed.
  Python 3.8 is a conservative minimum for the listing, not a second
  tested interpreter. No runtime test of macOS or BSD filesystems and
  no attempt to generalize the deliberately limited basename policy.
- Reproduce offline checks with
  `TMPDIR=/mnt/nvme python3 editorial/evidence/check-w8-offline.py`.
