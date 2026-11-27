# Chapter 32 — verification

See [chapter 31 evidence](chapter-31.md) for platform and layout matrix.
`listings/chapter-32/background-result.sh` passed on Linux under both
`sh` and Zsh `sh` emulation. The grouped command writes a single expected
line, the explicit `wait` succeeds, and the disposable directory is removed.

Separately, Bash 5.3.15 and Zsh 5.9.2 were started interactively with a
Python-allocated PTY and ordinary terminal key settings. In each: Ctrl-Z
stopped `sleep`, `jobs -l` identified it, `bg` resumed it, `fg` brought it
forward, and Ctrl-C returned the prompt. A background `cat` stopped on
terminal input, then exited on foreground Ctrl-D. The background `sleep |
cat` pipeline appeared together in the job display and completed. No real
work was interrupted, and persistent sessions/logout behavior was explained
from the documented model, not tested.

Approximate prose: 2,539 words. Counts: 3 figures, 2 tables, 11 input
blocks, 3 exercises with solutions, 1 dialogue.
