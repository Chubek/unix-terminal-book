#!/bin/sh
# POSIX sh syntax; mktemp and upstream rsync required. No remote endpoints.
set -eu
lab=$(mktemp -d)
cleanup() {
    cd /
    rm -f "$lab/source/agenda.txt" \
        "$lab/receive/agenda-received.txt" "$lab/receive/agenda-revised.txt"
    rmdir "$lab/source" "$lab/receive" "$lab"
}
trap cleanup EXIT
cd "$lab"
mkdir source receive
printf '%s\n' '18:00 open the hall' '18:15 check the chairs' > source/agenda.txt
with_slash=$(rsync -r -n -i ./source/ ./receive/)
without_slash=$(rsync -r -n -i ./source ./receive/)
printf '%s\n' "$with_slash" | grep -E ' agenda\.txt$'
printf '%s\n' "$without_slash" | grep -E ' source/agenda\.txt$'
test -z "$(ls -A ./receive)"
cp -i ./source/agenda.txt ./receive/agenda-received.txt
cmp ./source/agenda.txt ./receive/agenda-received.txt
printf '%s\n' '18:30 close the hall' > ./receive/agenda-revised.txt
status=0
cmp ./source/agenda.txt ./receive/agenda-revised.txt >/dev/null || status=$?
test "$status" -eq 1
printf '%s\n' 'Local preview and comparison assertions passed.'
