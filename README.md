# AI-Indicator: Backtesting & Optimization System

A professional-grade Python backtesting and parameter optimization engine for technical trading indicators.

## 🎯 Overview

This system automatically tests technical indicators with all parameter combinations and finds the parameter set that yields the **BEST and MOST STABLE profit** through systematic grid search optimization.

**Note**: This is NOT a price prediction AI. This is an indicator parameter optimization engine for quantitative trading research.

## ✨ Features

### Core Features
- **Complete Backtesting Engine**: Candle-by-candle simulation with no look-ahead bias
- **Grid Search Optimization**: Tests all combinations of indicator parameters
- **Multi-Metric Evaluation**: Profit, win rate, max drawdown, profit factor
- **Smart Scoring Function**: Balances profitability with stability
- **Modular Architecture**: Easy to extend to other indicators

### NEW: Multi-Symbol Multi-Timeframe Support
- **Batch Processing**: Test multiple symbols and timeframes simultaneously
- **CSV Folder Scanning**: Automatically detect and parse CSV files
- **No Header Required**: Works with real MT4/MT5 CSV exports
- **Comparison Charts**: Compare results across symbols and timeframes
- **Unified Results**: Single CSV export with all test results

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

### Three Ways to Use

#### Option 1: 🌐 **Multi-Symbol GUI (NEW - Recommended!)**

Test multiple symbols and timeframes simultaneously!

```bash
# Install dependencies
pip install -r requirements.txt

# Generate sample files (or use your own)
python generate_multi_csv.py

# Launch Multi-Symbol GUI
streamlit run gui_app_multi.py
```

**Features:**
- ✅ **Batch processing**: Test 10+ files at once
- ✅ **Auto-scan CSV folder**: Detects all files automatically
- ✅ **Multiple symbols**: AUDUSD, EURUSD, GBPUSD, USDJPY, etc.
- ✅ **Multiple timeframes**: M5, M15, M30, H1, H4, D1
- ✅ **No header required**: Works with MT4/MT5 CSV format
- ✅ **Comparison charts**: Compare performance across symbols/timeframes

📖 **See [HUONG_DAN_MULTI_GUI.md](HUONG_DAN_MULTI_GUI.md) for complete guide (Vietnamese)**

---

#### Option 2: 🖥️ **Single-File GUI (For Individual Testing)**

Beautiful web interface for testing one file at a time!

```bash
# Launch Single-File GUI
streamlit run gui_app.py
```

**Features:**
- ✅ Visual parameter configuration with sliders
- ✅ Real-time progress tracking
- ✅ Interactive charts (Bar, Scatter, Heatmap)
- ✅ One-click CSV download

📖 **See [HUONG_DAN_GUI.md](HUONG_DAN_GUI.md) for detailed GUI guide (Vietnamese)**

---

#### Option 3: 💻 **Command Line (For Automation)**

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
├── 🌐 Multi-Symbol GUI (NEW!)
│   ├── gui_app_multi.py           # Multi-Symbol GUI Application
│   ├── run_multi_gui.bat          # Windows Launcher (Multi)
│   ├── generate_multi_csv.py      # Generate Sample Multi-Files
│   └── HUONG_DAN_MULTI_GUI.md     # Multi-GUI Guide (Vietnamese)
│
├── 🖥️ Single-File GUI
│   ├── gui_app.py                 # Single-File GUI Application
│   ├── run_gui.bat                # Windows Launcher (Single)
│   ├── run_gui.sh                 # Linux/Mac Launcher
│   ├── HUONG_DAN_GUI.md           # GUI Guide (Vietnamese)
│   └── GUI_FEATURES.md            # GUI Features Overview
│
├── 💻 CLI Applications
│   ├── backtest_optimizer.py      # Full Optimizer (650 tests)
│   ├── quick_test.py              # Quick Test (16 tests)
│   ├── generate_sample_data.py    # Single-File Data Generator
│   ├── HUONG_DAN.md               # CLI Guide (Vietnamese)
│   └── QUICK_START.txt            # Quick Reference
│
├── 📁 Data & Results
│   ├── CSV/                       # Folder for multi-symbol CSVs
│   │   ├── AUDUSD5.csv           # AUDUSD M5 data
│   │   ├── AUDUSD15.csv          # AUDUSD M15 data
│   │   ├── EURUSD5.csv           # EURUSD M5 data
│   │   └── ...                    # More symbol/timeframe files
│   ├── AUDCAD15.csv               # Single-file test data
│   ├── results.csv                # CLI full results
│   └── quick_test_results.csv     # CLI quick results
│
├── 📦 Configuration
│   ├── requirements.txt           # Python Dependencies
│   ├── .gitignore                 # Git Ignore Rules
│   └── CACH_CHAY_GUI.txt         # How to Run GUI (Vietnamese)
│
└── 📖 Documentation
    ├── README.md                  # Main Documentation (English)
    ├── HUONG_DAN.md               # CLI Guide (Vietnamese)
    ├── HUONG_DAN_GUI.md           # Single-GUI Guide (Vietnamese)
    ├── HUONG_DAN_MULTI_GUI.md     # Multi-GUI Guide (Vietnamese)
    ├── GUI_FEATURES.md            # GUI Features Overview
    ├── QUICK_START.txt            # Quick Reference
    └── CACH_CHAY_GUI.txt          # Running Instructions
```

## 📈 Input Data Format

### Format 1: With Header (Original)

```csv
Date,Time,Open,High,Low,Close,Volume
2024.01.01,00:00,0.89500,0.89520,0.89480,0.89510,150
2024.01.01,00:15,0.89510,0.89530,0.89490,0.89520,200
```

### Format 2: Without Header (NEW - MT4/MT5)

```
2025.12.19	3:00	0.66423	0.6643	0.66399	0.6642	156
2025.12.19	3:05	0.66421	0.66426	0.66377	0.66378	178
2025.12.19	3:10	0.66377	0.66386	0.66362	0.66385	159
```

**Features:**
- ✅ Auto-detects header presence
- ✅ Supports tab or space separation
- ✅ Works with real MT4/MT5 CSV exports
- ✅ No manual conversion needed

**File Naming for Multi-Symbol:**
- Format: `SYMBOL` + `MINUTES` + `.csv`
- Examples:
  - `AUDUSD5.csv` → AUDUSD M5 (5 minutes)
  - `EURUSD15.csv` → EURUSD M15 (15 minutes)
  - `GBPUSD30.csv` → GBPUSD M30 (30 minutes)
  - `USDJPY60.csv` → USDJPY H1 (60 minutes)
  - `AUDUSD1440.csv` → AUDUSD D1 (1440 minutes)

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
