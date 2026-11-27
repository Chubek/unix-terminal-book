# Chapter 31 — verification

Native matrix for W6: EndeavourOS x86-64, Linux 6.18.52-1-lts, procps-ng 4.0.7,
GNU coreutils 9.11, Bash 5.3.15 as `/bin/sh`, and Zsh 5.9.2 in `sh` emulation
for the portable listings. File fixtures were disposable, under a scratch
`TMPDIR` on `/mnt/nvme`, on Btrfs, with an unprivileged login. No credentials,
installations, network workflows, privileged writes, or real work files were
used. None of the macOS or BSD cases was run natively.

`listings/chapter-31/timer-status.sh` passed under both shells. It starts only
its own timer, prints its `ps` PID/PPID/command, requests TERM, and collects
the child's status. Observed request status 0 and child status 143 in both
runs; the chapter does not prescribe 143. Foreground `ps` and `kill` syntax
is based on the linked POSIX manuals; `ps` population, names, and spacing
are not promises. The displayed PID and process row are illustrative. KILL,
recovery of interrupted writes, and system processes were not exercised.
OpenBSD's `ps(1)` manual documents `-A` for all processes and `-e` for
environment display; the worked list deliberately uses `-A`.

Author-side layout check for chapters 31–36: a standalone six-chapter
preview used pdfTeX 1.40.26 / TeX Live 2024, three print/answers passes with
makeindex, and two screen/noanswers passes. Print preview was 504 by 720 pt
(7 by 10 inches), 63 pages, with 36 accepted index entries and no overfull
boxes. All 18 figure pages were rasterized in grayscale at 72 dpi and checked
for layout and visible labels; no distinction relies on color. PDF text
extraction found six one-line dialogue conclusions in both outputs, 18
solutions in answers, and none in noanswers. External chapter references
cannot resolve in this slice; full-book integration is a separate gate.
The worker snapshot used the original support module and emitted duplicate
exercise anchors; W0 reports a shared fix made separately, not in this worktree.

Approximate prose (custom source count excluding listings, figures, tables,
and reading lists): 2,571 words. Counts: 3 figures, 2 tables, 8 input blocks,
3 exercises with solutions, 1 dialogue.
