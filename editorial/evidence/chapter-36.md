# Chapter 36 — verification

See [chapter 31 evidence](chapter-31.md) for platform and layout matrix.
`listings/chapter-36/grep-status.sh` passed under `sh` and Zsh `sh`
emulation with GNU grep 3.12-modified. It checked status 1 for lowercase
no-match and status 2 for missing input, separate empty stdout and nonempty
stderr captures for the missing input, and the expected output for the
exact and ignore-case matches. The chapter states a portable threshold
(greater than one for error), not the observed numeric error as a guarantee.
No report was posted and only fictional input was used.

macOS section is documentation-based. Apple Developer Documentation is
linked for Rosetta; local macOS tools and Homebrew identity checks are
marked macOS-only or conditional. `sysctl.proc_translated` availability,
the architecture seen in a translated session, `sw_vers`, and optional
Homebrew installations were not run. GNU grep success does not imply
equivalence for all Apple/BSD options.

Approximate prose: 2,565 words. Counts: 3 figures, 2 tables, 12 input
blocks, 3 exercises with solutions, 1 dialogue.
