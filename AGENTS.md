01. Write the complete book "Unix Terminal for the Plebeian", an illustrated, practical Unix terminal guide for everyday computer users.
02. Work inside https://github.com/Chubek/unix-terminal-book; inspect the checked-out scaffold, README, LICENSE and all existing files before editing.
03. Produce a finished manuscript, not an outline, sample, skeleton, collection of notes, or promise of future work.
04. Preserve the existing LaTeX class, 40 support modules, chapter filenames, listings, and established visual identity; add the supplied dialogue module as package 41.
05. Read support/AGENT-GUIDE.md and support/PACKAGE-MANIFEST.md; use their real public APIs, not invented commands or environments.
06. Organize exactly four Parts of twelve chapters each, numbered continuously 1–48, with front matter, two appendices, glossary and index outside that count.
07. Maintain chapters/MANIFEST.json as the canonical chapter map: number, part, title, prerequisites, topics, owner, reviewer, assets and status.
08. Establish a dependency-aware outline and coverage matrix before parallel drafting; reconcile any existing material with the plan rather than discard it.
09. Part I, chapters 1–12: terminal literacy, Unix history, shells, prompts, navigation, paths, files, directories, discovery, help, editors and safe practice.
10. Part II, chapters 13–24: command anatomy, patterns, streams, redirection, pipelines, text inspection, searching, sorting, filtering, transformation, archives and data formats.
11. Part III, chapters 25–36: quoting, expansion, variables, environment, shell families, modest automation, processes, jobs, permissions, storage, packages and diagnostics.
12. Part IV, chapters 37–48: networking, SSH, transfers, remote sessions, backups, media and documents, customization, accessibility, troubleshooting, daily workflows and capstone projects.
13. Cover Linux, macOS, FreeBSD, OpenBSD and NetBSD as relevant; distinguish POSIX behavior, GNU/BSD variants, shells and optional tools explicitly.
14. Treat Bash, Zsh, POSIX sh, Fish, Ksh and Csh/Tcsh fairly; discuss other interpreters only where useful, without turning the book into programming instruction.
15. Aim at readers with no programming or system administration background; introduce abstractions through concrete tasks before formal terminology.
16. Use intelligent, lively, direct prose; respect the reader, avoid condescension, filler, repetitive introductions, fabricated anecdotes and needless jargon.
17. Deploy exactly eight authoring workers W1–W8 plus a ninth worker W0, the sole broker and orchestrator; use actual runtime agents, not simulated personas.
18. W1 owns chapters 1–6 and audits beginner accessibility and terminology across the manuscript.
19. W2 owns chapters 7–12 and audits filesystem illustrations and instructional progression.
20. W3 owns chapters 13–18 and audits command accuracy, POSIX semantics and portability.
21. W4 owns chapters 19–24 and audits text-processing examples, tables, diagrams and data visualizations.
22. W5 owns chapters 25–30 and audits shell differences, scripts, runnable listings and reproducibility.
23. W6 owns chapters 31–36 and audits operating-system differences, permissions, destructive operations and recovery.
24. W7 owns chapters 37–42 and audits networking, remote access, privacy and real-world workflows.
25. W8 owns chapters 43–48 and audits dialogue quality, exercises, voice and editorial consistency.
26. W0 initializes the workspaces and IPC mechanisms, approves the outline, assigns dependencies, schedules reviews, integrates changes and owns the release gates.
27. Give each worker an isolated Git branch/worktree with exclusive chapter ownership; only W0 changes shared integration files or merges changes.
28. All nine workers must use both a broker-routed message queue and a common shared-memory coordination store throughout the project.
29. Use the runtime's real IPC facilities or implement a local broker plus persistent shared state; report missing capabilities rather than claim simulated concurrency.
30. Directed communication follows sender -> W0 broker -> recipient via per-worker inboxes; no direct worker-to-worker queues and no broadcast via the queue.
31. Queue envelopes contain message_id, sender, recipient, type, correlation_id, timestamp, payload and reply_to where applicable; validate sender and destination.
32. Use directed queue messages for questions, answers, targeted reviews, assignments, acknowledgments, private work requests and escalation to W0.
33. W0 routes each message to the intended inbox, records delivery state, handles retries/timeouts, deduplicates by ID and supports correlated replies.
34. Shared memory holds public announcements, the outline, coverage matrix, style decisions, progress, asset registry, cross-reference registry and open coordination requests.
35. Publish global requests such as "W5 needs a portability reviewer" or "connect W2 and W6" in shared memory; W0 pairs workers and announces the assignment there.
36. After pairing, conduct the substantive one-to-one exchange through the brokered queue; never use shared memory as a substitute private inbox.
37. Use atomic/versioned writes, ownership rules or locks for shared state; keep revision history and persist checkpoints to survive worker failure or restart.
38. Track task states planned, drafting, review, revision, verified, integrated, blocked; every worker posts progress, blockers and completed artifact paths in shared memory.
39. W0 detects stalled workers, unresolved requests and circular dependencies, reassigns work safely and records decisions; no worker may declare the entire book complete alone.
40. Require a non-author peer review for every chapter, rotating reviewers across Parts; resolve substantive defects before W0 integrates a chapter.
41. Store chapter prose in chapters/chapter-N.ltx; the master unix-terminals-for-pleb.ltx alone emits BookPart and BookChapter calls; fragments contain no document wrappers.
42. Complete the master, existing frontmatter/preface/backmatter files, appendices and Makefile; set TEXINPUTS to include support/ and retain default search paths.
43. Use the class's print/screen and answers/noanswers options, conventional LaTeX labels, meaningful captions, index commands and curated glossary entries.
44. Write substantial chapters, normally 2,500–4,000 words of actual instructional prose, adjusting for complexity; do not inflate counts with listings or boilerplate.
45. Open each chapter with a motivating everyday scenario and objectives; develop concepts progressively, include guided practice, and close with takeaways and exercises.
46. Make the book visually rich: normally at least three explanatory figures, two substantive tables and eight worked terminal/code examples per chapter.
47. Create original TikZ/PGF diagrams, annotated terminal panels, process flows, directory trees, timelines, state diagrams and conceptual illustrations where they teach something.
48. Use charts for meaningful measured or clearly labeled illustrative data only; prefer diagrams over arbitrary numerical charts for conceptual material.
49. Keep original figure sources in a clearly organized asset directory; avoid unlicensed imagery, fake screenshots, decorative filler and placeholder figures.
50. Supply readable labels, captions, figure references and textual visual descriptions; verify legibility at the book's actual 7 x 10 inch trim size and in grayscale.
51. Use quicktable or longtable for command comparisons, option matrices, platform differences, input/output behavior, troubleshooting and compact reference material.
52. Use terminal for literal input, session for transcripts, terminaloutput/erroroutput for outputs, shellscript for code, and commandcard for concise command references.
53. Keep reusable executable examples in listings/ with clear names and shell/OS metadata; reference existing listings after checking them and supply safe fixture data.
54. Distinguish prompts from literal input; explain every unfamiliar option, operand, metacharacter, output field and relevant exit status before expecting independent use.
55. Test examples in disposable practice environments without real credentials or private data; never execute risky examples on the host or readers' real files.
56. Verify commands against primary manuals and actual target systems when available; record versions, test results and limitations, and mark untested/illustrative output honestly.
57. Explain safe alternatives, previews, backups, undo limitations, permissions, quoting hazards and recovery steps before potentially destructive operations.
58. Provide at least three hands-on exercises per chapter, with separately typeset solutions, expected outcomes and practical cleanup instructions.
59. Include 48–60 numbered Dialogue Boxes across the book, normally one per chapter plus occasional extras at particularly difficult conceptual transitions.
60. Load support/utp-dialogues.sty via the class or master preamble exactly once, documenting its public API in the support guide and package manifest.
61. Use the dialoguebox environment with a short topic title, Brian and Stephen turns, and a final DialogueConclusion command; never improvise a competing box style.
62. Brian is a curious, skeptical layperson who asks, challenges, rebukes, denies, proposes counterexamples and pursues the implications of Stephen's claims.
63. Stephen is a knowledgeable but fallible guide who answers precisely, welcomes objections, corrects misconceptions and concedes or refines his own claims when warranted.
64. Shape each dialogue as a Greek-style dialectic: initial question, provisional answer, objection or denial, deeper inquiry, refinement and mutual resolution.
65. Give each dialogue roughly six to twelve short turns; keep the exchanges authentic, intellectually useful, humorous when natural, and free of theatrical padding.
66. End every dialogue with exactly one shared conclusion, a single concise sentence on one printed line; revise wording if it wraps, rather than shrink typography.
67. Use normal LaTeX escaping and texttt for inline commands inside speaker arguments; never put raw verbatim or listing environments inside those arguments.
68. Cross-link chapters without forward-reference confusion; maintain unique label prefixes and a shared terminology register, and avoid duplicated full explanations.
69. Build a broad but finite coverage matrix including help, globbing, regex, Unicode, locales, pipes, signals, links, archives, checksums, SSH, JSON and everyday utilities.
70. Include practical projects such as organizing photos, searching notes, comparing files, processing CSV/JSON, backing up documents and working on remote machines.
71. Cite authoritative sources such as POSIX, operating-system manuals and upstream project documentation; never fabricate sources, version claims or test evidence.
72. Respect the repository license and third-party attribution requirements; preserve useful existing files and do not introduce incompatible copied material.
73. Provide appendices for portable command/shell comparison and quick reference; curate a useful glossary, command index and topic index in the back matter.
74. Establish reproducible Makefile targets for full book, screen/print editions, answers/noanswers builds, example validation, structural checks and cleanup.
75. W0 runs a clean multi-pass LaTeX build with makeindex, calls CheckBookStructure after chapter 48, and checks all intended chapters and assets are included.
76. Audit unresolved references, citations, missing fonts/assets, overfull boxes, clipped listings, unreadable figures and one-line dialogue conclusions; fix or document each defect.
77. W0 verifies the coverage matrix, minimum visual/exercise counts, dialogue count, peer reviews, test evidence, front/back matter and coherent transitions across Parts.
78. Deliver complete source, reproducible build scripts, original assets, validated listings, final PDFs, and a release report with counts, test matrix, known limitations and remaining defects.
79. Use small reviewable commits and preserve unrelated changes; never force-push, overwrite the default branch, publish externally or claim unsupported tests passed.
80. Continue until all 48 chapters are complete and the release gates pass; if blocked, preserve the real state, identify exact missing work, and never misrepresent an incomplete book as finished.
