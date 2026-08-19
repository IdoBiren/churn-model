"""Download the Telco Customer Churn dataset into data/telco_churn.csv."""

from pathlib import Path
from urllib.request import urlopen

URL = (
    "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/"
    "master/data/Telco-Customer-Churn.csv"
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEST = PROJECT_ROOT / "data" / "telco_churn.csv"


def download(url: str = URL, dest: Path = DEST) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {url}")
    with urlopen(url, timeout=60) as response:
        payload = response.read()
    dest.write_bytes(payload)
    print(f"Saved {len(payload):,} bytes to {dest}")
    return dest


def main() -> None:
    dest = download()
    with dest.open(encoding="utf-8") as f:
        rows = sum(1 for _ in f) - 1  # exclude the header row
    print(f"{rows:,} data rows")


if __name__ == "__main__":
    main()
