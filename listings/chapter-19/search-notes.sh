#!/bin/sh
# POSIX sh and grep; ASCII text inputs. Read-only; pass explicit paths.
# Usage: sh search-notes.sh 'gate opens' ./meeting.txt ./errands.txt
if [ "$#" -lt 2 ]; then
    printf '%s\n' 'usage: search-notes.sh phrase ./file [./file ...]' >&2
    exit 2
fi
pattern=$1
shift
LC_ALL=C grep -n -i -F -e "$pattern" -- "$@"
