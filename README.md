# TickerFlow 📈

![CI](https://github.com/PratheekshaSD/tickerflow/actions/workflows/ci.yml/badge.svg)

A near real-time stock market data pipeline that extracts, transforms, and loads OHLCV data for Indian stocks (TCS, INFY, RELIANCE) into PostgreSQL — built with Python and pandas, containerized with Docker, and served via a REST API built with FastAPI.

## What it does 🚀

- 📥 Fetches live stock data every 5 minutes using yfinance
- 🧹 Cleans and computes metrics (daily returns, 7-day and 21-day moving averages)
- 💾 Loads enriched data into PostgreSQL with upsert logic (no duplicates!)
- 📡 Serves data through a REST API with auto-generated Swagger docs at `/docs`
- 🔁 Logs every pipeline run with status, ticker, and row count
- 🛡️ Handles failures gracefully — retries 3 times per ticker, isolates errors so one bad ticker never crashes the whole pipeline

## API Endpoints 🔌

| Method | Endpoint | Description |
|---|---|---|
| GET | `/stocks/{ticker}/latest` | Most recent OHLCV record for a ticker |
| GET | `/stocks/{ticker}/history?limit=10` | Last N records for a ticker |
| GET | `/health` | Pipeline health check + total record count |

**Run the API:**
```bash
python -m uvicorn api:app --reload
```
Interactive docs available at `http://localhost:8000/docs`

## Tech Stack 🛠️

- **Python** — core language
- **FastAPI** — REST API layer with auto-generated Swagger docs
- **yfinance** — stock data extraction
- **pandas** — data cleaning and metric computation
- **psycopg2** — PostgreSQL connection and queries
- **PostgreSQL** — data storage
- **Docker / Docker Compose** — containerized app + database
- **pytest** — 17-test suite covering extractor, transformer, loader, and pipeline
- **GitHub Actions** — CI/CD: runs the test suite against a live Postgres service on every push, then builds and pushes a Docker image to Docker Hub

## Architecture 🏗️

```
yfinance → Extractor → Transformer → Loader → PostgreSQL → FastAPI → /docs
```

- Each class has one job (separation of concerns)
- Failed tickers are logged and skipped — pipeline never crashes
- Upsert logic ensures reruns don't create duplicates
- API layer serves stored data through clean REST endpoints

## Project Structure 📁

```
tickerflow/
├── .github/
│   └── workflows/
│       └── ci.yml
├── tests/
├── api.py              # FastAPI REST API — 3 endpoints, Swagger docs
├── extractor.py
├── transformer.py
├── loader.py
├── pipeline.py
├── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## How to Run ▶️

### Option 1: Docker Compose (recommended)

```bash
docker-compose up --build
```

### Option 2: Run locally

```bash
pip install -r requirements.txt
python main.py
```

### Run the API

```bash
python -m uvicorn api:app --reload
```

## Running Tests 🧪

```bash
pytest
```

17 tests covering extractor retry logic, transformer calculations, loader upsert behavior, and full pipeline runs. CI runs this against a real Postgres service container on every push.

## CI/CD Pipeline ⚙️

Every push to `main`:
1. Spins up a Postgres service container
2. Runs the full pytest suite
3. Builds and pushes Docker image to Docker Hub (`pratheekshasd/tickerflow`)