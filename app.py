"""
Professional Investment Analytics Dashboard
============================================

A comprehensive portfolio analysis and optimization tool designed for 
professional fund managers and investment analysts.

Author: Tuan The Scientist
Version: 2.0.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from src.data_loader import fetch_stock_data, get_ticker_info
from src.analysis import (
    calculate_returns,
    calculate_cumulative_returns,
    calculate_volatility,
    calculate_sharpe_ratio,
    calculate_sortino_ratio,
    calculate_calmar_ratio,
    calculate_max_drawdown,
    calculate_drawdown_series,
    calculate_var,
    calculate_cvar,
    calculate_beta,
    calculate_alpha,
    calculate_rolling_volatility,
    calculate_rolling_sharpe,
    calculate_annualized_return,
    calculate_total_return,
    simulate_efficient_frontier,
    generate_performance_summary,
)

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="Investment Analytics Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-top: 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# HEADER
# =============================================================================

col_title, col_badge = st.columns([4, 1])
with col_title:
    st.markdown('<p class="main-header">📈 Investment Analytics Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Professional Portfolio Analysis & Optimization Platform</p>', unsafe_allow_html=True)

with col_badge:
    st.markdown("**v2.0** | Python 3.11+")
    st.markdown("Built for Fund Managers")

st.divider()

# =============================================================================
# SIDEBAR CONFIGURATION
# =============================================================================

st.sidebar.header("⚙️ Configuration")

# Ticker input
st.sidebar.subheader("Assets")
default_tickers = "AAPL, MSFT, GOOGL, AMZN, NVDA"
tickers_input = st.sidebar.text_area(
    "Enter Stock Tickers (comma or newline separated)",
    value=default_tickers,
    height=100,
    help="Enter ticker symbols like AAPL, MSFT, GOOGL"
)
tickers = [t.strip().upper() for t in tickers_input.replace('\n', ',').split(",") if t.strip()]

# Benchmark
benchmark_ticker = st.sidebar.selectbox(
    "Benchmark Index",
    options=["SPY", "QQQ", "IWM", "VTI", "^GSPC"],
    index=0,
    help="Select benchmark for Beta/Alpha calculations"
)

# Date range
st.sidebar.subheader("Date Range")
end_date = datetime.today()
start_date = end_date - timedelta(days=365 * 3)
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date_input = st.date_input("Start", value=start_date)
with col2:
    end_date_input = st.date_input("End", value=end_date)

# Advanced settings
with st.sidebar.expander("🔧 Advanced Settings", expanded=False):
    risk_free_rate = st.number_input(
        "Risk-free rate (annual, %)",
        min_value=-5.0,
        max_value=15.0,
        value=4.5,
        step=0.25,
        help="Current T-Bill rate ~4.5%"
    )
    
    confidence_level = st.slider(
        "VaR/CVaR Confidence Level",
        min_value=0.90,
        max_value=0.99,
        value=0.95,
        step=0.01
    )
    
    num_portfolios = st.slider(
        "Monte Carlo Simulations",
        min_value=1000,
        max_value=15000,
        value=5000,
        step=1000
    )
    
    random_seed = st.number_input(
        "Random Seed (reproducibility)",
        min_value=0,
        max_value=99999,
        value=42
    )

# Analyze button
analyze_clicked = st.sidebar.button("🚀 Run Analysis", type="primary", use_container_width=True)

st.sidebar.divider()
st.sidebar.markdown("**Made by Tuan The Scientist**")
st.sidebar.markdown("[GitHub](https://github.com/tuanthescientist)")

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def format_pct(value: float) -> str:
    """Format as percentage."""
    return f"{value:.2%}"

def format_number(value: float, decimals: int = 2) -> str:
    """Format number."""
    return f"{value:.{decimals}f}"

def create_metric_card(label: str, value: str, delta: str = None, delta_color: str = "normal"):
    """Create a styled metric card."""
    st.metric(label=label, value=value, delta=delta, delta_color=delta_color)

# =============================================================================
# MAIN ANALYSIS
# =============================================================================

if analyze_clicked:
    with st.spinner("Fetching market data..."):
        try:
            # Fetch data
            prices = fetch_stock_data(tickers, str(start_date_input), str(end_date_input))
            benchmark_prices = fetch_stock_data([benchmark_ticker], str(start_date_input), str(end_date_input))
            
            if prices.empty:
                st.error("❌ No data found. Please check your tickers and date range.")
                st.stop()
            
            # Calculate metrics
            returns = calculate_returns(prices)
            benchmark_returns = calculate_returns(benchmark_prices).iloc[:, 0]
            cum_returns = calculate_cumulative_returns(returns)
            
            # Ensure index alignment
            common_idx = returns.index.intersection(benchmark_returns.index)
            returns = returns.loc[common_idx]
            benchmark_returns = benchmark_returns.loc[common_idx]
            
            rf_decimal = risk_free_rate / 100
            
            # Generate summary
            summary = generate_performance_summary(prices, returns, rf_decimal)
            
            # Calculate additional metrics
            beta = calculate_beta(returns, benchmark_returns)
            alpha = calculate_alpha(returns, benchmark_returns, rf_decimal)
            
            # =================================================================
            # TAB LAYOUT
            # =================================================================
            
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Overview", 
                "📈 Performance", 
                "⚠️ Risk Analysis", 
                "🎯 Portfolio Optimization",
                "📥 Export"
            ])
            
            # =================================================================
            # TAB 1: OVERVIEW
            # =================================================================
            
            with tab1:
                st.header("Portfolio Overview")
                
                # Key metrics row
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    avg_return = summary['Annualized Return'].mean()
                    st.metric("Avg Annual Return", format_pct(avg_return))
                
                with col2:
                    avg_vol = summary['Volatility (Ann.)'].mean()
                    st.metric("Avg Volatility", format_pct(avg_vol))
                
                with col3:
                    avg_sharpe = summary['Sharpe Ratio'].mean()
                    st.metric("Avg Sharpe Ratio", format_number(avg_sharpe))
                
                with col4:
                    worst_dd = summary['Max Drawdown'].min()
                    st.metric("Worst Drawdown", format_pct(worst_dd))
                
                with col5:
                    avg_beta = beta.mean()
                    st.metric("Avg Beta", format_number(avg_beta))
                
                st.divider()
                
                # Summary table
                st.subheader("Performance Summary Table")
                
                # Format summary for display
                display_summary = summary.copy()
                for col in ['Total Return', 'Annualized Return', 'Volatility (Ann.)', 'Downside Dev', 
                           'Max Drawdown', 'VaR (95%)', 'CVaR (95%)']:
                    if col in display_summary.columns:
                        display_summary[col] = display_summary[col].apply(format_pct)
                
                for col in ['Sharpe Ratio', 'Sortino Ratio', 'Calmar Ratio', 'Omega Ratio']:
                    if col in display_summary.columns:
                        display_summary[col] = display_summary[col].apply(lambda x: format_number(x))
                
                st.dataframe(display_summary, use_container_width=True)
                
                # Beta/Alpha table
                st.subheader(f"Market Risk Metrics (vs {benchmark_ticker})")
                market_metrics = pd.DataFrame({
                    'Beta': beta.apply(lambda x: format_number(x)),
                    'Alpha (Ann.)': alpha.apply(lambda x: format_pct(x))
                })
                st.dataframe(market_metrics, use_container_width=True)
            
            # =================================================================
            # TAB 2: PERFORMANCE
            # =================================================================
            
            with tab2:
                st.header("Performance Analysis")
                
                # Normalized prices
                st.subheader("Normalized Price History (Base = 1.0)")
                normalized_prices = prices / prices.iloc[0]
                fig_norm = px.line(
                    normalized_prices,
                    title="",
                    labels={"value": "Normalized Price", "variable": "Asset"},
                )
                fig_norm.update_layout(hovermode="x unified", legend=dict(orientation="h"))
                st.plotly_chart(fig_norm, use_container_width=True)
                
                # Cumulative returns
                st.subheader("Cumulative Returns")
                fig_cum = px.line(
                    cum_returns,
                    title="",
                    labels={"value": "Cumulative Return", "variable": "Asset"},
                )
                fig_cum.update_layout(hovermode="x unified", legend=dict(orientation="h"))
                st.plotly_chart(fig_cum, use_container_width=True)
                
                # Rolling metrics
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Rolling 21-Day Volatility")
                    rolling_vol = calculate_rolling_volatility(returns, window=21)
                    fig_rvol = px.line(rolling_vol, labels={"value": "Volatility", "variable": "Asset"})
                    fig_rvol.update_layout(showlegend=True, legend=dict(orientation="h"))
                    st.plotly_chart(fig_rvol, use_container_width=True)
                
                with col2:
                    st.subheader("Rolling 63-Day Sharpe")
                    rolling_sharpe = calculate_rolling_sharpe(returns, window=63, risk_free_rate=rf_decimal)
                    fig_rsharpe = px.line(rolling_sharpe, labels={"value": "Sharpe", "variable": "Asset"})
                    fig_rsharpe.update_layout(showlegend=True, legend=dict(orientation="h"))
                    st.plotly_chart(fig_rsharpe, use_container_width=True)
            
            # =================================================================
            # TAB 3: RISK ANALYSIS
            # =================================================================
            
            with tab3:
                st.header("Risk Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Drawdown chart
                    st.subheader("Drawdown Over Time")
                    drawdown_series = calculate_drawdown_series(prices)
                    fig_dd = px.area(
                        drawdown_series,
                        labels={"value": "Drawdown", "variable": "Asset"},
                    )
                    fig_dd.update_layout(hovermode="x unified")
                    st.plotly_chart(fig_dd, use_container_width=True)
                
                with col2:
                    # Correlation matrix
                    st.subheader("Correlation Matrix")
                    corr_matrix = returns.corr()
                    fig_corr = px.imshow(
                        corr_matrix,
                        text_auto=".2f",
                        color_continuous_scale="RdBu_r",
                        zmin=-1, zmax=1
                    )
                    fig_corr.update_layout(width=500, height=500)
                    st.plotly_chart(fig_corr, use_container_width=True)
                
                # VaR/CVaR table
                st.subheader(f"Value at Risk Analysis ({confidence_level:.0%} Confidence)")
                
                var_hist = calculate_var(returns, confidence_level, method='historical')
                var_param = calculate_var(returns, confidence_level, method='parametric')
                cvar = calculate_cvar(returns, confidence_level)
                
                var_table = pd.DataFrame({
                    'VaR (Historical)': var_hist.apply(format_pct),
                    'VaR (Parametric)': var_param.apply(format_pct),
                    'CVaR (Expected Shortfall)': cvar.apply(format_pct)
                })
                st.dataframe(var_table, use_container_width=True)
                
                # Return distribution
                st.subheader("Return Distribution")
                fig_hist = go.Figure()
                for col in returns.columns:
                    fig_hist.add_trace(go.Histogram(x=returns[col], name=col, opacity=0.7))
                fig_hist.update_layout(barmode='overlay', xaxis_title="Daily Return", yaxis_title="Frequency")
                st.plotly_chart(fig_hist, use_container_width=True)
            
            # =================================================================
            # TAB 4: PORTFOLIO OPTIMIZATION
            # =================================================================
            
            with tab4:
                st.header("Portfolio Optimization")
                
                if len(tickers) < 2:
                    st.warning("⚠️ Add at least 2 tickers to run portfolio optimization.")
                else:
                    with st.spinner(f"Running {num_portfolios:,} Monte Carlo simulations..."):
                        sim_df, optimal = simulate_efficient_frontier(
                            returns, 
                            num_portfolios=num_portfolios,
                            risk_free_rate=rf_decimal,
                            random_seed=int(random_seed)
                        )
                    
                    # Efficient frontier plot
                    st.subheader("Efficient Frontier")
                    
                    fig_ef = px.scatter(
                        sim_df,
                        x="Volatility",
                        y="Return",
                        color="Sharpe",
                        color_continuous_scale="Viridis",
                        opacity=0.6,
                        labels={"Volatility": "Annualized Volatility", "Return": "Annualized Return"}
                    )
                    
                    # Add optimal portfolios
                    fig_ef.add_trace(go.Scatter(
                        x=[optimal['max_sharpe']['volatility']],
                        y=[optimal['max_sharpe']['return']],
                        mode='markers',
                        marker=dict(size=20, color='gold', symbol='star'),
                        name='Max Sharpe'
                    ))
                    
                    fig_ef.add_trace(go.Scatter(
                        x=[optimal['min_volatility']['volatility']],
                        y=[optimal['min_volatility']['return']],
                        mode='markers',
                        marker=dict(size=20, color='green', symbol='diamond'),
                        name='Min Volatility'
                    ))
                    
                    fig_ef.update_layout(height=600)
                    st.plotly_chart(fig_ef, use_container_width=True)
                    
                    # Optimal portfolios
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("⭐ Maximum Sharpe Portfolio")
                        st.metric("Expected Return", format_pct(optimal['max_sharpe']['return']))
                        st.metric("Expected Volatility", format_pct(optimal['max_sharpe']['volatility']))
                        st.metric("Sharpe Ratio", format_number(optimal['max_sharpe']['sharpe']))
                        
                        st.markdown("**Weights:**")
                        weights_df = pd.DataFrame.from_dict(
                            optimal['max_sharpe']['weights'], 
                            orient='index', 
                            columns=['Weight']
                        )
                        weights_df['Weight'] = weights_df['Weight'].apply(format_pct)
                        st.dataframe(weights_df)
                    
                    with col2:
                        st.subheader("🛡️ Minimum Volatility Portfolio")
                        st.metric("Expected Return", format_pct(optimal['min_volatility']['return']))
                        st.metric("Expected Volatility", format_pct(optimal['min_volatility']['volatility']))
                        st.metric("Sharpe Ratio", format_number(optimal['min_volatility']['sharpe']))
                        
                        st.markdown("**Weights:**")
                        weights_df = pd.DataFrame.from_dict(
                            optimal['min_volatility']['weights'], 
                            orient='index', 
                            columns=['Weight']
                        )
                        weights_df['Weight'] = weights_df['Weight'].apply(format_pct)
                        st.dataframe(weights_df)
            
            # =================================================================
            # TAB 5: EXPORT
            # =================================================================
            
            with tab5:
                st.header("Export Data")
                st.markdown("Download analysis results for further processing or reporting.")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.download_button(
                        "📊 Prices (CSV)",
                        prices.to_csv().encode("utf-8"),
                        file_name="prices.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    st.download_button(
                        "📈 Returns (CSV)",
                        returns.to_csv().encode("utf-8"),
                        file_name="daily_returns.csv",
                        mime="text/csv"
                    )
                
                with col3:
                    st.download_button(
                        "📉 Summary (CSV)",
                        summary.to_csv().encode("utf-8"),
                        file_name="performance_summary.csv",
                        mime="text/csv"
                    )
                
                with col4:
                    corr_csv = returns.corr().to_csv().encode("utf-8")
                    st.download_button(
                        "🔗 Correlation (CSV)",
                        corr_csv,
                        file_name="correlation_matrix.csv",
                        mime="text/csv"
                    )
                
                st.divider()
                
                st.subheader("Analysis Parameters")
                params = {
                    "Tickers": ", ".join(tickers),
                    "Benchmark": benchmark_ticker,
                    "Start Date": str(start_date_input),
                    "End Date": str(end_date_input),
                    "Risk-Free Rate": f"{risk_free_rate}%",
                    "Confidence Level": f"{confidence_level:.0%}",
                    "Monte Carlo Simulations": num_portfolios,
                    "Random Seed": random_seed
                }
                st.json(params)
        
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.exception(e)

else:
    # Welcome screen
    st.markdown("""
    ## Welcome to the Investment Analytics Dashboard
    
    This professional-grade tool provides comprehensive portfolio analysis capabilities:
    
    ### 🎯 Key Features
    
    | Feature | Description |
    |---------|-------------|
    | **Performance Metrics** | Total return, annualized return, volatility, Sharpe, Sortino, Calmar ratios |
    | **Risk Analysis** | VaR, CVaR, maximum drawdown, correlation analysis |
    | **Market Risk** | Beta, Alpha (Jensen's), benchmark comparison |
    | **Portfolio Optimization** | Monte Carlo efficient frontier simulation |
    | **Rolling Analytics** | Time-varying volatility and Sharpe ratios |
    | **Data Export** | One-click CSV downloads for all analyses |
    
    ### 🚀 Getting Started
    
    1. Enter your stock tickers in the sidebar (comma-separated)
    2. Select your benchmark index
    3. Adjust the date range and advanced settings as needed
    4. Click **Run Analysis** to generate the report
    
    ---
    
    *Built for professional fund managers and investment analysts.*
    """)
    
    # Show sample metrics
    st.info("💡 **Tip**: Use tickers like AAPL, MSFT, GOOGL, AMZN, NVDA for a tech-focused portfolio demo.")
