import pandas as pd
import pytest
from extractor import Extractor,InvalidTickerError,MaxRetriesExceededError

def test_fetch_ticker_data_success(mocker):
    fake_history_df=pd.DataFrame({'Close':[100.0,101.0]})

    mock_stock=mocker.Mock()
    mock_stock.history.return_value=fake_history_df

    mocker.patch('extractor.yf.Ticker',return_value=mock_stock)

    extractor=Extractor()
    result=extractor.fetch_ticker_data("TCS.NS")

    assert result is not None
    pd.testing.assert_frame_equal(result, fake_history_df)


#Test for invalid ticker
def test_invalid_ticker_error(mocker):
    fake_history_df=pd.DataFrame()

    mock_stock=mocker.Mock()
    mock_stock.history.return_value=fake_history_df

    mocker.patch('extractor.yf.Ticker',return_value=mock_stock)

    extractor=Extractor()

    with pytest.raises(InvalidTickerError):
        extractor.fetch_ticker_data("FAKESTOCK")

#Test for MaxRetriedExceededError
def test_max_retries_exhaustion(mocker):
    fake_history_df=pd.DataFrame({'Close':[100.0,101.0]})

    mock_stock=mocker.Mock()
    mock_stock.history.side_effect=Exception("network error")

    mocker.patch('extractor.yf.Ticker',return_value=mock_stock)

    extractor=Extractor()

    with pytest.raises(MaxRetriesExceededError):
        extractor.fetch_ticker_data("TCS.NCS")
        
