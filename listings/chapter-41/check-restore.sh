#!/bin/sh
# POSIX sh syntax; mktemp and tar with -cf/-tf/-xf required. Local fixtures only.
set -eu
lab=$(mktemp -d)
cleanup() {
    cd "$lab"
    rm -f documents/plan.txt documents/contact.txt \
        restore/monday/documents/plan.txt restore/monday/documents/contact.txt \
        restore/tuesday/documents/plan.txt restore/tuesday/documents/contact.txt \
        restore/jan07.check restore/jan08.check \
        vault/documents-2030-01-07.tar vault/documents-2030-01-08.tar \
        vault/jan07.cksum vault/jan08.cksum
    for d in restore/monday/documents restore/monday restore/tuesday/documents \
        restore/tuesday documents restore vault; do
        if test -d "$d"; then rmdir "$d"; fi
    done
    cd /
    rmdir "$lab"
}
trap cleanup EXIT
cd "$lab"
(umask 077; mkdir documents vault restore)
printf '%s\n' 'Monday: one box of flyers' > documents/plan.txt
printf '%s\n' 'Contact the community desk' > documents/contact.txt
tar -cf vault/documents-2030-01-07.tar documents
cksum < vault/documents-2030-01-07.tar > vault/jan07.cksum
printf '%s\n' 'Tuesday: two boxes of flyers' > documents/plan.txt
tar -cf vault/documents-2030-01-08.tar documents
cksum < vault/documents-2030-01-08.tar > vault/jan08.cksum
for day in monday tuesday; do
    case "$day" in
        monday) number=07 ;;
        tuesday) number=08 ;;
    esac
    archive=vault/documents-2030-01-$number.tar
    record=jan$number
    cksum < "$archive" > "restore/$record.check"
    cmp "restore/$record.check" "vault/$record.cksum"
    members=$(tar -tf "$archive" | LC_ALL=C sort)
    test "$members" = "$(printf '%s\n' documents/ documents/contact.txt documents/plan.txt)"
    mkdir "restore/$day"
    (cd "restore/$day" && tar -xf "../../$archive")
    cmp "restore/$day/documents/contact.txt" documents/contact.txt
done
test "$(cat restore/monday/documents/plan.txt)" = 'Monday: one box of flyers'
test "$(cat restore/tuesday/documents/plan.txt)" = 'Tuesday: two boxes of flyers'
cmp restore/tuesday/documents/plan.txt documents/plan.txt
status=0
cmp restore/monday/documents/plan.txt restore/tuesday/documents/plan.txt >/dev/null || status=$?
test "$status" -eq 1
printf '%s\n' 'Both restore drills passed.'
