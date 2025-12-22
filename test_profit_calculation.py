#!/usr/bin/env python3
"""
Test profit calculation to verify lot size and profit accuracy
"""

# Test profit calculation formula
print("=" * 80)
print("TEST: PROFIT CALCULATION VERIFICATION")
print("=" * 80)

# Standard Forex calculation
print("\n📊 STANDARD FOREX PROFIT CALCULATION:")
print("-" * 80)

# Example 1: EURUSD with 0.01 lot
print("\n1️⃣ EURUSD - 0.01 lot - 10 pips profit:")
profit_pips = 10.0
pip_value = 0.0001  # 5 digits
lot_size = 0.01
contract_size = 100000

# Current formula in code
profit_currency = profit_pips * pip_value * lot_size * contract_size
print(f"   Formula: {profit_pips} pips × {pip_value} × {lot_size} lot × {contract_size}")
print(f"   Calculation: {profit_pips} × {pip_value} × {lot_size} × {contract_size} = ${profit_currency:.2f}")

# Expected calculation
# For EURUSD: 1 pip on 0.01 lot = $0.10
# 10 pips × $0.10 = $1.00
expected = 10.0 * 0.10
print(f"   Expected: 10 pips × $0.10/pip = ${expected:.2f}")
print(f"   ✅ MATCH!" if abs(profit_currency - expected) < 0.01 else f"   ❌ MISMATCH!")

# Example 2: Large profit scenario
print("\n2️⃣ What would cause $7000 profit with 0.01 lot?")
target_profit = 7000.0
required_pips = target_profit / (pip_value * lot_size * contract_size)
print(f"   To get ${target_profit:.2f} profit with 0.01 lot:")
print(f"   Required pips = ${target_profit} / ({pip_value} × {lot_size} × {contract_size})")
print(f"   Required pips = ${target_profit} / {pip_value * lot_size * contract_size:.4f}")
print(f"   Required pips = {required_pips:.2f} pips")
print(f"   This is {required_pips/100:.2f}% price movement! ⚠️")

# Example 3: JPY pairs
print("\n3️⃣ USDJPY - 0.01 lot - 10 pips profit:")
profit_pips_jpy = 10.0
pip_value_jpy = 0.01  # 3 digits
lot_size_jpy = 0.01

profit_currency_jpy = profit_pips_jpy * pip_value_jpy * lot_size_jpy * contract_size
print(f"   Formula: {profit_pips_jpy} pips × {pip_value_jpy} × {lot_size_jpy} lot × {contract_size}")
print(f"   Result: ${profit_currency_jpy:.2f}")

# For USDJPY: 1 pip on 0.01 lot ≈ $0.10 (if USDJPY at 110.00)
# But this is simplified - actual value depends on current exchange rate
print(f"   Note: JPY pair profit depends on current exchange rate")

print("\n" + "=" * 80)
print("TESTING WITH REAL BACKTEST DATA")
print("=" * 80)

import pandas as pd
from backtest_optimizer import backtest_strategy, get_pip_value

# Load a small CSV file
csv_file = "AUDCAD15.csv"

try:
    data = pd.read_csv(csv_file)

    if 'Date' in data.columns and 'Time' in data.columns:
        data['timestamp'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
        data = data.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'})
        data = data[['timestamp', 'open', 'high', 'low', 'close', 'volume']]

    print(f"\n✅ Loaded {len(data)} candles from {csv_file}")

    # Run backtest with 0.01 lot
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

    print("\n📊 Backtest Results:")
    print(f"   Total Trades: {result['num_trades']}")
    print(f"   Winning Trades: {result['num_winning_trades']}")
    print(f"   Losing Trades: {result['num_losing_trades']}")
    print(f"   Total Winning Profit: ${result['total_winning_profit_currency']:.2f} ({result['total_winning_profit_pips']:.2f} pips)")
    print(f"   Total Losing Profit: ${result['total_losing_profit_currency']:.2f} ({result['total_losing_profit_pips']:.2f} pips)")
    print(f"   Final Profit: ${result['total_profit_currency']:.2f} ({result['total_profit_pips']:.2f} pips)")

    # Analyze individual trades
    print("\n" + "=" * 80)
    print("INDIVIDUAL TRADE ANALYSIS")
    print("=" * 80)

    if len(result['trades']) > 0:
        print(f"\nTotal trades: {len(result['trades'])}")

        # Show first 5 trades with detailed calculation
        print("\n🔍 First 5 Trades (Detailed):")
        for i, trade in enumerate(result['trades'][:5], 1):
            profit_pips = trade['profit_pips']
            profit_currency = trade['profit_currency']

            # Verify calculation
            pip_val = get_pip_value("AUDCAD")
            calculated_profit = profit_pips * pip_val * 0.01 * 100000

            print(f"\n   Trade #{i} ({trade['type'].upper()}):")
            print(f"      Entry: {trade['entry_price']:.5f}")
            print(f"      Exit: {trade['exit_price']:.5f}")
            print(f"      Profit: {profit_pips:.2f} pips")
            print(f"      Profit $: ${profit_currency:.2f}")
            print(f"      Verification: {profit_pips:.2f} × {pip_val} × 0.01 × 100000 = ${calculated_profit:.2f}")
            if abs(profit_currency - calculated_profit) < 0.01:
                print(f"      ✅ Calculation correct!")
            else:
                print(f"      ❌ Calculation mismatch! Expected ${calculated_profit:.2f}, got ${profit_currency:.2f}")

        # Show largest profit and loss
        winning_trades = [t for t in result['trades'] if t['profit_pips'] > 0]
        losing_trades = [t for t in result['trades'] if t['profit_pips'] < 0]

        if winning_trades:
            best_trade = max(winning_trades, key=lambda t: t['profit_pips'])
            print(f"\n🏆 LARGEST WINNING TRADE:")
            print(f"      Profit: {best_trade['profit_pips']:.2f} pips = ${best_trade['profit_currency']:.2f}")
            print(f"      Entry: {best_trade['entry_price']:.5f}")
            print(f"      Exit: {best_trade['exit_price']:.5f}")

        if losing_trades:
            worst_trade = min(losing_trades, key=lambda t: t['profit_pips'])
            print(f"\n💔 LARGEST LOSING TRADE:")
            print(f"      Profit: {worst_trade['profit_pips']:.2f} pips = ${worst_trade['profit_currency']:.2f}")
            print(f"      Entry: {worst_trade['entry_price']:.5f}")
            print(f"      Exit: {worst_trade['exit_price']:.5f}")

    print("\n" + "=" * 80)
    print("✅ PROFIT CALCULATION TEST COMPLETED")
    print("=" * 80)

except FileNotFoundError:
    print(f"\n❌ File not found: {csv_file}")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
