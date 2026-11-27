# Release report — editorial checkpoint, not released

No final manuscript or release PDF has been approved. `make check-release`
and the release PDF targets must remain failing until the chapter-level
requirements are met. An editorial PDF built with `make draft` is explicitly
marked as a draft on its cover.

## Integration baseline

The master includes four parts of twelve chapters, front matter,
two appendices, a curated glossary and a combined command/topic index.
All 41 support modules and their existing class load configuration are
retained. The following are counts in W0's initial integration build,
not a statement about unpublished work in the author worktrees:

| Item | Initial integration | Release requirement |
|---|---:|---:|
| Numbered chapter slots | 48 | 48 |
| Nonempty integrated chapters | 0 | 48 |
| Chapter figures | 0 | Normally at least 144 |
| Chapter tables | 0 | Normally at least 96 |
| Chapter worked example blocks | 0 | Normally at least 384 |
| Chapter exercises with solutions | 0 | At least 144 |
| Dialogue boxes | 0 | 48–60 |
| Chapter peer review receipts | 0 | 48 |

The macOS emphasis in Chapters 34–36 is assigned to W6. Chapter 35
will give Homebrew sustained attention while comparing it with the
package workflows on Linux and the BSDs. This is a drafting assignment,
not a completed feature.

All eight author groups have handed off manuscript sources for
non-author review. The first approved batch, Chapters 1, 3–6 and 31,
is integrated with evidence and review receipts. Chapter 5's revised
practice-directory transitions were independently rechecked. Other
chapters with open findings remain on their author branches. The
exercise hyperlinks now include a chapter component so the same visible
exercise number in different chapters does not collide; the edition
fixture checks cross-chapter anchor uniqueness.

The first staged **full-manuscript draft** included 48 draft chapters,
144 figures, 97 tables, 592 example blocks, 144 exercises and solutions,
and 48 dialogues. Multi-pass pdfLaTeX with `makeindex` produced 520
pages in print/answers and 482 pages in screen/noanswers, both 504 × 720
points. This was a proof from pre-revision branch snapshots, not a
release test or final review disposition.

The cover now contains an original TikZ terminal-to-files illustration.
W0 inspected color and grayscale renderings at 7 × 10 inches and
confirmed that the dedication, “Made Specially for M, R and H”, appears
by itself immediately after the cover, before the copyright page.

## Verified at this checkpoint

| Check | Environment | Result and scope |
|---|---|---|
| `make check-structure` | Python 3.14, EndeavourOS x86-64 | Manifest and master structure passed; no claims about unwritten chapters. |
| Multi-pass draft plus `makeindex` | pdfTeX 1.40.26, TeX Live 2024, EndeavourOS x86-64 | All four layout/answer draft combinations compiled. Print draft measured 504 × 720 PDF points (7 × 10 inches). |
| `make check-toolkit` | pdfLaTeX, LuaLaTeX and XeLaTeX, TeX Live 2024 | All four class option combinations on each engine passed dialogue presence and single-line, solution visibility and page-size smoke checks on the fixture. Not a full-book test. |
| `make check-examples` | `/bin/sh` and installed utilities, EndeavourOS x86-64 | Appendix fixture passed copy/compare, search, count/sort, stream edit/diff, checksum and archive assertions. |
| `python3 editorial/tests/test_coord.py` | Python 3.14, a throwaway Git repository | Private routing, correlation, ownership, revision conflicts, retry identity and timeout recovery tests passed. |
| `make check-release` | Python 3.14, same Linux environment | Failed as intended on missing integrated content and evidence. |

No native macOS, FreeBSD, OpenBSD or NetBSD command suite has been run
by W0. No live SSH sessions or package installations have been tested
by W0. Linux shell tests are not evidence of behavior on those platforms.

## Before release

1. Import authors' chapters only after non-author review and revision.
   Register each cited asset and verify examples and cleanup in disposable
   fixtures. Record any platform or optional-tool limits chapter by chapter.
2. Audit the prose length and editorial progression, references, index
   coverage, figure captions/descriptions and all dialogue conclusions.
3. Build all editions cleanly with `make editions`. Review warnings,
   citations, included sources, font embedding, listing breaks, black
   and white proof pages, and legibility at actual trim. Assess the
   complete PDF, not just the edition fixture.
4. Replace this checkpoint with measured final counts and the completed
   test matrix, record any known defects, and identify the final PDFs.
