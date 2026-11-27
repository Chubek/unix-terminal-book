# Chapter 24 — Read CSV and JSON

- 3 TikZ diagrams: `figures/chapter-24/{csv,json,filter}.tikz`; 2 tables, 3 exercises and solutions, 1 dialogue.
- Reusable `listings/chapter-24/photo-review.sh`: sh syntax with jq, single array on standard input and selected array to standard output.
- `verify-chapters-19-24.py` ran in disposable fixtures on EndeavourOS in sh and zsh with jq 1.8.2 and Python 3.14.7. Seven exact transcript cases verify the naive cut failure, decoded CSV captions, Boolean selection, score types and CSV export; the verifier parses the generated JSON report and compares it with the listing output independently of formatting. No files from a personal photo catalog were used.
- Python and jq are explicitly optional reader dependencies. Cites RFC 4180, RFC 8259 and upstream parser documentation. Neither optional tool's installation or package naming was tested on macOS or the BSDs.
