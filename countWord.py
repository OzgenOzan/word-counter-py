import argparse
import os
import re
import sys

import pandas as pd
import textract
from textract.exceptions import CommandLineError  # base class of textract ShellError

# --- Tokenization (WC-2) ------------------------------------------------------
# Unicode-aware word pattern. The old ASCII-only pattern
# ([^$α-ωΑ-Ωa-zA-Z0-9/`'\u2019-]+) silently destroyed characters outside its
# ranges: Turkish letters (çğıöşüÇĞİÖŞÜ) and Greek letters with tonos
# (ά έ ή ί ό ύ ώ, plus ΐ ΰ ϊ ϋ — most lie outside α-ω). [^\W_] matches any
# Unicode word character except underscore (letters/digits across ALL scripts);
# re.UNICODE is the default for str patterns in Python 3 but is passed
# explicitly for documentation. The extra characters kept by the old pattern
# ($, /, `, ', \u2019, -) are retained via an explicit keep-list so the original
# enzyme/protein-name handling intent is preserved (e.g. "5'-nucleotidase",
# "alpha/beta" stay single tokens).
WORD_PATTERN = re.compile(r"(?:[^\W_]|[$/`'\u2019-])+", re.UNICODE)

d = {}

# Errors we expect and tolerate per file (WC-4): filesystem I/O problems,
# undecodable text, and textract's own extraction failures. Anything else is a
# bug and should crash loudly instead of being swallowed.
EXPECTED_ERRORS = (OSError, UnicodeDecodeError, CommandLineError)


def getFileNames(path):
    result = set()
    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            result.add(os.path.join(root, name))
    return result


def wordCount(fileName):
    textAsBytes = textract.process(fileName)

    text = textAsBytes.decode("utf-8")

    # Unicode-aware tokenization (WC-2): extract word tokens directly instead
    # of replacing non-ASCII characters with spaces (see WORD_PATTERN above).
    word_list = WORD_PATTERN.findall(text.lower())

    for word in word_list:
        d[word] = d.get(word,0) + 1


def main(argv=None):
    # CLI arguments instead of the previously hardcoded r"C:\Users\path" (WC-1)
    parser = argparse.ArgumentParser(
        description="Count words across documents in a folder (recursively).")
    parser.add_argument("--input-dir", required=True,
                        help="Folder containing the documents to scan.")
    parser.add_argument("--output", default="output.xlsx",
                        help="Output Excel file (default: output.xlsx).")
    args = parser.parse_args(argv)

    files = getFileNames(args.input_dir)
    failures = []  # per-file failures, summarized at the end (WC-4)
    for file in sorted(files):  # sorted for deterministic processing order
        try:
            wordCount(file)
        except EXPECTED_ERRORS as e:
            failures.append((file, f"{type(e).__name__}: {e}"))
            print(f"Skipping {file}: {e}", file=sys.stderr)
            continue

    df = pd.DataFrame(list(d.items()),columns = ['Word','Count'])
    df.to_excel(args.output, index=False)

    if failures:
        print(f"\n{len(failures)} of {len(files)} file(s) failed:", file=sys.stderr)
        for file, err in failures:
            print(f"  {file}: {err}", file=sys.stderr)
    else:
        print(f"All {len(files)} file(s) processed successfully.")


if __name__ == "__main__":
    main()
