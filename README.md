An algorithm developed for counting words from documents in Python using pandas and textract. REGex pattern is tweaked to identify Latin characters all together (such as enzyme, protein names).

Our test data consists of 10 examples articles (Articles folder). We can identify word combinations written with dash, e.g. deep-learning, real-value... Also enzyme names such as ɑ-secretase, beta-secretase etc. (composed of Latin letters).

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

`textract` relies on external system binaries to parse documents. On
Debian/Ubuntu:

```
sudo apt-get install poppler-utils antiword
```

(See the [textract documentation](https://textract.readthedocs.io/) for other
platforms.)

## Usage

1. Set the documents folder in `main()` (`getFileNames(...)` call in
   `countWord.py`).
2. Run: `python countWord.py`
3. Counts are written to `output.xlsx` (`Word`, `Count` columns). Files that
   fail to parse are skipped with a warning on stderr instead of aborting the
   whole run.
