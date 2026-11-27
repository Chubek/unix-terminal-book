"""Check chapters 43–48 on a Unix host; run with TMPDIR on an approved volume.

Exercises the typeset commands in fresh fixtures. Never runs the SFTP example.
"""

import json
import os
from pathlib import Path
import pty
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]


def examples(n):
    text = (ROOT / f"chapters/chapter-{n}.ltx").read_text()
    return re.findall(r"\\begin\{terminal\}\n(.*?)\\end\{terminal\}", text, re.S)


def get(blocks, prefix):
    return next(b for b in blocks if b.startswith(prefix))


def shell_run(argv, code, cwd, expected=0, tty=False, stdin_script=False):
    env = {"PATH": os.environ["PATH"], "HOME": str(cwd), "TERM": "dumb",
           "LC_ALL": "C", "TMPDIR": str(cwd)}
    if tty:
        master, slave = pty.openpty()
        try:
            proc = subprocess.run(argv + ["-c", code], stdin=slave,
                                  text=True, capture_output=True,
                                  cwd=cwd, env=env, timeout=15)
        finally:
            os.close(master)
            os.close(slave)
    elif stdin_script:
        proc = subprocess.run(argv + ["-s"], input=code, text=True,
                              capture_output=True, cwd=cwd, env=env,
                              timeout=15)
    else:
        proc = subprocess.run(argv + ["-c", code], text=True,
                              capture_output=True, cwd=cwd, env=env,
                              timeout=15)
    if proc.returncode != expected:
        raise AssertionError((proc.returncode, code, proc.stdout, proc.stderr))
    return proc.stdout, proc.stderr


def copied(n, name, path):
    shutil.copyfile(ROOT / f"listings/chapter-{n}/{name}", path)


def blocks_run(n, shell, cwd, prefixes, extra="", expected=0):
    blocks = examples(n)
    code = "\n".join(get(blocks, prefix) for prefix in prefixes) + "\n" + extra
    return shell_run(shell, code, cwd, expected)


def check_setup_gate(n, shell, cwd):
    setup = get(examples(n), "lab=$(mktemp")
    fail = "mktemp() { return 1; }\ncd() { printf 'unexpected cd\\n'; }\n"
    out, err = shell_run(shell, fail + setup, cwd, expected=1)
    assert not out and not err


def check_43(cwd):
    bash = ["bash", "--noprofile", "--norc", "-i"]
    b = examples(43)
    copied(43, "candidate.sh", cwd / "candidate.sh")
    out, err = shell_run(bash, "PS1='practice> '\n" +
                         ". ./candidate.sh\ninspect .\nunalias inspect\n" +
                         get(b, "unset UTP43_NOTE\nUTP43_NOTE=visible") +
                         get(b, "unset UTP43_NOTE\nUTP43_NOTE=once"),
                         cwd)
    assert out.splitlines()[1:] == ["unset", "visible", "once", "unset"]
    assert out.splitlines()[0].endswith(" .") and "not found" not in err
    assert "syntax error" not in shell_run(["sh"], "sh -n ./candidate.sh", cwd)[1]
    if shutil.which("zsh"):
        assert shell_run(["zsh", "-f", "-i"],
                         ". ./candidate.sh\ninspect .\nexit\n", cwd,
                         stdin_script=True)[0].strip().endswith(" .")


def check_44(cwd, shell):
    out, _ = blocks_run(44, shell, cwd, [
        "lab=$(mktemp", "printf '%s\\n' 'open:", "head -n 2",
        "grep -n '^open:'", "grep -q '^waiting:'",
        "printf '%s\\n' 'Last open", "head -n 1 ./absent",
        "grep -n '^done:'", "rm ./done.txt", "rm ./tasks.txt",
    ])
    assert "search status: 0" in out and "No waiting items." in out
    assert out.count("3:open: choose next title") == 2
    assert "2:done: return the book" in out and "./absent.txt" in out
    assert out.splitlines()[3].strip() == "3"


def check_45(cwd, shell):
    out, err = blocks_run(45, shell, cwd, [
        "lab=$(mktemp", "mkdir ./work", "(cd ./other && { pwd",
        '(PATH="$lab/other"; command -v utp45-report\n printf',
        "ls -ld ./work", "(cd ./other && cat ../work/report.txt)",
        "(cd ./other && cat ./report.txt)", "rm ./work/report.txt",
    ])
    assert "helper ran" in out and "lookup status: 1" in out
    assert out.count("Inventory: four notebooks") == 2
    assert "Report passes the read-access check." in out
    assert "attempt status: 1" in out and "report.txt" in err
    assert "speed" in shell_run(shell, "stty -a", cwd, tty=True)[0]


