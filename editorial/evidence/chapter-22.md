# Chapter 22 — Transform and Compare Text

- 3 TikZ diagrams: `figures/chapter-22/{substitute,hunk,review}.tikz`; 2 tables, 3 exercises and solutions, 1 dialogue.
- `listings/chapter-22/preview-sign.sh` takes stdin and emits a preview on stdout; no write to the source.
- `verify-chapters-19-24.py` ran under sh and zsh on EndeavourOS with GNU sed 4.10, GNU Coreutils 9.11 and GNU diffutils 3.12. Four exact transcript assertions and a separate unified-hunk assertion verified the accidental broad substitution, selection, translation, status 0 for identical files and status 1 with unaffected context for the intended change. Listing and cleanup also passed.
- POSIX Issue 8 sed, tr and diff documentation are the portability bases. The GNU/BSD `sed -i` distinction is advisory; chapter commands intentionally do not use it. No native tests on macOS or the BSDs.
