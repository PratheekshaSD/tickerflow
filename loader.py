import psycopg2
from psycopg2.extras import execute_values
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
