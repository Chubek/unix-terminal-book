# Chapter 40 — Return to a Remote Session

- `TMPDIR=/mnt/nvme python3 listings/chapter-40/check-session.py` passed
  on Linux x86-64 with tmux 3.7c. Two local pseudo-terminal clients
  used a private socket and no tmux configuration. The first attached
  and set a marker, detached via the default prefix and `d`, and the
  second attached by exact name and printed the same shell variable.
  Exiting its only pane left no server sessions reachable. The version
  tested can leave a stale socket path, so the chapter does not require
  the path to disappear by itself.
- No SSH disconnection or server reboot was simulated; policy and
  installation notes for macOS/BSD are untested. See installed/upstream
  tmux documentation for options and key bindings. The Python utility
  is a reproduction harness, not a prerequisite of the reader's lab.
- Revision check: the printed construction and invocation, with a
  local stub in place of tmux, blocked an empty lab path, a relative
  path and an absolute path not matching the current directory.
  The valid case passed only the intended absolute socket. The real
  private tmux PTY check also passed separately.
- `figures/chapter-40/`: `location.tikz`, `detach.tikz`, `recover.tikz`.
  Slice build and grayscale check: see `chapter-37.md`.
