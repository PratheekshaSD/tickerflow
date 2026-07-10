import pandas as pd 
class Transformer:
    """
    Takes raw OHLCV data from Extractor and cleans + enriches it.
    This class ONLY transforms — no fetching, no storage.
    """
    def clean(self,df,ticker):

        df.drop(columns=['Dividends','Stock Splits'],inplace=True)
        df.dropna(subset=['Close'],inplace=True)
        df.reset_index(inplace=True)
        df['Ticker']=ticker
        return df
    
    def compute_metrics(self,df):
        df['daily_return']=(df['Close']-df['Close'].shift(1))/df['Close'].shift(1)
        df['avg7'] = df['Close'].rolling(window=7).mean() #moving average
        df['avg21']=df['Close'].rolling(window=21).mean()
        return df
    
    
    
# ****TESTCODE***
# if __name__=="__main__":
#     from extractor import Extractor
#     e=Extractor()
#     t=Transformer()

#     raw_df=e.fetch_ticker_data("TCS.NS")
#     cleaned_df =t.clean(raw_df,"TCS.NS")
#     final_df=t.compute_metrics(cleaned_df)
#     print(final_df.head())
#     print(final_df.columns)
#     print(final_df[['Close', 'average7', 'average21']].tail(10))