import pandas as pd
import pytest
from transformer import Transformer

def test_clean_removes_dividends_and_splits(raw_ohlcv_df):
    transformer=Transformer()
    result=transformer.clean(raw_ohlcv_df,ticker="TCS.NS")

    assert 'Dividends' not in result.columns  # clean() should drop the Dividends column entirely
    assert 'Stock Splits' not in result.columns  # clean() should drop the Stock Splits column entirely
    assert 'Ticker' in result.columns  # clean() should add a new Ticker column with the ticker symbol
    assert 'Date' in result.columns  # reset_index() should turn the Date index into a real column

def test_clean_drops_rows_with_missing_close(raw_ohlcv_df_with_nan):
    transformer=Transformer()
    result=transformer.clean(raw_ohlcv_df_with_nan,ticker="TCS.NS")

    assert len(result)==2

def test_compute_metrics_daily_return(raw_ohlcv_df):
    tranformer=Transformer()
    result=tranformer.compute_metrics(raw_ohlcv_df)

    assert pd.isna(result['daily_return'].iloc[0])
    assert result['daily_return'].iloc[1] ==pytest.approx(0.009615384615384616)

def test_compute_metrics_avg21(raw_ohlcv_df):
    transformer=Transformer()
    result=transformer.compute_metrics(raw_ohlcv_df)

    assert pd.isna(result['avg21'].iloc[19])
    assert result['avg21'].iloc[20]==pytest.approx(114.0)

def test_compute_metrics_avg7(raw_ohlcv_df):
    transformer=Transformer()
    result=transformer.compute_metrics(raw_ohlcv_df)

    assert pd.isna(result['avg7'].iloc[5])
    assert result['avg7'].iloc[6]==pytest.approx(107.0)

def test_clean_data_types(raw_ohlcv_df):
    transformer=Transformer()
    result=transformer.clean(raw_ohlcv_df,ticker="TCS.NS")

    assert pd.api.types.is_datetime64_any_dtype(result['Date'])
    # assert result['Close'].dtypes==float
    assert pd.api.types.is_float_dtype(result['Close'])


def test_compute_metrics_insufficient_data_returns_nan(raw_ohlcv_df_short):
    transformer=Transformer()
    result=transformer.compute_metrics(raw_ohlcv_df_short)

    assert result['avg7'].isna().all()
    assert result['avg21'].isna().all()