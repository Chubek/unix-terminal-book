# Chapter 20 — Sort and Count

- 3 TikZ diagrams: `figures/chapter-20/{groups,numbers,keys}.tikz`; 2 tables, 3 exercises and solutions, 1 dialogue.
- `listings/chapter-20/tally-suggestions.sh` uses sh syntax, sort and uniq in the C locale; input is ASCII, one vote per line.
- `verify-chapters-19-24.py` exercised the terminal blocks, listing and cleanup on EndeavourOS with GNU Coreutils 9.11, Bash 5.3.15 invoked as sh and zsh. It checks four exact transcript cases with implementation-dependent count padding stripped: adjacent runs, whole-list tally, ranking and a tie with an explicit secondary key.
- POSIX Issue 8 `sort` and `uniq` for keys, numeric comparison, locale and adjacency; no claims of native execution on macOS or any BSD. No locale other than C was required to reproduce the results. The book deliberately does not promise a representative for a numerically tied `sort -u`.
