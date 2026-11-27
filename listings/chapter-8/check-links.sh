#!/bin/sh
# sh syntax; requires test -ef, mktemp -d, and a same-filesystem scratch base.
# Use: TMPDIR=/absolute/trusted/scratch sh listings/chapter-8/check-links.sh
set -eu
export LC_ALL=C
root=$(mktemp -d "${TMPDIR:?set an absolute scratch directory}/utp08.XXXXXXXX")
printf 'Practice path: %s\n' "$root"
cd "$root"
mkdir ./forms ./events
mkdir ./events/june
mkdir -p ./events/july/check-in
if rmdir ./events/july; then
    exit 1
fi
rmdir ./events/july/check-in ./events/july
printf '%s\n' 'Item to repair:' > ./forms/intake.txt
ln ./forms/intake.txt ./events/june/intake-same.txt
[ ./forms/intake.txt -ef ./events/june/intake-same.txt ]
mv -i ./forms/intake.txt ./forms/intake-master.txt
[ ./forms/intake-master.txt -ef ./events/june/intake-same.txt ]
ln -s ../../forms/intake-master.txt ./events/june/intake-way.txt
ls -li ./forms/intake-master.txt ./events/june/intake-same.txt
ls -l ./events/june/intake-way.txt
cmp ./forms/intake-master.txt ./events/june/intake-way.txt
mv -i ./forms/intake-master.txt ./forms/intake-revised.txt
if cmp ./forms/intake-revised.txt ./events/june/intake-way.txt; then
    exit 1
else
    [ "$?" -gt 1 ]
fi
cmp ./forms/intake-revised.txt ./events/june/intake-same.txt
mv -i ./forms/intake-revised.txt ./forms/intake-master.txt
cmp ./forms/intake-master.txt ./events/june/intake-way.txt
ln -s ../forms ./events/current-forms
physical=$(cd ./forms && pwd -P)
cd -L ./events/current-forms
[ "$(pwd -L)" = "$root/events/current-forms" ]
[ "$(pwd -P)" = "$physical" ]
cd -L ../..
[ "$(pwd -L)" = "$root" ]
mkdir -p ./events/august/notes
rmdir ./events/august/notes ./events/august
cp -i ./forms/intake-master.txt ./events/june/independent.txt
cmp ./forms/intake-master.txt ./events/june/independent.txt
if [ ./forms/intake-master.txt -ef ./events/june/independent.txt ]; then
    exit 1
fi
ln -s ../forms/intake-master.txt ./events/shortcut.txt
cmp ./forms/intake-master.txt ./events/shortcut.txt
rm ./events/current-forms ./events/june/intake-way.txt ./events/june/intake-same.txt \
    ./events/june/independent.txt ./events/shortcut.txt ./forms/intake-master.txt
rmdir ./events/june ./events ./forms
cd /
rmdir "$root"
