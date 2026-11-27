#!/bin/sh
# POSIX sh and find syntax; requires GNU/BSD mktemp -d.
# Use: TMPDIR=/absolute/trusted/scratch sh listings/chapter-9/check-records.sh
set -eu
export LC_ALL=C
root=$(mktemp -d "${TMPDIR:?set an absolute scratch directory}/utp09.XXXXXXXX")
printf 'Practice path: %s\n' "$root"
cd "$root"
mkdir -p ./records/april ./records/may ./records/.drafts
touch ./records/april/agenda.txt ./records/may/agenda.txt
touch './records/may/Final Agenda.txt' ./records/.drafts/agenda.txt
mkdir ./records/may/agenda-old.txt
[ "$(find ./records -print | wc -l | tr -d ' ')" -eq 9 ]
[ "$(find ./records -name 'agenda.txt' -print | wc -l | tr -d ' ')" -eq 3 ]
[ "$(find ./records -name '*.txt' -print | wc -l | tr -d ' ')" -eq 5 ]
[ "$(find ./records -type f -name '*.txt' -print | wc -l | tr -d ' ')" -eq 4 ]
[ "$(find ./records -type d -name '*.txt' -print)" = ./records/may/agenda-old.txt ]
[ "$(find ./records -type d -name '.*' -print)" = ./records/.drafts ]
[ "$(find ./records -type f -name 'Final Agenda.txt' -print)" = './records/may/Final Agenda.txt' ]
touch ./shell-sample.txt
[ "$(printf '%s\n' '*.txt')" = '*.txt' ]
[ "$(printf '%s\n' *.txt)" = shell-sample.txt ]
names=$(find ./records -type f -name 'agenda-final.txt' -print)
[ -z "$names" ]
if find ./missing-records -print; then
    exit 1
fi
[ "$(find ./records/may -name 'agenda*.txt' -print | wc -l | tr -d ' ')" -eq 2 ]
[ "$(find ./records/may -type f -name '*.txt' -print | wc -l | tr -d ' ')" -eq 2 ]
rm ./records/april/agenda.txt ./records/may/agenda.txt \
    './records/may/Final Agenda.txt' ./records/.drafts/agenda.txt ./shell-sample.txt
rmdir ./records/may/agenda-old.txt ./records/april ./records/may ./records/.drafts ./records
cd /
rmdir "$root"
