#!/usr/bin/env python3
"""Download the UCI "Online Retail" dataset for the CDS3004 group project.

Usage:
    python data/download_data.py            # download if missing
    python data/download_data.py --force    # re-download

The script validates that the file loads and has the expected number of rows,
so a truncated/corrupt download is detected early instead of surfacing as a
mysterious pandas error later.
"""
from __future__ import annotations

import argparse
import pathlib
import sys
import urllib.request
import zipfile

DATA_DIR = pathlib.Path(__file__).resolve().parent
XLSX = DATA_DIR / "Online_Retail.xlsx"

XLSX_URL = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
)
ZIP_URL = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
EXPECTED_ROWS = 541_909


def _download(url: str, dest: pathlib.Path) -> None:
    print(f"  downloading {url}")
    with urllib.request.urlopen(url, timeout=120) as resp, open(dest, "wb") as fh:
        fh.write(resp.read())


def _validate(path: pathlib.Path) -> bool:
    try:
        import pandas as pd
    except ImportError:
        print("  ! pandas not installed; skipping validation")
        return True
    try:
        df = pd.read_excel(path)
    except Exception as exc:  # noqa: BLE001 - report any parse failure
        print(f"  ! cannot read {path.name}: {exc}")
        return False
    print(f"  OK: {len(df):,} rows x {df.shape[1]} columns")
    if len(df) != EXPECTED_ROWS:
        print(f"  ! expected {EXPECTED_ROWS:,} rows - file may be corrupted/truncated")
    return len(df) == EXPECTED_ROWS


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="re-download even if present")
    args = parser.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if XLSX.exists() and not args.force:
        print(f"[skip] {XLSX} already exists ({XLSX.stat().st_size / 1e6:.1f} MB)")
        _validate(XLSX)
        return 0

    print("[1/2] trying direct .xlsx download")
    try:
        _download(XLSX_URL, XLSX)
        if _validate(XLSX):
            print(f"[done] {XLSX}")
            return 0
    except Exception as exc:  # noqa: BLE001
        print(f"  ! direct download failed: {exc}")

    print("[2/2] trying .zip fallback")
    zip_path = DATA_DIR / "online_retail.zip"
    try:
        _download(ZIP_URL, zip_path)
        with zipfile.ZipFile(zip_path) as zf:
            names = [n for n in zf.namelist() if n.lower().endswith(".xlsx")]
            if not names:
                raise RuntimeError(f"no .xlsx inside zip: {zf.namelist()}")
            with zf.open(names[0]) as src, open(XLSX, "wb") as dst:
                dst.write(src.read())
        zip_path.unlink(missing_ok=True)
        if _validate(XLSX):
            print(f"[done] {XLSX}")
            return 0
    except Exception as exc:  # noqa: BLE001
        print(f"  ! zip fallback failed: {exc}")

    print(
        "\n[manual fallback] download the dataset in a browser and save it as:\n"
        f"  {XLSX}\n"
        f"  primary URL : {XLSX_URL}\n"
        f"  backup URL  : {ZIP_URL}\n"
        "Then re-run this script (it will validate the file)."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
