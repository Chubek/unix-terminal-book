# Chapter 42 — Inspect Media and Documents

- `TMPDIR=/mnt/nvme sh listings/chapter-42/check-media.sh` passed on
  Linux x86-64 with file 5.48, ImageMagick 7.1.2-31, TeX Live 2024,
  Poppler 26.08.0 and FFmpeg/ffprobe 9.0.1. The mislabeled text was
  classified as text; the PPM and PNG were recognized. The PNG
  derivative lost the observed comment and kept the same two-by-two
  pixel enumeration as the original. The locally built PDF had one
  page with the fixture sentence. A locally synthesized WAV tested the
  illustrative ffprobe command (`pcm_s16le`, one channel).
- No external files or conversion services were used. Source links
  cover the Netpbm specification, ImageMagick options, Poppler and
  FFmpeg. Optional package versions and metadata behavior on macOS
  and the BSDs were not tested. The selected comment check is not
  evidence of sanitization for other images or formats.
- `figures/chapter-42/`: `three-checks.tikz`, `derivative.tikz`,
  `content.tikz`. Slice build and grayscale check: see `chapter-37.md`.
