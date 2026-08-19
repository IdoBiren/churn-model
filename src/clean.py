"""Clean the raw Telco Customer Churn dataset and save data/telco_clean.csv."""

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "telco_churn.csv"
CLEAN_PATH = PROJECT_ROOT / "data" / "telco_clean.csv"


def clean(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    df = df.copy()

    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    rows_before = len(df)
    df = df.dropna(subset=["TotalCharges"])
    rows_dropped = rows_before - len(df)

    df = df.drop(columns=["customerID"])

    df["Churn"] = (df["Churn"] == "Yes").astype(int)

    return df, rows_dropped


def main() -> None:
    df = pd.read_csv(RAW_PATH)
    clean_df, rows_dropped = clean(df)

    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(CLEAN_PATH, index=False)

    print(f"Rows dropped (missing TotalCharges): {rows_dropped}")
    print(f"Remaining rows: {len(clean_df):,}")
    print(f"Saved cleaned data to {CLEAN_PATH}")


if __name__ == "__main__":
    main()
