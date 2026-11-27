#!/bin/sh
# POSIX sh; requires GNU/BSD mktemp -d. Sets up then removes only its fixtures.
# Use: TMPDIR=/absolute/trusted/scratch sh listings/chapter-12/check-cleanup.sh
set -eu
export LC_ALL=C
practice=$(mktemp -d "${TMPDIR:?set an absolute scratch directory}/utp-12.XXXXXXXX")
printf 'Practice path: %s\n' "$practice"
cd "$practice"
printf '%s\n' 'Train leaves at 08:12' > ./plan.txt
printf '%s\n' 'Possible earlier train' > ./scratch.txt
cp -i ./plan.txt ./reference.txt
cmp ./plan.txt ./reference.txt
mkdir ./hold
mv -i ./scratch.txt ./hold/scratch.txt
[ ! -e ./scratch.txt ]
[ -f ./hold/scratch.txt ]
mv -i ./hold/scratch.txt ./scratch.txt
[ "$(cat ./scratch.txt)" = 'Possible earlier train' ]
printf 'n\n' | rm -i ./scratch.txt || [ "$?" -eq 1 ]
[ -f ./scratch.txt ]
printf 'y\n' | rm -i ./scratch.txt
[ ! -e ./scratch.txt ]
cmp ./plan.txt ./reference.txt
cp -i ./reference.txt ./restored-plan.txt
[ "$(cat ./restored-plan.txt)" = 'Train leaves at 08:12' ]
cmp ./reference.txt ./restored-plan.txt
printf '%s\n' 'For review' > ./review-note.txt
printf 'n\n' | rm -i ./review-note.txt || [ "$?" -eq 1 ]
[ -f ./review-note.txt ]
printf 'y\n' | rm -i ./review-note.txt
[ ! -e ./review-note.txt ]
mv -i ./restored-plan.txt ./hold/restored-plan.txt
cmp ./reference.txt ./hold/restored-plan.txt
mv -i ./hold/restored-plan.txt ./restored-plan.txt
mkdir ./try-empty
touch ./try-empty/.marker
if rmdir ./try-empty; then
    exit 1
fi
printf 'y\n' | rm -i ./try-empty/.marker
rmdir ./try-empty
rm ./plan.txt ./reference.txt ./restored-plan.txt
rmdir ./hold
cd /
rmdir "$practice"
