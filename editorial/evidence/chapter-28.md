# Chapter 28: What Commands Inherit

- Author validation: Linux on EndeavourOS x86_64, GNU Bash 5.3.15(1)
  via `/bin/sh`, GNU `sort` and `env` from GNU coreutils 9.11.
  Reproduce using `python3 editorial/evidence/chapter-30-check.py`.
- Five checks assert output and status for export, child-only
  assignment, command-prefix precedence, `C` collation of simple ASCII
  data, an invocation with `env`, an export scoped to a subshell
  environment, and exported-empty versus unset. The validator's inherited
  environment is constructed explicitly; it does not print or copy
  the caller's settings except for selecting a writable fixture root.
- Portability basis: POSIX `command`, `env` and environment variables.
  Command paths shown in explanatory text are typical, not guaranteed.
  The tests do not claim to reproduce other installed locales or
  native macOS, FreeBSD, OpenBSD and NetBSD behavior.
- Assets: `figures/chapter-28/{inherit,override,search}.tikz`.
