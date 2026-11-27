#!/usr/bin/env python3
"""Build each edition in an isolated output directory."""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = "unix-terminals-for-pleb"
EDITIONS = ("print-answers", "print-noanswers", "screen-answers", "screen-noanswers")
BAD_LOG = re.compile(
    r"Overfull \\[hv]box|Missing character:|(?:Reference|Citation) .* undefined"
    r"|multiply defined|There were undefined|Package utp-(?:dialogues|structure) Warning"
    r"|destination with the same identifier|Font shape .* undefined"
    r"|Some font shapes were not available|Label\(s\) may have changed"
    r"|Rerun to get (?:cross-references|outlines)",
    re.IGNORECASE,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("edition", nargs="?", choices=EDITIONS)
    parser.add_argument("--engine", default="pdflatex")
    parser.add_argument("--makeindex", default="makeindex")
    parser.add_argument("--draft", action="store_true")
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    build = ROOT / "build"
    if args.clean:
        for name in (*EDITIONS, *(f"draft-{edition}" for edition in EDITIONS)):
            target = build / name
            if target.is_dir() and not target.is_symlink():
                shutil.rmtree(target)
        return
    if not args.edition:
        parser.error("choose an edition")
    if not args.draft:
        subprocess.run([sys.executable, str(ROOT / "editorial/check.py"), "--release"], check=True)
    name = f"draft-{args.edition}" if args.draft else args.edition
    dest = build / name
    dest.mkdir(parents=True, exist_ok=True)
    job = f"{BOOK}-{name}"
    job_stem = dest / job
    pdf = job_stem.with_suffix(".pdf")
    # Start without previous contents, indices, or bookmarks. Leave no stale
    # PDF that could be mistaken for a successful rebuild.
    for suffix in (".aux", ".idx", ".ind", ".ilg", ".toc", ".out", ".lof", ".lot", ".fls", ".log", ".pdf"):
        job_stem.with_suffix(suffix).unlink(missing_ok=True)
    env = os.environ.copy()
    env["TEXINPUTS"] = os.pathsep.join(
        (str(ROOT / "support"), str(ROOT), env.get("TEXINPUTS", ""), "")
    )
    env.setdefault("TMPDIR", str(dest))
    # LaTeX normally looks in its current working directory for the comment
    # package's scratch file. Distinct working directories keep editions
    # from overwriting one another when built in parallel.
    options = args.edition.replace("-", ",")
    draft = r"\def\UTPEditorialDraft{1}" if args.draft else ""
    tex = draft + rf"\def\UTPEditionOptions{{{options}}}\input{{{BOOK}.ltx}}"
    command = [
        args.engine, "-no-shell-escape", "-interaction=nonstopmode",
        "-halt-on-error", "-file-line-error", "-recorder", f"-jobname={job}", tex,
    ]

    def run(command, pass_name):
        transcript = dest / (pass_name + ".txt")
        with transcript.open("w") as stream:
            result = subprocess.run(command, cwd=dest, env=env, stdout=stream, stderr=subprocess.STDOUT)
        if result.returncode:
            raise SystemExit(f"{pass_name} failed; see {transcript}")

    release_ok = False
    try:
        run(command, "tex-1")
        run(command, "tex-2")
        stable = False
        for revision in range(3, 8):
            before = [
                job_stem.with_suffix(ext).read_bytes() if job_stem.with_suffix(ext).exists() else None
                for ext in (".aux", ".toc", ".idx", ".out")
            ]
            run([args.makeindex, job + ".idx"], "makeindex")
            run(command, f"tex-{revision}")
            after = [
                job_stem.with_suffix(ext).read_bytes() if job_stem.with_suffix(ext).exists() else None
                for ext in (".aux", ".toc", ".idx", ".out")
            ]
            if before == after:
                stable = True
                break
        if not stable and not args.draft:
            raise SystemExit("Contents, references or index entries did not converge after seven TeX passes")
        log = job_stem.with_suffix(".log").read_text(errors="replace")
        index_log = job_stem.with_suffix(".ilg").read_text(errors="replace")
        found = [line.strip() for line in log.splitlines() if BAD_LOG.search(line)]
        found.extend(
            line.strip() for line in index_log.splitlines()
            if re.search(r"^## .*|[1-9][0-9]* (?:warnings?|rejected)\b", line)
        )
        if found:
            print("\n".join(found))
            if not args.draft:
                raise SystemExit(f"PDF quality gates failed; see {job_stem.with_suffix('.log')}")
        if not args.draft:
            inputs = set()
            for line in job_stem.with_suffix(".fls").read_text(errors="replace").splitlines():
                if line.startswith("INPUT "):
                    inputs.add((dest / line[6:]).resolve())
            expected = [ROOT / f"chapters/chapter-{i}.ltx" for i in range(1, 49)]
            for chapter in json.loads((ROOT / "chapters/MANIFEST.json").read_text())["chapters"]:
                expected.extend(ROOT / path for path in chapter["assets"])
            for path in expected:
                if path not in inputs:
                    raise SystemExit(f"Recorded build omitted {path.relative_to(ROOT)}")
        release_ok = True
        print(pdf)
    finally:
        if not release_ok and pdf.exists():
            pdf.unlink()


if __name__ == "__main__":
    main()
