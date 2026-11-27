#!/bin/sh
# Run with an empty working directory by check.py. No external files.
set -eu
mkdir source target
printf '%s\n' 'ferry' 'walk' 'ferry' > source/notes.txt
cp -i source/notes.txt target/notes.txt
cmp source/notes.txt target/notes.txt
test "$(grep -nF -e ferry source/notes.txt)" = "$(printf '%s\n' '1:ferry' '3:ferry')"
test "$(head -n 1 source/notes.txt)" = ferry
test "$(wc -l < source/notes.txt | tr -d ' ')" = 3
test "$(LC_ALL=C sort source/notes.txt | uniq -c | tr -d ' ')" = "$(printf '%s\n' 2ferry 1walk)"
sed 's/ferry/train/' source/notes.txt > target/new.txt
if diff -u source/notes.txt target/new.txt > delta.txt; then
    exit 1
else
    test "$?" -eq 1
fi
grep -F -e '+train' delta.txt > /dev/null
cksum < source/notes.txt > source.sum
cksum < target/notes.txt > target.sum
cmp source.sum target.sum
tar -cf parcel.tar source/notes.txt
test "$(tar -tf parcel.tar)" = source/notes.txt
