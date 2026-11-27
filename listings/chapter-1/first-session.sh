#!/bin/sh
# POSIX sh; run from an empty disposable working directory.
# Read-only: prints messages and checks that observation does not move the shell.
set -eu
[ "$(printf '%s\n' 'Hello, terminal')" = 'Hello, terminal' ]
[ "$(printf '%s\n' 'Tea' 'Toast')" = 'Tea
Toast' ]
[ "$(printf '%s\n' 'Tea Toast')" = 'Tea Toast' ]
start=$(pwd)
printf '%s\n' 'Checking my starting point'
if pwd -Q; then
    printf '%s\n' 'Unexpected: pwd accepted the test option.'
    exit 1
fi
[ "$(pwd)" = "$start" ]
printf '%s\n' 'Chapter 1 checks passed.'
