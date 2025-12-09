# Investing Analytics

## Overview

Investing Analytics is a professional-grade tool designed for investment analysis, portfolio management, and financial data visualization. This project demonstrates advanced capabilities in fetching financial data, calculating key performance metrics, and simulating portfolio optimization scenarios.

It is built using Python and leverages powerful libraries such as `pandas`, `numpy`, `yfinance`, and `plotly`. The interactive dashboard is powered by `Streamlit`.

## Features

-   **Real-time Data Fetching**: Retrieves historical stock data using Yahoo Finance API.
-   **Financial Metrics**: Calculates Annualized Volatility, Sharpe Ratio, Maximum Drawdown, and Cumulative Returns.
-   **Interactive Visualizations**:
    -   Normalized Price History
    -   Cumulative Returns Charts
    -   Correlation Matrix Heatmaps
-   **Portfolio Optimization**: Simulates thousands of portfolios to visualize the Efficient Frontier and identify optimal risk-return profiles.

## Project Structure

```
InvestingAnalytics/
├── src/
│   ├── analysis.py       # Core financial calculations
│   └── data_loader.py    # Data fetching logic
├── tests/                # Unit tests
├── app.py                # Streamlit Dashboard entry point
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/tuanthescientist/InvestingAnalytics.git
    cd InvestingAnalytics
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To launch the interactive dashboard:

```bash
streamlit run app.py
```

Open your browser and navigate to the URL provided (usually `http://localhost:8501`).

## Methodology

### Metrics
-   **Sharpe Ratio**: Calculated as $ \frac{R_p - R_f}{\sigma_p} $, where $R_p$ is the portfolio return, $R_f$ is the risk-free rate, and $\sigma_p$ is the portfolio standard deviation.
-   **Volatility**: Annualized standard deviation of daily returns.
-   **Max Drawdown**: The maximum observed loss from a peak to a trough of a portfolio, before a new peak is attained.

### Portfolio Simulation
The Efficient Frontier is approximated by simulating 5,000 random portfolio weight combinations and plotting their expected volatility vs. expected return.

## License

MIT License
