# Chapter 29: Choose a Shell Without Guesswork

- Reproduce using `python3 editorial/evidence/chapter-30-check.py`.
- Linux runtime evidence:

  | Interpreter | Version | Check |
  |---|---|---|
  | `/bin/sh` (Bash symlink on this host) | GNU Bash 5.3.15(1) | Two quoted positional parameters; retains unmatched glob |
  | Bash | GNU Bash 5.3.15(1) | Native first index 0 passed |
  | Zsh | 5.9.2 | Native first index 1; rejects unmatched glob |
  | Fish | 4.9.3 | List first index 1 passed |
  | Ksh | Not present | Skipped; example is manual-based |
  | Tcsh | Not present | Skipped; example is manual-based |

- Samples run from an invented home with clean configuration variables.
  No login shell was reconfigured. No Apple or BSD login-default setting
  was runtime-tested. GNU Bash and the Bash-backed `sh` are two modes
  of one implementation, not independent portability evidence.
- Sources in the chapter: GNU Bash, Zsh and Fish upstream manuals,
  OpenBSD `ksh(1)`, and FreeBSD `tcsh(1)`.
- Assets: `figures/chapter-29/{roles,first,select}.tikz`.
