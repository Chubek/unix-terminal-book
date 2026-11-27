# Chapter 1 — terminal round trip

- Runtime: EndeavourOS Linux 6.18.52-1-lts, x86_64, Bash 5.3.15 as `/bin/sh`; also Zsh 5.9.2 run with `--emulate sh` on the same host. Tests used an empty disposable home/working directory, an otherwise empty environment, and `LC_ALL=C`.
- `listings/chapter-1/first-session.sh`: both shells passed single/multiple message checks, the rejected `pwd -Q` probe, and the invariant that `pwd` was unchanged. The Bash and Zsh diagnostics differed; the printed diagnostic is explicitly illustrative.
- References: POSIX `printf` and `pwd` for the requested operations; Apple Terminal User Guide for the macOS entry point. No macOS or BSD execution or GUI/screen-reader test claimed. Cleanup: no practice paths created.
- Illustrations: `figures/chapter-1/{layers,round-trip,recovery}.tikz`. Key local labels: `sec:1-open`, `sec:1-round-trip`, `sec:1-mistake`, `fig:1-layers`, `fig:1-roundtrip`, `fig:1-recovery`, `ex:1-lines`, `ex:1-invariant`, `ex:1-recover`.
- Runtime recipe: from an empty disposable directory, with `repo` pointing to the repository root, run `/bin/sh "$repo/listings/chapter-1/first-session.sh"`. See Chapter 6 evidence for the shared layout-gate report.
