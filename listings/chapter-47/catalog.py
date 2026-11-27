#!/usr/bin/env python3
"""Python 3.8+; Linux, macOS, BSD. Read the chapter's UTF-8 CSV."""
import csv
import json
import re
import sys


def read_catalog(path):
    seen = set()
    result = []
    with open(path, encoding="utf-8", newline="") as source:
        rows = csv.reader(source, strict=True)
        if next(rows, None) != ["filename", "album", "title"]:
            raise ValueError("expected filename,album,title header")
        for row in rows:
            if len(row) != 3:
                raise ValueError("expected three columns")
            name, album, title = row
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 _-]*\.jpg", name):
                raise ValueError("unsupported photo basename")
            if album not in ("street", "water"):
                raise ValueError("unknown album")
            if name.lower() in seen or not title.strip():
                raise ValueError("duplicate name or blank title")
            seen.add(name.lower())
            result.append({
                "source": "intake/" + name,
                "destination": "stage/" + album + "/" + name,
                "title": title,
            })
    if not result:
        raise ValueError("catalog has no photos")
    return result


if len(sys.argv) != 2:
    sys.exit("usage: python3 catalog.py catalog.csv")
try:
    catalog = read_catalog(sys.argv[1])
except (OSError, ValueError, csv.Error) as problem:
    sys.exit("catalog: " + str(problem))
print(json.dumps(catalog, indent=2))
