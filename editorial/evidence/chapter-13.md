# Chapter 13 — Anatomy of a Command

- Executable fixture/check: `sh listings/chapter-13/compare-drafts.sh`.
- Actual: EndeavourOS Linux 6.18.52-1-lts, x86-64; `/bin/sh` links to
  Bash 5.3.15, also tested as `bash`; GNU diffutils 3.12 and coreutils
  9.11. Both invocations passed. `cmp -s` returned 0/1/2 for equal,
  different, and missing. GNU `head` accepted both `./-revised.txt`
  and `-- -revised.txt`. Fixtures lived in new private directories
  under a dedicated NVMe `TMPDIR`.
- Manual checks: POSIX.1-2024 [cmp](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/cmp.html)
  specifies 0/1/>1; the diagnostic on an error with `-s` is unspecified.
  The Utility Syntax Guidelines describe the option delimiter; do not
  assume every program implements it. NetBSD's
  [mktemp](https://man.netbsd.org/mktemp.1) documents the default
  template and directory option; `mktemp` is not defined by POSIX.
- Layout: see `chapter-18.md`. No macOS/BSD execution.
