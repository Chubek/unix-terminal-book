#!/bin/sh
# POSIX sh syntax; mktemp -d is a widely available extension.
# Usage: sh count-boxes.sh (use the default last-stage pipeline rule)
set -eu
lab=$(mktemp -d)
trap 'rm -f "$lab/donations.txt" "$lab/box-rows.txt" "$lab/total.txt" "$lab/checked-rows.txt" "$lab/diagnostic.txt"; rmdir "$lab"' 0
cd "$lab"
printf '%s\n' 'Donation list' 'Saturday' 'Mystery box' \
    'Poetry box' 'Garden box' > donations.txt
test "$(tail -n +3 donations.txt | wc -l)" -eq 3
test "$(tail -n +3 donations.txt | tee box-rows.txt | wc -l)" -eq 3
tail -n +3 donations.txt | wc -l | tee total.txt
test "$(cat total.txt)" -eq 3
tail -n +3 donations.txt > checked-rows.txt
cmp -s box-rows.txt checked-rows.txt
test "$(tail -n +3 not-here.txt 2> diagnostic.txt | wc -l)" -eq 0
test -s diagnostic.txt
if tail -n +3 not-here.txt 2>/dev/null; then exit 1; fi
report=$(tail -n +3 donations.txt | wc -l donations.txt)
# read splits the count from the fixed fixture name and discards column padding.
read -r count name <<EOF
$report
EOF
test "$count" -eq 5
test "$name" = donations.txt
printf '%s\n' 'The missing producer reported an error; its consumer counted zero.'
