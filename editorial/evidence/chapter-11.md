# Chapter 11 — author validation

- Source: `chapters/chapter-11.ltx`; TikZ: `figures/chapter-11/editing.tikz` (buffer, vi mode transition, nano save sequence).
- `listings/chapter-11/editor-fixtures.sh` created four controlled ASCII files using the local `/bin/sh` (Bash 5.3.15) in private `TMPDIR`. It leaves them for interactive practice and prints the absolute path.
- Arch Linux 6.18.52-1-lts: pseudo-terminal checked Vim 9.2.1046 invoked as `vi -Nu NONE -n -i NONE`, and GNU nano 9.2 invoked with `-I` to skip local configuration. Vim received `GoPick up stamps`, Escape, `:wq`, and Enter; nano received the new first line, Ctrl+O, confirmation of the filename, then Ctrl+X. Verified exact bytes with `cmp` in both output files.
- In separate sessions, Vim `:q!` and nano's negative answer to the save-on-exit question both left the scratch file byte-identical to the original. `file` 5.48 classified the unmodified fixture as ASCII text.
- POSIX `vi` and the GNU nano manual cover the advertised interface; no nvi, macOS, FreeBSD, OpenBSD, NetBSD, custom key maps or assistive-technology runtime testing. Restoring a fresh copy is the same `cp`/`cmp` operation exercised for Chapter 7.
- Pending non-author review and integrated release.
