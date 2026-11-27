# Chapter 3 — command lookup and child-shell separation

- Runtime: EndeavourOS Linux 6.18.52-1-lts, x86_64; `/bin/sh` is Bash 5.3.15. Validation script also passed under Zsh 5.9.2 with `--emulate sh`. Both ran in a disposable directory with `LC_ALL=C`.
- `listings/chapter-3/shell-lookup.sh`: `cd`, `printf` and `pwd` gave bare names; `uname` resolved to `/usr/bin/uname`; `command -V printf` classified it as a builtin. The invented name gave no output and failed. A child `/bin/sh` moved to `/` while its parent's working directory stayed unchanged.
- Standards evidence: POSIX.1-2024 `command` defines `-v`/`-V` as lookup, not invocation, and leaves the descriptive wording unspecified. POSIX `cd` describes the scope of the directory change. No Ksh, Csh/Tcsh, Fish, BSD or macOS runtime claimed.
- Illustrations: `figures/chapter-3/{nested,lookup,directory}.tikz`. Key local labels: `sec:3-borrow`, `sec:3-lookup`, `sec:3-place`, `sec:3-separate`, `sec:3-choice`, `fig:3-nested`, `fig:3-lookup`, `fig:3-directory`, `ex:3-lookup`, `ex:3-printf`, `ex:3-parents`.
- Runtime recipe: from an empty disposable directory other than `/`, run `/bin/sh "$repo/listings/chapter-3/shell-lookup.sh"` with `repo` pointing to the repository root. No practice paths created.
