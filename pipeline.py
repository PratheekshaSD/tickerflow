from extractor import Extractor
from extractor import InvalidTickerError,MaxRetriesExceededError
from transformer import Transformer
from loader import Loader
import time
class Pipeline:
     """
    Orchestrates the full ETL flow.
    Extractor → Transformer → Loader, one ticker at a time.
    """
     def __init__(self,tickers,loader,extractor=None,transformer=None):
            self.tickers=tickers
            self.loader=loader
            self.extractor=extractor or Extractor()
            self.transformer=transformer or Transformer()
    
     def run_once(self):
           for ticker in self.tickers:
            try:
                  raw_df=self.extractor.fetch_ticker_data(ticker)
                  cleaned_df=self.transformer.clean(raw_df,ticker)
                  computed_df=self.transformer.compute_metrics(cleaned_df)
                  rows=self.loader.upsert_stock_data(computed_df)
                  self.loader.log_run(ticker,"success",rows_fetched=rows)

            except InvalidTickerError as e:
                  print(f"failed: {e}")
                  self.loader.log_run(ticker,'failed',error_messages=str(e))
                  continue
            except MaxRetriesExceededError as e:
                  print(f"failed: {e}")
                  self.loader.log_run(ticker,'failed',error_messages=str(e))
                  continue

            except Exception:
                       print("failed")
                       self.loader.log_run(ticker,'failed')
                       continue
                       
                        

     def run_forever(self,interval=300):
           while True:
                 self.run_once()
                 time.sleep(interval) 