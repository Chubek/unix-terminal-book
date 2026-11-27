#!/bin/sh
# Chapter 32: POSIX sh plus mktemp; tested on Linux.
# No interactive job-control keystrokes. Writes only a new scratch file.
set -eu
room=$(mktemp -d "${TMPDIR:-/tmp}/utp-jobs.XXXXXX")
trap 'rm -f "$room/result.txt"; rmdir "$room"' 0

( sleep 1 && printf '%s\n' 'practice finished' ) > "$room/result.txt" &
child=$!
printf '%s\n' 'The shell can continue.'
wait "$child"
printf 'job status: %s\n' "$?"
cat "$room/result.txt"
[ "$(cat "$room/result.txt")" = 'practice finished' ]
