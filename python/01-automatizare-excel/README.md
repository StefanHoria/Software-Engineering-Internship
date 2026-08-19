# Project 1 — Excel Automation

The first applied project: a script that corrects prices in an Excel workbook and adds a chart
automatically, as an alternative to doing the work by hand in the spreadsheet.

> 🇷🇴 Documentul în limba română: [README.ro.md](README.ro.md)

## What `exel_auto.py` does

1. Opens the workbook with `openpyxl` and selects `Sheet1`.
2. Walks every data row, takes the price from column 3 and writes into column 4 the price reduced by
   10 % (`* 0.9`).
3. Builds a `BarChart` over the newly created column and inserts it into the sheet at `E2`.
4. Saves the workbook over the original file.

## Running

```bash
pip install openpyxl
python -c "from exel_auto import process_workbook; process_workbook('transactions.xlsx')"
```

## Files

- `exel_auto.py` — the `process_workbook(filename)` function
- `transactions.xlsx`, `transactions2.xlsx` — the test workbooks

> The script overwrites the file passed as an argument. For repeated tests, work on a copy.
