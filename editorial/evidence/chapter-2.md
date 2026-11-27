# Chapter 2 — system and utility fingerprints

- Runtime: EndeavourOS Linux 6.18.52-1-lts, x86_64; `/bin/sh` is Bash 5.3.15; Zsh 5.9.2 in sh emulation; GNU Coreutils 9.11. Both shell runs of `listings/chapter-2/system-probes.sh` passed in an empty disposable directory (`LC_ALL=C`).
- Plain `uname` matched `-s`, while `uname -s -r` printed the observed name and release in that order. The actual release string was `6.18.52-1-lts`; the reported hardware name was `x86_64`. `ls --all` and `ls -a` agreed with the installed GNU utility; rejection on non-GNU implementations is an explicitly possible, not observed, outcome.
- Primary manual checks: The Open Group's POSIX.1-2024 `uname` specification describes default `-s`, `-r`, `-m`, and output field order; the GNU Coreutils `ls` manual confirms the two `-a`/`--all` spellings. macOS, FreeBSD, OpenBSD and NetBSD results in the table are illustrative, not a platform execution matrix.
- Illustrations: `figures/chapter-2/{identity,families,portability}.tikz`. Key local labels: `sec:2-clue`, `sec:2-family`, `sec:2-boundary`, `sec:2-handoff`, `fig:2-identity`, `fig:2-families`, `fig:2-portability`, `ex:2-identify`, `ex:2-replace`, `ex:2-field`.
- Runtime recipe: from an empty disposable directory, run `/bin/sh "$repo/listings/chapter-2/system-probes.sh"` with `repo` pointing to the repository root. No practice paths created.
