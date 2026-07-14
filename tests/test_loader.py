import pandas as pd
from datetime import date
from loader import Loader

def test_upsert_stock_data(test_loader):
    fake_df = pd.DataFrame({
        'Date': [date(2026, 1, 1)],
        'Ticker': ['TCS.NS'],
        'Open': [100.0],
        'High': [105.0],
        'Low': [99.0],
        'Close': [102.0],
        'Volume': [1000000],
        'daily_return': [0.02],
        'avg7': [101.5],
        'avg21': [100.8]
    })

    rows_inserted = test_loader.upsert_stock_data(fake_df)
    assert rows_inserted == 1

    # now check the database directly
    cursor = test_loader.connection.cursor()
    cursor.execute("SELECT ticker, close FROM stock_prices WHERE date = %s AND ticker = %s;", (date(2026, 1, 1), 'TCS.NS'))
    result = cursor.fetchone()
    cursor.close()

    assert result is not None
    assert result[0] == 'TCS.NS'
    assert result[1] == 102.0

def test_upsert_stock_data_updates_existing_row(test_loader):
    original_df = pd.DataFrame({
        'Date': [date(2026, 1, 1)],
        'Ticker': ['TCS.NS'],
        'Open': [100.0],
        'High': [105.0],
        'Low': [99.0],
        'Close': [102.0],
        'Volume': [1000000],
        'daily_return': [0.02],
        'avg7': [101.5],
        'avg21': [100.8]
    })

    updated_df = pd.DataFrame({
        'Date': [date(2026, 1, 1)],      # same date
        'Ticker': ['TCS.NS'],             # same ticker
        'Open': [100.0],
        'High': [106.0],
        'Low': [99.0],
        'Close': [110.0],                 # different close price
        'Volume': [1200000],
        'daily_return': [0.05],
        'avg7': [101.5],
        'avg21': [100.8]
    })

    test_loader.upsert_stock_data(original_df)     # first insert
    test_loader.upsert_stock_data(updated_df)       # should UPDATE, not duplicate

    cursor = test_loader.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM stock_prices WHERE date = %s AND ticker = %s;", (date(2026, 1, 1), 'TCS.NS'))
    row_count = cursor.fetchone()[0]

    cursor.execute("SELECT close FROM stock_prices WHERE date = %s AND ticker = %s;", (date(2026, 1, 1), 'TCS.NS'))
    close_price = cursor.fetchone()[0]
    cursor.close()

    assert row_count == 1        # still only ONE row — proves it updated, not duplicated
    assert close_price == 110.0  # proves the value actually changed

def test_log_run_success(test_loader):
    test_loader.log_run("TCS.NS", "success", rows_fetched=5)

    cursor = test_loader.connection.cursor()
    cursor.execute("SELECT ticker, status, rows_fetched FROM run_log WHERE ticker = %s;", ("TCS.NS",))
    result = cursor.fetchone()
    cursor.close()

    assert result is not None
    assert result[0] == "TCS.NS"
    assert result[1] == "success"
    assert result[2] == 5

def test_connect_failure(test_loader):
    bad_loader=Loader(
        host="localhost",
        database="tickerflow_test",
        user="postgres",
        password="wrong_password_definitely_incorrect"
    )
    result=bad_loader.connect()

    assert result is False
