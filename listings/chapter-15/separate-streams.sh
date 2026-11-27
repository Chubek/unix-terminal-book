#!/bin/sh
# POSIX sh syntax; mktemp -d is a widely available extension.
# Usage: sh separate-streams.sh
set -eu
lab=$(mktemp -d)
trap 'rm -f "$lab/roll.txt" "$lab/visible.txt" "$lab/diagnostic.txt"; rmdir "$lab"' 0
cd "$lab"
printf '%s\n' Asha Bea Chen > roll.txt
status=0
cat roll.txt not-here.txt > visible.txt 2> diagnostic.txt || status=$?
test "$status" -ne 0
test -s diagnostic.txt
cmp -s roll.txt visible.txt
test "$(wc -l < roll.txt)" -eq 3
test "$(wc -l < /dev/null)" -eq 0
test "$(printf 'Saturday names\n' | cat - roll.txt | wc -l)" -eq 4
printf 'Data lines: %s\n' "$(wc -l < visible.txt)"
printf 'A diagnostic was produced; cat returned %s.\n' "$status"
