from extractor import Extractor
from transformer import Transformer
from loader import Loader
import time
class Pipeline:
     """
    Orchestrates the full ETL flow.
    Extractor → Transformer → Loader, one ticker at a time.
    """
     def __init__(self,tickers,loader):
            self.tickers=tickers
            self.loader=loader
    
     def run_once(self):
           extractor=Extractor()
           transformer=Transformer()
           for ticker in self.tickers:
                 raw_df=extractor.fetch_ticker_data(ticker)

                 if raw_df is None:
                       print("failed")
                       self.loader.log_run(ticker,'failed')
                       continue
                 
                 cleaned_df=transformer.clean(raw_df,ticker)
                 computed_df=transformer.compute_metrics(cleaned_df)
                 rows=self.loader.upsert_stock_data(computed_df)
                 self.loader.log_run(ticker,"success",rows_fetched=rows)

     def run_forever(self,interval=300):
           while True:
                 self.run_once()
                 time.sleep(interval) 