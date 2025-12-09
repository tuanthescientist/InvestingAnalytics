"""Portfolio Analytics Module

This module provides institutional-grade financial metrics for portfolio analysis.
All functions follow industry-standard conventions and are designed for use in
professional fund management contexts.

Author: Tuan The Scientist
Version: 2.0.0
"""

import numpy as np
import pandas as pd
from typing import Tuple, Optional, Dict, Any
from scipy import stats


# =============================================================================
# BASIC RETURN CALCULATIONS
# =============================================================================

def calculate_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily logarithmic returns from price series.
    
    Args:
        prices: DataFrame with asset prices (columns=tickers, index=dates)
    
    Returns:
        DataFrame of daily percentage returns
    """
    return prices.pct_change().dropna()


def calculate_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily logarithmic returns (continuous compounding).
    
    Args:
        prices: DataFrame with asset prices
    
    Returns:
        DataFrame of log returns
    """
    return np.log(prices / prices.shift(1)).dropna()


def calculate_cumulative_returns(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate cumulative returns from daily returns.
    
    Args:
        returns: DataFrame of daily returns
    
    Returns:
        DataFrame of cumulative returns (starting from 1.0)
    """
    return (1 + returns).cumprod()


def calculate_total_return(prices: pd.DataFrame) -> pd.Series:
    """
    Calculate total return over the entire period.
    
    Args:
        prices: DataFrame with asset prices
    
    Returns:
        Series of total returns per asset
    """
    return (prices.iloc[-1] / prices.iloc[0]) - 1


def calculate_annualized_return(returns: pd.DataFrame, periods_per_year: int = 252) -> pd.Series:
    """
    Calculate annualized return using geometric mean.
    
    Args:
        returns: DataFrame of daily returns
        periods_per_year: Trading days per year (default 252)
    
    Returns:
        Series of annualized returns
    """
    total_periods = len(returns)
    cumulative = (1 + returns).prod()
    return cumulative ** (periods_per_year / total_periods) - 1


# =============================================================================
# RISK METRICS
# =============================================================================

def calculate_volatility(returns: pd.DataFrame, annualized: bool = True, periods_per_year: int = 252) -> pd.Series:
    """
    Calculate volatility (standard deviation of returns).
    
    Args:
        returns: DataFrame of daily returns
        annualized: Whether to annualize the volatility
        periods_per_year: Trading days per year
    
    Returns:
        Series of volatilities per asset
    """
    vol = returns.std()
    if annualized:
        vol = vol * np.sqrt(periods_per_year)
    return vol


def calculate_downside_deviation(returns: pd.DataFrame, target: float = 0.0, annualized: bool = True) -> pd.Series:
    """
    Calculate downside deviation (semi-deviation below target).
    Used in Sortino ratio calculation.
    
    Args:
        returns: DataFrame of daily returns
        target: Target return (default 0)
        annualized: Whether to annualize
    
    Returns:
        Series of downside deviations
    """
    downside_returns = returns[returns < target]
    downside_dev = np.sqrt((downside_returns ** 2).mean())
    if annualized:
        downside_dev = downside_dev * np.sqrt(252)
    return downside_dev


def calculate_max_drawdown(prices: pd.DataFrame) -> pd.Series:
    """
    Calculate maximum drawdown from peak.
    
    Args:
        prices: DataFrame with asset prices
    
    Returns:
        Series of maximum drawdowns (negative values)
    """
    rolling_max = prices.cummax()
    drawdown = (prices - rolling_max) / rolling_max
    return drawdown.min()


def calculate_drawdown_series(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate drawdown series over time.
    
    Args:
        prices: DataFrame with asset prices
    
    Returns:
        DataFrame of drawdowns at each point in time
    """
    rolling_max = prices.cummax()
    return (prices - rolling_max) / rolling_max


def calculate_var(returns: pd.DataFrame, confidence: float = 0.95, method: str = 'historical') -> pd.Series:
    """
    Calculate Value at Risk (VaR).
    
    Args:
        returns: DataFrame of daily returns
        confidence: Confidence level (default 95%)
        method: 'historical' or 'parametric'
    
    Returns:
        Series of VaR values (as positive numbers representing potential loss)
    """
    if method == 'historical':
        return -returns.quantile(1 - confidence)
    elif method == 'parametric':
        z_score = stats.norm.ppf(1 - confidence)
        return -(returns.mean() + z_score * returns.std())
    else:
        raise ValueError("Method must be 'historical' or 'parametric'")


def calculate_cvar(returns: pd.DataFrame, confidence: float = 0.95) -> pd.Series:
    """
    Calculate Conditional Value at Risk (Expected Shortfall).
    Average loss beyond VaR threshold.
    
    Args:
        returns: DataFrame of daily returns
        confidence: Confidence level (default 95%)
    
    Returns:
        Series of CVaR values
    """
    var = -calculate_var(returns, confidence, method='historical')
    cvar = returns[returns <= var].mean()
    return -cvar


# =============================================================================
# RISK-ADJUSTED RETURN METRICS
# =============================================================================

def calculate_sharpe_ratio(
    returns: pd.DataFrame, 
    risk_free_rate: float = 0.0, 
    annualized: bool = True,
    periods_per_year: int = 252
) -> pd.Series:
    """
    Calculate Sharpe Ratio.
    
    Formula: (Rp - Rf) / σp
    
    Args:
        returns: DataFrame of daily returns
        risk_free_rate: Annual risk-free rate (decimal)
        annualized: Whether to annualize
        periods_per_year: Trading days per year
    
    Returns:
        Series of Sharpe ratios
    """
    daily_rf = risk_free_rate / periods_per_year
    excess_returns = returns - daily_rf
    mean_excess = excess_returns.mean()
    std_dev = returns.std()
    
    sharpe = mean_excess / std_dev
    if annualized:
        sharpe = sharpe * np.sqrt(periods_per_year)
    
    return sharpe


def calculate_sortino_ratio(
    returns: pd.DataFrame, 
    risk_free_rate: float = 0.0, 
    target: float = 0.0,
    annualized: bool = True
) -> pd.Series:
    """
    Calculate Sortino Ratio (penalizes only downside volatility).
    
    Formula: (Rp - Rf) / Downside Deviation
    
    Args:
        returns: DataFrame of daily returns
        risk_free_rate: Annual risk-free rate
        target: Target return for downside calculation
        annualized: Whether to annualize
    
    Returns:
        Series of Sortino ratios
    """
    daily_rf = risk_free_rate / 252
    excess_returns = returns.mean() - daily_rf
    downside_dev = calculate_downside_deviation(returns, target, annualized=False)
    
    sortino = excess_returns / downside_dev
    if annualized:
        sortino = sortino * np.sqrt(252)
    
    return sortino


def calculate_calmar_ratio(prices: pd.DataFrame, returns: pd.DataFrame) -> pd.Series:
    """
    Calculate Calmar Ratio (annualized return / max drawdown).
    
    Args:
        prices: DataFrame with asset prices
        returns: DataFrame of daily returns
    
    Returns:
        Series of Calmar ratios
    """
    ann_return = calculate_annualized_return(returns)
    max_dd = abs(calculate_max_drawdown(prices))
    return ann_return / max_dd


def calculate_omega_ratio(returns: pd.DataFrame, threshold: float = 0.0) -> pd.Series:
    """
    Calculate Omega Ratio (probability-weighted gains vs losses).
    
    Args:
        returns: DataFrame of daily returns
        threshold: Return threshold (default 0)
    
    Returns:
        Series of Omega ratios
    """
    gains = returns[returns > threshold].sum()
    losses = abs(returns[returns < threshold].sum())
    return gains / losses


def calculate_information_ratio(
    returns: pd.DataFrame, 
    benchmark_returns: pd.Series
) -> pd.Series:
    """
    Calculate Information Ratio (excess return / tracking error).
    
    Args:
        returns: DataFrame of asset returns
        benchmark_returns: Series of benchmark returns
    
    Returns:
        Series of Information ratios
    """
    excess_returns = returns.subtract(benchmark_returns, axis=0)
    tracking_error = excess_returns.std() * np.sqrt(252)
    mean_excess = excess_returns.mean() * 252
    return mean_excess / tracking_error


# =============================================================================
# MARKET/FACTOR METRICS
# =============================================================================

def calculate_beta(returns: pd.DataFrame, market_returns: pd.Series) -> pd.Series:
    """
    Calculate Beta (systematic risk relative to market).
    
    Args:
        returns: DataFrame of asset returns
        market_returns: Series of market/benchmark returns
    
    Returns:
        Series of Beta values
    """
    betas = {}
    market_var = market_returns.var()
    
    for col in returns.columns:
        covariance = returns[col].cov(market_returns)
        betas[col] = covariance / market_var
    
    return pd.Series(betas)


def calculate_alpha(
    returns: pd.DataFrame, 
    market_returns: pd.Series, 
    risk_free_rate: float = 0.0
) -> pd.Series:
    """
    Calculate Jensen's Alpha (excess return over CAPM prediction).
    
    Formula: α = Rp - [Rf + β(Rm - Rf)]
    
    Args:
        returns: DataFrame of asset returns
        market_returns: Series of market returns
        risk_free_rate: Annual risk-free rate
    
    Returns:
        Series of Alpha values (annualized)
    """
    daily_rf = risk_free_rate / 252
    beta = calculate_beta(returns, market_returns)
    
    asset_excess = returns.mean() - daily_rf
    market_excess = market_returns.mean() - daily_rf
    
    alpha = (asset_excess - beta * market_excess) * 252
    return alpha


def calculate_treynor_ratio(
    returns: pd.DataFrame, 
    market_returns: pd.Series, 
    risk_free_rate: float = 0.0
) -> pd.Series:
    """
    Calculate Treynor Ratio (excess return per unit of systematic risk).
    
    Formula: (Rp - Rf) / β
    
    Args:
        returns: DataFrame of asset returns
        market_returns: Series of market returns
        risk_free_rate: Annual risk-free rate
    
    Returns:
        Series of Treynor ratios
    """
    daily_rf = risk_free_rate / 252
    beta = calculate_beta(returns, market_returns)
    excess_return = (returns.mean() - daily_rf) * 252
    return excess_return / beta


# =============================================================================
# ROLLING METRICS
# =============================================================================

def calculate_rolling_volatility(returns: pd.DataFrame, window: int = 21, annualized: bool = True) -> pd.DataFrame:
    """
    Calculate rolling volatility.
    
    Args:
        returns: DataFrame of daily returns
        window: Rolling window size (default 21 = 1 month)
        annualized: Whether to annualize
    
    Returns:
        DataFrame of rolling volatilities
    """
    rolling_vol = returns.rolling(window=window).std()
    if annualized:
        rolling_vol = rolling_vol * np.sqrt(252)
    return rolling_vol


def calculate_rolling_sharpe(
    returns: pd.DataFrame, 
    window: int = 63, 
    risk_free_rate: float = 0.0
) -> pd.DataFrame:
    """
    Calculate rolling Sharpe ratio.
    
    Args:
        returns: DataFrame of daily returns
        window: Rolling window size (default 63 = 3 months)
        risk_free_rate: Annual risk-free rate
    
    Returns:
        DataFrame of rolling Sharpe ratios
    """
    daily_rf = risk_free_rate / 252
    excess_returns = returns - daily_rf
    
    rolling_mean = excess_returns.rolling(window=window).mean()
    rolling_std = returns.rolling(window=window).std()
    
    return (rolling_mean / rolling_std) * np.sqrt(252)


def calculate_rolling_beta(
    returns: pd.DataFrame, 
    market_returns: pd.Series, 
    window: int = 63
) -> pd.DataFrame:
    """
    Calculate rolling Beta.
    
    Args:
        returns: DataFrame of asset returns
        market_returns: Series of market returns
        window: Rolling window size
    
    Returns:
        DataFrame of rolling Betas
    """
    rolling_betas = pd.DataFrame(index=returns.index, columns=returns.columns)
    
    for col in returns.columns:
        cov = returns[col].rolling(window=window).cov(market_returns)
        var = market_returns.rolling(window=window).var()
        rolling_betas[col] = cov / var
    
    return rolling_betas.astype(float)


# =============================================================================
# PORTFOLIO OPTIMIZATION
# =============================================================================

def calculate_portfolio_performance(
    weights: np.ndarray, 
    mean_returns: pd.Series, 
    cov_matrix: pd.DataFrame, 
    risk_free_rate: float = 0.0
) -> Tuple[float, float, float]:
    """
    Calculate portfolio performance metrics.
    
    Args:
        weights: Array of portfolio weights
        mean_returns: Series of mean daily returns
        cov_matrix: Covariance matrix of returns
        risk_free_rate: Annual risk-free rate
    
    Returns:
        Tuple of (annualized_return, annualized_volatility, sharpe_ratio)
    """
    portfolio_return = np.sum(mean_returns * weights) * 252
    portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    sharpe = (portfolio_return - risk_free_rate) / portfolio_std
    return portfolio_return, portfolio_std, sharpe


def simulate_efficient_frontier(
    returns: pd.DataFrame, 
    num_portfolios: int = 5000, 
    risk_free_rate: float = 0.0,
    random_seed: Optional[int] = None
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Simulate efficient frontier using Monte Carlo.
    
    Args:
        returns: DataFrame of daily returns
        num_portfolios: Number of random portfolios to simulate
        risk_free_rate: Annual risk-free rate
        random_seed: Optional random seed for reproducibility
    
    Returns:
        Tuple of (simulation_results_df, optimal_portfolios_dict)
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    num_assets = len(returns.columns)
    
    results = np.zeros((4, num_portfolios))
    weights_record = []
    
    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        weights_record.append(weights)
        
        p_return, p_std, p_sharpe = calculate_portfolio_performance(
            weights, mean_returns, cov_matrix, risk_free_rate
        )
        
        results[0, i] = p_std
        results[1, i] = p_return
        results[2, i] = p_sharpe
        results[3, i] = p_return / p_std  # Return per unit risk
    
    sim_df = pd.DataFrame(results.T, columns=['Volatility', 'Return', 'Sharpe', 'ReturnPerRisk'])
    
    # Find optimal portfolios
    max_sharpe_idx = results[2].argmax()
    min_vol_idx = results[0].argmin()
    
    optimal = {
        'max_sharpe': {
            'weights': dict(zip(returns.columns, weights_record[max_sharpe_idx])),
            'return': results[1, max_sharpe_idx],
            'volatility': results[0, max_sharpe_idx],
            'sharpe': results[2, max_sharpe_idx]
        },
        'min_volatility': {
            'weights': dict(zip(returns.columns, weights_record[min_vol_idx])),
            'return': results[1, min_vol_idx],
            'volatility': results[0, min_vol_idx],
            'sharpe': results[2, min_vol_idx]
        }
    }
    
    return sim_df, optimal


# =============================================================================
# SUMMARY STATISTICS
# =============================================================================

def generate_performance_summary(prices: pd.DataFrame, returns: pd.DataFrame, risk_free_rate: float = 0.0) -> pd.DataFrame:
    """
    Generate comprehensive performance summary.
    
    Args:
        prices: DataFrame of asset prices
        returns: DataFrame of daily returns
        risk_free_rate: Annual risk-free rate
    
    Returns:
        DataFrame with all key metrics
    """
    summary = pd.DataFrame(index=returns.columns)
    
    # Return metrics
    summary['Total Return'] = calculate_total_return(prices)
    summary['Annualized Return'] = calculate_annualized_return(returns)
    
    # Risk metrics
    summary['Volatility (Ann.)'] = calculate_volatility(returns)
    summary['Downside Dev'] = calculate_downside_deviation(returns)
    summary['Max Drawdown'] = calculate_max_drawdown(prices)
    summary['VaR (95%)'] = calculate_var(returns, 0.95)
    summary['CVaR (95%)'] = calculate_cvar(returns, 0.95)
    
    # Risk-adjusted metrics
    summary['Sharpe Ratio'] = calculate_sharpe_ratio(returns, risk_free_rate)
    summary['Sortino Ratio'] = calculate_sortino_ratio(returns, risk_free_rate)
    summary['Calmar Ratio'] = calculate_calmar_ratio(prices, returns)
    summary['Omega Ratio'] = calculate_omega_ratio(returns)
    
    return summary.round(4)
