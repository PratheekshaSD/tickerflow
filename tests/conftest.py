import pandas as pd
import pytest

@pytest.fixture
def raw_ohlcv_df():
    n=22
    data={
        'Open':[100.0+i for i  in range(n)],
        'High':[105.0+i for i in range(n)],
        'Low':[99.0+i for i in range(n)],
        'Close':[104.0+i for i in range(n)],
        'Volume':[1000+(i*100) for i in range(n)],
        'Dividends':[0.0]*n,
        'Stock Splits':[0.0]*n,
    }
    df =pd.DataFrame(data,index=pd.date_range('2024-01-01',periods=n))
    df.index.name='Date'
    return df

@pytest.fixture
def raw_ohlcv_df_with_nan():
    data = {
        'Open': [100.0, 101.0, 102.0],
        'High': [105.0, 106.0, 107.0],
        'Low': [99.0, 100.0, 101.0],
        'Close': [104.0, None, 106.0],
        'Volume': [1000, 1100, 1200],
        'Dividends': [0.0, 0.0, 0.0],
        'Stock Splits': [0.0, 0.0, 0.0],
    }
    df = pd.DataFrame(data, index=pd.date_range('2024-01-01', periods=3))
    df.index.name = 'Date'
    return df