def check_46(cwd, shell):
    b = examples(46)
    script = ROOT / "listings/chapter-46/check-notes.sh"
    setup = (get(b, "lab=$(mktemp") + get(b, "mkdir ./notes") +
             get(b, "printf '%s\\n' 'Start at ten'"))
    # Copy using the harness rather than asking a reader to type a system path.
    out, err = shell_run(shell, setup + f'cp "{script}" ./check-notes.sh\n' +
                         "\n".join(get(b, x) for x in [
                             "grep -Fin -e 'library'", "head -n 1",
                             "diff -u ./before.txt ./after.txt\n",
                             "diff -u ./before.txt ./after.txt >",
                             "diff -u ./after.txt ./after.txt",
                             "sh -n", "sh ./check-notes.sh 'opens at'",
                             "mv -i ./notes/thursday.txt", "rm ./notes/monday.txt",
                         ]), cwd)
    assert "search status: 0" in out and "search status: 1" in out
    assert "same file, status: 0" in out and "comparison status: 1" in out
    assert "Handoffs differ." in out and "No note matches." in out
    assert "routine status: 2" in out and "Could not check all notes." in err


def check_47(cwd, shell):
    b = examples(47)
    script = ROOT / "listings/chapter-47/catalog.py"
    out, err = shell_run(shell, get(b, "lab=$(mktemp") +
                         f'cp "{script}" ./catalog.py\n' +
                         "\n".join(get(b, x) for x in [
                             "file ./intake", "printf '%s\\n' 'filename,album,title'",
                             "python3 ./catalog.py ./catalog.csv >", "mkdir ./stage/water",
                             "cmp ./intake/canal.jpg ./stage/water",
                             "cksum < ./intake/canal.jpg", "grep -n -F",
                             "printf '%s\\n' 'filename,album,title' \\\n    'canal.jpg,parking",
                             "cmp ./intake/canal.jpg './stage/street", "rm './stage/street",
                         ]), cwd)
    catalog = json.JSONDecoder().raw_decode(out[out.index("["):])[0]
    assert [row["title"] for row in catalog] == ["Canal, after rain", "Green front door"]
    assert [row["destination"] for row in catalog] == [
        "stage/water/canal.jpg", "stage/street/front door.jpg"]
    assert "canal comparison: 0" in out and "door comparison: 0" in out
    assert "mismatched pair: 1" in out and "correct pair: 0" in out
    assert "trial status: 1" in out and "unknown album" in err
    sums = re.findall(r"^\d+ \d+$", out, re.M)
    assert len(sums) == 2 and sums[0] == sums[1]


def check_48(cwd, shell, tar="tar"):
    b = examples(48)
    code = "\n".join(get(b, x) for x in [
        "lab=$(mktemp", "find ./source", "tar -cf", "cksum < ./round",
        "cp -i ./round", "ls -a ./restored", "cmp ./source/contact.txt ./restored/source/contact.txt",
        "cksum < ./handoff", "cmp ./source/contact.txt ./restored/source/notes",
        "printf '%s\\n' 'round-01.tar: offline", "rm ./restored",
    ])
    out, _ = shell_run(shell, re.sub(r"\btar -", tar + " -", code), cwd)
    assert "retrieval comparison status: 0" in out
    assert "contact comparison status: 0" in out and "meeting comparison status: 0" in out
    assert "wrong-path comparison status: 1" in out and "right-path comparison status: 0" in out
    sums = re.findall(r"^\d+ \d+$", out, re.M)
    assert len(sums) == 3 and len(set(sums)) == 1


def main():
    with tempfile.TemporaryDirectory(prefix="utp-w8-tests.") as root:
        root = Path(root)
        check_43(root)
        (root / "candidate.sh").unlink()
        print("43: Bash prompt/alias candidate and inheritance, Zsh if installed")
        for shell in [["sh"], ["bash", "--noprofile", "--norc"], ["zsh", "-f"]]:
            if not shutil.which(shell[0]):
                continue
            for n in (44, 45, 46):
                check_setup_gate(n, shell, root)
            check_44(root, shell)
            check_45(root, shell)
            check_46(root, shell)
            check_47(root, shell)
            check_48(root, shell)
            if shutil.which("bsdtar"):
                check_48(root, shell, "bsdtar")
            assert not list(root.iterdir()), "one of the chapter cleanups left files"
            print(f"44–48: checked disposable fixture round trips with {shell[0]}")


if __name__ == "__main__":
    main()
