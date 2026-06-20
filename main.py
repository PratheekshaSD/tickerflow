from pipeline import Pipeline
from loader import Loader
loader =Loader(
    host="localhost",
    database="postgres",
    user="postgres",
    password="password"
)

if loader.connect():
    loader.create_tables()

    pipeline = Pipeline(tickers=["TCS.NS", "INFY.NS", "RELIANCE.NS"], loader=loader)
    pipeline.run_forever()
else:
    print("Could not connect to the database ,exiting pls pls do something *puppy eyes🎀🎀✨✨")