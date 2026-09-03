# EM Macro Data Pipeline

A Python pipeline that extracts, cleans, and exports macroeconomic data for six Central American and Caribbean economies, ready for analysis in any tool.

## Countries Covered

- Panama (anchor)
- Costa Rica
- Dominican Republic
- Guatemala
- Uruguay
- El Salvador

These economies share structural characteristics: small and open, trade-dependent, and sensitive to US monetary policy — making them a meaningful peer group for comparative analysis.

## Data Sources

| Source | Indicators |
|---|---|
| World Bank REST API | GDP growth, CPI inflation, government debt, current account balance, FDI inflows, lending rate, unemployment rate |
| FRED (St. Louis Fed) | US Federal Funds Rate, VIX, USD Index |

Data covers 2000–2023. No manual downloads — all data is fetched programmatically via API calls.

## Output

The pipeline produces two files in the `data/` folder:

- `wb_data.csv` — World Bank indicators by country and year
- `fred_data.csv` — FRED global context indicators by year
- `em_macro_dashboard.xlsx` — merged dataset with two sheets, ready for analysis

These files can be consumed by any analysis or visualization tool — Power BI, Tableau, Excel, or directly in Python.

## Project Structure

```
EM Macro/
│
├── main.py                  # Orchestrates the full pipeline
├── .env                     # FRED API key (not committed)
├── data/                    # Generated output files (not committed)
└── modules/
    ├── wb_fetcher.py        # Pulls World Bank indicators via REST API
    ├── fred_fetcher.py      # Pulls global context indicators from FRED
    └── exporter.py          # Merges datasets and exports to Excel
```

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/TonyJC99/em-macro-dashboard.git
cd em-macro-dashboard
```

**2. Install dependencies**
```bash
pip install requests pandas openpyxl fredapi python-dotenv
```

**3. Create a `.env` file in the `EM Macro` folder**
```
FRED_API_KEY=your_key_here
```

Get a free FRED API key at [fred.stlouisfed.org](https://fred.stlouisfed.org/docs/api/api_key.html).

**4. Run the pipeline**
```bash
python main.py
```

## Key Design Decisions

- All percentage indicators are stored as decimals (8% → 0.08) for correct downstream formatting without manipulation
- VIX and USD Index are left as raw index values — they are not percentages
- File paths are anchored with `Path(__file__).resolve()` so the pipeline runs correctly regardless of working directory
- All cleaning and normalization happens in Python, not in the consuming tool

## Technologies

- Python 3.12
- pandas, requests, fredapi, python-dotenv, openpyxl
