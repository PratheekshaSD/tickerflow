if __name__ == "__main__":
    e = Extractor()
    df = e.fetch_ticker_data("FAKERSTOCK")
    if df is not None:
        print(df.head())
    else:
        print("No data returned")