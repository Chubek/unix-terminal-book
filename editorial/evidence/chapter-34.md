# Chapter 34 — verification

See [chapter 31 evidence](chapter-31.md) for platform and layout matrix.
`listings/chapter-34/space-check.sh` passed under `sh` and Zsh `sh`
emulation with GNU `df`, `du`, and `wc` on Linux/Btrfs. `df -Pk` found
the same mount for both the isolated directory and its child directory;
the byte count was 13. `du` reported allocated usage, including the
explicitly addressed hidden fixture; allocation numbers are not required
outcomes. The chapter's short `df` table is illustrative. An actual
full disk or mounting/unmounting was not required.

The APFS explanation was checked against Apple's Disk Utility User Guide
pages on volume groups/space sharing and snapshot viewing. `diskutil` and
`tmutil` examples are macOS-only read-only lookups, with local manuals named
in the text. They were not executed. Native BSD storage tooling and
optional `lsof` were not executed. No mount, snapshot, disk, service, or
large collection was modified.

Approximate prose: 2,578 words. Counts: 3 figures, 2 tables, 12 input
blocks, 3 exercises with solutions, 1 dialogue.
