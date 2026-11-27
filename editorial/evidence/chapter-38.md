# Chapter 38 — Sign In Safely with SSH

- Linux x86-64, OpenSSH 10.5p1/OpenSSL 3.6.4:
  `TMPDIR=/mnt/nvme sh listings/chapter-38/check-key-lab.sh` passed.
  With explicit empty configuration and `-G -T`, both fictional
  destinations printed the intended host, user and port. A new,
  disposable Ed25519 public file produced a stable fingerprint with the
  synthetic comment. The private fixture was never used to authenticate
  or installed into any account; both fixture files were removed.
- No connections, remote sign-ins or host-key persistence tests were
  run. The prompt and remote shell output are explicitly illustrative.
  The OpenSSH manuals are primary sources for the non-POSIX utilities.
  Availability and defaults on macOS and the BSDs were not tested.
- `figures/chapter-38/`: `destination.tikz`, `identity.tikz`,
  `shells.tikz`. Slice build and grayscale check: see `chapter-37.md`.
- Revision check: the explicit `mktemp` template was rerun with the
  test scratch directory on nvme. An invalid template stopped its
  `&&` chain before the subsequent commands. The print/answers and
  screen/noanswers slice builds both retained the exact fixture cleanup.
