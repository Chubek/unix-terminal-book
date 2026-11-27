# Chapter 35 — verification

See [chapter 31 evidence](chapter-31.md) for platform and layout matrix.
`listings/chapter-35/lookup-check.sh` passed on EndeavourOS under both
`sh` and Zsh `sh` emulation. `command -v jq` found the system's local
`jq`; `jq --version` reported 1.8.2. Native local inventory check
`pacman -Q jq` (Pacman 7.1.0, libalpm 16.0.1) reported `jq 1.8.2-1`.
Read-only comparisons only: no package install, cache refresh, download,
repository session, or startup file edit was done.

Debian/Ubuntu, Fedora, FreeBSD, OpenBSD, NetBSD and Homebrew inspections
are documentation-based, not native tests. Homebrew reference operations
include formulae/casks, installation prefixes, shell setup, catalog and
inventory, updates, targeted upgrades, removal, and recovery. Reference
transaction forms are explicitly not a sequence of runnable exercises.
Actual availability and policy are specific to the reader's system.

Approximate prose: 2,592 words. Counts: 3 figures, 3 tables, 14 input
blocks, 3 exercises with solutions, 1 dialogue.
