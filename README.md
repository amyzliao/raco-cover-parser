# cover parser
For bangyen's very cool research project

## dependencies
- python virtual environment recommended
- requests `python -m pip install requests`
- beautiful soup `python -m pip install beautifulsoup4`

## setup and usage
if using virtual env:
```
cd *into root directory*
Scripts/activate
```
run the parser:
```
cd *into root directory*
py parseCoverHTML.py > output.html
```

## output
`output.html` contains output of running `parseCoverHTML.py`.
This file contains 3 things (in this order):
1. test to row: mapping of tests to row indices
2. line coverage matrix: rows correspond to tests, columns correspond to line numbers of the program
    - 0 means that test does not cover that line
    - 1 means that test does cover that line
    - *which line number*? see "ranges of lines considered" in #3 below
3. stats coverage matrix: maps test row indices to stats and info about that test