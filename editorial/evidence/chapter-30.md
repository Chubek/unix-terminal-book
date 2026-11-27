# Chapter 30: Make a Small Repeatable Task

Run the selected chapter 25–30 checks with Python 3 from checkout root:

```sh
python3 editorial/evidence/chapter-30-check.py
```

It uses a temporary directory (honoring `TMPDIR`), an invented home,
the `C` locale, and a minimal environment. It extracts selected blocks
from the owned chapter fragments and invokes the shared listing
directly. It checks arguments, exit status, standard output and standard
error independently, then checks that sample file contents are still
unchanged. It makes no network calls. It is not a generic manuscript
executor.

Author system: Linux 6.18.52-1-lts, EndeavourOS x86_64, Python
3.14.7, `/bin/sh` linked to GNU Bash 5.3.15(1). Local run:
29 selected checks passed across six chapters; Ksh and Tcsh unavailable
and skipped. Chapter 30 checks two test/branch examples, `sh -n`,
successful relative and absolute path operands, mixed fixture
outcomes, argument misuse, and empty and option-like candidates.
The test doesn't deliberately create unreadable files or race filesystem
changes. Native macOS, FreeBSD, OpenBSD and NetBSD were not tested by W5.

Script language and semantics reference: POSIX Shell Command
Language §2.9, `sh`, and `test`. Invocation in the listing is
intentional: pass it to `sh` rather than relying on its executable bit.
It emits human-readable diagnostics, not a machine-readable catalog.

- Listing: `listings/chapter-30/preview-notes.sh`.
- Assets: `figures/chapter-30/{test,loop,result}.tikz`.

## Typesetting checkpoint

A temporary six-chapter wrapper using the repository class and manifest
titles (numbered 25–30) passed pdfLaTeX, `makeindex`, and two further
pdfLaTeX passes in both `print,answers` and `screen,noanswers` modes.
External chapter labels were represented by matching numbered stub
anchors (not a test of the full master). Final logs showed no overfull
boxes, unresolved references or dialogue-width warnings. Both modes
accepted all 36 local index entries; `pdftotext -layout` found six
dialogue conclusions in each edition, 18 solution headers in the answer
build and none in the no-answer build.
