# AI-Indicator: Backtesting & Optimization System

A professional-grade Python backtesting and parameter optimization engine for technical trading indicators.

## 🎯 Overview

This system automatically tests technical indicators with all parameter combinations and finds the parameter set that yields the **BEST and MOST STABLE profit** through systematic grid search optimization.

**Note**: This is NOT a price prediction AI. This is an indicator parameter optimization engine for quantitative trading research.

## ✨ Features

- **Complete Backtesting Engine**: Candle-by-candle simulation with no look-ahead bias
- **Grid Search Optimization**: Tests all combinations of indicator parameters
- **Multi-Metric Evaluation**: Profit, win rate, max drawdown, profit factor
- **Smart Scoring Function**: Balances profitability with stability
- **Clean Output**: Top 10 results + full CSV export
- **Modular Architecture**: Easy to extend to other indicators

## 📊 Current Implementation

### Indicator: RSI (Relative Strength Index)

**Parameters to Optimize:**
- RSI Period: 5 to 30 (step 1) → 26 values
- Overbought: 65 to 85 (step 5) → 5 values
- Oversold: 15 to 35 (step 5) → 5 values
- **Total Combinations**: 650

### Trading Rules

- **BUY Signal**: RSI < oversold threshold
- **SELL Signal**: RSI > overbought threshold
- **Position Management**: One position at a time
- **Exit Conditions**:
  - Take Profit: 20 pips
  - Stop Loss: 15 pips
- **Fixed Lot Size**: 0.1
- **Spread**: 1.2 pips (no commission, no slippage)

## 🚀 Quick Start

### Two Ways to Use

#### Option 1: 🖥️ **GUI (Recommended for Beginners)**

Beautiful web interface with interactive charts!

```bash
# Install dependencies
pip install -r requirements.txt

# Launch GUI
streamlit run gui_app.py
```

Then open browser at: **http://localhost:8501**

**Features:**
- ✅ Visual parameter configuration with sliders
- ✅ Real-time progress tracking
- ✅ Interactive charts (Bar, Scatter, Heatmap)
- ✅ One-click CSV download
- ✅ No coding required!

📖 **See [HUONG_DAN_GUI.md](HUONG_DAN_GUI.md) for detailed GUI guide (Vietnamese)**

---

#### Option 2: 💻 **Command Line (For Automation)**

### Prerequisites

```bash
pip install pandas numpy
```

### Generate Sample Data

```bash
python generate_sample_data.py
```

This creates `AUDCAD15.csv` with ~2500 candles of M15 (15-minute) data.

### Run Optimization

```bash
python backtest_optimizer.py
```

### Expected Output

```
================================================================================
 BACKTESTING & OPTIMIZATION SYSTEM
 Technical Indicator Parameter Optimizer
================================================================================

Loading data from AUDCAD15.csv...
Loaded 2500 candles from 2024-01-01 to 2024-02-06

Progress: 650/650 (100.0%)

TOP 10 PARAMETER SETS (Ranked by Score)
────────────────────────────────────────
Rank #1  ★ BEST PARAMETERS ★
────────────────────────────────────────
Parameters:
  RSI Period:   18
  Overbought:   85
  Oversold:     25

Performance:
  Total Profit:        56.40 pips
  Win Rate:           100.00%
  Profit Factor:       56.40
  Max Drawdown:         0.00 (0.00%)
  SCORE:             1056.25
```

## 📁 File Structure

```
AI-Indicator/
├── gui_app.py                  # 🖥️ GUI Application (Streamlit)
├── backtest_optimizer.py       # 💻 CLI Optimization Engine
├── quick_test.py               # ⚡ Quick Test (16 combinations)
├── generate_sample_data.py     # 📊 Sample Data Generator
├── run_gui.sh                  # 🚀 GUI Launch Script
│
├── AUDCAD15.csv                # 📁 Input: OHLCV Data (M15)
├── results.csv                 # 📄 Output: Full Results
├── quick_test_results.csv      # 📄 Output: Quick Test Results
│
├── requirements.txt            # 📦 Python Dependencies
├── .gitignore                  # 🚫 Git Ignore Rules
│
├── README.md                   # 📖 Documentation (English)
├── HUONG_DAN.md                # 📖 CLI Guide (Vietnamese)
├── HUONG_DAN_GUI.md            # 📖 GUI Guide (Vietnamese)
├── GUI_FEATURES.md             # 📖 GUI Features Overview
└── QUICK_START.txt             # 📖 Quick Reference
```

## 📈 Input Data Format

CSV file with the following columns:

```
Date, Time, Open, High, Low, Close, Volume
2024.01.01, 00:00, 0.89500, 0.89520, 0.89480, 0.89510, 150
```

