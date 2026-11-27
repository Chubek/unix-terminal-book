# Drafting and coverage plan

`chapters/MANIFEST.json` is the dependency-aware outline and the detailed
coverage matrix: each row specifies what is taught, what the reader must
already know, and who writes and reviews the chapter. W0 approved this
initial map before assignment. A prerequisite is a reader dependency, not
a drafting dependency; coordinate changes to the contract through W0.

| Strand | Introduce | Develop | Put to work |
|---|---|---|---|
| Terminal and documentation | 1–4, 10 | 13, 28–29, 36 | 43–45 |
| Files, links and safety | 5–9, 11–12 | 14, 23, 33–34 | 39, 41–42, 47–48 |
| Text, streams and patterns | 13–19 | 20–24, 25–26 | 46–47 |
| Shell and operating system | 2–3 | 25–36 | 40, 43–46 |
| Network and preservation | 23, 33 | 37–42 | 47–48 |

## Shared editorial contract

- Use `ch:N` for chapter headings (W0 inserts these in the master), and
  `sec:N-*`, `fig:N-*` and `ex:N-*` for local labels. Backward chapter
  references use `\ref{ch:N}`; mark forward references as optional.
- A **terminal** is the interface; a **shell** reads and interprets
  commands; a **prompt** signals readiness; the **working directory** is
  the base for relative paths. Use **option**, **operand**, **argument**,
  **standard input**, **standard output**, **standard error**, **exit
  status**, **glob**, **regular expression** and **locale** consistently.
- Use `sh` for portable practice syntax unless the chapter teaches another
  shell. Before chapter 12, use a uniquely named new practice directory
  and tell readers to stop if setup fails. Later chapters may use an
  isolated `mktemp -d` directory, with platform notes if needed. Never
  depend on another chapter's practice files.
- Add source diagrams under `figures/chapter-N/`, reusable listings under
  `listings/chapter-N/`, and validation notes under
  `editorial/evidence/chapter-N.md`. Existing empty scaffold files are
  reserved, not deleted; only W0 decides shared-file changes.
- Provide exact checks and cleanup for practice and exercises. Report
  actual system and shell test evidence separately from manual-based or
  illustrative examples. No live-network tests without authorization.
- W0 reviews ownership and release gates independently of non-author
  review. Peer reviewers report findings before W0 changes status to
  verified; a draft commit is not review evidence.
