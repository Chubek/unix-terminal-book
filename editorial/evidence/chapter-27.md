# Chapter 27: Keep a Value in a Variable

- Author validation: Linux on EndeavourOS x86_64, GNU Bash 5.3.15(1)
  invoked via `/bin/sh`. Reproduce using
  `python3 editorial/evidence/chapter-30-check.py`.
- Three grouped checks verify assignments and brace boundaries,
  defaults for unset/empty/nonempty lookups, then counts and argument
  boundaries under quoted `$@` versus quoted `$*`. The middle
  argument in the last test is intentionally empty.
- Portability basis: POSIX Shell Command Language §§2.5 and 2.6.
  Native macOS and BSD systems were not available in this check.
  This chapter assumes a fresh `sh` and its ordinary unset handling.
- Assets: `figures/chapter-27/{assignment,defaults,forward}.tikz`.
