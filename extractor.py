import yfinance as yf
import time


class Extractor:
    """
    Handles fetching raw stock price data from yfinance.
    This class ONLY fetches — no cleaning, no storage, no analysis.
    """


    def __init__(self, max_retries=3, retry_delay=5):
        self.max_retries=max_retries
        self.retry_delay=retry_delay


    def fetch_ticker_data(self, ticker, start_date=None):
        stock=yf.Ticker(ticker)
        for attempt in range(1,self.max_retries+1):
            print(f"Attempt {attempt}/{self.max_retries} for {ticker}")
            try:
                if start_date is None:
                    df =stock.history(period="1y")
                    
                else:
                  df=stock.history(start=start_date)#history() returns in DataFrame only.

                if df.empty:
                     print("Fetched Nothing")
                else:
                    print("Fetch: Success")
                    return df
            except Exception as e:
                print(f"Something is fishy, Error {e}")

            if attempt<self.max_retries:
                time.sleep(self.retry_delay)
            
        print("Ran out of Attempts")
        return None
    
if __name__ == "__main__":
    e = Extractor()
    df = e.fetch_ticker_data("FAKERSTOCK")
    if df is not None:
        print(df.head())
    else:
        print("No data returned")
       
          




