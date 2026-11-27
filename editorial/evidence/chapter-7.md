# Chapter 7 — author validation

- Source: `chapters/chapter-7.ltx`; TikZ: `figures/chapter-7/operations.tikz` (copy, destination and move figures).
- Reproducer: `listings/chapter-7/check-rota.sh`; invoke with `TMPDIR` set to an existing, private, absolute scratch directory. It creates and removes only its named fixtures.
- Passed in GNU/Linux 6.18.52-1-lts, Arch Linux, Bash 5.3.15 as `/bin/sh` and native Bash, plus Zsh 5.9.2 (`-f`). GNU Coreutils 9.11, GNU Diffutils 3.12, and `file` 5.48.
- Checked: source retained by a copy; both existing-directory and explicit-file destinations; old working name absent after move; equality and difference status; a declined interactive copy leaves the ready copy unchanged. On this GNU release a declined overwrite returned 1, not 0.
- The common utility semantics were cross-checked against the installed POSIX programmer's manuals where present and against GNU local manuals. macOS, FreeBSD, OpenBSD and NetBSD behavior is documentation-based or expected under the specified POSIX subsets; no runtime coverage of those systems, cross-filesystem moves, or metadata preservation.
- Pending non-author review and the integrated release build.
