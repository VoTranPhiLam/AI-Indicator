"""
Backtesting & Optimization System for Trading Indicators
Author: Quantitative Trading Research Team
Description: Automated parameter optimization engine for technical indicators
"""

import pandas as pd
import numpy as np
from itertools import product
import math
from typing import Dict, List, Tuple, Optional


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_pip_value(symbol: str) -> float:
    """
    Get pip value based on symbol type.

    JPY pairs (USDJPY, EURJPY, etc.) use 3 digits: 1 pip = 0.01
    Other pairs use 5 digits: 1 pip = 0.0001

    Args:
        symbol: Trading symbol (e.g., 'EURUSD', 'USDJPY')

    Returns:
        Pip value (0.01 for JPY pairs, 0.0001 for others)
    """
    symbol_upper = symbol.upper()

    # Check if symbol contains JPY
    if 'JPY' in symbol_upper:
        return 0.01  # 3 digits: XXX.XX
    else:
        return 0.0001  # 5 digits: X.XXXXX


# ============================================================================
# DATA LOADING
# ============================================================================

def load_data(filepath: str, has_header: bool = None) -> pd.DataFrame:
    """
    Load and normalize OHLCV data from CSV file.

    Supports two formats:
    1. With header: Date,Time,Open,High,Low,Close,Volume
    2. Without header (auto-detect): First row is data

    Args:
        filepath: Path to CSV file
        has_header: True if CSV has header, False if not, None for auto-detect

    Returns:
        DataFrame with normalized columns: timestamp, open, high, low, close, volume
    """
    print(f"Loading data from {filepath}...")

    # Auto-detect header or use specified value
    if has_header is None:
        # Try to detect by reading first line
        with open(filepath, 'r') as f:
            first_line = f.readline().strip()
            # If first line contains 'Date' or 'Time', it's a header
            has_header = 'date' in first_line.lower() or 'time' in first_line.lower()

    # Read CSV with or without header
    if has_header:
        df = pd.read_csv(filepath, sep=None, engine='python')
        df.columns = df.columns.str.lower()
    else:
        # No header - define column names
        # Auto-detect separator (tab or comma)
        df = pd.read_csv(
            filepath,
            header=None,
            names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'],
            sep=None,
            engine='python'
        )

    # Drop any NaN columns that may have been added
    df = df.dropna(axis=1, how='all')

    # Combine Date and Time into timestamp
    if 'date' in df.columns and 'time' in df.columns:
        df['timestamp'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str))
        df = df.drop(['date', 'time'], axis=1)
    elif 'timestamp' not in df.columns:
        raise ValueError("CSV must contain either 'timestamp' or 'date'+'time' columns")

    # Ensure timestamp is datetime
    if df['timestamp'].dtype != 'datetime64[ns]':
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Sort by timestamp
    df = df.sort_values('timestamp').reset_index(drop=True)

    # Ensure required columns exist
    required_cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Select only required columns
    df = df[required_cols]

    print(f"Loaded {len(df)} candles from {df['timestamp'].min()} to {df['timestamp'].max()}")

    return df


# ============================================================================
# TECHNICAL INDICATORS
# ============================================================================

