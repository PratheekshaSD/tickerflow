import pandas as pd
from extractor import Extractor
def test_fetch_ticker_data_success(mocker):
    fake_history_df=pd.DataFrame({'Close':[100.0,101.0]})

    mock_stock=mocker.Mock()
    mock_stock.history.return_value=fake_history_df

    mocker.patch('extractor.yf.Ticker',return_value=mock_stock)

    extractor=Extractor()
    result=extractor.fetch_ticker_data("TCS.NS")

    assert result is not None
    pd.testing.assert_frame_equal(result, fake_history_df)
