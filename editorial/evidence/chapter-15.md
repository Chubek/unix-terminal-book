# Chapter 15 — Input, Output, and Errors

- Executable check: `sh listings/chapter-15/separate-streams.sh`.
- Actual: Linux host in `chapter-13.md`. Both `sh` and `bash` checks
  passed. GNU `cat` preserved the three correct rows on stdout, put
  a diagnostic on stderr, and returned 1 after the missing operand.
  `/dev/null` yielded a zero count. A separate pseudo-terminal test
  fed two newline-terminated names and the usual EOF control key to
  GNU `wc -l`; it printed 2 and exited 0. A second pseudo-terminal
  run sent the interrupt control key and observed SIGINT, no count.
  A pending-input test sent `Asha` without Enter followed by Ctrl+D:
  the counter did not finish until a second Ctrl+D and then printed
  zero newlines, returning 0. The fixture script also passed with
  `zsh --emulate sh`.
- Manual basis: the POSIX `cat`/`wc` utility descriptions and the
  POSIX General Terminal Interface's canonical-input EOF behavior.
  No exact diagnostic wording or cross-stream display order promised.
- No macOS/BSD execution or alternative terminal settings tested.
  Layout: see `chapter-18.md`.
