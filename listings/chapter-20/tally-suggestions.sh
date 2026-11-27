#!/bin/sh
# POSIX sh syntax, sort, uniq, and non-POSIX mktemp. ASCII stdin, one vote per line.
# Usage: sh tally-suggestions.sh < votes.txt
# Use a completed input file; status of any outside pipe producer is unknown.
case ${TMPDIR:-/tmp} in
    /*) ;;
    *) printf '%s\n' 'TMPDIR must be an absolute path.' >&2; exit 1 ;;
esac
scratch=$(mktemp -d "${TMPDIR:-/tmp}/utp20-tally.XXXXXX") || exit "$?"
trap 'rm -f "$scratch/sorted" "$scratch/counted" "$scratch/ranked"; rmdir "$scratch"' 0
trap 'exit 1' HUP INT TERM
LC_ALL=C sort > "$scratch/sorted" || exit "$?"
LC_ALL=C uniq -c "$scratch/sorted" > "$scratch/counted" || exit "$?"
LC_ALL=C sort -k 1,1nr -k 2 "$scratch/counted" > "$scratch/ranked" || exit "$?"
cat "$scratch/ranked"
