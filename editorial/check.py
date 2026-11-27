#!/usr/bin/env python3
"""Validate the chapter contract and run explicitly registered practice checks."""

import argparse
import json
import os
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATES = {"planned", "drafting", "review", "revision", "verified", "integrated", "blocked"}
REQUIRED = {"number", "part", "title", "prerequisites", "topics", "owner", "reviewer", "assets", "status"}


def contents(path):
    return (ROOT / path).read_text()


def begins(text, group):
    return re.findall(r"(?m)^[ \t]*\\begin\{(" + group + r")\}", text)


def validate(release):
    manifest = json.loads(contents("chapters/MANIFEST.json"))
    chapters = manifest["chapters"]
    master = contents("unix-terminals-for-pleb.ltx")
    errors = []

    def require(ok, issue):
        if not ok:
            errors.append(issue)

    require([c["number"] for c in chapters] == list(range(1, 49)), "manifest must list chapters 1–48 in order")
    require(Counter(c["part"] for c in chapters) == {i: 12 for i in range(1, 5)}, "expected 4 parts of 12 chapters")
    require(len(manifest["parts"]) == 4, "expected 4 part titles")
    events = re.findall(r"(?m)^\\(BookPart|BookChapter)\{([^{}]+)\}(?:\\label\{ch:(\d+)\})?", master)
    expected = []
    for c in chapters:
        if (c["number"] - 1) % 12 == 0:
            expected.append(("BookPart", manifest["parts"][c["part"] - 1], ""))
        expected.append(("BookChapter", c["title"], str(c["number"])))
    require(events == expected, "master part/chapter titles and labels must match the manifest in order")
    inputs = re.findall(r"(?m)^\\input\{chapters/chapter-(\d+)\.ltx\}", master)
    require(inputs == [str(i) for i in range(1, 49)], "master chapter inputs must be 1–48 in order")
    require(bool(re.search(r"\\input\{chapters/chapter-48\.ltx\}\s*\\CheckBookStructure\s*\\BeginAppendices", master)),
            "master must check structure after chapter 48 and before appendices")
    primary = master[master.index(r"\BeginAppendices"):]
    require(len(re.findall(r"(?m)^\\chapter\{", primary)) == 2, "master must emit exactly two appendices")
    require(sum(path.read_text().count(r"\RequirePackage{utp-dialogues}") for path in
                [*ROOT.glob("*.cls"), *ROOT.glob("support/*.sty")]) +
            master.count(r"\usepackage{utp-dialogues}") == 1, "load the dialogue module exactly once")
    labels = Counter(re.findall(r"\\label\{([^{}]+)\}", master))
    totals = Counter()
    for chapter in chapters:
        n = chapter["number"]
        part = (n - 1) // 12 + 1
        prefix = f"chapter {n}"
        require(REQUIRED <= chapter.keys(), f"{prefix}: missing required map fields")
        require(chapter["part"] == part, f"{prefix}: wrong part")
        require(chapter["owner"] == f"W{(n - 1) // 6 + 1}", f"{prefix}: wrong owner")
        reviewer = chapter["reviewer"]
        require(reviewer in {f"W{i}" for i in range(1, 9)} and reviewer != chapter["owner"],
                f"{prefix}: invalid peer reviewer")
        priors = chapter["prerequisites"]
        require(all(1 <= p < n for p in priors) and len(priors) == len(set(priors)),
                f"{prefix}: prerequisites must be unique earlier chapters")
        require(bool(chapter["topics"]), f"{prefix}: no coverage topics")
        require(chapter["status"] in STATES, f"{prefix}: unknown status")
        require(isinstance(chapter["assets"], list), f"{prefix}: assets must be a list")
        for asset in chapter["assets"]:
            file = ROOT / asset
            require(not Path(asset).is_absolute() and file.resolve().is_relative_to(ROOT) and file.is_file()
                    and file.stat().st_size > 0, f"{prefix}: missing or invalid asset {asset}")
        raw = contents(f"chapters/chapter-{n}.ltx")
        source = re.sub(r"(?m)^[ \t]*%.*$", "", raw)
        require(not re.search(r"\\(?:BookChapter|BookPart|part|chapter|documentclass)\b|\\(?:begin|end)\{document\}", source),
                f"{prefix}: document wrapper or part/chapter declaration in fragment")
        labels.update(re.findall(r"\\label\{([^{}]+)\}", source))
        figures = len(begins(source, r"figure\*?")) + len(re.findall(r"\\(?:BookFigure|AccessibleFigure)\b", source))
        tables = len(begins(source, "quicktable|longtable"))
        examples = len(begins(source, "terminal|session|shellscript")) + len(re.findall(r"\\ShellFile\b", source))
        exercises = len(begins(source, "exercise"))
        solutions = len(begins(source, "solution"))
        dialogues = re.findall(r"\\begin\{dialoguebox\}(.*?)\\end\{dialoguebox\}", source, re.S)
        totals.update({
            "nonempty chapters": bool(source.strip()), "figures": figures, "tables": tables,
            "example blocks": examples, "exercises": exercises, "solutions": solutions,
            "dialogues": len(dialogues), "integrated chapters": chapter["status"] == "integrated",
        })
        for dialogue in dialogues:
            require(6 <= len(re.findall(r"\\(?:Brian|Stephen)\{", dialogue)) <= 12,
                    f"{prefix}: dialogue must have 6–12 speaker turns")
            require(dialogue.count(r"\DialogueConclusion{") == 1 and
                    not re.search(r"\\DialogueConclusion.*\\(?:Brian|Stephen)\{", dialogue, re.S),
                    f"{prefix}: dialogue must end with one conclusion")
        if release:
            require(chapter["status"] == "integrated", f"{prefix}: not integrated")
            require(bool(source.strip()) and bool(begins(source, "objectives")) and bool(begins(source, "takeaways")),
                    f"{prefix}: missing chapter content, objectives or takeaways")
            require(figures >= 3 and tables >= 2 and examples >= 8, f"{prefix}: visual/table/example minimum not met")
            require(exercises >= 3 and solutions == exercises, f"{prefix}: missing exercise or solution")
            require(bool(dialogues), f"{prefix}: missing dialogue")
            require(r"\FigurePlaceholder" not in source, f"{prefix}: placeholder figure")
            for folder in ("evidence", "reviews"):
                record = ROOT / "editorial" / folder / f"chapter-{n}.md"
                require(record.is_file() and record.stat().st_size > 0, f"{prefix}: no {folder} record")
    for name in ("frontmatter", "preface", "appendix-a", "appendix-b", "backmatter"):
        source = contents(f"chapters/{name}.ltx")
        require(bool(source.strip()), f"{name}: empty")
        labels.update(re.findall(r"\\label\{([^{}]+)\}", source))
    require(all(count == 1 for count in labels.values()), "duplicate LaTeX label")
    if release:
        require(48 <= totals["dialogues"] <= 60, "expected 48–60 dialogues")
    print(", ".join(f"{v} {k}" for k, v in totals.items()))
    if errors:
        raise SystemExit("\n".join(errors))


def examples():
    # Only run curated harnesses, never arbitrary terminal boxes or all files
    # in listings/. A harness must work on artificial fixtures in a fresh cwd.
    registry = json.loads(contents("editorial/example-checks.json"))
    if not registry:
        raise SystemExit("No curated example checks registered")
    build = ROOT / "build"
    build.mkdir(exist_ok=True)
    for entry in registry:
        path = (ROOT / entry["path"]).resolve()
        if not path.is_relative_to(ROOT / "editorial") or not path.is_file():
            raise SystemExit(f"Invalid example harness: {entry['path']}")
        with tempfile.TemporaryDirectory(prefix="example-", dir=build) as temp:
            env = {"PATH": os.defpath, "HOME": temp, "TMPDIR": temp, "LC_ALL": "C"}
            subprocess.run([entry["interpreter"], str(path)], check=True, env=env, cwd=temp, timeout=60)
        print(f"PASS: {entry['path']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--release", action="store_true")
    modes.add_argument("--examples", action="store_true")
    args = parser.parse_args()
    if args.examples:
        examples()
    else:
        validate(args.release)
