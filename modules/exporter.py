# modules/exporter.py
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def export_to_excel(wb_path=None, fred_path=None, output_path=None):
    if wb_path is None:
        wb_path = BASE_DIR / "data" / "wb_data.csv"
    if fred_path is None:
        fred_path = BASE_DIR / "data" / "fred_data.csv"
    if output_path is None:
        output_path = BASE_DIR / "data" / "em_macro_dashboard.xlsx"

    wb_df   = pd.read_csv(wb_path)
    fred_df = pd.read_csv(fred_path)

    merged = pd.merge(wb_df, fred_df, on="Year", how="left")
    merged = merged.sort_values(["Country", "Year"]).reset_index(drop=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        merged.to_excel(writer, sheet_name="Full_Data", index=False)
        fred_df.to_excel(writer, sheet_name="FRED_Global", index=False)

    print(f"Exported to {output_path}")
    return merged

if __name__ == "__main__":
    df = export_to_excel()
    print(df.head(20))