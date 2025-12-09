import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

from src.data_loader import fetch_stock_data
from src.analysis import (
    calculate_returns,
    calculate_cumulative_returns,
    calculate_volatility,
    calculate_sharpe_ratio,
    calculate_max_drawdown,
)

st.set_page_config(page_title="Investment Analytics Dashboard", layout="wide")

st.title("📈 Professional Investment Analytics Dashboard")
st.markdown("### A comprehensive tool for portfolio analysis and optimization")

# Sidebar for user input
st.sidebar.header("Configuration")

default_tickers = "AAPL, MSFT, GOOGL, AMZN, TSLA"
tickers_input = st.sidebar.text_input(
    "Enter Stock Tickers (comma separated)", value=default_tickers
)
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

end_date = datetime.today()
start_date = end_date - timedelta(days=365 * 3)
start_date_input = st.sidebar.date_input("Start Date", value=start_date)
end_date_input = st.sidebar.date_input("End Date", value=end_date)

with st.sidebar.expander("Advanced settings", expanded=False):
    risk_free_rate = st.number_input(
        "Risk-free rate (annual, %)",
        min_value=-5.0,
        max_value=10.0,
        value=2.0,
        step=0.25,
        help="Used for Sharpe ratio adjustment",
    )
    num_portfolios = st.slider(
        "Simulated portfolios (efficient frontier)",
        min_value=1000,
        max_value=10000,
        value=5000,
        step=500,
    )
    random_seed = st.number_input(
        "Random seed (optional)", min_value=0, max_value=10_000, value=42
    )

analyze_clicked = st.sidebar.button("Analyze", type="primary")

def render_downloads(prices: pd.DataFrame, returns: pd.DataFrame, cum_returns: pd.DataFrame):
    st.subheader("Export Data")
    col1, col2, col3 = st.columns(3)
    col1.download_button(
        "Download Prices (CSV)",
        prices.to_csv().encode("utf-8"),
        file_name="prices.csv",
    )
    col2.download_button(
        "Download Returns (CSV)",
        returns.to_csv().encode("utf-8"),
        file_name="returns.csv",
    )
    col3.download_button(
        "Download Cumulative Returns (CSV)",
        cum_returns.to_csv().encode("utf-8"),
        file_name="cumulative_returns.csv",
    )


if analyze_clicked:
    with st.spinner("Fetching data..."):
        try:
            prices = fetch_stock_data(
                tickers, str(start_date_input), str(end_date_input)
            )

            if prices.empty:
                st.error("No data found. Please check your tickers.")
            else:
                returns = calculate_returns(prices)
                cum_returns = calculate_cumulative_returns(returns)
                volatility = calculate_volatility(returns)
                sharpe = calculate_sharpe_ratio(
                    returns, risk_free_rate=risk_free_rate / 100
                )
                max_dd = calculate_max_drawdown(prices)

                st.header("Key Metrics (Annualized)")
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Median Volatility", f"{volatility.median():.2%}")
                    st.dataframe(volatility.apply(lambda x: f"{x:.2%}"))

                with col2:
                    st.metric("Average Sharpe", f"{sharpe.mean():.2f}")
                    st.dataframe(sharpe.apply(lambda x: f"{x:.2f}"))

                with col3:
                    st.metric("Worst Max Drawdown", f"{max_dd.min():.2%}")
                    st.dataframe(max_dd.apply(lambda x: f"{x:.2%}"))

                st.header("Performance Visualization")

                normalized_prices = prices / prices.iloc[0]
                fig_norm = px.line(
                    normalized_prices, title="Normalized Price History (Base=1.0)"
                )
                st.plotly_chart(fig_norm, use_container_width=True)

                fig_cum = px.line(cum_returns, title="Cumulative Returns")
                st.plotly_chart(fig_cum, use_container_width=True)

                st.header("Correlation Matrix")
                corr_matrix = returns.corr()
                fig_corr = px.imshow(
                    corr_matrix,
                    text_auto=True,
                    title="Asset Correlation",
                    color_continuous_scale="RdBu",
                )
                st.plotly_chart(fig_corr, use_container_width=True)

                if len(tickers) > 1:
                    st.header("Portfolio Optimization (Efficient Frontier Simulation)")
                    if random_seed:
                        np.random.seed(int(random_seed))

                    results = np.zeros((3, num_portfolios))
                    mean_returns = returns.mean()
                    cov_matrix = returns.cov()

                    for i in range(num_portfolios):
                        weights = np.random.random(len(tickers))
                        weights /= np.sum(weights)

                        portfolio_return = np.sum(mean_returns * weights) * 252
                        portfolio_std_dev = (
                            np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
                            * np.sqrt(252)
                        )

                        results[0, i] = portfolio_std_dev
                        results[1, i] = portfolio_return
                        results[2, i] = (portfolio_return - risk_free_rate / 100) / portfolio_std_dev

                    sim_frame = pd.DataFrame(
                        results.T, columns=["Volatility", "Return", "Sharpe Ratio"]
                    )

                    fig_ef = px.scatter(
                        sim_frame,
                        x="Volatility",
                        y="Return",
                        color="Sharpe Ratio",
                        title="Efficient Frontier Simulation",
                        hover_data=["Sharpe Ratio"],
                        color_continuous_scale="Viridis",
                    )
                    st.plotly_chart(fig_ef, use_container_width=True)
                else:
                    st.info("Add at least two tickers to run portfolio optimization.")

                render_downloads(prices, returns, cum_returns)

        except Exception as e:
            st.error(f"An error occurred: {e}")

else:
    st.info("Click 'Analyze' to start.")
