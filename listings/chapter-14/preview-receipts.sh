#!/bin/sh
# POSIX sh syntax; mktemp -d is a widely available extension.
# Usage: sh preview-receipts.sh, or zsh --emulate sh preview-receipts.sh
# Native Zsh is not a substitute here: its unmatched-glob default differs.
set -eu
export LC_ALL=C
lab=$(mktemp -d)
trap 'rm -f "$lab/march-1.txt" "$lab/march-2.txt" "$lab/march-12.txt" "$lab/march coffee.txt" "$lab/feb-1.txt" "$lab/march-1.pdf" "$lab/.march-3.txt" "$lab/archive/march-4.txt"; rmdir "$lab/archive" "$lab"' 0
cd "$lab"
mkdir archive
touch march-1.txt march-2.txt march-12.txt 'march coffee.txt'
touch feb-1.txt march-1.pdf .march-3.txt archive/march-4.txt
set -- ./march*.txt
test "$#" -eq 4
seen=no
for path in "$@"; do
    if test "$path" = './march coffee.txt'; then seen=yes; fi
done
test "$seen" = yes
set -- ./march-[!2].txt
test "$#" -eq 1
test "$1" = ./march-1.txt
set -- ./.march-?.txt
test "$1" = ./.march-3.txt
set -- ./april*.txt
test "$1" = './april*.txt'
paths=$(find . -type f -name 'march-?.txt' -print)
test "$(printf '%s\n' "$paths" | awk 'END { print NR }')" -eq 3
printf '[%s]\n' ./march*.txt ./*/march-?.txt
