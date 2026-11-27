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

        def guarded_setup(chapter):
            setup = block(chapter, "practice=$(mktemp -d) &&")
            success = subprocess.run([sh], input=setup, cwd=work, env=env, text=True,
                                     capture_output=True, timeout=15, check=False)
            created = Path(success.stdout.strip())
            assert success.returncode == 0 and not success.stderr and created.is_dir(), success
            assert created.parent == Path(tmp).resolve(), created
            failed = subprocess.run([sh], input=setup, cwd=work,
                                    env=dict(env, TMPDIR=str(work / "missing-parent")),
                                    text=True, capture_output=True, timeout=15, check=False)
            assert failed.returncode != 0 and not failed.stdout and failed.stderr, failed
            checks.append(f"{chapter}: guarded scratch setup")
            print(f"PASS {chapter}: guarded scratch setup and intentional failure")

        guarded_setup(25)
        code(25, "printf '<%s>\\n' Hall plan.txt",
             out="<Hall>\n<plan.txt>\n<Hall plan.txt>\n")
        code(25, "meeting='Tuesday setup'", out="<$meeting>\n<Tuesday setup>\n")
        code(25, "printf '%s\\n' 'Send for comments'", out="Send for comments\nApproved\n")
        code(25, "grep -F", out="Hall [draft]\n")
        code(25, "printf '%s\\n' 'This is a filename'", out="This is a filename\n")
        code(25, "printf '<%s>\\n' 'Hall [draft]'.*", out="<Hall [draft].txt>\n<Hall [draft].*>\n")
        code(25, "printf '<%s>\\n' Hall\\ [draft].txt\nmv -i",
             out="<Hall d.txt>\n<Hall a.txt>\nSend for comments\n")
        assert (work / "Hall d.txt").read_text() == "Approved\n"
        assert not (work / "Hall a.txt").exists()

        work = work / "reading-group"
        work.mkdir()
        guarded_setup(26)
        assert not list(work.iterdir())
        (work / "Long title.txt").write_text("Friday selection\n")
        (work / "Short.txt").write_text("Tuesday selection\n")
        code(26, "pattern='*.txt'", out=(
            "<*.txt>\n<Long title.txt>\n<Short.txt>\n<./Long title.txt>\n<./Short.txt>\n"
        ))
        code(26, 'printf \'<%s>\\n\' ~ "$HOME"', out=f"<{home}>\n<{home}>\n<~>\n<{home}/Reading group>\n")
        code(26, """printf '<%s>\\n' "$(printf 'queue""", out="<queue>\n<first\nsecond>\n")
        code(26, "title=$(cat 'Long title.txt')", out="<Friday selection>\n<Friday>\n<selection>\n")
        code(26, 'label="', out="<'two>\n<words'>\n<'two words'>\n")
        code(26, "printf '<%s>\\n' ./*.bak", out="<./*.bak>\n")
        code(26, "value=$(printf '%s' '')", out="Status: 0; value: <>\nStatus: 1; value: <>\n")
        code(26, "report='*.txt Friday'", out=(
            "<Long title.txt>\n<Short.txt>\n<Friday>\n<*.txt>\n<Friday>\n<*.txt Friday>\n"
        ))

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
        code(27, "set -- '$HOME' '*' ''", out="Supplied: <$HOME>\nSupplied: <*>\nSupplied: <>\n")
        heading_prefix = "set -- 'For printing' 'June notes.txt' 'Floor plan.pdf'\n"
        heading_code = block(27, heading_prefix)
        check("27: shift title and preserve paths", [sh], source=heading_code, out=(
            "Heading: <For printing>\nRemaining count: 2\n"
            "Attachment or marker: <June notes.txt>\nAttachment or marker: <Floor plan.pdf>\n"
            "Attachment or marker: <end>\n"
        ))
        check("27: no heading supplied", [sh], source=heading_code.replace(heading_prefix, "set --\n"))
        check("27: an explicit blank heading", [sh], source=heading_code.replace(heading_prefix, "set -- ''\n"),
              out="Heading: <>\nRemaining count: 0\nAttachment or marker: <end>\n")

        check("28: export, child changes, and prefix override", [sh],
              source=(block(28, "unset SWAP_LABEL") + block(28, "sh -c 'SWAP_LABEL=changed")
                      + block(28, "SWAP_LABEL='Outdoor items'")),
              out=("Parent: <Kitchen items>\nChild: <unset>\nChild: <Kitchen items>\n"
                   "<changed>\nParent: <Kitchen items>\n<Outdoor items>\n<Kitchen items>\n"))
        code(28, "printf '%s\\n' apple Apple Book", out="Apple\nBook\napple\n")
        code(28, "env SWAP_LABEL=Preview", out="<Preview>\n")
        code(28, "SWAP_LABEL='Kitchen items'",
             out="Before: <Kitchen items>\nInside: <Children>\nAfter: <Kitchen items>\n")
        code(28, "export SWAP_LABEL=''", out="<>\n<unset>\n")

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
        posix_probe, zsh_probe = block(29, "sh -c 'printf \"<%s>\\n\" ./*.absent'").splitlines()
        check("29: sh leaves unmatched pattern", [sh], source=posix_probe + "\n", out="<./*.absent>\n")
        if shutil.which("zsh", path=env["PATH"]):
            outcome = subprocess.run([sh], input=zsh_probe + "\n", capture_output=True,
                                     cwd=work, env=env, text=True, timeout=15, check=False)
            assert outcome.returncode != 0 and not outcome.stdout and "no matches found" in outcome.stderr, outcome
            checks.append("29: zsh rejects unmatched pattern")
            print("PASS 29: zsh rejects unmatched pattern")

        (work / "May notes.txt").write_text("Sample minutes\n")
        (work / "agenda.txt").write_text("Sample agenda\n")
        (work / "Handouts").mkdir()
        code(30, "test -f './May notes.txt'", out="Present: 0\nDirectory: 1\n")
        code(30, "if [ -f", out="Found a regular file\n")
        code(30, "printf '<%s>\\n' ./May notes.txt",
             out="<./May>\n<notes.txt>\n<./agenda.txt>\n<./May notes.txt>\n<./agenda.txt>\n")
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
        (work / "May-link.txt").symlink_to("May notes.txt")
        check("30: symlink passes when target is regular and readable", [sh, PREVIEW, "./May-link.txt"],
              out="Would include: <./May-link.txt>\n")
        (work / "Blank.txt").touch()
        check("30: empty readable regular file passes", [sh, PREVIEW, "./Blank.txt"],
              out="Would include: <./Blank.txt>\n")
        assert (work / "May notes.txt").read_text() == "Sample minutes\n"
        assert (work / "agenda.txt").read_text() == "Sample agenda\n"
    print(f"{len(checks)} selected checks passed")


if __name__ == "__main__":
    main()
