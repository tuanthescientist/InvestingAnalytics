import numpy as np
import pandas as pd

def calculate_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Calculates daily returns."""
    return prices.pct_change().dropna()

def calculate_cumulative_returns(returns: pd.DataFrame) -> pd.DataFrame:
    """Calculates cumulative returns."""
    return (1 + returns).cumprod()

def calculate_volatility(returns: pd.DataFrame, annualized: bool = True) -> pd.Series:
    """Calculates volatility (standard deviation)."""
    vol = returns.std()
    if annualized:
        vol = vol * np.sqrt(252)
    return vol

def calculate_sharpe_ratio(returns: pd.DataFrame, risk_free_rate: float = 0.0, annualized: bool = True) -> pd.Series:
    """Calculates Sharpe Ratio."""
    excess_returns = returns - risk_free_rate / 252
    mean_excess_return = excess_returns.mean()
    std_dev = returns.std()
    
    sharpe = mean_excess_return / std_dev
    
    if annualized:
        sharpe = sharpe * np.sqrt(252)
        
    return sharpe

def calculate_max_drawdown(prices: pd.DataFrame) -> pd.Series:
    """Calculates Maximum Drawdown."""
    rolling_max = prices.cummax()
    drawdown = (prices - rolling_max) / rolling_max
    return drawdown.min()

def calculate_portfolio_performance(weights: np.array, mean_returns: pd.Series, cov_matrix: pd.DataFrame, risk_free_rate: float = 0.0):
    """
    Calculates portfolio performance metrics.
    """
    returns = np.sum(mean_returns * weights) * 252
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    sharpe = (returns - risk_free_rate) / std
    return returns, std, sharpe
