#!/bin/sh
# POSIX sh; pass a new disposable absolute directory to serve as HOME.
set -eu
case ${1-} in /*) ;; *) exit 2 ;; esac
HOME=$1
export HOME
cd
[ "$(pwd)" = "$1" ]
mkdir ./utp-path-6-8562
cd ./utp-path-6-8562
mkdir ./albums ./shared
mkdir './albums/April photos'
[ "$(printf '%s\n' './albums/April photos')" = './albums/April photos' ]
[ "$(printf '%s\n' ./albums/April photos)" = './albums/April
photos' ]
ls -d './albums/April photos/'
cd './albums/April photos'
album=$(pwd)
cd .
[ "$(pwd)" = "$album" ]
cd ..
[ "$(pwd)" = "$HOME/utp-path-6-8562/albums" ]
cd ../shared
[ "$(pwd)" = "$HOME/utp-path-6-8562/shared" ]
cd "$album"
[ "$(pwd)" = "$album" ]
cd ~
[ "$(pwd)" = "$HOME" ]
[ "$(printf '%s\n' '~')" = '~' ]
rmdir './utp-path-6-8562/albums/April photos'
rmdir ./utp-path-6-8562/albums
rmdir ./utp-path-6-8562/shared
rmdir ./utp-path-6-8562
[ ! -d ./utp-path-6-8562 ]
printf '%s\n' 'Chapter 6 checks passed.'
