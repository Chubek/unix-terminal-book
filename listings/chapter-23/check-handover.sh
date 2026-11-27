#!/bin/sh
# POSIX sh syntax; requires gzip and tar. Lists a trusted practice archive.
# Usage: sh check-handover.sh < handover.tar.gz
# Run the gzip integrity check on the named archive separately before use:
# portable pipeline status reports tar's result, not gzip's.
gzip -dc | tar -tf -
