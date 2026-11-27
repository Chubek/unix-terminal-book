#!/usr/bin/env python3
"""Smoke-test the real class in both layouts with and without solutions."""

import argparse
import itertools
import os
import subprocess
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", default="pdflatex")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    build = root / "build"
    build.mkdir(exist_ok=True)
    env = os.environ.copy()
    env["TEXINPUTS"] = os.pathsep.join((str(root / "support"), str(root), env.get("TEXINPUTS", ""), ""))
    with tempfile.TemporaryDirectory(dir=build, prefix="toolkit-") as temp:
        for layout, answers in itertools.product(("print", "screen"), ("answers", "noanswers")):
            dest = Path(temp) / f"{layout}-{answers}"
            dest.mkdir()
            tex = rf"\def\UTPEditionOptions{{{layout},{answers}}}\input{{editorial/tests/edition-fixture.ltx}}"
            result = subprocess.run(
                [args.engine, "-no-shell-escape", "-halt-on-error", "-interaction=nonstopmode", "-jobname=fixture", tex],
                cwd=dest, env=env, capture_output=True, text=True,
            )
            if result.returncode:
                raise SystemExit(result.stdout + result.stderr)
            log = (dest / "fixture.log").read_text(errors="replace")
            if "Dialogue conclusion exceeds one line" in log or "Overfull \\" in log:
                raise SystemExit(f"Fixture overflow in {layout}-{answers}")
            text = subprocess.check_output(["pdftotext", str(dest / "fixture.pdf"), "-"], text=True)
            info = subprocess.check_output(["pdfinfo", str(dest / "fixture.pdf")], text=True)
            expected = ("Dialogue Box 1", "Use a fixture, not your own files.", "This exercise appears in both editions.")
            if not all(phrase in text for phrase in expected):
                raise SystemExit(f"Fixture dialogue or exercise missing in {layout}-{answers}")
            if ("fixture answer token" in text) != (answers == "answers"):
                raise SystemExit(f"Wrong solution visibility in {layout}-{answers}")
            if "504 x 720 pts" not in info:
                raise SystemExit(f"Wrong page dimensions in {layout}-{answers}")
            print(f"PASS: {args.engine} {layout}-{answers}")


if __name__ == "__main__":
    main()
