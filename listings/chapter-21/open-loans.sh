#!/bin/sh
# POSIX sh and awk. TSV input on standard input; item, shelf, state.
# Usage: sh open-loans.sh < loans.tsv
awk -F '\t' -v OFS='\t' 'NR == 1 || $3 == "out" { print $3, $1 }'
