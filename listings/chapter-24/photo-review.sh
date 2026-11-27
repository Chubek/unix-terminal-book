#!/bin/sh
# POSIX sh syntax; requires optional jq. JSON array on standard input.
# Usage: sh photo-review.sh < photos.json
jq '[.[] | select(.share == true) | {id, caption}]'
