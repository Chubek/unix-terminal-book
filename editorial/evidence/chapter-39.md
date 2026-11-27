# Chapter 39 — Transfer Files Between Machines

- `TMPDIR=/mnt/nvme sh listings/chapter-39/check-transfer.sh` passed on
  Linux x86-64 with upstream rsync 3.5.0-g471e17dc (protocol 32).
  Dry runs predicted `agenda.txt` versus `source/agenda.txt` without
  writing either. The local `cp` copy matched byte-for-byte; the
  synthetic different version gave `cmp` status 1. Only known fixture
  files were removed in cleanup.
- OpenSSH `scp(1)` and `sftp(1)` document endpoint syntax, interactive
  commands and protocol defaults; rsync's upstream manual documents
  itemized output and source-slash behavior. No remote transfer or
  remote preview was attempted. SFTP exchange is illustrative. macOS and
  BSD rsync implementations/versions were not available for execution.
- Revision check: reran local previews/comparisons and verified the
  printed setup's success and failure branches on Linux. The `scp`
  and SFTP example sequences are alternatives, not sequential uploads.
- `figures/chapter-39/`: `direction.tikz`, `sftp.tikz`, `contents.tikz`.
  Slice build and grayscale check: see `chapter-37.md`.
