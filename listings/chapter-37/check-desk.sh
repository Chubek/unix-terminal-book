#!/bin/sh
# POSIX sh syntax; mktemp required. Optional host observations are local only.
set -eu
desk=$(mktemp -d "${TMPDIR:-/tmp}/utp-desk.XXXXXXXX")
cleanup() {
    cd /
    rm -f "$desk/desk.log"
    rmdir "$desk"
}
trap cleanup EXIT
cd "$desk"
printf '%s\n' \
  '14:00 lookup: no answer recorded' \
  '14:05 lookup: IPv4 192.0.2.25' \
  '14:05 transport: connection opened' \
  '14:05 web: HTTP 404 for /rooms/tuesday' > desk.log
test "$(grep -F -c 'lookup:' desk.log)" -eq 2
test "$(grep -F -c 'web:' desk.log)" -eq 1
test "$(grep -F -c 'transport:' desk.log)" -eq 1
status=0
grep -F 'TLS:' desk.log || status=$?
test "$status" -eq 1
status=0
grep -F 'transport:' absent.log 2>/dev/null || status=$?
test "$status" -gt 1
printf '%s\n' 'Desk report assertions passed.'
