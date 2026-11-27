#!/bin/sh
# Chapter 36: POSIX sh plus mktemp; tested with GNU grep on Linux.
# Run wholly offline against fictional text in a new temporary directory.
set -eu
export LC_ALL=C
room=$(mktemp -d "${TMPDIR:-/tmp}/utp-report.XXXXXX")
trap 'rm -f "$room/sample.txt" "$room/out.txt" "$room/err.txt"
rmdir "$room"' 0
cd "$room"
printf '%s\n' 'Meeting: Tuesday' > ./sample.txt
result=0
grep -F 'meeting' ./sample.txt || result=$?
printf 'lowercase status: %s\n' "$result"
[ "$result" -eq 1 ]
result=0
grep -F 'Meeting' ./not-created.txt > ./out.txt 2> ./err.txt || result=$?
printf 'missing input status: %s\n' "$result"
[ "$result" -gt 1 ]
[ ! -s ./out.txt ]
[ -s ./err.txt ]
[ "$(grep -F 'Meeting' ./sample.txt)" = 'Meeting: Tuesday' ]
[ "$(grep -Fi 'meeting' ./sample.txt)" = 'Meeting: Tuesday' ]
cd /
