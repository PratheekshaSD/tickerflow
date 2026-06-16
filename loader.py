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
            databse=self.database,
            user=self.user,
            password=self.password,
            port=self.port 
        )
            
            print("Connected to PostgreSQL!")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
        