The system automatically normalizes to:
```
timestamp, open, high, low, close, volume
```

## 🎯 Optimization Logic

### Scoring Function

```python
score = (
    profit * 1.0
    - abs(max_drawdown) * 0.7
    + winrate * 10
    - number_of_trades * 0.05
)
```

### Validation Criteria

Only parameter sets that meet these criteria are considered valid:
- `profit > 0`
- `max_drawdown < 30%` of peak equity

Results are ranked by score, not just profit, to ensure stability.

## 📊 Performance Metrics

For each parameter combination, the system calculates:

| Metric | Description |
|--------|-------------|
| **Total Profit** | Net profit in pips and currency |
| **Win Rate** | Percentage of winning trades |
| **Number of Trades** | Total trades executed |
| **Profit Factor** | Gross profit / Gross loss |
| **Max Drawdown** | Largest peak-to-trough decline |
| **Score** | Composite optimization score |

## 🔧 Customization

### Change Indicator Parameters

Edit `param_grid` in `backtest_optimizer.py`:

```python
param_grid = {
    'rsi_period': list(range(5, 31)),      # 5 to 30
    'overbought': list(range(65, 90, 5)),  # 65 to 85
    'oversold': list(range(15, 40, 5))     # 15 to 35
}
```

### Adjust Trading Parameters

```python
tp_pips = 20.0        # Take profit
sl_pips = 15.0        # Stop loss
spread_pips = 1.2     # Spread
lot_size = 0.1        # Position size
```

### Modify Scoring Function

Edit the `calculate_score()` function in `backtest_optimizer.py`:

```python
def calculate_score(metrics: Dict) -> float:
    profit = metrics['total_profit_pips']
    max_dd = abs(metrics['max_drawdown'])
    win_rate = metrics['win_rate']
    num_trades = metrics['num_trades']

    # Customize weights here
    score = (
        profit * 1.0
        - max_dd * 0.7
        + win_rate * 10
        - num_trades * 0.05
    )

    return score
```

## 🧪 System Validation

The backtesting engine ensures:

✅ **No Look-Ahead Bias**: Only uses data available at each candle
✅ **No Repainting**: Indicator values are fixed once calculated
✅ **Realistic Execution**: Accounts for spread on every trade
✅ **Proper Edge Cases**: Handles insufficient data gracefully

## 📤 Output Files

### Console Output
- Top 10 parameter sets ranked by score
- Best parameters highlighted
- Summary statistics

### results.csv
Complete results for all 650 parameter combinations with columns:
- `rsi_period`, `overbought`, `oversold`
- `total_profit_pips`, `total_profit_currency`
- `num_trades`, `win_rate`, `profit_factor`
- `max_drawdown`, `max_drawdown_pct`
- `score`, `valid`

## 🔮 Future Extensions

This system is designed to be easily extended to other indicators:

- **MACD**: Optimize fast/slow/signal periods
- **Bollinger Bands**: Optimize period and standard deviation
- **Moving Average Crossover**: Optimize fast/slow MA periods
- **Custom Indicators**: Add your own indicator functions

## 📝 Code Architecture

```python
load_data()              # Load and normalize CSV data
  ↓
compute_rsi()            # Calculate technical indicator
  ↓
backtest_strategy()      # Simulate trades candle-by-candle
  ↓
evaluate_metrics()       # Calculate performance metrics
  ↓
optimize_parameters()    # Grid search all combinations
  ↓
calculate_score()        # Rank by composite score
  ↓
print_top_results()      # Display top 10
save_results()           # Export to CSV
```

## ⚙️ Technical Details

- **Language**: Python 3.11+
- **Dependencies**: pandas, numpy (standard libraries only)
- **Framework**: No external backtesting frameworks
- **Code Quality**: Professional, modular, well-commented
- **Performance**: ~650 backtests in < 5 seconds

## 📊 Example Results

Best parameter set from sample data:

```
RSI Period: 18
Overbought: 85
Oversold: 25

Total Profit: 56.40 pips
Win Rate: 100.00%
Number of Trades: 3
Profit Factor: 56.40
Max Drawdown: 0.00%
Score: 1056.25
```

## ⚠️ Disclaimer

This system is for **educational and research purposes only**. Past performance does not guarantee future results. Always:

- Backtest on out-of-sample data
- Consider transaction costs and slippage
- Account for market conditions
- Use proper risk management
- Never risk more than you can afford to lose

## 📄 License

This project is provided as-is for quantitative trading research.

## 🤝 Contributing

Feel free to extend this system to other indicators and share your findings!

---

**Built with precision for quantitative trading research.**
