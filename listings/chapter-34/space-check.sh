#!/bin/sh
# Chapter 34: POSIX sh plus mktemp; tested on Linux.
# Filesystem observations only; never mounts, erases, or modifies volumes.
set -eu
room=$(mktemp -d "${TMPDIR:-/tmp}/utp-space.XXXXXX")
notes=$room/notes
trap 'rm -f "$notes/list.txt" "$room/.note"
if [ -d "$notes" ]; then rmdir "$notes"; fi
rmdir "$room"' 0
mkdir "$notes"
printf 'a short list\n' > "$notes/list.txt"
printf 'hidden item\n' > "$room/.note"

bytes=$(wc -c < "$notes/list.txt")
# wc may pad the count with spaces; test an integer, not its formatting.
[ "$bytes" -eq 13 ]
df -Pk "$room"
df -Pk "$notes"
du -k "$notes/list.txt"
du -sk "$room"
du -sk "$notes" "$room/.note"
