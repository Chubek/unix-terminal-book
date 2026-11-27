#!/bin/sh
# POSIX sh syntax; mktemp -d is a widely available extension.
# Usage: sh measure-catalog.sh (set a UTF-8 locale to check character counts)
set -eu
lab=$(mktemp -d)
trap 'rm -f "$lab/catalog.txt" "$lab/partial.txt" "$lab/accent.txt" "$lab/combining.txt"; rmdir "$lab"' 0
cd "$lab"
printf '%s\n' 'Library sale' 'Saturday' 'Art books' 'Field guides' \
    'Mystery novels' 'End of list' > catalog.txt
test "$(head -n 1 catalog.txt)" = 'Library sale'
test "$(tail -n 1 catalog.txt)" = 'End of list'
test "$(tail -n +3 catalog.txt | head -n 3 | tail -n 1)" = 'Mystery novels'
test "$(wc -l < catalog.txt)" -eq 6
test "$(wc -w < catalog.txt)" -eq 12
test "$(wc -c < catalog.txt)" -eq 72
printf '%s' 'last but not terminated' > partial.txt
test "$(wc -l < partial.txt)" -eq 0
test "$(wc -w < partial.txt)" -eq 4
printf 'Caf\303\251\n' > accent.txt
printf 'Cafe\314\201\n' > combining.txt
test "$(wc -c < accent.txt)" -eq 6
test "$(wc -c < combining.txt)" -eq 7
status=0
cmp -s accent.txt combining.txt || status=$?
test "$status" -eq 1
case $(locale charmap) in
    UTF-8|UTF8|utf-8|utf8)
        test "$(wc -m < accent.txt)" -eq 5
        test "$(wc -m < combining.txt)" -eq 6
        printf '%s\n' 'Verified UTF-8 character counts: 5 and 6.'
        ;;
    *) printf '%s\n' 'Character counts skipped: active locale is not UTF-8.' ;;
esac
wc -l -w -c catalog.txt
