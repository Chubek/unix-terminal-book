# Unix Terminal for the Plebeian

Source for an illustrated, practical guide to the Unix terminal for everyday computer users. The book covers Linux, macOS, FreeBSD, OpenBSD and NetBSD, and distinguishes shared command interfaces from platform and shell extensions.

## Install and build

Keep `unix-terminals-for-pleb.cls` and its 41 support modules in the repository. The class loads them automatically; do not load them again individually. The underlying TeX distribution is not bundled.

Use Make, Python 3.10 or later, `makeindex`, and a full TeX Live or MacTeX installation (or equivalent MiKTeX installation) with Latin Modern, tcolorbox, listings, TikZ/PGF, geometry, titlesec, tocloft, fancyhdr, enumitem, hyperref, bookmark, csquotes, makeidx, comment, microtype, fontspec and their dependencies. The Makefile sets the support search path while retaining TeX's default paths. The build disables shell escape. Terminal commands are printed, never run by TeX.

```sh
make check-structure
make check-examples
make book                    # print edition with solutions
make editions                # all four edition combinations
make clean                   # remove edition build products
```

`make print`, `make screen`, `make answers` and `make noanswers` select subsets of the editions. Individual targets include `screen-noanswers`. Each edition writes to its own directory under `build/`. `TEXENGINE=lualatex` or `TEXENGINE=xelatex` selects another installed engine; see the release report for verified combinations.

Release builds require completed, peer-reviewed chapters and reject unresolved references, overfull boxes and other tracked log defects. `make draft` builds an explicitly named editorial PDF without applying the release gates. It is not a substitute for a release. `make check-examples` runs only registered fixture checks, not arbitrary code copied from the book.

## Class options and defaults

- `print` (default): 7 x 10 inch trim, asymmetric inner/outer margins, no colored PDF hyperlinks. Boxes retain their colors; this is not a guaranteed grayscale or press-ready PDF mode.
- `screen`: symmetric margins, colored PDF links.
- `answers` (default): includes solutions; `noanswers`: omits entire `solution` environments.
- Standard `book` options are forwarded, e.g. `oneside`, `twoside`, `10pt`, `12pt`, `openright`. Default is 11 pt, two-sided, open-any. The toolkit's geometry sets the page size regardless of standard paper-size options; override with `\geometry{...}` in the preamble if necessary.

## Manuscript structure

The four top-level sections are represented by LaTeX parts, with twelve chapters per part and continuous chapter numbering 1–48. Within a chapter use ordinary `\section` and `\subsection`. Use `\BookPart{Title}` and `\BookChapter{Title}` for the counted main manuscript. Call `\CheckBookStructure` immediately after chapter 48, before appendices. It emits warnings if the count differs from four parts, twelve chapters per part, and 48 total. Starting a new `\BookPart` also checks the previous part. The counters track these wrapper commands only, not ordinary `\part` or `\chapter` calls. Use `\chapter` for appendices, and `\FrontChapter`/`\BackChapter` for unnumbered matter.

The detailed chapter map is [`chapters/MANIFEST.json`](chapters/MANIFEST.json). The master is [`unix-terminals-for-pleb.ltx`](unix-terminals-for-pleb.ltx). Chapter fragments contain prose, not `\chapter` or document wrappers. Original diagram sources live under `figures/`; runnable source and fixture materials live under `listings/`.

## Agent-facing authoring reference

See [`support/AGENT-GUIDE.md`](support/AGENT-GUIDE.md) for authoring conventions and the public API, [`support/PACKAGE-MANIFEST.md`](support/PACKAGE-MANIFEST.md) for the module inventory, and [`editorial/PLAN.md`](editorial/PLAN.md) for the dependency and coverage plan.

## Limitations

- Listings are optimized for ASCII shell commands. Test non-ASCII filenames and Unicode output explicitly; `listings` is not a universal Unicode terminal emulator, even under LuaLaTeX/XeLaTeX. Colors and visible line wrapping are typesetting aids; a PDF copy operation is not guaranteed to reconstruct byte-for-byte shell input. Supply downloadable scripts separately when exact bytes matter.
- Inline verbatim commands cannot appear in moving arguments (headings, captions, bookmarks) or ordinary macro arguments. Use escaped `\texttt{...}` there. The delimiter for verbatim must not occur in its contents. Do not put listing environments in table cells or captured macro arguments.
- Text descriptions improve usability but do not guarantee tagged PDF, PDF/UA, PDF/X, or WCAG conformance. The layout has not been professionally preflighted for a specific printer.
- Platform labels are editorial metadata, not automatic compatibility tests. The author must verify command behavior on the stated systems and shells.
- The packages are designed as a coordinated set for the `book` class. Arbitrary combinations with other document classes or packages have not been tested.

## Validation performed

See [`editorial/RELEASE.md`](editorial/RELEASE.md) for actual validation results, tested systems, and release status.
