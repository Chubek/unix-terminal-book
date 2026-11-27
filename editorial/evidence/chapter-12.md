# Chapter 12 — author validation

- Source: `chapters/chapter-12.ltx`; TikZ: `figures/chapter-12/safety.tikz` (review workflow, hold vs removal, and restore).
- `listings/chapter-12/check-cleanup.sh` ran on private `TMPDIR` under `/mnt/nvme` using GNU Coreutils 9.11 and GNU Diffutils 3.12. It passed on Arch Linux 6.18.52-1-lts with Bash 5.3.15 as `/bin/sh` and native Bash, and Zsh 5.9.2 (`-f`).
- Checked unique fresh creation, moving to and from a hold, exact-file `rm -i` with negative and affirmative responses in the C locale, refusal to remove a nonempty directory, and byte-verified recovery from a separate copy. The script removes only explicitly named, newly created fixture paths; it never uses recursive removal.
- GNU and POSIX local documentation consulted, with BSD primary documentation cited for the optional `mktemp` syntax. No macOS/BSD runtime test; no forensic recovery, data erasure, shared-directory or configured Trash testing. The printed plain `mkdir` alternative uses the basic creation pattern exercised in Chapter 8.
- Progression audit: read-only navigation and path lessons before byte-copying; empty-directory removal before link cleanup; read-only search before irreversible actions; known original before editing; exact removal and recovery only after all these concepts. Each chapter establishes a fresh fixture rather than requiring an earlier tree.
- Pending non-author review and integrated release.
