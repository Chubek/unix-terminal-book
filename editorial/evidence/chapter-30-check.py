#!/usr/bin/env python3
"""Check selected worked examples in chapters 25–30 in a disposable directory."""

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PREVIEW = ROOT / "listings/chapter-30/preview-notes.sh"


def main():
    sh = shutil.which("sh")
    assert sh, "sh is required"
    checks = []
    with tempfile.TemporaryDirectory(prefix="utp-ch25-30-") as tmp:
        work = Path(tmp)
        home = work / "home"
        home.mkdir()
        env = {
            "PATH": os.defpath,
            "HOME": str(home),
            "LC_ALL": "C",
            "TMPDIR": tmp,
            "XDG_CONFIG_HOME": str(home / "config"),
            "XDG_DATA_HOME": str(home / "data"),
        }

        def check(name, argv, *, out="", err="", status=0, source=None):
            result = subprocess.run(
                argv, input=source, text=True, capture_output=True,
                cwd=work, env=env, timeout=15, check=False,
            )
            actual = result.returncode, result.stdout, result.stderr
            assert actual == (status, out, err), f"{name}: {actual!r}"
            checks.append(name)
            print(f"PASS {name}")

        def block(chapter, starts):
            text = (ROOT / f"chapters/chapter-{chapter}.ltx").read_text()
            blocks = re.findall(r"\\begin\{terminal\}\n(.*?)\\end\{terminal\}", text, re.S)
            matches = [b for b in blocks if b.startswith(starts)]
            assert len(matches) == 1, (chapter, starts, len(matches))
            return matches[0]

        def code(chapter, starts, **kwargs):
            check(f"{chapter}: {starts}", [sh], source=block(chapter, starts), **kwargs)

        code(25, "printf '<%s>\\n' Hall plan.txt",
             out="<Hall>\n<plan.txt>\n<Hall plan.txt>\n")
        code(25, "meeting='Tuesday setup'", out="<$meeting>\n<Tuesday setup>\n")
        code(25, "printf '%s\\n' 'Send for comments'", out="Send for comments\nApproved\n")
        code(25, "grep -F", out="Hall [draft]\n")
        code(25, "printf '%s\\n' 'This is a filename'", out="This is a filename\n")

        work = work / "reading-group"
        work.mkdir()
        (work / "Long title.txt").write_text("Friday selection\n")
        (work / "Short.txt").write_text("Tuesday selection\n")
        code(26, "pattern='*.txt'", out=(
            "<*.txt>\n<Long title.txt>\n<Short.txt>\n<./Long title.txt>\n<./Short.txt>\n"
        ))
        code(26, 'printf \'<%s>\\n\' ~ "$HOME"', out=f"<{home}>\n<{home}>\n<~>\n<{home}/Reading group>\n")
        code(26, """printf '<%s>\\n' "$(printf 'queue""", out="<queue>\n<first\nsecond>\n")
        code(26, "title=$(cat", out="<Friday selection>\n<Friday>\n<selection>\n")
        code(26, 'label="', out="<'two>\n<words'>\n<'two words'>\n")
        code(26, "printf '<%s>\\n' ./*.bak", out="<./*.bak>\n")

        check("27: assignment and name boundaries", [sh],
              source=block(27, "packet='Welcome packet'") + block(27, "unset packet_notes"),
              out=("<Welcome packet.txt>\n<Welcome packet.pdf>\n<Volunteer guide.txt>\n"
                   "<Volunteer guide.pdf>\n<Volunteer guide.txt>\n<.txt>\n<Volunteer guide_notes.txt>\n"))
        code(27, "unset remark", out="<Draft>\n<Draft>\n<>\n<Draft>\n<For volunteers>\n<For volunteers>\n")
        check("27: keep or flatten positional parameters", [sh],
              source=block(27, "set -- 'Welcome packet.txt'") + block(27, 'printf \'<%s>\\n\' "$*"'),
              out=("Count: 3\nFirst: <Welcome packet.txt>\nAgain: <Welcome packet.txt>\nAgain: <>\n"
                   "Again: <Volunteer guide.pdf>\n<Welcome packet.txt  Volunteer guide.pdf>\n"
                   "<end>\n<Welcome packet.txt>\n<>\n<Volunteer guide.pdf>\n<end>\n<end>\n"))

        check("28: export, child changes, and prefix override", [sh],
              source=(block(28, "unset SWAP_LABEL") + block(28, "sh -c 'SWAP_LABEL=changed")
                      + block(28, "SWAP_LABEL='Outdoor items'")),
              out=("Parent: <Kitchen items>\nChild: <unset>\nChild: <Kitchen items>\n"
                   "<changed>\nParent: <Kitchen items>\n<Outdoor items>\n<Kitchen items>\n"))
        code(28, "printf '%s\\n' apple Apple Book", out="Apple\nBook\napple\n")
        code(28, "env SWAP_LABEL=Preview", out="<Preview>\n")

        code(29, "sh -c 'set -- \"Paper notes\" \"Photo index\"; printf \"<%s>\\n\" \"$@\"'",
             out="<Paper notes>\n<Photo index>\n")
        for recipe in block(29, "bash -c 'title=(\"Paper notes\" \"Photo index\"); printf \"<%s>\\n\" \"${title[0]}\"'").splitlines():
            shell = recipe.split()[0]
            shell_path = shutil.which(shell, path=env["PATH"])
            if shell_path:
                check(f"29: native {shell} indexing", [sh], source=recipe + "\n", out="<Paper notes>\n")
            else:
                print(f"SKIP 29: {shell} unavailable")
        for shell, starts, output in [("ksh", "ksh -c", "<Paper notes>\n"), ("tcsh", "tcsh -f", "Paper notes\n")]:
            if shutil.which(shell, path=env["PATH"]):
                code(29, starts, out=output)
            else:
                print(f"SKIP 29: {shell} unavailable")

        (work / "May notes.txt").write_text("Sample minutes\n")
        (work / "agenda.txt").write_text("Sample agenda\n")
        (work / "Handouts").mkdir()
        code(30, "test -f './May notes.txt'", out="Present: 0\nDirectory: 1\n")
        code(30, "if [ -f", out="Found a regular file\n")
        check("30: syntax check", [sh, "-n", PREVIEW])
        check("30: success", [sh, PREVIEW, "./May notes.txt", "./agenda.txt"],
              out="Would include: <./May notes.txt>\nWould include: <./agenda.txt>\n")
        check("30: absolute path", [sh, PREVIEW, str(work / "May notes.txt")],
              out=f"Would include: <{work / 'May notes.txt'}>\n")
        check("30: fail then pass", [sh, PREVIEW, "./absent.txt", "./agenda.txt", "./Handouts"],
              out="Would include: <./agenda.txt>\n", status=1, err=(
                  "Not a readable regular file: <./absent.txt>\n"
                  "Not a readable regular file: <./Handouts>\n"
              ))
        check("30: no arguments", [sh, PREVIEW], status=2,
              err="Usage: preview-notes.sh ./file ...\n")
        check("30: option-like or empty arguments", [sh, PREVIEW, "-n", ""], status=1,
              err="Use ./ or an absolute path: <-n>\nUse ./ or an absolute path: <>\n")
        assert (work / "May notes.txt").read_text() == "Sample minutes\n"
        assert (work / "agenda.txt").read_text() == "Sample agenda\n"
    print(f"{len(checks)} selected checks passed")


if __name__ == "__main__":
    main()
