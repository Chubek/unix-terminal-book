#!/bin/sh
# POSIX sh syntax; mktemp -d is a widely available extension.
# Usage: sh route-booking.sh
set -eu
lab=$(mktemp -d)
trap 'rm -f "$lab/booking.txt" "$lab/handoff.txt" "$lab/disposable.txt" "$lab/included.txt" "$lab/problem.txt" "$lab/combined.txt" "$lab/data-only.txt" "$lab/original-output.txt" "$lab/protected.txt" "$lab/opened-first.txt"; rmdir "$lab"' 0
cd "$lab"
printf '%s\n' 'Room 4' 'Thursday 18:00' > booking.txt
cat booking.txt > handoff.txt
printf '%s\n' 'Bring key' >> handoff.txt
test "$(wc -l < handoff.txt)" -eq 3
printf '%s\n' throwaway > disposable.txt
if false > disposable.txt; then exit 1; fi
test "$(wc -c < disposable.txt)" -eq 0
if cat booking.txt missing.txt > included.txt 2> problem.txt; then exit 1; fi
if cat booking.txt missing.txt > combined.txt 2>&1; then exit 1; fi
if (cat booking.txt missing.txt 2>&1 > data-only.txt) > original-output.txt
then
    exit 1
fi
cmp -s booking.txt included.txt
cmp -s booking.txt data-only.txt
cmp -s problem.txt original-output.txt
test "$(wc -l < combined.txt)" -gt 2
printf '%s\n' 'first copy' > protected.txt
if (set -C; printf '%s\n' 'second copy' > protected.txt) 2>/dev/null
then
    exit 1
fi
test "$(cat protected.txt)" = 'first copy'
if (cat booking.txt > opened-first.txt 2> absent-dir/problem.txt) 2>/dev/null
then
    exit 1
fi
test -f opened-first.txt
test "$(wc -c < opened-first.txt)" -eq 0
printf '%s\n' 'Verified split streams, duplication order, and truncation.'
