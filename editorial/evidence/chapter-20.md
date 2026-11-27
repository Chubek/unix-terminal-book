# Chapter 20 — Sort and Count

- 3 TikZ diagrams: `figures/chapter-20/{groups,numbers,keys}.tikz`; 2 tables, 3 exercises and solutions, 1 dialogue.
- `listings/chapter-20/tally-suggestions.sh` uses sh syntax, sort and uniq in the C locale, and non-POSIX mktemp for scratch space; input is a completed ASCII votes file, one vote per line.
- `verify-chapters-19-24.py` exercised the terminal blocks, listing and cleanup on EndeavourOS with GNU Coreutils 9.11, Bash 5.3.15 invoked as sh and zsh. It checks four exact transcript cases with implementation-dependent count padding stripped: adjacent runs, whole-list tally, ranking and a tie with an explicit secondary key. It also checks that `sort -f -u` emits one representative and injects failures with partial output into each stage of the listing: all return the error without publishing incomplete output or leaving scratch files.
- POSIX Issue 8 `sort` and `uniq` for keys, numeric comparison, locale and adjacency; no claims of native execution on macOS or any BSD. No locale other than C was required to reproduce the results. The book deliberately does not promise a representative for a numerically tied `sort -u`.
