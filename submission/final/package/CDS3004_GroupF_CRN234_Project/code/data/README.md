# Data — UCI Online Retail

## Source
- **Dataset**: *Online Retail* — UCI Machine Learning Repository
- **Page**: <https://archive.ics.uci.edu/dataset/352/online+retail>
- **File**: `Online_Retail.xlsx` (23 MB, 541,909 rows x 8 columns)
- **Coverage**: 2010-12-01 08:26 to 2011-12-09 12:50
- **Domain**: UK-based online giftware retailer; invoice-level transactions

## Schema
| Column | Type | Notes |
|---|---|---|
| InvoiceNo | string | 6-digit; starts with `C` for cancellations |
| StockCode | string | product code; contains service codes (POST, M, D, C2, ...) |
| Description | string | product name; 1,454 missing |
| Quantity | int | negative on returns/cancellations |
| InvoiceDate | datetime | minute resolution |
| UnitPrice | float | GBP; 0 or negative for adjustments/free items |
| CustomerID | float | **135,080 rows missing (24.9%)** |
| Country | string | mostly United Kingdom |

## Getting the file
```bash
python data/download_data.py          # downloads + validates row count
```

For Google Colab: upload `Online_Retail.xlsx` into `data/` of the project
(or run `data/download_data.py` from the notebook before analysis).

## Licence / ethics
- Public research dataset released by UCI for research/teaching use.
- Contains no names, addresses or other direct identifiers; CustomerID is a
  retailer-internal identifier. We only report aggregate/segment-level findings.
- We do **not** commit the 23 MB spreadsheet to GitHub — each user downloads it
  with the script above (see `.gitignore`).
