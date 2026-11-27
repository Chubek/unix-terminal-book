#!/bin/sh
# POSIX sh syntax; GNU/BSD mktemp -d and file are required.
# Use: TMPDIR=/absolute/trusted/scratch sh listings/chapter-7/check-rota.sh
set -eu
export LC_ALL=C
root=$(mktemp -d "${TMPDIR:?set an absolute scratch directory}/utp07.XXXXXXXX")
printf 'Practice path: %s\n' "$root"
cd "$root"
printf '%s\n' 'Saturday: morning shift' > './rota original.txt'
cp -i './rota original.txt' './rota working.txt'
mkdir ./outbox
cp -i './rota original.txt' ./outbox
cp -i './rota original.txt' './outbox/week 1.txt'
file './rota original.txt' ./outbox
cmp './rota original.txt' './rota working.txt'
printf '%s\n' 'Saturday: evening shift' > ./different.txt
if cmp './rota original.txt' ./different.txt; then
    exit 1
else
    [ "$?" -eq 1 ]
fi
mv -i './rota working.txt' './outbox/rota ready.txt'
[ ! -e './rota working.txt' ]
printf 'n\n' | cp -i ./different.txt './outbox/rota ready.txt' || [ "$?" -eq 1 ]
cmp './rota original.txt' './outbox/rota ready.txt'
cp -i './rota original.txt' './outbox/weekend handoff.txt'
cmp './rota original.txt' './outbox/weekend handoff.txt'
mv -i './outbox/rota ready.txt' ./proof.txt
cmp './rota original.txt' ./proof.txt
mv -i ./proof.txt './outbox/rota ready.txt'
[ ! -e ./proof.txt ]
rm './rota original.txt' ./different.txt './outbox/rota original.txt' \
    './outbox/week 1.txt' './outbox/rota ready.txt' \
    './outbox/weekend handoff.txt'
rmdir ./outbox
cd /
rmdir "$root"
