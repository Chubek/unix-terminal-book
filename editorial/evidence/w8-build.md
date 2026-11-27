# W8 chapter-fragment checks

The authored material is in `chapters/chapter-43.ltx` through
`chapters/chapter-48.ltx`. Each fragment has three original TikZ figures
with visual descriptions, two quicktables, at least eight worked or
hands-on command blocks, three exercises and separated solutions, and
one seven-turn dialogue. All six dialogue conclusions fit one line.

| Chapter | Approximate instructional words |
| --- | ---: |
| 43 | 2,860 |
| 44 | 2,770 |
| 45 | 2,600 |
| 46 | 2,590 |
| 47 | 2,620 |
| 48 | 2,580 |

Counts include dialogue and exercise prose, but exclude tables, display
listings, source links and inline commands. Use the integration team's
manuscript-wide word count for the release.

Chapter-fragment build: TeX Live 2024 pdfLaTeX and makeindex, using the
repository class and dialogue package. An isolated harness simulated
chapter labels 1–42; it did not validate the earlier chapters or the
master. It compiled all six chapters together in both `print,answers`
and `screen,noanswers` with two resolving LaTeX passes after makeindex.
PDF text inspection found all 18 figure captions, six conclusions in
each edition, 18 solutions in answers and none in noanswers. The page
size is 504 × 720 PDF points (7 × 10 inches). Grayscale raster inspection
checked diagram shapes and labels; this does not imply general PDF
accessibility conformance.

See `editorial/evidence/chapter-N.md` for per-chapter command test
coverage and limits. No macOS or BSD host, screen reader, remote
connection, credentials, or real backup data were used.
