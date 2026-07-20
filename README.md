# TickerFlow 📈

![CI](https://github.com/PratheekshaSD/tickerflow/actions/workflows/ci.yml/badge.svg)

A near real-time stock market data pipeline that extracts, transforms, and loads OHLCV data for Indian stocks (TCS, INFY, RELIANCE) into PostgreSQL — built with Python and pandas, containerized with Docker, and tested and deployed via a GitHub Actions CI/CD pipeline.

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
- **Docker / Docker Compose** — containerized app + database
- **pytest** — 17-test suite covering extractor, transformer, loader, and pipeline
- **GitHub Actions** — CI/CD: runs the test suite against a live Postgres service on every push, then builds and pushes a Docker image to Docker Hub once tests pass

## Project Structure

```
tickerflow/
├── .github/
│   └── workflows/
│       └── ci.yml      # CI/CD pipeline: test → build → push Docker image
├── tests/               # pytest suite (extractor, transformer, loader, pipeline)
├── extractor.py         # Fetches raw OHLCV data from yfinance with retry logic
├── transformer.py       # Cleans data and computes moving averages + daily returns
├── loader.py            # Handles all PostgreSQL operations (upsert, logging)
├── pipeline.py           # Orchestrates ETL flow, runs forever in a loop
├── main.py               # Entry point — configure credentials and start pipeline
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## How to Run

### Option 1: Docker Compose (recommended)

```bash
docker-compose up --build
```

This spins up the app and a PostgreSQL container together, with tables created automatically on first run.

### Option 2: Run locally

1. **Install dependencies**
```bash
pip install -r requirements.txt
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

## Running Tests

```bash
pytest
```

The suite covers extractor retry logic, transformer calculations, loader upsert behavior, and full pipeline runs (17 tests total). CI runs this same suite against a real Postgres service container on every push.

## CI/CD Pipeline

Every push to `main` triggers a GitHub Actions workflow that:

1. Spins up a Postgres service container
2. Installs dependencies and runs the full pytest suite
3. If tests pass, builds the Docker image and pushes it to Docker Hub (`pratheekshasd/tickerflow`)

This ensures broken code never gets tested against a false-positive local setup, and that a deployable image always exists for the latest passing commit on `main`.

## Architecture

Extractor → Transformer → Loader → PostgreSQL

- Each class has one job (separation of concerns)
- Failed tickers are logged and skipped — pipeline never crashes
- Upsert logic ensures reruns don't create duplicates