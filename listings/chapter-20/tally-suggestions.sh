#!/bin/sh
# POSIX sh, sort, uniq. ASCII suggestions on standard input, one vote per line.
# Usage: sh tally-suggestions.sh < votes.txt
LC_ALL=C sort | LC_ALL=C uniq -c | LC_ALL=C sort -k 1,1nr -k 2
