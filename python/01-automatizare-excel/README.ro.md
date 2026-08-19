# Proiect 1 — Automatizare Excel

> 🇬🇧 English version: [README.md](README.md)
Primul proiect aplicat: un script care corectează prețurile dintr-un registru Excel și
adaugă automat un grafic, ca alternativă la munca manuală în foaia de calcul.

## Ce face `exel_auto.py`

1. Deschide registrul cu `openpyxl` și selectează `Sheet1`.
2. Parcurge fiecare rând de date, ia prețul din coloana 3 și scrie în coloana 4 prețul
   redus cu 10 % (`* 0.9`).
3. Construiește un `BarChart` peste coloana nou-creată și îl inserează în foaie la `E2`.
4. Salvează registrul peste fișierul original.

## Rulare

```bash
pip install openpyxl
python -c "from exel_auto import process_workbook; process_workbook('transactions.xlsx')"
```

## Fișiere

- `exel_auto.py` — funcția `process_workbook(filename)`
- `transactions.xlsx`, `transactions2.xlsx` — registrele de test

> Scriptul suprascrie fișierul primit ca argument. Pentru teste repetate, lucrează pe o copie.
