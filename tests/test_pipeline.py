from extractor import Extractor
from loader import Loader
from transformer import Transformer 
from pipeline import Pipeline
from extractor import InvalidTickerError, MaxRetriesExceededError
import pytest

def test_run_once_success(mocker):
    fake_extractor = mocker.Mock()
    fake_extractor.fetch_ticker_data.return_value = "fake_raw_df"

    fake_transformer = mocker.Mock()
    fake_transformer.clean.return_value = "fake_cleaned_df"
    fake_transformer.compute_metrics.return_value = "fake_computed_df"

    fake_loader = mocker.Mock()
    fake_loader.upsert_stock_data.return_value = 5

    pipeline = Pipeline(
        tickers=["TCS.NS"],
        loader=fake_loader,
        extractor=fake_extractor,
        transformer=fake_transformer
    )

    pipeline.run_once()

    fake_loader.log_run.assert_called_once_with("TCS.NS", "success", rows_fetched=5)


def test_invalid_ticker_error(mocker):
    fake_extractor = mocker.Mock()
    fake_extractor.fetch_ticker_data.side_effect = InvalidTickerError("No data found for ticker: TCS.NS")

    fake_transformer = mocker.Mock()
    fake_loader = mocker.Mock()

    pipeline = Pipeline(
        tickers=["TCS.NS"],
        loader=fake_loader,
        extractor=fake_extractor,
        transformer=fake_transformer
    )

    pipeline.run_once()

    fake_loader.log_run.assert_called_once_with(
        "TCS.NS", "failed", error_messages="No data found for ticker: TCS.NS"
    )


def test_max_retries(mocker):
    fake_extractor = mocker.Mock()
    fake_extractor.fetch_ticker_data.side_effect = MaxRetriesExceededError("Failed to fetch TCS.NS after 3 attempts")

    fake_transformer = mocker.Mock()
    fake_loader = mocker.Mock()

    pipeline = Pipeline(
        tickers=["TCS.NS"],
        loader=fake_loader,
        extractor=fake_extractor,
        transformer=fake_transformer
    )

    pipeline.run_once()

    fake_loader.log_run.assert_called_once_with(
        "TCS.NS", "failed", error_messages="Failed to fetch TCS.NS after 3 attempts"
    )