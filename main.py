import os
from dotenv import load_dotenv
load_dotenv() #reads my env file and makes them available via os.getenv()

from pipeline import Pipeline
from loader import Loader
loader = Loader(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=int(os.getenv("DB_PORT", 5432))
)

if loader.connect():
    loader.create_tables()

    pipeline = Pipeline(tickers=["TCS.NS", "INFY.NS", "RELIANCE.NS"], loader=loader)
    pipeline.run_forever()
else:
    print("Could not connect to the database ,exiting pls pls do something *puppy eyes🎀🎀✨✨")