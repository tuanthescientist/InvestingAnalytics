import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from src.data_loader import fetch_stock_data
from src.analysis import (
    calculate_returns, 
    calculate_cumulative_returns, 
    calculate_volatility, 
    calculate_sharpe_ratio, 
    calculate_max_drawdown
)

st.set_page_config(page_title="Investment Analytics Dashboard", layout="wide")

st.title("📈 Professional Investment Analytics Dashboard")
st.markdown("### A comprehensive tool for portfolio analysis and optimization")

# Sidebar for user input
st.sidebar.header("Configuration")

# Default tickers
default_tickers = "AAPL, MSFT, GOOGL, AMZN, TSLA"
tickers_input = st.sidebar.text_input("Enter Stock Tickers (comma separated)", value=default_tickers)
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

# Date range
end_date = datetime.today()
start_date = end_date - timedelta(days=365*3) # 3 years default

start_date_input = st.sidebar.date_input("Start Date", value=start_date)
end_date_input = st.sidebar.date_input("End Date", value=end_date)

if st.sidebar.button("Analyze"):
    with st.spinner("Fetching data..."):
        try:
            prices = fetch_stock_data(tickers, str(start_date_input), str(end_date_input))
            
            if prices.empty:
                st.error("No data found. Please check your tickers.")
            else:
                # Calculations
                returns = calculate_returns(prices)
                cum_returns = calculate_cumulative_returns(returns)
                volatility = calculate_volatility(returns)
                sharpe = calculate_sharpe_ratio(returns)
                max_dd = calculate_max_drawdown(prices)

                # Metrics Display
                st.header("Key Metrics (Annualized)")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.subheader("Volatility")
                    st.dataframe(volatility.apply(lambda x: f"{x:.2%}"))
                
                with col2:
                    st.subheader("Sharpe Ratio")
                    st.dataframe(sharpe.apply(lambda x: f"{x:.2f}"))
                    
                with col3:
                    st.subheader("Max Drawdown")
                    st.dataframe(max_dd.apply(lambda x: f"{x:.2%}"))

                # Charts
                st.header("Performance Visualization")
                
                # Normalized Prices
                normalized_prices = prices / prices.iloc[0]
                fig_norm = px.line(normalized_prices, title="Normalized Price History (Base=1.0)")
                st.plotly_chart(fig_norm, use_container_width=True)

                # Cumulative Returns
                fig_cum = px.line(cum_returns, title="Cumulative Returns")
                st.plotly_chart(fig_cum, use_container_width=True)
                
                # Correlation Matrix
                st.header("Correlation Matrix")
                corr_matrix = returns.corr()
                fig_corr = px.imshow(corr_matrix, text_auto=True, title="Asset Correlation")
                st.plotly_chart(fig_corr, use_container_width=True)

                # Efficient Frontier (Simulation)
                if len(tickers) > 1:
                    st.header("Portfolio Optimization (Efficient Frontier Simulation)")
                    num_portfolios = 5000
                    results = np.zeros((3, num_portfolios))
                    weights_record = []
                    
                    mean_returns = returns.mean()
                    cov_matrix = returns.cov()
                    
                    for i in range(num_portfolios):
                        weights = np.random.random(len(tickers))
                        weights /= np.sum(weights)
                        weights_record.append(weights)
                        
                        portfolio_return = np.sum(mean_returns * weights) * 252
                        portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
                        
                        results[0,i] = portfolio_std_dev
                        results[1,i] = portfolio_return
                        results[2,i] = (portfolio_return) / portfolio_std_dev # Sharpe Ratio (assuming 0 risk-free)
                        
                    sim_frame = pd.DataFrame(results.T, columns=['Volatility', 'Return', 'Sharpe Ratio'])
                    
                    fig_ef = px.scatter(sim_frame, x='Volatility', y='Return', color='Sharpe Ratio', 
                                      title="Efficient Frontier Simulation", hover_data=['Sharpe Ratio'])
                    st.plotly_chart(fig_ef, use_container_width=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")

else:
    st.info("Click 'Analyze' to start.")
