# Chapter 14 — Match Names with Patterns

- Executable fixture/check: `sh listings/chapter-14/preview-receipts.sh`.
  It asserts membership/counts with `LC_ALL=C`, then prints a preview.
- Actual: Linux host in `chapter-13.md`, GNU findutils 4.11.0-modified.
  Scripts passed with `sh` and `bash`. Separate fresh-shell checks found
  an unchanged April glob with default Bash, `[]` with `nullglob`, and
  no stdout/nonzero status with `failglob`, Zsh 5.9.2 (`-f`), and Fish
  4.9.3 (`--no-config`). This compares glob behavior, not whether all
  POSIX sh examples work in these interactive shells.
- Manual check: POSIX.1-2024 [Shell Command Language](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html),
  §§2.6.6 and 2.14 distinguish pathname expansion from pattern notation
  in other settings.
- No macOS/BSD execution. Layout: see `chapter-18.md`.
