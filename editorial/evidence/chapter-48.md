# Chapter 48 — Capstone: Deliver and Restore a Remote Backup

- Linux 6.18.52: offline archive creation, inventory, local delivery
  and retrieval, returned bundle comparison, restore to a clean target,
  both document comparisons and the negative wrong-path check passed.
  Tested GNU tar 1.35 and libarchive bsdtar 3.8.9 on the same Linux
  host under Bash 5.3.15, its `/bin/sh` mode, and Zsh 5.9.2. The tar
  programs were tested separately, not as a cross-system interchange.
- Verified OpenSSH 10.5p1 `sftp(1)` command syntax locally. The SFTP
  sequence is illustrative and runs only with the reader's authorization;
  no host contacted and no server replies or security tests claimed.
  No macOS or BSD runtime tests, ACL restoration, remote persistence or
  actual incident recovery tested.
- Reproduce offline checks with
  `TMPDIR=/mnt/nvme python3 editorial/evidence/check-w8-offline.py`.
