#!/usr/bin/env python3
"""Assemble pinned worker snapshots into a separate editorial proof tree."""

import argparse
import subprocess
import tarfile
import tempfile
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "9d22ff3"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def extract(dest, ref, paths=()):
    data = git("archive", ref, "--", *paths)
    with tarfile.open(fileobj=BytesIO(data)) as archive:
        for entry in archive.getmembers():
            if (not (entry.isdir() or entry.isfile()) or
                    not (dest / entry.name).resolve().is_relative_to(dest)):
                raise SystemExit(f"Unexpected archive member: {entry.name}")
        archive.extractall(dest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("refs", nargs=8, metavar="COMMIT", help="author snapshots in W1–W8 order")
    args = parser.parse_args()
    build = ROOT / "build"
    build.mkdir(exist_ok=True)
    dest = Path(tempfile.mkdtemp(dir=build, prefix="whole-book-proof-"))
    extract(dest, "HEAD")
    for worker, ref in enumerate(args.refs, 1):
        first = 6 * worker - 5
        numbers = set(range(first, first + 6))
        paths = git("diff", "--name-only", "--diff-filter=AM", "-z", BASE, ref).decode().strip("\0").split("\0")
        for path in paths:
            # Author snapshot extraction cannot overwrite W0's shared files.
            if not (
                any(path in {f"chapters/chapter-{n}.ltx", f"editorial/evidence/chapter-{n}.md"} or
                    path.startswith((f"figures/chapter-{n}/", f"listings/chapter-{n}/", f"editorial/evidence/chapter-{n}-")) for n in numbers)
                or path.startswith("editorial/evidence/") and not path.startswith("editorial/evidence/chapter-")
            ):
                raise SystemExit(f"W{worker} source contains unexpected path {path}")
        extract(dest, ref, paths)
    (dest / "author-snapshots.txt").write_text("\n".join(
        f"W{i}: {git('rev-parse', ref).decode().strip()}" for i, ref in enumerate(args.refs, 1)
    ) + "\n")
    print(dest)


if __name__ == "__main__":
    main()
