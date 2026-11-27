# Chapter 9 — author validation

- Source: `chapters/chapter-9.ltx`; TikZ: `figures/chapter-9/search.tikz` (boundary, predicates and quoting).
- Reproducer: `listings/chapter-9/check-records.sh`; use `TMPDIR` set to private, absolute scratch. The script measures counts because traversal order is not a portable contract.
- Passed on Arch Linux 6.18.52-1-lts, GNU Findutils 4.11.0, Bash 5.3.15 as `/bin/sh` and native Bash, and Zsh 5.9.2 (`-f`).
- Checked: exact and glob matching, a directory named like a file, a regular file whose name has a space, traversal under a hidden parent, limited starting path, shell expansion of the unquoted pattern, absent match with successful search, and a missing start with an unsuccessful search.
- Local POSIX and GNU manuals consulted. No BSD/macOS execution or runtime check of unreadable or concurrently modified trees. Output order in prose is not asserted.
- Pending non-author review and integrated release.
