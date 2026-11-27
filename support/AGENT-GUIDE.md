# Instructions for a manuscript-writing agent

Use the class `unix-terminals-for-pleb` and its 40 automatically loaded modules. Write chapter fragments, not standalone documents. Keep one master manuscript file responsible for `\BookPart`, `\BookChapter`, front matter, appendices and back matter. Each chapter fragment begins with prose or an objectives box, not another `\chapter`.

## Editorial contract

- The audience consists of everyday computer users, not programmers or system administrators. Define jargon before relying on it. Introduce the terminal as an ordinary tool for common tasks.
- Use a progressive structure: start with safe, reversible actions and familiar goals. Do not introduce root privileges, destructive operations or configuration changes without explaining why and how to recover.
- Distinguish the terminal application, shell, command, option, operand, prompt, output, and exit status. Do not imply that prompts are commands or that all systems behave identically.
- Prefer portable examples where practical. Distinguish POSIX shell syntax from Bash, Zsh, Fish, and other shell-specific features. Separate GNU and BSD/macOS command options. Do not label a command portable without verifying it. Mark optional third-party tools and installation requirements.
- Present literal input in `terminal`, a mixed prompt/input/output transcript in `session`, pure output in `terminaloutput`, error messages in `erroroutput`, scripts in `shellscript`, and file text in `filecontentsbox`. Avoid ambiguous `$`/`#` prefixes in input-only examples. Do not imply illustrative output was collected from a real system.
- Prefer exercises that use a dedicated temporary practice directory. Explain cleanup and risks. Avoid unqualified recursive deletion, permission changes, network exposure, or piping downloaded code into a shell. Avoid putting real credentials or personal data into examples.
- Use consistent labels, e.g. `ch:files`, `sec:paths`, `fig:pipe`. Give every glossary entry a unique stable key, and maintain one curated glossary. Add useful index entries where concepts are explained, not mechanically at every mention.
- Cite primary documentation or manuals where needed. Do not invent citations, flags, outputs, platform support, or versions. Test examples independently of LaTeX compilation.

## Suggested chapter pattern (adapt, do not mechanically pad)

```latex
\begin{objectives}
\item Explain the practical goal.
\item Perform a safe task independently.
\end{objectives}
\section{A practical starting point}
Write the explanation here.
\begin{terminal}
pwd
\end{terminal}
\begin{platformnote}{macOS and Linux}
Explain verified differences where relevant.
\end{platformnote}
\begin{exercise}{Practice the technique}
Describe the task and expected result.
\end{exercise}
\begin{solution}
Explain the solution here.
\end{solution}
\begin{takeaways}
\item State the key transferable lesson.
\end{takeaways}
```

## Public API by module

All commands below are supplied by the class. Standard LaTeX constructs such as `figure`, `table`, `longtable`, `\label`, `\ref`, `\cite`, `\footnote`, `\url`, and `\includegraphics` remain available.

