#!/bin/sh
# POSIX sh and sed. Old sign on standard input; candidate on standard output.
# Usage: sh preview-sign.sh < sign.txt
sed 's/^Close: 5$/Close: 6/'
