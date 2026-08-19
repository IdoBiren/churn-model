"""Exploratory data analysis for the Telco Customer Churn dataset."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "telco_churn.csv"
PLOTS_DIR = PROJECT_ROOT / "plots"


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def print_shape(df: pd.DataFrame) -> None:
    print("=== Shape ===")
    print(f"{df.shape[0]:,} rows x {df.shape[1]} columns\n")


def print_dtypes(df: pd.DataFrame) -> None:
    print("=== Column dtypes ===")
    print(df.dtypes)
    print()


def print_missing(df: pd.DataFrame) -> None:
    print("=== Missing values per column ===")
    missing = df.isna().sum()
    missing = missing[missing > 0]
    if missing.empty:
        print("No missing values (NaN) detected.")
    else:
        print(missing)
    print()


def print_churn_rate(df: pd.DataFrame) -> float:
    churn_rate = (df["Churn"] == "Yes").mean()
    print("=== Churn rate ===")
    print(df["Churn"].value_counts())
    print(f"Churn rate: {churn_rate:.2%}\n")
    return churn_rate


def plot_class_balance(df: pd.DataFrame, dest_dir: Path = PLOTS_DIR) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    counts = df["Churn"].value_counts()

    fig, ax = plt.subplots(figsize=(6, 4))
    counts.plot(kind="bar", ax=ax, color=["#4C72B0", "#DD8452"])
    ax.set_title("Class balance: Churn")
    ax.set_xlabel("Churn")
    ax.set_ylabel("Number of customers")
    for i, value in enumerate(counts):
        ax.text(i, value, f"{value:,}", ha="center", va="bottom")
    fig.tight_layout()

    dest = dest_dir / "class_balance.png"
    fig.savefig(dest)
    plt.close(fig)
    return dest


def plot_tenure_by_churn(df: pd.DataFrame, dest_dir: Path = PLOTS_DIR) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 4))
    for churn_value, color in [("No", "#4C72B0"), ("Yes", "#DD8452")]:
        subset = df.loc[df["Churn"] == churn_value, "tenure"]
        ax.hist(subset, bins=30, alpha=0.6, label=churn_value, color=color)
    ax.set_title("Tenure distribution by churn")
    ax.set_xlabel("Tenure (months)")
    ax.set_ylabel("Number of customers")
    ax.legend(title="Churn")
    fig.tight_layout()

    dest = dest_dir / "tenure_by_churn.png"
    fig.savefig(dest)
    plt.close(fig)
    return dest


def main() -> None:
    df = load_data()
    print_shape(df)
    print_dtypes(df)
    print_missing(df)
    print_churn_rate(df)

    class_balance_path = plot_class_balance(df)
    tenure_path = plot_tenure_by_churn(df)
    print("=== Plots saved ===")
    print(class_balance_path)
    print(tenure_path)


if __name__ == "__main__":
    main()