| Module | Commands and environments |
|---|---|
| colors | Color names `UTPInk`, `UTPAccent`, `UTPMuted`, `UTPRule`, `UTPSoft`, `UTPCode`, `UTPWarn`, `UTPDanger`, `UTPGood` |
| typography | Engine-specific fonts, paragraph spacing and microtypography (automatic) |
| layout | `\KeepNext[lines]` (default 4), page geometry |
| metadata | `\BookSubtitle{text}`, `\BookEdition{text}`, `\BookPublisher{text}` |
| headers | Running headers and page numbers (automatic) |
| structure | `\BookPart{title}`, `\BookChapter{title}`, `\CheckBookStructure` |
| contents | `\BookContents`, `\DetailedContents` (call before the contents to include subsections) |
| prose | `\PlainEnglish{text}`, `\FirstUse{term}`, `\AsideText{text}` |
| lists | `steps`, `terms` environments; standard lists |
| tables | `quicktable` environment with column spec, `Y` flexible text column, `M{width}` monospace column; `\toprule`, `\midrule`, `\bottomrule` |
| figures | `\BookFigure[width]{file}{caption}{label}`, `\FigurePlaceholder{text}{caption}` |
| terminal | `terminal[options]` literal environment, shared `utpcode` listing style |
| inline | `\cmd|literal|`, `\literal|literal|`, `\OptionName|literal|`, `\Placeholder{text}` |
| paths | `\FilePath{/path}`, `\EnvVar{$HOME}`, `\FileName{notes.txt}` (URL-style literal arguments) |
| keys | `\Key{key}`, `\KeyChord{key1}{key2}`, `\EnterKey`, `\TabKey` |
| callouts | `notebox[title]`, `tipbox[title]`, `conceptbox[title]` |
| safety | `warningbox[title]`, `dangerbox[title]`, `recoverybox[title]`, `\RiskLabel{text}` |
| platforms | `\Platform{name}`, `\Linux`, `\macOS`, `\FreeBSD`, `\OpenBSD`, `\NetBSD`, `\POSIXShell`, `\BashShell`, `\ZshShell`, `platformnote{platforms}` |
| commands | `commandcard{name}`, `\CommandField{label}{text}`, `\CommandSyntax|literal|`, `\CommandOption{option}{explanation}` |
| sessions | `session[options]`, `\UserPrompt`, `\RootPrompt`, `\PromptReminder` |
| scripts | `shellscript[options]`, `\ShellFile[options]{file}`; syntax-colored Bash listing style |
| output | `terminaloutput[options]`, `erroroutput[options]`, `filecontentsbox[options]` |
| exercises | `exercise[box options]{title}`, `\ExerciseHint{text}`, `\ExerciseGoal{text}` |
| solutions | `solution` environment, included or suppressed with class options |
| objectives | `objectives`, `prerequisites` list environments, `\EstimatedTime{text}` |
| summaries | `takeaways` list environment, `\NextChapter{text}` |
| checklists | `checklist` list environment (`\item` unchecked, `\CheckedItem` checked) |
| troubleshooting | `troubleshoot{title}`, `\Symptom{text}`, `\LikelyCause{text}`, `\TryThis{text}`, `\VerifyFix{text}` |
| glossary | `bookglossary`, `\GlossaryEntry{key}{term}{definition}`, `\GlossaryLink{key}{display text}` |
| index | `\IndexTerm{term}`, `\IndexCommand{name}`, `\PrintBookIndex`; ordinary `\index{entry}` |
| references | `furtherreading`, `\ReadingItem{title}{description}{url}`, `\SourceNote{text}` |
| frontmatter | `\MakeBookTitle`, `copyrightpage`, `\FrontChapter{title}` |
| backmatter | `\BeginAppendices`, `\BackChapter{title}`, `\BookSee{type}{label}` |
| diagrams | `\PipeDiagram{input}{process}{output}`, TikZ styles `utp node`, `utp arrow` |
| sidebars | `sidebar[title]`, `historybox[title]`, `mythbox[title]` |
| accessibility | `\VisualDescription{text}`, `\AccessibleFigure[width]{file}{caption}{label}{description}`, `\NonvisualCue{text}` |
| conventions | `\BookConventions` |
| manpages | `\ManPage{name}{section}`, `\ManCommand{name}{section}`, `\HelpSource{name}{text}` |
| workflows | `workflow{title}`, `\WorkflowGoal{text}`, `\WorkflowResult{text}`, `\WorkflowCleanup{text}` |
| links | `\WebLink{url}{text}`, hyperlink styling and bookmarks |

## Syntax details

- All environment names in the API table are used as `\begin{name}` ... `\end{name}`. For literal environments, put opening and closing markers on their own lines. Optional listing settings immediately follow the opening marker: `\begin{terminal}[title={Try this}]`. Options are tcolorbox keys. For the hidden `solution` mode, the opening and closing environment markers must appear alone on their respective lines without indentation.
- Literal inline content supports characters such as `%`, `$`, `_`, `#`, `\`, and braces. Use another delimiter if `|` occurs inside the literal: `\cmd+printf '%s\n' x | wc -l+`. Do not use inline verbatim in arguments like `\caption{...}`. Regular prose and arguments follow LaTeX escaping rules. Use `\texttt{...}` with proper escaping for headings, or supply short plain-text titles.
- Platform and key macros with no argument consume the following source whitespace. Use `\Linux{} users` or `\Linux\ users` to retain a space.
- `\IndexTerm` and `\IndexCommand` are for simple terms/names. For makeindex-special characters such as `!`, `@`, `|`, or `"`, use a suitably escaped explicit `\index` entry instead.
- `quicktable` example: `\begin{quicktable}{M{1in}Y}` with the body containing normal rows and rules. Use `longtable` for long multipage tables.
- Glossary definitions are manually curated; `\GlossaryLink` does not generate entries. Indexing requires the makeindex build step. `\BookSee{Chapter}{ch:files}` uses a standard label.
- Use text-only descriptions for the pipe diagram's three nodes; lengthy labels may exceed the page width. Provide a textual description when meaning is not obvious.
