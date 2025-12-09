# Investing Analytics

## Executive Summary

Investing Analytics is a portfolio analytics and optimization dashboard designed to mirror the workflows of professional fund managers. It pulls market data live, computes institutional-grade risk/return metrics, and visualizes an efficient frontier to support capital allocation and fund-raising conversations.

**Why this matters to a hiring manager:**
- Shows end-to-end ownership: data sourcing, quantitative analytics, UX, testing, and deployment readiness.
- Communicates decisions with polished visuals and exportable evidence (CSV downloads for auditability).
- Encapsulates best practices: clean architecture, reproducible environment, and guardrails for risk (Sharpe, drawdown, correlation awareness).

## Features (built for the desk)

- **Live data ingestion** via Yahoo Finance (`yfinance`) with flexible ticker inputs and date ranges.
- **Institutional metrics**: annualized volatility, Sharpe (risk-free adjustable), max drawdown, cumulative returns.
- **Portfolio optimization**: Monte Carlo simulation (1k–10k portfolios) to approximate the efficient frontier; configurable random seed for reproducibility.
- **Visual analytics**: normalized price curves, cumulative returns, correlation heatmap, efficient frontier scatter with Sharpe coloring.
- **Exports**: one-click CSV downloads for prices, returns, and cumulative returns.
- **Resilient UX**: clear error messaging, guardrails for insufficient tickers, and sensible defaults for fast demos.

## Architecture at a glance

```
app.py               # Streamlit UI, user inputs, visualization, orchestration
src/
    data_loader.py     # Data acquisition (Yahoo Finance)
    analysis.py        # Portfolio math: returns, vol, Sharpe, drawdown, frontier helpers
tests/
    test_analysis.py   # Unit tests for analytical functions
requirements.txt     # Reproducible dependencies
.gitignore           # Clean repo hygiene
```

## Quickstart

```bash
git clone https://github.com/tuanthescientist/InvestingAnalytics.git
cd InvestingAnalytics
python -m venv .venv
.\.venv\Scripts\activate   # On macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the URL Streamlit prints (default `http://localhost:8501`).

## Usage Guide (demo script)

1) **Enter tickers**: e.g., `AAPL, MSFT, GOOGL, AMZN, TSLA`.
2) **Set dates**: default is trailing 3 years; adjust to showcase different regimes.
3) **Advanced settings**: tweak risk-free rate (for Sharpe) and number of simulated portfolios; set a seed for reproducibility.
4) **Run**: click **Analyze**.
5) **Read the story**:
     - KPI cards: median volatility, average Sharpe, worst drawdown.
     - Charts: normalized price path, cumulative returns, correlation map.
     - Efficient frontier: hover to see risk/return/Sharpe; discuss allocation intuition.
6) **Export**: download CSVs to share with PMs/ICs or attach to an investment memo.

## Methodology (concise)

- **Returns**: daily % change, $r_t = \frac{P_t - P_{t-1}}{P_{t-1}}$.
- **Cumulative return**: $(1 + r_t)$ compounded.
- **Volatility**: $\sigma_{ann} = \sigma_{daily} \times \sqrt{252}$.
- **Sharpe**: $\frac{\mu - r_f}{\sigma}$, annualized by $\sqrt{252}$; $r_f$ user-configurable.
- **Max drawdown**: min of $\frac{P_t - \max(P)}{\max(P)}$ over the horizon.
- **Efficient frontier (simulated)**: random weights, normalized to 1. Compute expected return and volatility from sample mean/covariance, color by Sharpe.

## Testing

```bash
python -m unittest discover -s tests
```

## Roadmap (next hires can extend)

- Add factor regressions (Fama-French) to decompose returns.
- Include CVaR/Expected Shortfall and stress scenarios.
- Add optimizer-based frontier (e.g., quadratic programming) beside Monte Carlo.
- Connect to fundamental APIs for valuation overlays (P/E, EBITDA, FCFE yields).
- Publish a hosted demo (Streamlit Cloud) with nightly cache refresh.

## Talking points for interviews

- **Risk-aware defaults**: Adjustable risk-free rate, sharpe-driven coloring, drawdown-first framing.
- **Reproducibility**: Pin-able random seed for frontier simulation; CSV exports for audit.
- **Modular design**: Data ingestion isolated from analytics; easy to swap data provider or plug in optimizer.
- **Speed to insight**: Sensible defaults produce a story in <10 seconds on commodity hardware.

## Tech Stack

- Streamlit, Plotly, Pandas, NumPy, SciPy, yfinance
- Python 3.11+

## License

MIT License
