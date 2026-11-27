#!/bin/sh
# POSIX sh; expects local man/apropos pages, mktemp -d, and a C-locale cp.
# Use: TMPDIR=/absolute/trusted/scratch sh listings/chapter-10/check-manual.sh
set -eu
export LC_ALL=C
# The -w report checks local page resolution, not pager interaction.
man -w cp
man -w ls
man -w mv
man -w find
man -w 1 printf
man -w 3 printf
man -w 1 cmp
man -k 'copy files'
apropos 'copy files'
man -k 'compare'
command -V cd
command -V printf
command -V cp
root=$(mktemp -d "${TMPDIR:?set an absolute scratch directory}/utp10.XXXXXXXX")
printf 'Practice path: %s\n' "$root"
cd "$root"
touch ./one.txt ./two.txt
printf 'n\n' | cp -i ./one.txt ./two.txt || [ "$?" -eq 1 ]
cmp ./one.txt ./two.txt
rm ./one.txt ./two.txt
cd /
rmdir "$root"
