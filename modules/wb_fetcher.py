# modules/wb_fetcher.py
import requests
import pandas as pd
import os
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

COUNTRIES = ["PA", "CR", "DO", "GT", "UY", "SV"]

COUNTRY_NAMES = {
    "PAN": "Panama",
    "CRI": "Costa Rica",
    "DOM": "Dominican Republic",
    "GTM": "Guatemala",
    "URY": "Uruguay",
    "SLV": "El Salvador"
}

PERCENTAGE_INDICATORS = {
    "NY.GDP.MKTP.KD.ZG",
    "FP.CPI.TOTL.ZG",
    "GC.DOD.TOTL.GD.ZS",
    "BN.CAB.XOKA.GD.ZS",
    "BX.KLT.DINV.WD.GD.ZS",
    "FR.INR.LEND",
    "SL.UEM.TOTL.ZS",
}

INDICATORS = {
    "NY.GDP.MKTP.KD.ZG":    "GDP_Growth",
    "FP.CPI.TOTL.ZG":       "CPI_Inflation",
    "GC.DOD.TOTL.GD.ZS":    "Govt_Debt_GDP",
    "BN.CAB.XOKA.GD.ZS":    "Current_Account_GDP",
    "BX.KLT.DINV.WD.GD.ZS": "FDI_Inflows_GDP",
    "FR.INR.LEND":           "Lending_Rate",
    "SL.UEM.TOTL.ZS":       "Unemployment_Rate",
}

START_YEAR = 2000
END_YEAR   = 2023

def fetch_indicator(indicator_code, countries, start_year, end_year):
    country_str = ";".join(countries)
    url = (
        f"https://api.worldbank.org/v2/country/{country_str}"
        f"/indicator/{indicator_code}"
        f"?format=json&per_page=1000&date={start_year}:{end_year}"
    )
    records = []
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=15)
            data = r.json()
            for entry in data[1]:
                value = entry["value"]
                if value is not None and indicator_code in PERCENTAGE_INDICATORS:
                    value = value / 100
                records.append({
                    "Country": COUNTRY_NAMES.get(entry["countryiso3code"], entry["countryiso3code"]),
                    "Year":    int(entry["date"]),
                    "Value":   value
                })
            return records
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            time.sleep(3)
    return records

def fetch_world_bank_data(save_path=None):
    if save_path is None:
        save_path = BASE_DIR / "data" / "wb_data.csv"

    all_dfs = []

    for code, name in INDICATORS.items():
        print(f"Fetching {name}...")
        records = fetch_indicator(code, COUNTRIES, START_YEAR, END_YEAR)
        if records:
            df = pd.DataFrame(records).rename(columns={"Value": name})
            all_dfs.append(df)
        time.sleep(1)

    if not all_dfs:
        print("No data fetched.")
        return None

    merged = all_dfs[0]
    for df in all_dfs[1:]:
        merged = pd.merge(merged, df, on=["Country", "Year"], how="outer")

    merged = merged.sort_values(["Country", "Year"]).reset_index(drop=True)

    save_path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(save_path, index=False)
    print(f"Saved to {save_path}")
    return merged

if __name__ == "__main__":
    df = fetch_world_bank_data()
    if df is not None:
        print(df.head(20))