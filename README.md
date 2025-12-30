<div align="center">

# 📈 Investing Analytics

### Professional Portfolio Analysis & Optimization Platform

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

*A comprehensive investment analytics dashboard designed for investment professionals*

[Features](#-features) • [Demo](#-quick-demo) • [Installation](#-installation) • [Documentation](#-methodology) • [Contributing](#-contributing)

**Author:** Tuan Tran

</div>

---

## 📋 Executive Summary

**Investing Analytics** is a production-ready portfolio analytics and optimization dashboard that mirrors the workflows of professional fund managers. It integrates live market data, computes institutional-grade risk/return metrics, and visualizes efficient frontiers to support capital allocation decisions and fund-raising conversations.

### 🎯 Why This Matters to Hiring Managers

| Competency | Demonstration |
|------------|---------------|
| **End-to-End Ownership** | Data sourcing → Quantitative analytics → UX → Testing → Deployment readiness |
| **Communication Skills** | Polished visuals with exportable evidence (CSV downloads for auditability) |
| **Best Practices** | Clean architecture, reproducible environment, risk guardrails (Sharpe, drawdown, correlation) |
| **Technical Depth** | 15+ institutional-grade metrics including VaR, CVaR, Beta, Alpha, Sortino, Calmar |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         INVESTING ANALYTICS v2.0                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        📊 PRESENTATION LAYER                        │   │
│  │                                                                     │   │
│  │   app.py                                                            │   │
│  │   ├── Streamlit UI Components                                       │   │
│  │   ├── User Input Handling (Tickers, Dates, Parameters)              │   │
│  │   ├── Interactive Visualizations (Plotly)                           │   │
│  │   ├── Tab-based Navigation (Overview, Performance, Risk, Optimize)  │   │
│  │   └── Export Functionality (CSV Downloads)                          │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        💼 BUSINESS LOGIC LAYER                      │   │
│  │                                                                     │   │
│  │   src/                                                              │   │
│  │   ├── analysis.py          # Core Analytics Engine                  │   │
│  │   │   ├── Return Calculations (Simple, Log, Cumulative)            │   │
│  │   │   ├── Risk Metrics (Vol, VaR, CVaR, Drawdown)                  │   │
│  │   │   ├── Risk-Adjusted Returns (Sharpe, Sortino, Calmar, Omega)   │   │
│  │   │   ├── Market Risk (Beta, Alpha, Treynor)                       │   │
│  │   │   ├── Rolling Analytics (21d Vol, 63d Sharpe)                  │   │
│  │   │   └── Portfolio Optimization (Monte Carlo Frontier)            │   │
│  │   │                                                                 │   │
│  │   └── data_loader.py       # Data Acquisition                       │   │
│  │       ├── Yahoo Finance API Integration                            │   │
│  │       ├── Multi-ticker Batch Downloads                             │   │
│  │       └── Ticker Info Retrieval                                    │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        🧪 TESTING LAYER                             │   │
│  │                                                                     │   │
│  │   tests/                                                            │   │
│  │   └── test_analysis.py     # Unit Tests for Analytics Functions     │   │
│  │       ├── Return Calculation Tests                                  │   │
│  │       ├── Volatility Tests                                          │   │
│  │       └── Edge Case Handling                                        │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        📦 CONFIGURATION                             │   │
│  │                                                                     │   │
│  │   requirements.txt         # Pinned Dependencies                    │   │
│  │   .gitignore              # Repository Hygiene                      │   │
│  │   README.md               # Documentation                           │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

                              DATA FLOW
                              
    ┌──────────┐      ┌──────────────┐      ┌─────────────┐      ┌──────────┐
    │  Yahoo   │ ───▶ │ data_loader  │ ───▶ │  analysis   │ ───▶ │  app.py  │
    │ Finance  │      │    .py       │      │    .py      │      │ (Charts) │
    └──────────┘      └──────────────┘      └─────────────┘      └──────────┘
         │                  │                     │                    │
         │              Prices DF            Metrics DF           Visualizations
         │                  │                     │                    │
         └──────────────────┴─────────────────────┴────────────────────┘
                                    │
                                    ▼
                              ┌──────────┐
                              │   CSV    │
                              │ Exports  │
                              └──────────┘
```

### 📁 File Structure

```
InvestingAnalytics/
│
├── 📄 app.py                    # Main Streamlit application
│                                 # - Page configuration & styling
│                                 # - Sidebar controls
│                                 # - 5-tab analysis interface
│                                 # - Export functionality
│
├── 📁 src/                       # Source modules
│   ├── 📄 __init__.py
│   ├── 📄 data_loader.py        # Data acquisition layer
│   │                             # - fetch_stock_data()
│   │                             # - get_ticker_info()
│   │
│   └── 📄 analysis.py           # Analytics engine (500+ lines)
│                                 # - 20+ financial functions
│                                 # - Full docstrings & type hints
│
├── 📁 tests/                     # Test suite
│   └── 📄 test_analysis.py      # Unit tests
│
├── 📄 requirements.txt          # Dependencies
├── 📄 .gitignore                # Git ignore rules
└── 📄 README.md                 # This file
```

---

## ✨ Features

### 📊 Performance Metrics

| Metric | Formula | Description |
|--------|---------|-------------|
| **Total Return** | $(P_{end} / P_{start}) - 1$ | Overall gain/loss |
| **Annualized Return** | $(1 + r)^{252/n} - 1$ | Geometric mean annualized |
| **Cumulative Return** | $\prod(1 + r_t)$ | Compounded growth |

### ⚠️ Risk Metrics

| Metric | Formula | Description |
|--------|---------|-------------|
| **Volatility** | $\sigma \times \sqrt{252}$ | Annualized standard deviation |
| **Downside Deviation** | $\sqrt{\mathbb{E}[\min(r, 0)^2]}$ | Below-target volatility |
| **Max Drawdown** | $\min\left(\frac{P_t - P_{max}}{P_{max}}\right)$ | Worst peak-to-trough |
| **VaR (95%)** | $-\text{percentile}(r, 5\%)$ | Daily loss threshold |
| **CVaR / ES** | $\mathbb{E}[r \mid r < \text{VaR}]$ | Expected shortfall |

### 📈 Risk-Adjusted Returns

| Metric | Formula | Use Case |
|--------|---------|----------|
| **Sharpe Ratio** | $\frac{r_p - r_f}{\sigma_p}$ | Risk-adjusted excess return |
| **Sortino Ratio** | $\frac{r_p - r_f}{\sigma_{downside}}$ | Downside-only volatility |
| **Calmar Ratio** | $\frac{r_{ann}}{\|MDD\|}$ | Return per drawdown |
| **Omega Ratio** | $\frac{\sum gains}{\sum losses}$ | Probability-weighted |
| **Treynor Ratio** | $\frac{r_p - r_f}{\beta}$ | Systematic risk adjusted |

### 🎯 Market Risk

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Beta** | $\frac{Cov(r_i, r_m)}{Var(r_m)}$ | Systematic risk exposure |
| **Alpha (Jensen's)** | $r_p - [r_f + \beta(r_m - r_f)]$ | Manager skill premium |
| **Information Ratio** | $\frac{r_p - r_b}{\sigma_{tracking}}$ | Active return per risk |

### 🔄 Rolling Analytics

- **21-Day Rolling Volatility**: Short-term risk dynamics
- **63-Day Rolling Sharpe**: Quarterly risk-adjusted performance
- **Rolling Beta**: Time-varying market sensitivity

### 🎲 Portfolio Optimization

- **Monte Carlo Simulation**: 1,000–15,000 random portfolios
- **Efficient Frontier Visualization**: Risk vs. Return scatter with Sharpe coloring
- **Optimal Portfolio Identification**:
  - ⭐ Maximum Sharpe Portfolio
  - 🛡️ Minimum Volatility Portfolio
- **Reproducibility**: Configurable random seed

---

## 🚀 Quick Demo

### Prerequisites

- Python 3.11+
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/tuanthescientist/InvestingAnalytics.git
cd InvestingAnalytics

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch the dashboard
streamlit run app.py
```

### First Analysis

1. **Enter tickers**: `AAPL, MSFT, GOOGL, AMZN, NVDA`
2. **Select benchmark**: `SPY` (S&P 500 ETF)
3. **Set date range**: Last 3 years (default)
4. **Configure settings**: Risk-free rate 4.5%, 5000 simulations
5. **Click**: 🚀 **Run Analysis**
6. **Explore tabs**: Overview → Performance → Risk → Optimization → Export

---

## 📐 Methodology

### 🎓 Investment Philosophy & Framework

This project is built upon the principles of **Quantitative Investing** and **Modern Portfolio Theory (MPT)**. Below are the core methodologies implemented:

#### 1. Modern Portfolio Theory (MPT)

**Founder**: Harry Markowitz (1952) - Nobel Prize in Economics 1990

**Core Principles**: 
- Investors can construct an "optimal" portfolio through diversification to achieve the highest expected return for a given level of risk
- Portfolio risk depends not only on the individual asset risks but also on the **correlation** between assets
- Diversification reduces unsystematic (idiosyncratic) risk while systematic (market) risk remains

**Implementation in this Project**:
- **Efficient Frontier Simulation**: Simulate thousands of random portfolios to approximate the efficient frontier
- **Correlation Matrix**: Analyze asset correlations to understand diversification benefits
- **Portfolio Optimization**: Identify Max Sharpe and Min Volatility portfolios

```
                    Expected Return
                         ▲
                         │      ★ Max Sharpe Portfolio
                         │    ●●●●
                         │  ●●    ●●
                         │●●        ●●  ← Efficient Frontier
                         │            ●
                    ◆ Min│Vol          ●
                         │              ●
                         └──────────────────▶ Risk (Volatility)
```

#### 2. Capital Asset Pricing Model (CAPM)

**Developer**: William Sharpe (1964) - Nobel Prize in Economics 1990

**CAPM Formula**:
$$E(R_i) = R_f + \beta_i \times (E(R_m) - R_f)$$

Where:
- $E(R_i)$: Expected return of the asset
- $R_f$: Risk-free rate (e.g., T-Bill yield)
- $\beta_i$: Beta coefficient (sensitivity to market movements)
- $E(R_m)$: Expected market return

**Interpretation Guide**:

| Metric | Meaning | Implication |
|--------|---------|-------------|
| **Beta = 1** | Asset moves with the market | Average systematic risk |
| **Beta > 1** | Asset is more volatile than market | Higher risk, higher potential return |
| **Beta < 1** | Asset is more stable than market | Defensive, lower risk |
| **Alpha > 0** | Outperforms CAPM prediction | Skilled portfolio management |
| **Alpha < 0** | Underperforms expectations | Strategy needs review |

#### 3. Risk-Adjusted Performance Metrics

**Why Important?**: High returns are meaningless if accompanied by excessive risk. Risk-adjusted metrics enable fair comparison between investment strategies.

| Metric | Formula | When to Use |
|--------|---------|-------------|
| **Sharpe Ratio** | $(R_p - R_f) / \sigma_p$ | General comparison, most popular |
| **Sortino Ratio** | $(R_p - R_f) / \sigma_{downside}$ | Focus on downside risk only |
| **Calmar Ratio** | $R_{ann} / \|MaxDD\|$ | Assess recovery capability |
| **Omega Ratio** | $\Sigma gains / \Sigma losses$ | Full probability distribution |
| **Treynor Ratio** | $(R_p - R_f) / \beta$ | Well-diversified portfolios |

**Sharpe Ratio Interpretation Guide**:
- **< 0**: Strategy worse than holding cash
- **0 - 1**: Below average, needs improvement
- **1 - 2**: Good, acceptable performance
- **2 - 3**: Very good, highly efficient
- **> 3**: Excellent (rare, verify data integrity)

#### 4. Value at Risk (VaR) & Conditional VaR (CVaR)

**VaR (Value at Risk)**: "With X% confidence, the maximum loss in one day will not exceed Y%"

**Example**: VaR 95% = 2.5% means: On 95% of trading days, you will not lose more than 2.5%

**CVaR (Conditional VaR / Expected Shortfall)**: "If losses exceed VaR, what is the average loss?"

```
    Probability
         ▲
         │
       ██│
      ███│
     ████│      ┌────────────────┐
    █████│      │ 95% of returns │
   ██████│◄─────┤ fall here      │
  ███████│      └────────────────┘
 ████████│                          
█████████│────────┬─────────────────▶ Return
         │        │
         │     VaR│95%
         │        │
         │     ◄──┴──► CVaR (Expected Shortfall)
         │        Tail Risk Zone (5%)
```

**Why CVaR is Superior to VaR**:
- VaR does not indicate the severity of losses when they occur
- CVaR measures the "tail" of the distribution - where rare but catastrophic events happen
- CVaR is a coherent risk measure (satisfies subadditivity)

#### 5. Drawdown Analysis

**Max Drawdown (MDD)**: The largest peak-to-trough decline over a specific time period

$$MDD = \frac{P_{trough} - P_{peak}}{P_{peak}} \times 100\%$$

**Why Important?**:
- Shows the actual "worst case scenario" that occurred
- Assesses investor's psychological tolerance
- Calmar Ratio uses MDD as the denominator

**Historical Examples**:
| Event | S&P 500 Max Drawdown | Recovery Time |
|-------|----------------------|---------------|
| Dot-com Crash (2000-2002) | -49% | ~7 years |
| Financial Crisis (2008-2009) | -57% | ~4 years |
| COVID Crash (2020) | -34% | ~5 months |

#### 6. Monte Carlo Simulation

**Principle**: Use randomness to estimate possible outcomes through repeated sampling

**Application in Portfolio Optimization**:
1. Generate N random portfolio weight combinations (e.g., 5,000 sets)
2. Calculate Expected Return and Volatility for each portfolio
3. Plot all (Risk, Return) points on a scatter chart
4. Identify the Efficient Frontier - the boundary of optimal portfolios
5. Locate Max Sharpe and Min Volatility portfolios

**Reproducibility**: Use Random Seed to ensure results can be replicated

---

### Return Calculations

```
Daily Return:       r_t = (P_t - P_{t-1}) / P_{t-1}
Log Return:         r_t = ln(P_t / P_{t-1})
Cumulative Return:  (1 + r_1)(1 + r_2)...(1 + r_n)
Annualized Return:  (Total Return + 1)^(252/n) - 1
```

### Risk Metrics

```
Volatility (Ann.):  σ_daily × √252
Downside Dev:       √(mean of squared negative returns)
Max Drawdown:       min((P_t - running_max) / running_max)
VaR (95%):          -5th percentile of daily returns
CVaR:               mean of returns below VaR threshold
```

### Risk-Adjusted Metrics

```
Sharpe:    (μ - r_f) / σ × √252
Sortino:   (μ - r_f) / σ_down × √252
Calmar:    Annualized Return / |Max Drawdown|
Omega:     Σ(gains above threshold) / Σ(losses below threshold)
```

### CAPM Metrics

```
Beta:      Cov(r_asset, r_market) / Var(r_market)
Alpha:     r_asset - [r_f + β(r_market - r_f)]
Treynor:   (r_asset - r_f) / β
```

---

## 🧪 Testing

```bash
# Run all tests
python -m unittest discover -s tests

# Run with verbose output
python -m unittest discover -s tests -v
```

---

## 🗺️ Roadmap

### v2.1 (Next Release)
- [ ] Factor regressions (Fama-French 3-factor, 5-factor)
- [ ] Stress testing scenarios (2008, COVID, etc.)
- [ ] Quadratic programming optimizer (beside Monte Carlo)

### v2.2
- [ ] Fundamental overlays (P/E, EV/EBITDA, FCF Yield)
- [ ] Sector/industry breakdown
- [ ] ESG scoring integration

### v3.0
- [ ] Multi-user authentication
- [ ] Portfolio persistence (database)
- [ ] Scheduled reports & alerts
- [ ] Streamlit Cloud deployment

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| **Frontend** | Streamlit, Plotly |
| **Analytics** | Pandas, NumPy, SciPy |
| **Data** | yfinance (Yahoo Finance API) |
| **Visualization** | Plotly Express, Plotly Graph Objects |
| **Testing** | unittest |
| **Language** | Python 3.11+ |

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Tuan Tran**

- GitHub: [@tuanthescientist](https://github.com/tuanthescientist)

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

*Built with ❤️ for the investment community*

</div>
