# Chapter 33 — verification

See [chapter 31 evidence](chapter-31.md) for platform and layout matrix.
`listings/chapter-33/mode-check.sh` passed on Linux/Btrfs as an
unprivileged user under `sh` and Zsh `sh` emulation. Symbolic chmod produced
600 on the fictional text file, removing owner write left contents readable,
removing owner search on the intermediate directory prevented reading
the known child pathname, and restoring search made it readable again.
The subshell mask 077 yielded a 600 file and left the calling mask
unchanged. Only named fixture files were removed.

POSIX `chmod` and `umask`, the FreeBSD Handbook, and Apple's macOS User
Guide are cited. The Apple-hosted privacy documentation was consulted.
Native macOS privacy prompts, ACLs, network filesystems, and privileged
access checks were not exercised; the text distinguishes those layers
from the tested basic mode rules.

Approximate prose: 2,574 words. Counts: 3 figures, 2 tables, 10 input
blocks, 3 exercises with solutions, 1 dialogue.
