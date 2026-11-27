# Chapter 16 — Send Output Somewhere Else

- Executable check: `sh listings/chapter-16/route-booking.sh`.
- Actual: Linux host in `chapter-13.md`. Checks passed under `sh` and
  `bash` for truncation before `false`, appending, separated streams,
  left-to-right duplication (including the diagnostic reaching the
  original stdout), noclobber rejecting replacement, and a failed
  later redirection leaving the earlier destination empty. Intentional
  truncation targets only a dummy fixture.
- Manual basis: POSIX.1-2024 §2.7 defines redirection, descriptor
  duplication, and left-to-right evaluation. The chapter does not
  teach nonportable `&>` or promise diagnostic ordering.
- No execution on macOS/BSD or non-Bash `sh`. Layout: `chapter-18.md`.
