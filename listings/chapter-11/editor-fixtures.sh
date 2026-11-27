#!/bin/sh
# POSIX sh; requires GNU/BSD mktemp -d. Creates but does not edit or delete.
# Use: TMPDIR=/absolute/trusted/scratch sh listings/chapter-11/editor-fixtures.sh
set -eu
root=$(mktemp -d "${TMPDIR:?set an absolute scratch directory}/utp11.XXXXXXXX")
cd "$root"
printf '%s\n' 'Buy oats' 'Return library book' > ./errands.txt
cp -i ./errands.txt ./errands-original.txt
cp -i ./errands-original.txt ./errands-nano.txt
cp -i ./errands-original.txt ./errands-test.txt
printf '%s\n' "$root"
