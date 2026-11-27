#!/usr/bin/env python3
"""W0-only editor for the canonical chapter map."""

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "chapters/MANIFEST.json"
STATES = ("planned", "drafting", "review", "revision", "verified", "integrated", "blocked")


def chapter_assets(n):
    source = (ROOT / f"chapters/chapter-{n}.ltx").read_text()
    figures = re.findall(r"\\input\{(figures/chapter-" + str(n) + r"/[\w.-]+)\}", source)
    listings = re.findall(r"\\ShellFile(?:\[[^\n]*?\])?\{(listings/chapter-" + str(n) + r"/[\w.-]+)\}", source)
    assets = sorted(set(figures + listings))
    if not figures or any(not (ROOT / asset).is_file() for asset in assets):
        raise SystemExit(f"Chapter {n}: missing registered figure or listing source")
    return assets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("status", choices=STATES)
    parser.add_argument("chapters", nargs="+", type=int, choices=range(1, 49), metavar="N")
    args = parser.parse_args()
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    if branch != "utp/integration":
        raise SystemExit("only W0 edits the canonical chapter map")
    data = json.loads(MANIFEST.read_text())
    for n in args.chapters:
        chapter = data["chapters"][n - 1]
        if chapter["number"] != n:
            raise SystemExit(f"Chapter {n} is out of order")
        if args.status in {"verified", "integrated"}:
            if chapter["status"] not in {"review", "revision", "verified", "integrated"}:
                raise SystemExit(f"Chapter {n} is not yet in the review workflow")
            for folder in ("evidence", "reviews"):
                record = ROOT / "editorial" / folder / f"chapter-{n}.md"
                if not record.is_file() or record.stat().st_size == 0:
                    raise SystemExit(f"Chapter {n}: missing {folder} record")
            chapter["assets"] = chapter_assets(n)
        chapter["status"] = args.status

    rows = ",\n".join("    " + json.dumps(chapter, ensure_ascii=False, separators=(",", ":"))
                      for chapter in data["chapters"])
    result = "{\n  \"parts\": " + json.dumps(data["parts"], ensure_ascii=False) + ",\n"
    result += "  \"chapters\": [\n" + rows + "\n  ]\n}\n"
    with tempfile.NamedTemporaryFile(dir=MANIFEST.parent, prefix=".manifest-", delete=False, mode="w") as f:
        scratch = Path(f.name)
        f.write(result)
    try:
        scratch.chmod(MANIFEST.stat().st_mode & 0o777)
        scratch.replace(MANIFEST)
    finally:
        scratch.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
