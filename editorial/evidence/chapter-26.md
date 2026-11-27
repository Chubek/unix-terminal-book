# Chapter 26: See What the Shell Expands

- Author validation: Linux on EndeavourOS x86_64, GNU Bash 5.3.15(1)
  invoked via `/bin/sh`; clean `C` locale and throwaway fixture.
- Reproduce with `python3 editorial/evidence/chapter-30-check.py`.
  Seven chapter checks verify exact text and status for quoted and
  unquoted glob operands, tilde expansion with an invented home,
  command substitution with internal and trailing newlines,
  field splitting, quotes inside a value, a POSIX no-match result
  and two empty captures caused by commands with different statuses.
  POSIX shell pathname behavior is tested separately from the
  explanation of Zsh's native defaults.
- Portability basis: POSIX Shell Command Language §2.6 and Zsh's
  `Expansion` manual. Native macOS and BSD implementations were
  not tested in this author check. Sorting of names outside `C`,
  optional Bash settings and other glob modes are not benchmarked.
- Assets: `figures/chapter-26/{order,notes,glob}.tikz`.
