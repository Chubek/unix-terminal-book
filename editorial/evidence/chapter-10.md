# Chapter 10 — author validation

- Source: `chapters/chapter-10.ltx`; TikZ: `figures/chapter-10/documentation.tikz` (pager, sections and help-source decision).
- `listings/chapter-10/check-manual.sh` exercises local page resolution, keyword searches, command identity reports, and a declined `cp -i` with empty scratch fixtures. `man -w` is a verifier shortcut, not guaranteed by the POSIX lookup synopsis.
- Passed on Arch Linux 6.18.52-1-lts with mandoc 1.14.6, GNU Coreutils 9.11, and Bash 5.3.15 as `/bin/sh` and native Bash, and Zsh 5.9.2 (`-f`). Both sectioned `printf` lookups resolved; local sections had extra matching suffixes in the same lookup. Do not promise this result when local page collections differ.
- A pseudo-terminal check ran `man cp` with `PAGER=less` (less 704), waited for the synopsis, and sent slash search, next, and quit; the viewer exited successfully. This does not establish the key bindings of every pager or a complete visual reading of its search matches.
- POSIX `man(1p)`, local `man`, `apropos`, `cp`, and shell documentation used for comparison. macOS/BSD behavior is manual-based only, and Bash `help` is intentionally described as shell-specific.
- Pending non-author review and integrated release.
