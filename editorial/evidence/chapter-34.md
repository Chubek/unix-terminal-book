# Chapter 34 — verification

See [chapter 31 evidence](chapter-31.md) for platform and layout matrix.
`listings/chapter-34/space-check.sh` passed under `sh` and Zsh `sh`
emulation with GNU `df`, `du`, and `wc` on Linux/Btrfs. `df -Pk` found
the same mount for both the isolated directory and its child directory;
the byte count was 13. `du` reported allocated usage, including the
explicitly addressed hidden fixture; allocation numbers are not required
outcomes. The chapter's short `df` table is illustrative. An actual
full disk or mounting/unmounting was not required.

The exact revised manuscript setup, exercise-2, and final cleanup
blocks were also exercised together under Linux `/bin/sh` and Zsh
`sh` emulation. With the current directory changed to a sibling with
all three target names, both guarded blocks printed the mismatch
warning, made no removal requests, and left every sentinel unchanged.
Back in the recorded physical practice directory, the test confirmed
the three interactive removal prompts separately and verified that
the setup directory was removed and its saved variable cleared.
The latest print preview compiled without overfull boxes.

The APFS explanation was checked against Apple's Disk Utility User Guide
pages on volume groups/space sharing and snapshot viewing. `diskutil` and
`tmutil` examples are macOS-only read-only lookups, with local manuals named
in the text. They were not executed. Native BSD storage tooling and
optional `lsof` were not executed. No mount, snapshot, disk, service, or
large collection was modified.

Approximate prose: 2,578 words. Counts: 3 figures, 2 tables, 12 input
blocks, 3 exercises with solutions, 1 dialogue.
