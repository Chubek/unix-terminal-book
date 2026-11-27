# Chapter 18 — Look Inside Text

- Executable check: `sh listings/chapter-18/measure-catalog.sh`.
- Actual: Linux host in `chapter-13.md`; `sh` and `bash` checks passed
  under `LC_ALL=C.utf8`. GNU `wc` reported 6 newlines, 12 words and 72
  bytes; the two UTF-8 fixtures had 6 and 7 bytes, 5 and 6 characters.
  The unterminated file had zero newlines and four words. A separate
  pseudo-terminal check with `less` 704 (`TERM=xterm`, `LESS` empty,
  `LESSHISTFILE=-`) confirmed it displayed the closing line and quit
  with `q`. Optional pager keys were not exhaustively tested.
- Manual checks: POSIX.1-2024 [wc](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/wc.html)
  specifies newline counting, output fields, multi-input totals, and
  `LC_CTYPE`. OpenBSD [wc(1)](https://man.openbsd.org/wc) describes
  locale-sensitive `-m`. `less` is optional; UTF-8 locale names vary.
- No execution on macOS, FreeBSD, OpenBSD, or NetBSD.

## Isolated LaTeX check, chapters 13–18

Three passes and `makeindex` for print/answers and screen/noanswers
using TeX Live 2024 pdfLaTeX at 504 × 720 pt. Both editions produced
PDFs. The index accepted 40 entries, none rejected. Text extraction
showed 18 solution headings with answers and none with noanswers.
No overfull-box or long-dialogue-conclusion warning; local chapter
and figure references resolved. References to chapters outside the
isolated six remained unresolved by design. This was not the full
book build or a physical grayscale proof.
