# Week 1 Python Project Template
# Simple CSV Summary Script for Rodney

import csv
from pathlib import Path


def summarize_csv(file_path: str) -> None:
    """
    Print basic information about a CSV file:
    - Total rows
    - Column names
    """
    path = Path(file_path)

    if not path.exists():
        print(f"[ERROR] File not found: {path}")
        return

    try:
        with path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        print(f"File: {path}")
        print(f"Total rows (excluding header): {len(rows)}")

        if rows:
            print("Columns:", ", ".join(rows[0].keys()))
        else:
            print("No data rows found in this file.")

    except Exception as e:
        print("[ERROR] Something went wrong while reading the CSV:")
        print(e)


if __name__ == "__main__":
    sample_path = "sample.csv"
    summarize_csv(sample_path)
