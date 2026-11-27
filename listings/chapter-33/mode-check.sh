#!/bin/sh
# Chapter 33: POSIX sh plus mktemp; tested on an ordinary Linux account.
# All tested mode changes are on newly created fictional data.
set -eu
export LC_ALL=C
room=$(mktemp -d "${TMPDIR:-/tmp}/utp-mode.XXXXXX")
folder=$room/folder
budget=$folder/budget.txt
trap 'if [ -d "$folder" ]; then
    chmod u+x "$folder"; rm -f "$budget"; rmdir "$folder"
fi
rm -f "$room/new.txt"; rmdir "$room"' 0

mkdir -m 700 "$folder"
printf '%s\n' 'fictional lunch budget' > "$budget"
chmod u=rw,go= "$budget"
case "$(ls -ld "$budget")" in -rw-------*) ;; *) exit 1 ;; esac
chmod u-w "$budget"
case "$(ls -ld "$budget")" in -r--------*) ;; *) exit 1 ;; esac
cat "$budget"
chmod u+w "$budget"
chmod u-x "$folder"
if [ "$(id -u)" -eq 0 ]; then
    printf '%s\n' 'Skip access denial check: elevated uid.'
elif cat "$budget" 2>/dev/null; then
    printf '%s\n' 'Expected directory traversal to fail.' >&2
    exit 1
fi
chmod u+x "$folder"
[ "$(cat "$budget")" = 'fictional lunch budget' ]

before=$(umask)
( umask 077; printf '%s\n' demo > "$room/new.txt" )
case "$(ls -ld "$room/new.txt")" in -rw-------*) ;; *) exit 1 ;; esac
[ "$(umask)" = "$before" ]
