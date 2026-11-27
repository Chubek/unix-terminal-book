# Chapter 21 — Keep the Rows and Columns You Need

- 3 TikZ diagrams: `figures/chapter-21/{boundaries,rule,paste}.tikz`; 2 tables, 3 exercises and solutions, 1 dialogue.
- Reusable `listings/chapter-21/open-loans.sh`: POSIX shell and awk with tab-delimited data on standard input, header first.
- `verify-chapters-19-24.py` checked the examples, listing and cleanup under sh and zsh on EndeavourOS with GNU Coreutils 9.11, GNU Awk 5.4.1 and GNU sed 4.10. Six transcript checks include projection with preserved tab bytes, the reordered header and filtered report, shape check, paste and sorting whole records. The first printed TSV transcript uses illustrative spaces for readability; validation tests the real tabs.
- Citations cover POSIX Issue 8 cut, paste and awk. `sed -n 'l'` visualization wording describes GNU sed and explicitly notes representation differences. The non-POSIX mktemp setup and plain `mkdir` fallback were exercised in separate disposable directories. macOS, FreeBSD, OpenBSD and NetBSD were not execution-tested.
