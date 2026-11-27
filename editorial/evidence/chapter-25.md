# Chapter 25: Quote What You Mean

- Author validation: EndeavourOS x86_64, Linux 6.18.52-1-lts;
  `/bin/sh` resolves to GNU Bash 5.3.15(1) on this host. GNU grep
  identifies itself as `3.12-modified`; GNU coreutils reports 9.11.
- Reproduce with `python3 editorial/evidence/chapter-30-check.py` at
  checkout root (use a writable `TMPDIR`; no personal files needed).
  Eight chapter checks assert argument count as rendered by the format
  probe, expansion versus literal dollars, literal versus bracket-glob
  file reads, exact grep matches, a leading-hyphen filename and an
  exact stem with a deliberate wildcard suffix, guarded practice
  setup on success and failure, and fixture rename and restoration.
  The here-document fixture tests its delimiters with the actual utility.
- The selected examples are checked. Interactive continuation prompts,
  completion spelling and manual cleanup confirmations were discussed
  but not tested in a pseudo-terminal.
- Portability basis: POSIX Shell Command Language §§2.2 and 2.7,
  POSIX `grep -F`; `mktemp -d` is not a POSIX dependency. No native
  macOS, FreeBSD, OpenBSD or NetBSD test in this author check.
- Assets: `figures/chapter-25/{boundaries,segments,layers}.tikz`.
