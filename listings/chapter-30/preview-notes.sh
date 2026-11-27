#!/bin/sh
# Interpreter: POSIX sh. Read-only; run as sh preview-notes.sh ./file ...
# Intended for Linux, macOS, FreeBSD, OpenBSD and NetBSD.

if [ "$#" -eq 0 ]; then
    printf '%s\n' 'Usage: preview-notes.sh ./file ...' >&2
    exit 2
fi

result=0
for note in "$@"; do
    case "$note" in
        ./*|/*) ;;
        *)
            printf 'Use ./ or an absolute path: <%s>\n' "$note" >&2
            result=1
            continue
            ;;
    esac
    if [ -f "$note" ] && [ -r "$note" ]; then
        printf 'Would include: <%s>\n' "$note"
    else
        printf 'Not a readable regular file: <%s>\n' "$note" >&2
        result=1
    fi
done
exit "$result"
