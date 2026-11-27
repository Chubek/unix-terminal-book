# Chapter 17 — Build a Pipeline

- Executable check: `sh listings/chapter-17/count-boxes.sh`.
- Actual: Linux host in `chapter-13.md`. Pipeline and `tee` checks
  passed with `sh` and `bash`: three rows, intermediate rows identical
  to directly redirected rows, and successful count of an empty
  stream after a missing file. Targeted tests in `sh`, Bash and Zsh
  5.9.2 showed the failed producer still led to a count of zero;
  status changed from 0 to 1 with `pipefail`.
- Manual checks: POSIX.1-2024 §2.9.2 specifies `pipefail`, so its
  earlier non-standard status must be qualified by edition. FreeBSD
  15.1 [`tail(1)`](https://man.freebsd.org/cgi/man.cgi?query=tail&sektion=1)
  documents `-n +N` from the beginning of the file.
- No macOS/BSD execution. Layout: see `chapter-18.md`.
