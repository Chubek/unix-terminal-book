# Chapter 8 — author validation

- Source: `chapters/chapter-8.ltx`; TikZ: `figures/chapter-8/directory-links.tikz` (tree, hard-link identity and symbolic-link traversal).
- Reproducer: `listings/chapter-8/check-links.sh`; use `TMPDIR` on a private filesystem that supports hard and symbolic links. The verifier additionally uses a shell `test` implementation that supports `-ef`; the reader does not need that test.
- Passed on Arch Linux 6.18.52-1-lts with GNU Coreutils 9.11, GNU Diffutils 3.12, Bash 5.3.15 as `/bin/sh` and native Bash, and Zsh 5.9.2 (`-f`).
- Checked: nested directory creation, refusal on nonempty removal, hard-link identity before and after renaming, dangling and restored relative symbolic links, independently copied bytes, and logical versus physical routes with a symlink to a directory.
- Local POSIX/GNU documentation consulted for `ln`, `mkdir`, `rmdir`, `cd`, `pwd` and `ls`. Non-Linux behavior is manual-based only. No claim about editor replacement behavior on a particular editor or non-native volume.
- Progression audit: Chapter 5's two `Plans` nodes correctly represent separate directory entries; Chapter 6's parent-route figure starts at `albums`, not the filesystem root. The later hard-link figure changes the relationship explicitly (two names, one file); the relative-link figure instead starts at the containing directory. Routings and visual descriptions agree in source. Chapter 8 now demonstrates the logical/physical distinction foreshadowed in Chapter 6.
- Pending non-author review and the integrated release build.
