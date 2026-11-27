#!/bin/sh
# POSIX sh; Linux, macOS, BSD. Run from the chapter 46 fixture root.
needle=${1:-library}
printf '%s\n' 'Note matches:'
grep -Fin -e "$needle" ./notes/monday.txt ./notes/thursday.txt
case $? in
    0) ;;
    1) printf '%s\n' 'No note matches.' ;;
    *) printf '%s\n' 'Could not check all notes.' >&2; exit 2 ;;
esac
printf '%s\n' 'Handoff comparison:'
diff -u ./before.txt ./after.txt
case $? in
    0) printf '%s\n' 'Handoffs are identical.' ;;
    1) printf '%s\n' 'Handoffs differ.' ;;
    *) printf '%s\n' 'Comparison failed.' >&2; exit 2 ;;
esac
