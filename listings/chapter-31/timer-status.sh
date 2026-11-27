#!/bin/sh
# Chapter 31: POSIX sh; needs sleep, ps, and kill. Tested on Linux.
# This signals only the child timer created immediately below.
sleep 15 &
timer=$!
case "$timer" in
    ''|*[!0-9]*|0) exit 1 ;;
esac

if ! ps -p "$timer" -o pid -o ppid -o args; then
    wait "$timer"
    exit 1
fi

kill -s TERM "$timer"
request=$?
wait "$timer"
result=$?
printf 'request status: %s\nchild status: %s\n' "$request" "$result"
[ "$request" -eq 0 ] && [ "$result" -gt 128 ]
