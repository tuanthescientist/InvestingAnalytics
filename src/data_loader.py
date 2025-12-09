import yfinance as yf
import pandas as pd
from typing import List, Optional

def fetch_stock_data(tickers: List[str], start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches historical stock data for the given tickers.

    Args:
        tickers (List[str]): List of stock tickers (e.g., ['AAPL', 'MSFT']).
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: Adjusted Close prices for the tickers.
    """
    if not tickers:
        return pd.DataFrame()
    
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    
    if isinstance(data, pd.Series):
        data = data.to_frame()
        data.columns = tickers
        
    return data

def get_ticker_info(ticker: str) -> dict:
    """
    Fetches basic information for a single ticker.
    """
    stock = yf.Ticker(ticker)
    return stock.info
