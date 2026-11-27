#!/bin/sh
# POSIX sh syntax; uses non-POSIX mktemp -d (Linux/macOS/BSD implementations).
# Usage: sh compare-drafts.sh
set -eu
lab=$(mktemp -d)
trap 'rm -f "$lab/schedule.txt" "$lab/Saturday draft.txt" "$lab/-revised.txt"; rmdir "$lab"' 0
cd "$lab"
printf '%s\n' 'Doors noon' 'Tea at one' > schedule.txt
cp schedule.txt 'Saturday draft.txt'
printf '%s\n' 'Doors noon' 'Tea at two' > ./-revised.txt
cmp -s schedule.txt 'Saturday draft.txt'
different=0
cmp -s schedule.txt ./-revised.txt || different=$?
problem=0
cmp -s schedule.txt not-created.txt 2>/dev/null || problem=$?
test "$different" -eq 1
test "$problem" -gt 1
test "$(head -n 1 ./-revised.txt)" = 'Doors noon'
test "$(head -n 1 -- -revised.txt)" = 'Doors noon'
printf 'Equal: 0; different: %s; missing: %s\n' "$different" "$problem"
