#!/usr/bin/env python3
"""Unix Python 3 + tmux 3.x + xterm terminfo. Two local PTY clients only."""
import errno
import os
import pty
import select
import subprocess
import tempfile
import time


def wait_for(predicate):
    limit = time.monotonic() + 8
    while time.monotonic() < limit:
        if predicate():
            return
        time.sleep(0.03)
    raise AssertionError("Timed out waiting for the private tmux session")


def main():
    with tempfile.TemporaryDirectory(prefix="utp40-") as lab:
        socket = os.path.join(lab, "lab.sock")
        env = dict(os.environ, TERM="xterm", ENV="/dev/null", PS1="practice> ")
        env.pop("TMUX", None)
        base = ["tmux", "-S", socket]
        child = None
        terminal = None

        def run(*words, check=True):
            return subprocess.run(
                base + list(words), cwd=lab, env=env, check=check,
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )

        def attach(first=False):
            nonlocal child, terminal
            master, slave = pty.openpty()
            args = (["-f", "/dev/null", "new-session", "-s", "lesson", "sh"]
                    if first else ["attach-session", "-t", "=lesson"])
            try:
                child = subprocess.Popen(
                    base + args, stdin=slave, stdout=slave, stderr=slave,
                    cwd=lab, env=env,
                )
            finally:
                os.close(slave)
            terminal = master
            wait_for(lambda: run("list-clients", check=False).stdout and child.poll() is None)

        def send(data):
            os.write(terminal, data)

        def wait_output(line):
            def receive():
                if select.select([terminal], [], [], 0.1)[0]:
                    try:
                        observed.extend(os.read(terminal, 4096))
                    except OSError as error:
                        if error.errno != errno.EIO:
                            raise
                return line in observed

            observed = bytearray()
            wait_for(receive)

        def close_client():
            nonlocal terminal, child
            assert child.wait(timeout=8) == 0
            os.close(terminal)
            terminal = None
            child = None

        try:
            attach(first=True)
            send(b"marker=returned; printf '%s\\n' \"$marker\"\r")
            wait_output(b"\nreturned")
            send(b"\x02d")  # default Ctrl-b, then d
            close_client()
            assert run("list-sessions").stdout.startswith("lesson:")
            attach()
            send(b"printf '%s:%s\\n' second \"$marker\"\r")
            wait_output(b"\nsecond:returned")
            send(b"exit\r")
            close_client()
            wait_for(lambda: run("list-sessions", check=False).returncode != 0)
        finally:
            if child is not None and child.poll() is None:
                child.terminate()
                child.wait(timeout=8)
            if terminal is not None:
                os.close(terminal)
            if os.path.exists(socket):
                run("kill-server", check=False)
    print("Private tmux attach, detach, return and exit assertions passed.")


if __name__ == "__main__":
    main()
