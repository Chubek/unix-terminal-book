# Chapter 41 — Back Up and Restore Documents

- `TMPDIR=/mnt/nvme sh listings/chapter-41/check-restore.sh` passed on
  Linux x86-64 with GNU tar 1.35 and again with bsdtar 3.8.9 selected
  temporarily as `tar`. Both runs checked scoped member lists and
  checksum records, extracted each dated version in its own folder, read
  the intended updates, and compared a constant file. The two dated
  plans differed while the live file still matched Tuesday. No user's
  documents or backup device were touched.
- POSIX `cksum` default output and GNU tar/FreeBSD tar documentation
  are linked. A Linux libarchive test is not a FreeBSD, NetBSD,
  OpenBSD or macOS machine test. Extended metadata, encrypted storage,
  separate devices and real failure recovery were not tested.
- `figures/chapter-41/`: `history.tikz`, `versions.tikz`, `drill.tikz`.
  Slice build and grayscale check: see `chapter-37.md`.
- Revision check: both tar implementations passed again with the
  explicit `mktemp` template and nvme test scratch. The revised
  print/answers and screen/noanswers slice builds both retained
  concrete cleanup steps outside the solutions.
