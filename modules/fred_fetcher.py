# modules/fred_fetcher.py
import pandas as pd
import os
import time
from fredapi import Fred
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

FRED_INDICATORS = {
    "FEDFUNDS": "US_Fed_Funds_Rate",
    "VIXCLS":   "VIX",
    "DTWEXBGS": "USD_Index",
}

PERCENTAGE_INDICATORS = {"FEDFUNDS"}

START_DATE = "2000-01-01"
END_DATE   = "2023-12-31"

def fetch_fred_data(save_path=None):
    if save_path is None:
        save_path = BASE_DIR / "data" / "fred_data.csv"

    fred = Fred(api_key=os.getenv("FRED_API_KEY"))
    all_dfs = []

    for code, name in FRED_INDICATORS.items():
        print(f"Fetching {name}...")
        for attempt in range(5):
            try:
                series = fred.get_series(code, START_DATE, END_DATE)
                if code in PERCENTAGE_INDICATORS:
                    series = series / 100
                df = series.resample("YE").mean().reset_index()
                df.columns = ["Date", name]
                df["Year"] = df["Date"].dt.year
                df = df[["Year", name]]
                all_dfs.append(df)
                break
            except Exception as e:
                print(f"  Attempt {attempt+1} failed: {e}")
                time.sleep(5)

    if not all_dfs:
        print("No FRED data fetched.")
        return None

    merged = all_dfs[0]
    for df in all_dfs[1:]:
        merged = pd.merge(merged, df, on="Year", how="outer")

    merged = merged.sort_values("Year").reset_index(drop=True)

    save_path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(save_path, index=False)
    print(f"Saved to {save_path}")
    return merged

if __name__ == "__main__":
    df = fetch_fred_data()
    if df is not None:
        print(df)