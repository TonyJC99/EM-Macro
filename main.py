# main.py
# Runs the full EM Macro Dashboard data pipeline.

from modules.wb_fetcher import fetch_world_bank_data
from modules.fred_fetcher import fetch_fred_data
from modules.exporter import export_to_excel

if __name__ == "__main__":
    print("=== Step 1: World Bank ===")
    fetch_world_bank_data()

    print("\n=== Step 2: FRED ===")
    fetch_fred_data()

    print("\n=== Step 3: Export ===")
    export_to_excel()

    print("\nPipeline complete. Open data/em_macro_dashboard.xlsx in Power BI.")