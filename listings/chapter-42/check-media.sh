#!/bin/sh
# POSIX sh syntax. Linux tested; optional tools: ImageMagick 7, pdfLaTeX,
# Poppler, FFmpeg (including ffprobe); also requires mktemp and file.
set -eu
export LC_ALL=C
lab=$(mktemp -d "${TMPDIR:-/tmp}/utp-media.XXXXXXXX")
cleanup() {
    cd "$lab"
    rm -f ./not-a-pdf.pdf ./tiles.ppm ./tiles.png ./release/tiles-share.png \
        ./program.tex ./program.pdf ./program.aux ./program.log ./clip.wav
    rmdir ./release
    cd /
    rmdir "$lab"
}
trap cleanup EXIT
cd "$lab"
mkdir release
printf '%s\n' 'This is only a line of text.' > ./not-a-pdf.pdf
file ./not-a-pdf.pdf | grep 'text'
printf '%s\n' P3 '# synthetic tiles' '2 2' '255' \
  '255 0 0  0 255 0' '0 0 255  255 255 255' > ./tiles.ppm
file ./tiles.ppm | grep -Ei 'netpbm|pixmap'
magick ./tiles.ppm -set comment 'fictional noticeboard' ./tiles.png
magick ./tiles.png -strip ./release/tiles-share.png
test "$(magick identify -format '%w x %h: %c\n' ./tiles.png)" = \
    '2 x 2: fictional noticeboard'
test "$(magick identify -format '%w x %h: %c\n' ./release/tiles-share.png)" = '2 x 2: '
test "$(magick ./tiles.png txt:-)" = "$(magick ./release/tiles-share.png txt:-)"
printf '%s\n' '\documentclass{article}' '\begin{document}' \
  'The practice event begins at noon.\end{document}' > ./program.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error ./program.tex >/dev/null
file ./program.pdf | grep 'PDF document'
pdfinfo ./program.pdf | grep -E '^Pages:[[:space:]]+1$'
pdftotext ./program.pdf - | grep -F 'The practice event begins at noon.'
# Generate a local sine wave, not a downloaded media stream.
ffmpeg -v error -nostdin -n -f lavfi -i 'sine=frequency=440:duration=1' ./clip.wav
stream=$(ffprobe -v error -show_streams ./clip.wav)
printf '%s\n' "$stream" | grep -Fx 'codec_name=pcm_s16le'
printf '%s\n' "$stream" | grep -Fx 'channels=1'
test "$(ls ./release)" = tiles-share.png
printf '%s\n' 'Local image, PDF and audio checks passed.'
