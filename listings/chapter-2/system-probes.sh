#!/bin/sh
# POSIX sh; use an empty disposable working directory.
# The GNU long option is a probe, not a requirement for passing the checks.
set -eu
name=$(uname -s)
release=$(uname -r)
[ "$(uname)" = "$name" ]
[ "$(uname -s -r)" = "$name $release" ]
[ -n "$(uname -m)" ]
[ "$(printf '%s\n' 'A familiar request')" = 'A familiar request' ]
all=$(ls -a)
if extra=$(ls --all); then
    [ "$all" = "$extra" ]
    printf '%s\n' 'This ls also accepted --all.'
else
    printf '%s\n' 'This ls did not accept --all.'
fi
printf '%s\n' 'Chapter 2 checks passed.'
