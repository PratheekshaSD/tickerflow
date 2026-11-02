from fastapi import FastAPI
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5434,
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


@app.get("/stocks/{ticker}/latest")
def get_latest(ticker: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, ticker, open, high, low, close, volume
        FROM stock_prices
        WHERE ticker = %s
        ORDER BY date DESC
        LIMIT 1
    """, (ticker,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row is None:
        return {"error": "ticker not found"}
    return {
        "date": row[0],
        "ticker": row[1],
        "open": row[2],
        "high": row[3],
        "low": row[4],
        "close": row[5],
        "volume": row[6]
    }

@app.get("/stocks/{ticker}/history")
def get_history(ticker: str, limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, ticker, open, high, low, close, volume
        FROM stock_prices
        WHERE ticker = %s
        ORDER BY date DESC
        LIMIT %s
    """, (ticker, limit))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    if not rows:
        return {"error": "ticker not found"}
    return [
        {
            "date": row[0],
            "ticker": row[1],
            "open": row[2],
            "high": row[3],
            "low": row[4],
            "close": row[5],
            "volume": row[6]
        }
        for row in rows
    ]


@app.get("/health")
def health_check():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM stock_prices")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return {"status": "healthy", "total_records": count}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}