#!/usr/bin/env python3
"""Verify author-owned worked commands on synthetic data; run with TMPDIR set."""
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
SHELL = os.environ.get("UTP_TEST_SH", "sh")


def run(code, cwd, status=0, args=(), stdin=None, env=None):
    result = subprocess.run(
        [SHELL, "-c", code, "verify", *map(str, args)],
        cwd=cwd, text=True, input=stdin, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    assert result.returncode == status, (code, result)
    return result.stdout


def cleanup(code, cwd, env):
    # Feed answers only to explicitly named interactive removals in the fixture.
    removals = "\n".join(line for line in code.splitlines() if line.startswith("rm -i "))
    assert removals
    remaining = code[code.rindex(removals) + len(removals):]
    for line in removals.splitlines():
        result = run(line, cwd, stdin="y\n" * 20, env=env)
        assert not result, result
    run(remaining.replace("cd /tmp", 'cd "$TMPDIR"'), cwd, env=env)
    assert not cwd.exists(), cwd


ANSWER_CASES = {
    19: {
        "grep -n -F 'gate opens'": "3:Update: north gate opens at 10\n",
        "grep -n -i -F 'gate'": (
            "meeting.txt:1:Gate opens at 9\n"
            "meeting.txt:3:Update: north gate opens at 10\n"
            "errands.txt:1:gate code changed\n"
            "errands.txt:4:Repaint gatepost\n"
        ),
        "grep -n '^Update:'": "3:Update: north gate opens at 10\n",
        "grep -n '[[:digit:]]$'": (
            "1:Gate opens at 9\n3:Update: north gate opens at 10\n4:Reminder: tea at 11\n"
        ),
        "grep -n -E": "3:Update: north gate opens at 10\n4:Reminder: tea at 11\n",
        "grep -F 'snow'": "status: 1\nstatus: 2\n",
    },
    20: {
        "uniq -c votes.txt": "1 Chess\n1 Knitting\n2 Chess\n1 Maps\n1 Knitting\n",
        "LC_ALL=C sort votes.txt |": "3 Chess\n2 Knitting\n1 Maps\n",
        "printf '%s\\n' Maps Maps Maps": "4 Maps\n3 Chess\n2 Knitting\n",
        "printf '%s\\n' '3 Maps'": "3 Chess\n3 Maps\n1 Knitting\n",
    },
    21: {
        "cut -f 1,3": "item\tstate\nHand saw\tout\nClamp set\tin\nStep ladder\tout\nOut bin\tin\n",
        "awk -F '\\t' '$3 == \"out\" { print $1 }'": "Hand saw\nStep ladder\n",
        "awk -F '\\t' -v": "state\titem\nout\tHand saw\nout\tStep ladder\n",
        "awk -F '\\t' 'NF": "status: 0\n",
        "cut -f 1 loans.tsv >": "state\titem\nout\tHand saw\nin\tClamp set\nout\tStep ladder\nin\tOut bin\n",
        "awk 'NR > 1": "Clamp set\tin\nHand saw\tout\nOut bin\tin\nStep ladder\tout\n",
    },
    22: {
        "sed 's/5/6/'": "Repair cafe\nClose: 6\nAccessible entrance\nAsk about Bay 6\n",
        "sed -n": "Close: 5\n",
        "printf '%s\\n' 'A--B----C'": "A-B-C\nrooms  and \n",
        "diff -u sign.txt sign.txt": "status: 0\n",
    },
    23: {
        "gzip -c handover.tar": "status: 0\n",
        "tar -cf rota-only.tar": "handover/rota.txt\n",
        "cat recovered/handover/key-note.txt": "Return the practice key to the desk.\n",
    },
    24: {
        "cut -d": 'caption\n"Bridge\n"The ""Old"" Gate"\n',
        "python3 -": '001: Bridge, east side\n002: The "Old" Gate\n',
        "jq -r '.[] | select(.share == true) | .id'": "001\n",
        "jq -r '.[] | select(.share == false)": "002\n",
        "jq '.[] | .score | type'": '"number"\n"null"\n',
        "jq -c '.[] | {id, share_type": '{"id":"001","share_type":"boolean"}\n{"id":"002","share_type":"boolean"}\n',
        "jq -r '.[] | select(.share == true) | [.id": '"001","Bridge, east side"\n',
    },
}
NONZERO = {
    19: {"grep -n '^Reminder:'": 1},
    22: {"diff -u sign-candidate.txt": 1},
}
LISTING = {
    19: ("search-notes.sh", "", ("gate opens", "meeting.txt", "errands.txt"), "meeting.txt:1:Gate opens at 9\nmeeting.txt:3:Update: north gate opens at 10\n"),
    20: ("tally-suggestions.sh", "votes.txt", (), "4 Maps\n3 Chess\n2 Knitting\n"),
    21: ("open-loans.sh", "loans.tsv", (), "state\titem\nout\tHand saw\nout\tStep ladder\n"),
    22: ("preview-sign.sh", "sign.txt", (), "Repair cafe\nClose: 6\nAccessible entrance\nAsk about Bay 5\n"),
    23: ("check-handover.sh", "handover.tar.gz", (), None),
    24: ("photo-review.sh", "photos.json", (), None),
}
MEMBERS = {"handover/", "handover/key-note.txt", "handover/rota.txt"}


def verify(chapter, root):
    source = ROOT / "chapters" / f"chapter-{chapter}.ltx"
    blocks = re.findall(r"\\begin\{terminal\}\n(.*?)\\end\{terminal\}", source.read_text(), re.S)
    assert len(blocks) >= 11
    setup = blocks[0].splitlines(keepends=True)
    assert setup[0].startswith("practice=$(mktemp -d /tmp/utp")
    assert setup[1] == 'cd "$practice"\n'
    work = root / f"utp{chapter}.fixture"
    work.mkdir()
    env = dict(os.environ, TMPDIR=str(root), practice=str(work), LC_ALL="C")
    run("".join(setup[2:]), work, env=env)
    matches = set()
    for block in blocks[1:-1]:
        status = next((value for prefix, value in NONZERO.get(chapter, {}).items() if block.startswith(prefix)), 0)
        out = run(block, work, status, env=env)
        if chapter == 20:
            out = "".join(line.lstrip(" ") + "\n" for line in out.splitlines())
        for prefix, expected in ANSWER_CASES[chapter].items():
            if block.startswith(prefix):
                assert out == expected, (chapter, prefix, repr(out), repr(expected))
                matches.add(prefix)
        if chapter == 23 and "tar -tf" in block and not block.startswith("tar -cf rota-only.tar"):
            assert set(out.splitlines()) == MEMBERS, out
        if chapter == 23 and block.startswith("cp -i"):
            first, second = (line.split()[0] for line in out.splitlines())
            assert first == second and re.fullmatch(r"[0-9a-f]{64}", first), out
        if chapter == 22 and block.startswith("sed 's/^Close: 5$/Close: 6/' sign.txt >"):
            assert "@@ -1,4 +1,4 @@" in out and "-Close: 5\n+Close: 6\n" in out, out
            assert " Accessible entrance\n" in out and out.endswith("status: 1\n"), out
    assert matches == ANSWER_CASES[chapter].keys(), matches
    name, input_file, args, expected = LISTING[chapter]
    listing = ROOT / "listings" / f"chapter-{chapter}" / name
    if input_file:
        out = run('"$1" "$2" < "$3"', work, args=(SHELL, listing, input_file), env=env)
    else:
        out = run('"$1" "$2" "$3" "$4" "$5"', work, args=(SHELL, listing, *args), env=env)
    if chapter == 20:
        out = "".join(line.lstrip(" ") + "\n" for line in out.splitlines())
    if chapter == 23:
        assert set(out.splitlines()) == MEMBERS
        assert (work / "handover.tar").read_bytes() == (work / "restored.tar").read_bytes()
        for name in ("rota.txt", "key-note.txt"):
            assert (work / "handover" / name).read_bytes() == (work / "recovered" / "handover" / name).read_bytes()
    elif chapter == 24:
        import json
        assert json.loads(out) == [{"id": "001", "caption": "Bridge, east side"}]
        assert json.loads((work / "review.json").read_text()) == json.loads(out)
    else:
        assert out == expected, (name, repr(out), repr(expected))
    cleanup(blocks[-1], work, env)
    print(f"chapter {chapter}: {len(blocks)} terminal blocks, {len(matches)} exact transcript cases, listing and cleanup PASS")


with tempfile.TemporaryDirectory(prefix="utp-w4-") as temporary:
    for number in range(19, 25):
        verify(number, Path(temporary))
