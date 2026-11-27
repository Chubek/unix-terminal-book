SHELL := /bin/sh
TEXENGINE ?= pdflatex
MAKEINDEX ?= makeindex
PYTHON ?= python3
EDITIONS := print-answers print-noanswers screen-answers screen-noanswers

.DEFAULT_GOAL := book
.PHONY: book editions print screen answers noanswers $(EDITIONS) draft check-structure check-release check-examples check-toolkit clean

book: print-answers
editions: $(EDITIONS)
print: print-answers
screen: screen-answers
answers: print-answers screen-answers
noanswers: print-noanswers screen-noanswers

$(EDITIONS): check-release
	$(PYTHON) editorial/build.py --engine "$(TEXENGINE)" --makeindex "$(MAKEINDEX)" $@

# For editorial use only. Draft output does not satisfy release gates.
draft: check-structure
	$(PYTHON) editorial/build.py --engine "$(TEXENGINE)" --makeindex "$(MAKEINDEX)" --draft print-answers

check-structure:
	$(PYTHON) editorial/check.py

check-release:
	$(PYTHON) editorial/check.py --release

check-examples:
	$(PYTHON) editorial/check.py --examples

check-toolkit:
	$(PYTHON) editorial/check-toolkit.py --engine "$(TEXENGINE)"

clean:
	$(PYTHON) editorial/build.py --clean
