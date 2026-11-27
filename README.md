# Unix Terminal for the Plebeian — LaTeX toolkit v1.0

A modular book-design system for a practical, non-programmer-oriented introduction to Unix terminals, covering Linux, macOS, BSD and other Unix-like environments.

## Install and build

Extract the archive into your manuscript directory. Keep `unix-terminals-for-pleb.cls` and all 40 `utp-*.sty` files in that directory (or install them together in a local TEXMF tree). The class automatically loads all 40 packages in dependency order. Do not load them again individually. These are original wrapper/support modules around standard LaTeX packages; the underlying TeX distribution is not bundled.

Use a recent full TeX Live or MacTeX distribution (or equivalent MiKTeX installation), including Latin Modern fonts, tcolorbox, listings, TikZ/PGF, geometry, titlesec, tocloft, fancyhdr, enumitem, hyperref, bookmark, csquotes, makeidx, comment, microtype, fontspec and their dependencies. No shell escape, Python, Pygments, external image generators or shell execution is required. Terminal commands are printed, never run.

Compile the demonstration:

```sh
latexmk -pdf example.tex
```

Or manually:

```sh
pdflatex example.tex
makeindex example.idx
pdflatex example.tex
pdflatex example.tex
```

Use `latexmk -lualatex example.tex` or `latexmk -xelatex example.tex` for other engines. `example.tex` is a one-chapter demonstration, not the book manuscript. The archive includes no compiled PDFs or build artifacts.

## Class options and defaults

- `print` (default): 7 x 10 inch trim, asymmetric inner/outer margins, no colored PDF hyperlinks. Boxes retain their colors; this is not a guaranteed grayscale or press-ready PDF mode.
- `screen`: symmetric margins, colored PDF links.
- `answers` (default): includes solutions; `noanswers`: omits entire `solution` environments.
- Standard `book` options are forwarded, e.g. `oneside`, `twoside`, `10pt`, `12pt`, `openright`. Default is 11 pt, two-sided, open-any. The toolkit's geometry sets the page size regardless of standard paper-size options; override with `\geometry{...}` in the preamble if necessary.

## Manuscript structure

The four top-level sections are represented by LaTeX parts, with twelve chapters per part and continuous chapter numbering 1–48. Within a chapter use ordinary `\section` and `\subsection`. Use `\BookPart{Title}` and `\BookChapter{Title}` for the counted main manuscript. Call `\CheckBookStructure` immediately after chapter 48, before appendices. It emits warnings if the count differs from four parts, twelve chapters per part, and 48 total. Starting a new `\BookPart` also checks the previous part. The counters track these wrapper commands only, not ordinary `\part` or `\chapter` calls. Use `\chapter` for appendices, and `\FrontChapter`/`\BackChapter` for unnumbered matter.

```latex
\documentclass[print,twoside,answers]{unix-terminals-for-pleb}
\author{Author name}
\BookSubtitle{A practical guide for everyday computer users}
\BookEdition{First edition}
\begin{document}
\frontmatter
\MakeBookTitle
\FrontChapter{How to use this book}
\BookConventions
\BookContents
\mainmatter
\BookPart{Part title}
\BookChapter{Chapter title}
\input{chapters/ch01}
% Repeat for the remaining chapters and parts.
% \CheckBookStructure  % enable once all 48 chapters are present
\BeginAppendices
% \chapter{Quick reference}
\backmatter
% Glossary and other back matter
\PrintBookIndex
\end{document}
```

The title defaults to “Unix Terminal for the Plebeian.” Override it with `\title{...}` if needed. Author, date, publisher and edition are intentionally unset. `\BookPublisher{...}` and `\date{...}` supply optional metadata.

## Agent-facing authoring reference

See `AGENT-GUIDE.md` for consistent manuscript conventions and the complete public command/environment inventory. See `PACKAGE-MANIFEST.md` for the exact 40-module inventory. `example.tex` demonstrates the principal features.

## Limitations

- Listings are optimized for ASCII shell commands. Test non-ASCII filenames and Unicode output explicitly; `listings` is not a universal Unicode terminal emulator, even under LuaLaTeX/XeLaTeX. Colors and visible line wrapping are typesetting aids; a PDF copy operation is not guaranteed to reconstruct byte-for-byte shell input. Supply downloadable scripts separately when exact bytes matter.
- Inline verbatim commands cannot appear in moving arguments (headings, captions, bookmarks) or ordinary macro arguments. Use escaped `\texttt{...}` there. The delimiter for verbatim must not occur in its contents. Do not put listing environments in table cells or captured macro arguments.
- Text descriptions improve usability but do not guarantee tagged PDF, PDF/UA, PDF/X, or WCAG conformance. The layout has not been professionally preflighted for a specific printer.
- Platform labels are editorial metadata, not automatic compatibility tests. The author must verify command behavior on the stated systems and shells.
- The packages are designed as a coordinated set for the `book` class. Arbitrary combinations with other document classes or packages have not been tested.

## Validation performed

The sample manuscript was compiled in the supplied environment with pdfLaTeX, LuaLaTeX and XeLaTeX. A pdfLaTeX multi-pass build with `makeindex` resolved the sample cross-references and index. A separate print/two-sided/noanswers build verified solution omission. The four-part structure is checked by the optional counting commands, not by the TeX engine itself.