def compute_rsi(close_prices: pd.Series, period: int) -> pd.Series:
    """
    Calculate RSI (Relative Strength Index) indicator.

    Args:
        close_prices: Series of closing prices
        period: RSI period (e.g., 14)

    Returns:
        Series with RSI values (0-100)
    """
    # Calculate price changes
    delta = close_prices.diff()

    # Separate gains and losses
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    # Calculate average gain and loss using Wilder's smoothing (EMA)
    avg_gain = gain.ewm(com=period - 1, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period, adjust=False).mean()

    # Calculate RS and RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def compute_ichimoku(
    high: pd.Series,
    low: pd.Series,
    tenkan_period: int = 9,
    kijun_period: int = 26,
    senkou_b_period: int = 52
) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Calculate Ichimoku Kinko Hyo indicator.

    Args:
        high: Series of high prices
        low: Series of low prices
        tenkan_period: Tenkan-sen period (default 9)
        kijun_period: Kijun-sen period (default 26)
        senkou_b_period: Senkou Span B period (default 52)

    Returns:
        Tuple of (tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span)
    """
    # Tenkan-sen (Conversion Line): (highest high + lowest low) / 2 for tenkan_period
    tenkan_sen = (high.rolling(window=tenkan_period).max() +
                  low.rolling(window=tenkan_period).min()) / 2

    # Kijun-sen (Base Line): (highest high + lowest low) / 2 for kijun_period
    kijun_sen = (high.rolling(window=kijun_period).max() +
                 low.rolling(window=kijun_period).min()) / 2

    # Senkou Span A and B are NOT used for entry signals in EA_ICHIMOKU_MT4.mq4
    # They are only for cloud visualization
    # We keep them for completeness but don't shift to avoid NaN issues
    senkou_span_a = (tenkan_sen + kijun_sen) / 2
    senkou_span_b = (high.rolling(window=senkou_b_period).max() +
                     low.rolling(window=senkou_b_period).min()) / 2

    # Chikou Span (Lagging Span): Not used in this strategy
    chikou_span = pd.Series(index=high.index, dtype=float)

    return tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span


def find_swing_low(low: pd.Series, current_index: int, bars_to_check: int = 5) -> float:
    """
    Find the lowest low in recent candles (swing low for SL calculation).

    Args:
        low: Series of low prices
        current_index: Current candle index
        bars_to_check: Number of bars to check for swing low

    Returns:
        Swing low price
    """
    if current_index < 1:
        return low.iloc[current_index] if current_index >= 0 else 0.0

    start_idx = max(1, current_index - bars_to_check + 1)
    end_idx = current_index + 1

    # Find the lowest low in the range
    swing_low = low.iloc[start_idx:end_idx].min()

    return swing_low


def find_swing_high(high: pd.Series, current_index: int, bars_to_check: int = 5) -> float:
    """
    Find the highest high in recent candles (swing high for SL calculation).

    Args:
        high: Series of high prices
        current_index: Current candle index
        bars_to_check: Number of bars to check for swing high

    Returns:
        Swing high price
    """
    if current_index < 1:
        return high.iloc[current_index] if current_index >= 0 else 0.0

    start_idx = max(1, current_index - bars_to_check + 1)
    end_idx = current_index + 1

    # Find the highest high in the range
    swing_high = high.iloc[start_idx:end_idx].max()

    return swing_high


# ============================================================================
# BACKTESTING ENGINE
# ============================================================================

def backtest_strategy(
    data: pd.DataFrame,
    tenkan_period: int = 9,
    kijun_period: int = 26,
    senkou_b_period: int = 52,
    rsi_period: int = 14,
    rsi_buy_threshold: float = 50.0,
    rsi_sell_threshold: float = 50.0,
    risk_reward_ratio: float = 1.2,
    sl_buffer_pips: float = 3.0,
    bars_check_swing: int = 5,
    spread_pips: float = 1.2,
    lot_size: float = 0.01,
    symbol: str = "EURUSD"  # Used to detect JPY pairs for pip_value
) -> Dict:
    """
    Backtest Ichimoku + RSI Filter strategy on given data.

    Trading Rules (Based on EA_ICHIMOKU_MT4.mq4):
    - BUY when: Tenkan crosses ABOVE Kijun AND RSI >= rsi_buy_threshold
    - SELL when: Tenkan crosses BELOW Kijun AND RSI <= rsi_sell_threshold
    - SL: Swing Low/High + buffer
    - TP: Risk:Reward ratio (default 1:1.2)
    - One position at a time

    Args:
        data: DataFrame with OHLCV data
        tenkan_period: Tenkan-sen period (default 9)
        kijun_period: Kijun-sen period (default 26)
        senkou_b_period: Senkou Span B period (default 52)
        rsi_period: RSI period for trend filter (default 14)
        rsi_buy_threshold: RSI must be >= this for BUY (default 50)
        rsi_sell_threshold: RSI must be <= this for SELL (default 50)
        risk_reward_ratio: TP/SL ratio (default 1.2)
        sl_buffer_pips: Buffer distance from swing high/low (default 3.0 pips)
        bars_check_swing: Number of bars to check for swing high/low (default 5)
        spread_pips: Spread in pips
        lot_size: Position size
        symbol: Trading symbol (used to detect JPY pairs for pip value)

    Returns:
        Dictionary with backtest results
    """
    # Auto-detect pip value based on symbol (JPY pairs use 0.01, others use 0.0001)
    pip_value = get_pip_value(symbol)

    # Calculate Ichimoku
    data = data.copy()
    data['tenkan'], data['kijun'], data['senkou_a'], data['senkou_b'], data['chikou'] = compute_ichimoku(
        data['high'], data['low'], tenkan_period, kijun_period, senkou_b_period
    )

    # Calculate RSI for trend filter
    data['rsi'] = compute_rsi(data['close'], rsi_period)

    # Drop NaN values ONLY from columns we actually use for entry signals
    # Don't drop based on senkou_a, senkou_b, chikou since they're not used
    data = data.dropna(subset=['tenkan', 'kijun', 'rsi']).reset_index(drop=True)

    if len(data) < max(tenkan_period, kijun_period, senkou_b_period, rsi_period) + 10:
        # Not enough data for meaningful backtest
        return {
            'trades': [],
            'equity_curve': [1000.0],  # Starting equity
            'total_profit_pips': 0.0,
            'total_profit_currency': 0.0,
            'num_trades': 0,
            'win_rate': 0.0,
            'profit_factor': 0.0,
            'max_drawdown': 0.0,
            'max_drawdown_pct': 0.0
        }

    # Initialize trading state
    position = None  # None, 'long', or 'short'
    entry_price = 0.0
    stop_loss = 0.0
    take_profit = 0.0
    entry_index = 0
    trades = []
    equity = 1000.0  # Starting equity in currency units
    equity_curve = [equity]

    # Convert spread to price
    spread_price = spread_pips * pip_value
    sl_buffer = sl_buffer_pips * pip_value

    # Simulate trading candle by candle
    for i in range(1, len(data)):  # Start from 1 to check previous candle
        current_candle = data.iloc[i]
        prev_candle = data.iloc[i - 1]

        # Get current indicator values
        tenkan_current = current_candle['tenkan']
        kijun_current = current_candle['kijun']
        tenkan_prev = prev_candle['tenkan']
        kijun_prev = prev_candle['kijun']
        rsi_current = current_candle['rsi']

        # Check if we have an open position
        if position is not None:
            # Check for exit conditions
            exit_triggered = False
            exit_price = 0.0
            exit_reason = ''

            if position == 'long':
                # Check TP/SL for long position
                if current_candle['high'] >= take_profit:
                    exit_triggered = True
                    exit_price = take_profit
                    exit_reason = 'TP'
                elif current_candle['low'] <= stop_loss:
                    exit_triggered = True
                    exit_price = stop_loss
                    exit_reason = 'SL'

            elif position == 'short':
                # Check TP/SL for short position
                if current_candle['low'] <= take_profit:
                    exit_triggered = True
                    exit_price = take_profit
                    exit_reason = 'TP'
                elif current_candle['high'] >= stop_loss:
                    exit_triggered = True
                    exit_price = stop_loss
                    exit_reason = 'SL'

            if exit_triggered:
                # Close position
                if position == 'long':
                    profit_pips = (exit_price - entry_price) / pip_value
                else:  # short
                    profit_pips = (entry_price - exit_price) / pip_value

                # Account for spread (paid on entry)
                profit_pips -= spread_pips

                # Convert to currency
                profit_currency = profit_pips * pip_value * lot_size * 100000  # 100k per lot

                # Update equity
                equity += profit_currency
                equity_curve.append(equity)

                # Record trade
                trades.append({
                    'entry_index': entry_index,
                    'exit_index': i,
                    'entry_timestamp': data.iloc[entry_index]['timestamp'],
                    'exit_timestamp': current_candle['timestamp'],
                    'type': position,
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'profit_pips': profit_pips,
                    'profit_currency': profit_currency,
                    'exit_reason': exit_reason
                })

                # Clear position
                position = None

        # Check for entry signals (only if no position)
        if position is None and not math.isnan(tenkan_current) and not math.isnan(kijun_current) and not math.isnan(rsi_current):

            # BUY SIGNAL: Tenkan crosses ABOVE Kijun AND RSI >= threshold
            if tenkan_current > kijun_current and tenkan_prev <= kijun_prev and rsi_current >= rsi_buy_threshold:
                position = 'long'

                # Entry price: Ask price (close + spread)
                entry_price = current_candle['close'] + spread_price
                entry_index = i

                # Calculate SL: Swing Low - buffer
                swing_low = find_swing_low(data['low'], i, bars_check_swing)
                stop_loss = swing_low - sl_buffer

                # Calculate TP: Entry + (Risk * RR_Ratio)
                sl_distance = entry_price - stop_loss
                take_profit = entry_price + (sl_distance * risk_reward_ratio)

            # SELL SIGNAL: Tenkan crosses BELOW Kijun AND RSI <= threshold
            elif tenkan_current < kijun_current and tenkan_prev >= kijun_prev and rsi_current <= rsi_sell_threshold:
                position = 'short'

                # Entry price: Bid price (close - spread)
                entry_price = current_candle['close'] - spread_price
                entry_index = i

                # Calculate SL: Swing High + buffer
                swing_high = find_swing_high(data['high'], i, bars_check_swing)
                stop_loss = swing_high + sl_buffer

                # Calculate TP: Entry - (Risk * RR_Ratio)
                sl_distance = stop_loss - entry_price
                take_profit = entry_price - (sl_distance * risk_reward_ratio)

    # Close any remaining open position at the last candle
    if position is not None:
        current_candle = data.iloc[-1]
        exit_price = current_candle['close']

        if position == 'long':
            profit_pips = (exit_price - entry_price) / pip_value - spread_pips
        else:
            profit_pips = (entry_price - exit_price) / pip_value - spread_pips

        profit_currency = profit_pips * pip_value * lot_size * 100000
        equity += profit_currency
        equity_curve.append(equity)

        trades.append({
            'entry_index': entry_index,
            'exit_index': len(data) - 1,
            'entry_timestamp': data.iloc[entry_index]['timestamp'],
            'exit_timestamp': current_candle['timestamp'],
            'type': position,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'profit_pips': profit_pips,
            'profit_currency': profit_currency,
            'exit_reason': 'EOD'
        })

    # Calculate metrics
    metrics = evaluate_metrics(trades, equity_curve)

    return {
        'trades': trades,
        'equity_curve': equity_curve,
        **metrics
    }


# ============================================================================
# PERFORMANCE METRICS
# ============================================================================

def evaluate_metrics(trades: List[Dict], equity_curve: List[float]) -> Dict:
    """
    Calculate performance metrics from trades and equity curve.

    Args:
        trades: List of trade dictionaries
        equity_curve: List of equity values over time

    Returns:
        Dictionary with performance metrics
    """
    if len(trades) == 0:
        return {
            'total_profit_pips': 0.0,
            'total_profit_currency': 0.0,
            'num_trades': 0,
            'win_rate': 0.0,
            'profit_factor': 0.0,
            'max_drawdown': 0.0,
            'max_drawdown_pct': 0.0
        }

    # Total profit
    total_profit_pips = sum(t['profit_pips'] for t in trades)
    total_profit_currency = sum(t['profit_currency'] for t in trades)

    # Number of trades
    num_trades = len(trades)

    # Win rate
    winning_trades = [t for t in trades if t['profit_pips'] > 0]
    win_rate = len(winning_trades) / num_trades if num_trades > 0 else 0.0

    # Profit factor
    gross_profit = sum(t['profit_pips'] for t in trades if t['profit_pips'] > 0)
    gross_loss = abs(sum(t['profit_pips'] for t in trades if t['profit_pips'] < 0))
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else (gross_profit if gross_profit > 0 else 0.0)

    # Maximum drawdown
    if len(equity_curve) > 1:
        peak = equity_curve[0]
        max_drawdown = 0.0
        max_drawdown_pct = 0.0

        for equity in equity_curve:
            if equity > peak:
                peak = equity
            drawdown = peak - equity
            drawdown_pct = (drawdown / peak * 100) if peak > 0 else 0.0

            if drawdown > max_drawdown:
                max_drawdown = drawdown
                max_drawdown_pct = drawdown_pct
    else:
        max_drawdown = 0.0
        max_drawdown_pct = 0.0

    return {
        'total_profit_pips': total_profit_pips,
        'total_profit_currency': total_profit_currency,
        'num_trades': num_trades,
        'win_rate': win_rate * 100,  # Convert to percentage
        'profit_factor': profit_factor,
        'max_drawdown': max_drawdown,
        'max_drawdown_pct': max_drawdown_pct
    }


# ============================================================================
# OPTIMIZATION ENGINE
# ============================================================================

def calculate_score(metrics: Dict) -> float:
    """
    Calculate optimization score based on multiple metrics.

    Score formula:
    score = profit * 1.0 - abs(max_drawdown) * 0.7 + winrate * 10 - number_of_trades * 0.05

    Args:
        metrics: Dictionary with performance metrics

    Returns:
        Score value (higher is better)
    """
    profit = metrics['total_profit_pips']
    max_dd = abs(metrics['max_drawdown'])
    win_rate = metrics['win_rate']
    num_trades = metrics['num_trades']

    score = (
        profit * 1.0
        - max_dd * 0.7
        + win_rate * 10
        - num_trades * 0.05
    )

    return score


def is_valid_result(metrics: Dict) -> bool:
    """
    Check if result meets minimum quality criteria.

    Criteria:
    - profit > 0
    - max_drawdown < 30% of peak equity

    Args:
        metrics: Dictionary with performance metrics

    Returns:
        True if result is valid, False otherwise
    """
    if metrics['total_profit_pips'] <= 0:
        return False

    if metrics['max_drawdown_pct'] >= 30.0:
        return False

    return True


def optimize_parameters(
    data: pd.DataFrame,
    param_grid: Dict,
    tp_pips: float,
    sl_pips: float,
    spread_pips: float,
    lot_size: float
) -> Tuple[List[Dict], pd.DataFrame]:
    """
    Test all parameter combinations and find the best.

    Args:
        data: DataFrame with OHLCV data
        param_grid: Dictionary with parameter ranges
        tp_pips: Take profit in pips
        sl_pips: Stop loss in pips
        spread_pips: Spread in pips
        lot_size: Position size

    Returns:
        Tuple of (results_list, results_dataframe)
    """
    print("\n" + "="*80)
    print("STARTING PARAMETER OPTIMIZATION")
    print("="*80)

    # Generate all parameter combinations
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())
    combinations = list(product(*param_values))

    total_combinations = len(combinations)
    print(f"\nTotal parameter combinations to test: {total_combinations}")
    print(f"Parameter ranges:")
    for name, values in param_grid.items():
        print(f"  {name}: {min(values)} to {max(values)} ({len(values)} values)")
    print()

    results = []

    # Test each combination
    for idx, combo in enumerate(combinations):
        # Create parameter dictionary
        params = dict(zip(param_names, combo))

        # Progress indicator
        if (idx + 1) % 50 == 0 or idx == 0:
            print(f"Progress: {idx + 1}/{total_combinations} ({(idx + 1) / total_combinations * 100:.1f}%)")

        # Run backtest
        backtest_result = backtest_strategy(
            data=data,
            rsi_period=params['rsi_period'],
            overbought=params['overbought'],
            oversold=params['oversold'],
            tp_pips=tp_pips,
            sl_pips=sl_pips,
            spread_pips=spread_pips,
            lot_size=lot_size
        )

        # Calculate score
        score = calculate_score(backtest_result)
        valid = is_valid_result(backtest_result)

        # Store result
        result = {
            'rsi_period': params['rsi_period'],
            'overbought': params['overbought'],
            'oversold': params['oversold'],
            'total_profit_pips': backtest_result['total_profit_pips'],
            'total_profit_currency': backtest_result['total_profit_currency'],
            'num_trades': backtest_result['num_trades'],
            'win_rate': backtest_result['win_rate'],
            'profit_factor': backtest_result['profit_factor'],
            'max_drawdown': backtest_result['max_drawdown'],
            'max_drawdown_pct': backtest_result['max_drawdown_pct'],
            'score': score,
            'valid': valid
        }

        results.append(result)

    print(f"\nCompleted: {total_combinations}/{total_combinations} (100.0%)")

    # Convert to DataFrame
    results_df = pd.DataFrame(results)

    # Sort by score (descending)
    results_df = results_df.sort_values('score', ascending=False).reset_index(drop=True)

    return results, results_df


# ============================================================================
# OUTPUT & REPORTING
# ============================================================================

def print_top_results(results_df: pd.DataFrame, top_n: int = 10):
    """
    Print top N parameter sets ranked by score.

    Args:
        results_df: DataFrame with all results
        top_n: Number of top results to display
    """
    print("\n" + "="*80)
    print(f"TOP {top_n} PARAMETER SETS (Ranked by Score)")
    print("="*80)

    # Filter valid results only
    valid_results = results_df[results_df['valid'] == True]

    if len(valid_results) == 0:
        print("\n⚠ WARNING: No valid results found!")
        print("  All parameter combinations either had:")
        print("  - Negative profit, OR")
        print("  - Max drawdown >= 30%")
        print("\nShowing top results without validation filter:")
        valid_results = results_df

    top_results = valid_results.head(top_n)

    for rank, (idx, row) in enumerate(top_results.iterrows(), 1):
        print(f"\n{'─'*80}")
        print(f"Rank #{rank} {' ★ BEST PARAMETERS ★' if rank == 1 else ''}")
        print(f"{'─'*80}")
        print(f"Parameters:")
        print(f"  RSI Period:   {row['rsi_period']}")
        print(f"  Overbought:   {row['overbought']}")
        print(f"  Oversold:     {row['oversold']}")
        print(f"\nPerformance:")
        print(f"  Total Profit:   {row['total_profit_pips']:>10.2f} pips")
        print(f"  Profit ($):     {row['total_profit_currency']:>10.2f}")
        print(f"  Number Trades:  {row['num_trades']:>10.0f}")
        print(f"  Win Rate:       {row['win_rate']:>10.2f}%")
        print(f"  Profit Factor:  {row['profit_factor']:>10.2f}")
        print(f"  Max Drawdown:   {row['max_drawdown']:>10.2f} ({row['max_drawdown_pct']:.2f}%)")
        print(f"  SCORE:          {row['score']:>10.2f}")


def save_results(results_df: pd.DataFrame, filepath: str = 'results.csv'):
    """
    Save all results to CSV file.

    Args:
        results_df: DataFrame with all results
        filepath: Output CSV file path
    """
    results_df.to_csv(filepath, index=False)
    print(f"\n{'='*80}")
    print(f"All results saved to: {filepath}")
    print(f"Total results: {len(results_df)}")
    print(f"Valid results: {len(results_df[results_df['valid'] == True])}")
    print(f"{'='*80}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution function.
    """
    print("\n" + "="*80)
    print(" BACKTESTING & OPTIMIZATION SYSTEM")
    print(" Technical Indicator Parameter Optimizer")
    print("="*80)

    # ========================================================================
    # CONFIGURATION
    # ========================================================================

    # Data file
    data_file = 'AUDCAD15.csv'

    # RSI parameter grid
    param_grid = {
        'rsi_period': list(range(5, 31)),  # 5 to 30, step 1
        'overbought': list(range(65, 90, 5)),  # 65 to 85, step 5
        'oversold': list(range(15, 40, 5))  # 15 to 35, step 5
    }

    # Trading parameters
    tp_pips = 20.0
    sl_pips = 15.0
    spread_pips = 1.2
    lot_size = 0.1

    # Output file
    results_file = 'results.csv'

    print("\nConfiguration:")
    print(f"  Data file:      {data_file}")
    print(f"  Take Profit:    {tp_pips} pips")
    print(f"  Stop Loss:      {sl_pips} pips")
    print(f"  Spread:         {spread_pips} pips")
    print(f"  Lot Size:       {lot_size}")
    print(f"  Results file:   {results_file}")

    # ========================================================================
    # LOAD DATA
    # ========================================================================

    try:
        data = load_data(data_file)
    except FileNotFoundError:
        print(f"\n❌ ERROR: File '{data_file}' not found!")
        print("Please ensure the CSV file is in the current directory.")
        return
    except Exception as e:
        print(f"\n❌ ERROR loading data: {e}")
        return

    # ========================================================================
    # OPTIMIZE PARAMETERS
    # ========================================================================

    try:
        results_list, results_df = optimize_parameters(
            data=data,
            param_grid=param_grid,
            tp_pips=tp_pips,
            sl_pips=sl_pips,
            spread_pips=spread_pips,
            lot_size=lot_size
        )
    except Exception as e:
        print(f"\n❌ ERROR during optimization: {e}")
        import traceback
        traceback.print_exc()
        return

    # ========================================================================
    # DISPLAY RESULTS
    # ========================================================================

    print_top_results(results_df, top_n=10)

    # ========================================================================
    # SAVE RESULTS
    # ========================================================================

    save_results(results_df, results_file)

    # ========================================================================
    # SUMMARY
    # ========================================================================

    print("\n" + "="*80)
    print(" OPTIMIZATION COMPLETE")
    print("="*80)

    valid_count = len(results_df[results_df['valid'] == True])
    if valid_count > 0:
        best = results_df[results_df['valid'] == True].iloc[0]
        print(f"\n✓ Best parameters found:")
        print(f"  RSI Period: {best['rsi_period']}, Overbought: {best['overbought']}, Oversold: {best['oversold']}")
        print(f"  Expected Profit: {best['total_profit_pips']:.2f} pips ({best['total_profit_currency']:.2f} $)")
        print(f"  Score: {best['score']:.2f}")
    else:
        print("\n⚠ No valid parameter combinations found.")
        print("  Consider adjusting:")
        print("  - Parameter ranges")
        print("  - TP/SL levels")
        print("  - Validation criteria")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
