import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
import os

class Loader:
    """
    Handles all database operations.
    This class ONLY loads — no fetching, no transforming.
    """
    def __init__(self,host,database,user,password,port=5432):
        self.host=host
        self.database=database
        self.user=user
        self.password=password
        self.port=port
    
    def connect(self):
        try:
            self.connection=psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port 
        )
            
            print("Connected to PostgreSQL!")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
        
    def create_tables(self):
        cursor =self.connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS stock_prices(
            date DATE,
            ticker VARCHAR,
            open FLOAT,
            high FLOAT, 
            low FLOAT,
            close FLOAT, 
            volume BIGINT, 
            daily_return FLOAT, 
            avg7 FLOAT,
            avg21 FLOAT, 
            PRIMARY KEY(date,ticker)
            );"""
        )

        cursor.execute(
           """CREATE TABLE IF NOT EXISTS run_log( 
            id SERIAL PRIMARY KEY,
            run_timestamp TIMESTAMP, 
            ticker VARCHAR ,
            status VARCHAR,
            rows_fetched INTEGER, 
            error_messages TEXT
            );"""
        )

        self.connection.commit()
        cursor.close()

    def upsert_stock_data(self,df):
        cursor=self.connection.cursor()
        sql="""INSERT INTO stock_prices
                    (date,ticker,open,high,low,close,volume,daily_return,avg7,avg21)
                    VALUES %s
                    ON CONFLICT(date,ticker)
                    DO UPDATE SET
                    open =EXCLUDED.open,
                    high=EXCLUDED.high,
                    low=EXCLUDED.low,
                    close=EXCLUDED.close,
                    volume=EXCLUDED.volume,
                    daily_return=EXCLUDED.daily_return,
                    avg7=EXCLUDED.avg7,
                    avg21=EXCLUDED.avg21;
                    """
            
        values=[
                (
                    row['Date'],
                    row['Ticker'],
                    row['Open'],
                    row['High'],
                    row['Low'],
                    row['Close'],
                    row['Volume'],
                    row['daily_return'],
                    row["avg7"],
                    row['avg21']
                )
                for _, row in df.iterrows()
            ]  
          
        execute_values(cursor,sql,values)
        self.connection.commit()
        cursor.close()

        return len(values) 
     
    def log_run(self, ticker, status,rows_fetched=0,error_messages=None):
          cursor=self.connection.cursor()
          cursor.execute(""" 
        INSERT INTO run_log(run_timestamp, ticker, status, rows_fetched, error_messages)
        VALUES (%s, %s, %s, %s, %s)
            """,(datetime.now(), ticker, status, rows_fetched, error_messages))
          self.connection.commit()
          cursor.close()

