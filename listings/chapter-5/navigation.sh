#!/bin/sh
# POSIX sh; use a new disposable directory as HOME.
# Pass that same existing absolute directory as the only argument.
set -eu
case ${1-} in /*) ;; *) exit 2 ;; esac
HOME=$1
export HOME
cd
[ "$(pwd)" = "$1" ]
mkdir ./utp-nav-5-7319
cd ./utp-nav-5-7319
mkdir ./Holiday ./Volunteers
mkdir ./Holiday/Plans ./Volunteers/Plans
[ "$(ls -1)" = 'Holiday
Volunteers' ]
[ "$(ls ./Holiday)" = Plans ]
[ "$(ls ./Volunteers)" = Plans ]
[ "$(ls -d ./Volunteers/Plans)" = ./Volunteers/Plans ]
cd ./Holiday/Plans
[ "$(pwd)" = "$HOME/utp-nav-5-7319/Holiday/Plans" ]
[ -z "$(ls)" ]
if cd ./Not-Made; then exit 1; fi
[ "$(pwd)" = "$HOME/utp-nav-5-7319/Holiday/Plans" ]
cd
rmdir ./utp-nav-5-7319/Holiday/Plans
rmdir ./utp-nav-5-7319/Volunteers/Plans
rmdir ./utp-nav-5-7319/Holiday
rmdir ./utp-nav-5-7319/Volunteers
rmdir ./utp-nav-5-7319
[ ! -d ./utp-nav-5-7319 ]
printf '%s\n' 'Chapter 5 checks passed.'
