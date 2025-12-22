#!/usr/bin/env python3
"""
Test winning/losing trades statistics display
"""

import pandas as pd
from backtest_optimizer import backtest_strategy

# Load test data
print("=" * 80)
print("TEST: WINNING/LOSING TRADES STATISTICS")
print("=" * 80)

# Read sample CSV file
csv_file = "AUDCAD15.csv"  # Use existing test file

try:
    data = pd.read_csv(csv_file)

    # Handle different CSV formats
    if 'Date' in data.columns and 'Time' in data.columns:
        # Format: Date,Time,Open,High,Low,Close,Volume
        data['timestamp'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
        data = data.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'})
        data = data[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    elif 'timestamp' not in data.columns:
        # Format: tab-separated without header
        data.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        data['timestamp'] = pd.to_datetime(data['timestamp'])

    print(f"\n✅ Loaded {len(data)} candles from {csv_file}")

    # Run backtest with default parameters
    print("\n" + "=" * 80)
    print("Running backtest with Ichimoku strategy...")
    print("=" * 80)

    result = backtest_strategy(
        data=data,
        tenkan_period=9,
        kijun_period=26,
        senkou_b_period=52,
        rsi_period=14,
        rsi_buy_threshold=50.0,
        rsi_sell_threshold=50.0,
        risk_reward_ratio=1.2,
        sl_buffer_pips=3.0,
        bars_check_swing=5,
        spread_pips=1.2,
        lot_size=0.01,
        symbol="AUDCAD"
    )

    print("\n" + "=" * 80)
    print("BACKTEST RESULTS")
    print("=" * 80)

    # Display basic stats
    print(f"\n📊 Trading Statistics:")
    print(f"   Total Trades:          {result['num_trades']}")
    print(f"   Winning Trades:        {result['num_winning_trades']} ✅")
    print(f"   Losing Trades:         {result['num_losing_trades']} ❌")
    print(f"   Win Rate:              {result['win_rate']:.2f}%")

    # Display profit breakdown
    print(f"\n💰 Profit Breakdown:")
    print(f"   Total Winning Profit:  +{result['total_winning_profit_pips']:.2f} pips (${result['total_winning_profit_currency']:.2f})")
    print(f"   Total Losing Profit:   {result['total_losing_profit_pips']:.2f} pips (${result['total_losing_profit_currency']:.2f})")
    print(f"   Final Profit:          {result['total_profit_pips']:.2f} pips (${result['total_profit_currency']:.2f})")

    # Display other metrics
    print(f"\n📈 Other Metrics:")
    print(f"   Profit Factor:         {result['profit_factor']:.2f}")
    print(f"   Max Drawdown:          {result['max_drawdown_pct']:.2f}%")

    # Verify calculations
    print("\n" + "=" * 80)
    print("VERIFICATION")
    print("=" * 80)

    # Check: num_winning_trades + num_losing_trades should equal num_trades (or close to it, accounting for breakeven trades)
    total_w_l = result['num_winning_trades'] + result['num_losing_trades']
    print(f"\n✓ Winning + Losing = {total_w_l} (Total = {result['num_trades']})")

    if total_w_l <= result['num_trades']:
        print(f"  ✅ Correct! (Difference = {result['num_trades'] - total_w_l} breakeven trades)")
    else:
        print(f"  ❌ ERROR: Sum exceeds total trades!")

    # Check: total_winning_profit + total_losing_profit should equal total_profit
    calc_total = result['total_winning_profit_pips'] + result['total_losing_profit_pips']
    print(f"\n✓ Winning Profit + Losing Profit = {calc_total:.2f} pips")
    print(f"  Total Profit = {result['total_profit_pips']:.2f} pips")

    if abs(calc_total - result['total_profit_pips']) < 0.01:
        print(f"  ✅ Correct! Match!")
    else:
        print(f"  ❌ ERROR: Mismatch! Difference = {abs(calc_total - result['total_profit_pips']):.2f} pips")

    # Display sample trades
    print("\n" + "=" * 80)
    print("SAMPLE TRADES")
    print("=" * 80)

    if len(result['trades']) > 0:
        # Show first 3 winning trades
        winning_trades = [t for t in result['trades'] if t['profit_pips'] > 0][:3]
        if winning_trades:
            print("\n✅ Sample Winning Trades:")
            for i, trade in enumerate(winning_trades, 1):
                print(f"   {i}. {trade['type'].upper()}: {trade['profit_pips']:.2f} pips (${trade['profit_currency']:.2f})")

        # Show first 3 losing trades
        losing_trades = [t for t in result['trades'] if t['profit_pips'] < 0][:3]
        if losing_trades:
            print("\n❌ Sample Losing Trades:")
            for i, trade in enumerate(losing_trades, 1):
                print(f"   {i}. {trade['type'].upper()}: {trade['profit_pips']:.2f} pips (${trade['profit_currency']:.2f})")

    print("\n" + "=" * 80)
    print("✅ TEST COMPLETED SUCCESSFULLY!")
    print("=" * 80)

except FileNotFoundError:
    print(f"\n❌ File not found: {csv_file}")
    print("Please make sure you have CSV data files in the 'data/' directory.")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
