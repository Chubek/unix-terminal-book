#!/bin/sh
# POSIX sh; no writes. Run from a disposable working directory other than /.
set -eu
start=$(pwd)
[ "$start" != / ]
command -v cd
command -v uname
command -v printf
command -V printf
if command -v utp-invented-63098; then
    printf '%s\n' 'Choose a different invented name for this check.'
    exit 1
fi
command -v pwd
[ "$(/bin/sh -c 'cd / && pwd')" = / ]
[ "$(pwd)" = "$start" ]
printf '%s\n' 'Chapter 3 checks passed.'
