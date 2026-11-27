#!/bin/sh
# Chapter 35: POSIX sh; tested on Linux. No package or network operations.
# Checks selection without running the looked-up tool.
set -eu
printf '%s\n' 'Operating system family:'
uname -s
printf '%s\n' 'Shell lookup for sh:'
command -v sh
if command -v jq; then
    printf '%s\n' 'jq resolves in this shell; inspect the identification above.'
else
    printf '%s\n' 'jq does not resolve in this shell; no install attempted.'
fi
if [ -r /etc/os-release ]; then
    grep -E '^(NAME|VERSION_ID)=' /etc/os-release || :
fi
