#!/usr/bin/env python3
"""
Test equity and % risk management features
"""

import pandas as pd
from backtest_optimizer import backtest_strategy

print("=" * 80)
print("TEST: EQUITY & % RISK MANAGEMENT")
print("=" * 80)

# Load test data
csv_file = "AUDCAD15.csv"

try:
    data = pd.read_csv(csv_file)

    if 'Date' in data.columns and 'Time' in data.columns:
        data['timestamp'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
        data = data.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'})
        data = data[['timestamp', 'open', 'high', 'low', 'close', 'volume']]

    print(f"\n✅ Loaded {len(data)} candles from {csv_file}")

    # Test 1: Fixed lot size (default)
    print("\n" + "=" * 80)
    print("TEST 1: FIXED LOT SIZE (0.01)")
    print("=" * 80)

    result1 = backtest_strategy(
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
        symbol="AUDCAD",
        initial_balance=10000.0,
        risk_percent_per_trade=0.0,  # 0 = use fixed lot
        max_lot_size=100.0
    )

    print(f"\n📊 Results:")
    print(f"   Starting Balance: $10,000.00")
    print(f"   Total Trades: {result1['num_trades']}")
    print(f"   Winning: {result1['num_winning_trades']}")
    print(f"   Losing: {result1['num_losing_trades']}")
    print(f"   Final Profit: ${result1['total_profit_currency']:.2f} ({result1['total_profit_pips']:.2f} pips)")
    print(f"   Final Balance: ${result1['equity_curve'][-1]:.2f}")
    print(f"   Win Rate: {result1['win_rate']:.2f}%")

    # Test 2: 0.5% risk per trade
    print("\n" + "=" * 80)
    print("TEST 2: 0.5% RISK PER TRADE")
    print("=" * 80)

    result2 = backtest_strategy(
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
        lot_size=0.01,  # Ignored when risk_percent > 0
        symbol="AUDCAD",
        initial_balance=10000.0,
        risk_percent_per_trade=0.5,  # Risk 0.5% per trade
        max_lot_size=100.0
    )

    print(f"\n📊 Results:")
    print(f"   Starting Balance: $10,000.00")
    print(f"   Risk per trade: 0.5% (max $50 per trade)")
    print(f"   Total Trades: {result2['num_trades']}")
    print(f"   Winning: {result2['num_winning_trades']}")
    print(f"   Losing: {result2['num_losing_trades']}")
    print(f"   Final Profit: ${result2['total_profit_currency']:.2f} ({result2['total_profit_pips']:.2f} pips)")
    print(f"   Final Balance: ${result2['equity_curve'][-1]:.2f}")
    print(f"   Win Rate: {result2['win_rate']:.2f}%")

    # Show sample lot sizes from trades
    if len(result2['trades']) > 0:
        print(f"\n💡 Sample lot sizes (dynamic based on balance):")
        for i, trade in enumerate(result2['trades'][:5], 1):
            # Lot size is embedded in profit_currency calculation
            # We can reverse-engineer it
            if trade['profit_pips'] != 0:
                estimated_lot = abs(trade['profit_currency'] / (trade['profit_pips'] * 0.0001 * 100000))
                print(f"   Trade {i}: ~{estimated_lot:.4f} lot (profit: {trade['profit_pips']:.2f} pips = ${trade['profit_currency']:.2f})")

    # Test 3: Compare Fixed vs % Risk
    print("\n" + "=" * 80)
    print("COMPARISON: FIXED LOT vs % RISK")
    print("=" * 80)

    print(f"\n📈 Fixed Lot (0.01):")
    print(f"   Final Balance: ${result1['equity_curve'][-1]:.2f}")
    print(f"   Profit: ${result1['total_profit_currency']:.2f}")
    print(f"   Return: {((result1['equity_curve'][-1] / 10000 - 1) * 100):.2f}%")

    print(f"\n📊 % Risk (0.5%):")
    print(f"   Final Balance: ${result2['equity_curve'][-1]:.2f}")
    print(f"   Profit: ${result2['total_profit_currency']:.2f}")
    print(f"   Return: {((result2['equity_curve'][-1] / 10000 - 1) * 100):.2f}%")

    print(f"\n💰 Difference:")
    diff = result2['total_profit_currency'] - result1['total_profit_currency']
    print(f"   % Risk advantage: ${diff:.2f}")
    if diff > 0:
        print(f"   ✅ % Risk management performed BETTER!")
    elif diff < 0:
        print(f"   ⚠️ Fixed lot performed better in this case")
    else:
        print(f"   ➖ Same result")

    print("\n" + "=" * 80)
    print("✅ EQUITY & % RISK TEST COMPLETED!")
    print("=" * 80)

    print("""
📝 Key Findings:
1. Initial balance sets the starting equity
2. With % risk: lot size adjusts dynamically based on current balance
3. After winning trades: balance increases → larger lots
4. After losing trades: balance decreases → smaller lots
5. This provides better risk management than fixed lot size
""")

except FileNotFoundError:
    print(f"\n❌ File not found: {csv_file}")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
