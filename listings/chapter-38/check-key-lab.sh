#!/bin/sh
# POSIX sh syntax; OpenSSH with -G and Ed25519, mktemp required.
# This does not connect or enroll the disposable teaching key.
set -eu
lab=$(mktemp -d)
cleanup() {
    cd /
    rm -f "$lab/demo-key" "$lab/demo-key.pub"
    rmdir "$lab"
}
trap cleanup EXIT
cd "$lab"
for pair in learner:2222 student:2022; do
    user=${pair%:*}
    port=${pair#*:}
    cfg=$(ssh -F /dev/null -G -T -p "$port" "$user@unix.example.org")
    printf '%s\n' "$cfg" | grep -Fx 'host unix.example.org'
    printf '%s\n' "$cfg" | grep -Fx "user $user"
    printf '%s\n' "$cfg" | grep -Fx "port $port"
done
ssh-keygen -q -t ed25519 -C practice-only -f ./demo-key -N ''
fingerprint=$(ssh-keygen -lf ./demo-key.pub)
test "$(ssh-keygen -lf ./demo-key.pub)" = "$fingerprint"
printf '%s\n' "$fingerprint" | grep -E 'SHA256:.* practice-only ' >/dev/null
printf '%s\n' 'Offline SSH and key assertions passed.'
