# TickerFlow 📈

A near real-time stock market data pipeline that extracts, transforms, and loads OHLCV data for Indian stocks (TCS, INFY, RELIANCE) into PostgreSQL — built with Python and pandas.

## What it does
- Fetches live stock data every 5 minutes using yfinance
- Cleans and computes metrics (daily returns, 7-day and 21-day moving averages)
- Loads enriched data into PostgreSQL with upsert logic (no duplicates!!)
- Logs every pipeline run with status, ticker, and row count
- Handles failures gracefully — retries 3 times per ticker, isolates errors so one bad ticker doesn't crash the whole pipeline

## Tech Stack
- **Python** — core language
- **yfinance** — stock data extraction
- **pandas** — data cleaning and metric computation
- **psycopg2** — PostgreSQL connection and queries
- **PostgreSQL** — data storage

## Project Structure
```
tickerflow/
├── extractor.py    # Fetches raw OHLCV data from yfinance with retry logic
├── transformer.py  # Cleans data and computes moving averages + daily returns
├── loader.py       # Handles all PostgreSQL operations (upsert, logging)
├── pipeline.py     # Orchestrates ETL flow, runs forever in a loop
├── main.py         # Entry point — configure credentials and start pipeline
└── README.md
```

## How to Run

1. **Install dependencies**
```bash
pip install yfinance pandas psycopg2-binary
```

2. **Set up PostgreSQL** — make sure PostgreSQL is running and update credentials in `main.py`:
```python
loader = Loader(
    host="localhost",
    database="postgres",
    user="postgres",
    password="your_password"
)
```

3. **Run the pipeline**
```bash
python main.py
```

The pipeline will connect to PostgreSQL, create tables if they don't exist, and start fetching data every 5 minutes — printing live updates to the terminal.

## Architecture
Extractor → Transformer → Loader → PostgreSQL
- Each class has one job (separation of concerns)
- Failed tickers are logged and skipped — pipeline never crashes
- Upsert logic ensures reruns don't create duplicates