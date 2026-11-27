# First edition release report

**Unix Terminal for the Plebeian**, by **B. Netandyuhoo**. All 48
chapters are integrated on `utp/integration`, with evidence and non-author
review receipts for every chapter. The default branch was not changed;
nothing was pushed or published.

| Edition | Pages | Solutions | PDF |
|---|---:|---:|---|
| Print with answers | 532 | 144 | [`build/print-answers/unix-terminals-for-pleb-print-answers.pdf`](../build/print-answers/unix-terminals-for-pleb-print-answers.pdf) |
| Print without answers | 500 | 0 | [`build/print-noanswers/unix-terminals-for-pleb-print-noanswers.pdf`](../build/print-noanswers/unix-terminals-for-pleb-print-noanswers.pdf) |
| Screen with answers | 530 | 144 | [`build/screen-answers/unix-terminals-for-pleb-screen-answers.pdf`](../build/screen-answers/unix-terminals-for-pleb-screen-answers.pdf) |
| Screen without answers | 496 | 0 | [`build/screen-noanswers/unix-terminals-for-pleb-screen-noanswers.pdf`](../build/screen-noanswers/unix-terminals-for-pleb-screen-noanswers.pdf) |

PDFs are local build products. Use `make -j4 editions` to recreate them.
All editions use 7 × 10 inch pages; the cover is followed immediately
by the dedication page, “Made Specially for M, R and H.”

## Manuscript counts

- Four parts of twelve chapters, two appendices, front matter, glossary
  and combined command/topic index.
- 144 chapter figures with captions and text descriptions, plus the
  cover illustration; 97 chapter tables and 614 worked input blocks.
- 144 exercises and 144 corresponding solutions (suppressed in the
  no-answers editions), and 48 continuously numbered dialogues with
  one-line conclusions.
- Approximately 120,500 words across the chapters, a median of about
  2,500 per chapter. This source estimate includes objectives, exercises
  and solutions but excludes dialogue, terminal listings, figures,
  tables and references. Some introductory chapters are shorter.
- 48 non-author review receipts in `editorial/reviews/`, 48 chapter
  evidence records in `editorial/evidence/`, and 255 accepted index
  entries with no rejects in each edition.

## Verification

| Area | Environment and outcome |
|---|---|
| Book structure and peer review | `make check-release` passed: manifest, all chapter files and registered assets, labels, required counts, evidence and review receipts. |
| Full PDFs | All four clean pdfLaTeX 1.40.26 / TeX Live 2024 multi-pass builds and `makeindex` passed on EndeavourOS x86-64. The recorder confirmed every chapter and registered asset. No reported overfull boxes, undefined references or citations, duplicate PDF destinations, missing glyphs, substituted fonts, or wrapped dialogue conclusions. |
| PDF inspection | Poppler checks on all four PDFs found the correct author and dedication, 144 figure captions, 48 numbered dialogue headings and conclusions, the expected solution count, and embedded fonts. W0 inspected color cover renderings and a grayscale print proof sampled across all four parts at trim size. |
| Toolkit options | pdfLaTeX, LuaLaTeX and XeLaTeX smoke tests passed in all four layout/answer combinations, including unique exercise anchors and genuine solution omission. Only pdfLaTeX was used on the complete release. |
| Practice runtime | `make check-examples` passed all 34 registered harnesses on EndeavourOS Linux 6.18.52, x86-64. Nested suites checked Bash-backed `/bin/sh` 5.3.15, Bash, Zsh 5.9.2 and selected Fish cases. A separate `C.UTF-8` run verified Chapter 18 character counts. |
| Optional tools and remote examples | Isolated Linux checks included GNU tar and Linux libarchive tar, local tmux PTYs, OpenSSH configuration/key behavior without a live connection, rsync preview, jq/Python, and local media/PDF processing. See per-chapter evidence for exact scope. |
| Broker | Eight author sessions and W0 used isolated Git roles, a directed broker and versioned common state. `python3 editorial/tests/test_coord.py` passed routing, correlation, acknowledgment, ownership, revision conflicts, stable retries and timeout recovery in disposable repositories. |

## Limits

- macOS (including APFS, Homebrew and Rosetta), FreeBSD, OpenBSD and
  NetBSD material was checked against platform/upstream documentation
  where cited, not run on native installations here. Ksh and Tcsh were
  unavailable for the Linux suite. Live transfer/authentication, package
  installation, and actual assistive-technology behavior were not tested.
- Final TeX logs contain non-overflow spacing notices: 46 print/answers,
  33 print/noanswers, 48 screen/answers and 37 screen/noanswers. These are
  underfull-box notices, not clipped content; logs retain line/page
  locations. No physical press proof, tagged-PDF or PDF/UA certification
  is claimed.
