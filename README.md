An algorithm developed for counting words from documents in Python using pandas and textract. REGex pattern is tweaked to identify Latin characters all together (such as enzyme, protein names).

Tokenization is Unicode-aware: word characters across all scripts are kept,
including Turkish (çğıöşüÇĞİÖŞÜ) and Greek letters with tonos
(ά έ ή ί ό ύ ώ), alongside the original enzyme/protein-name characters
($, /, `, ', ’, -).

It can be useful to clear out the unnecessary words using excel. Some algorithms which can be used in VBA:

> Delete Rows with a Specific Word/Value
```
Sub DeleteRowswithSpecificValue()
For i = Selection.Rows.Count To 1 Step -1
If Cells(i, 2).Value = "Certain Text or Value" Then
Cells(i, 2).EntireRow.Delete
End If
Next i
End Sub
```

> Delete Words from cells that exceed certain character count
```
=IF(LEN(A2)>35,"Yes","")
```

I want to develop this algorithm into a web aplication.

## Installation

Python 3.9+ recommended.

```
pip install -r requirements.txt
```

> **Note on `textract` maintenance:** the pinned `textract==1.6.5` was the
> last upstream release for over four years (March 2022 to April 2026) — the
> project was effectively unmaintained during that period. 2.x releases
> (starting with 2.0.0, April 2026) now exist on PyPI but have NOT been
> verified against this repo; treat any upgrade as a deliberate, tested
> change.

`textract` relies on external system binaries to parse documents. On
Debian/Ubuntu:

```
sudo apt-get install poppler-utils antiword
```

- `poppler-utils` provides `pdftotext` for PDF files
- `antiword` handles legacy `.doc` files
- other formats need their own binaries (e.g. `tesseract-ocr` for images,
  `unrtf` for RTF)

(See the [textract documentation](https://textract.readthedocs.io/) for other
platforms.)

## Usage

```
python countWord.py --input-dir /path/to/documents
# optionally override the output file (default: output.xlsx):
python countWord.py --input-dir /path/to/documents --output counts.xlsx
```

Counts are written to the output Excel file (`Word`, `Count` columns). Files
that fail to parse are skipped with a warning on stderr, and a per-file
failure summary is printed at the end of the run.
