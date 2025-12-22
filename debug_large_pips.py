#!/usr/bin/env python3
"""
Debug why GBPUSD D1 has such large pip values (200+ pips per trade)
"""

import pandas as pd
import numpy as np
from backtest_optimizer import backtest_strategy, find_swing_low, find_swing_high, get_pip_value

print("=" * 80)
print("DEBUG: LARGE PIP VALUES IN D1 TIMEFRAME")
print("=" * 80)

# Create synthetic GBPUSD D1 data to test
print("\n📊 Creating synthetic GBPUSD D1 data...")

# GBPUSD typical daily range: 50-100 pips
# Let's create 100 days of data with realistic price movement
np.random.seed(42)
base_price = 1.2500

dates = pd.date_range('2024-01-01', periods=100, freq='D')
data = pd.DataFrame({
    'timestamp': dates
})

# Simulate realistic daily candles
prices = [base_price]
for i in range(99):
    # Daily change: -50 to +50 pips
    change = np.random.uniform(-0.0050, 0.0050)
    prices.append(prices[-1] + change)

data['close'] = prices
data['open'] = data['close'] + np.random.uniform(-0.0020, 0.0020, 100)
data['high'] = data[['open', 'close']].max(axis=1) + np.random.uniform(0.0010, 0.0040, 100)
data['low'] = data[['open', 'close']].min(axis=1) - np.random.uniform(0.0010, 0.0040, 100)
data['volume'] = np.random.randint(1000, 5000, 100)

print(f"✅ Created {len(data)} candles")
print(f"   Price range: {data['low'].min():.4f} - {data['high'].max():.4f}")
print(f"   Avg daily range: {((data['high'] - data['low']).mean() / 0.0001):.2f} pips")

# Test swing detection
print("\n" + "=" * 80)
print("TEST SWING HIGH/LOW DETECTION")
print("=" * 80)

test_index = 50  # Middle of data
bars_check = 5

swing_low = find_swing_low(data['low'], test_index, bars_check)
swing_high = find_swing_high(data['high'], test_index, bars_check)
current_price = data.iloc[test_index]['close']

print(f"\nAt candle {test_index}:")
print(f"   Current close: {current_price:.5f}")
print(f"   Swing Low (last {bars_check} bars): {swing_low:.5f}")
print(f"   Swing High (last {bars_check} bars): {swing_high:.5f}")

# Calculate what SL/TP would be for LONG
pip_value = get_pip_value("GBPUSD")
spread_pips = 1.2
sl_buffer_pips = 3.0
risk_reward = 1.2

spread_price = spread_pips * pip_value
sl_buffer = sl_buffer_pips * pip_value

entry_price = current_price + spread_price
stop_loss = swing_low - sl_buffer
sl_distance = entry_price - stop_loss
take_profit = entry_price + (sl_distance * risk_reward)

sl_distance_pips = sl_distance / pip_value
tp_distance_pips = (take_profit - entry_price) / pip_value

print(f"\n🔍 LONG Trade Calculation:")
print(f"   Entry: {entry_price:.5f}")
print(f"   SL: {stop_loss:.5f} (distance: {sl_distance_pips:.2f} pips)")
print(f"   TP: {take_profit:.5f} (distance: {tp_distance_pips:.2f} pips)")
print(f"   Risk:Reward: 1:{risk_reward}")

if sl_distance_pips > 200:
    print(f"   ⚠️ SL is {sl_distance_pips:.0f} pips away - VERY LARGE!")
    print(f"   This means swing_low from last {bars_check} days is very far")

# Now run actual backtest
print("\n" + "=" * 80)
print("RUNNING BACKTEST ON SYNTHETIC DATA")
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
    symbol="GBPUSD"
)

print(f"\n📊 Results:")
print(f"   Total Trades: {result['num_trades']}")
print(f"   Winning: {result['num_winning_trades']}")
print(f"   Losing: {result['num_losing_trades']}")

if result['num_trades'] > 0:
    print(f"\n💰 Profit Breakdown:")
    print(f"   Total Winning: {result['total_winning_profit_pips']:.2f} pips (${result['total_winning_profit_currency']:.2f})")
    print(f"   Total Losing: {result['total_losing_profit_pips']:.2f} pips (${result['total_losing_profit_currency']:.2f})")
    print(f"   Final: {result['total_profit_pips']:.2f} pips (${result['total_profit_currency']:.2f})")

    avg_win_pips = result['total_winning_profit_pips'] / result['num_winning_trades'] if result['num_winning_trades'] > 0 else 0
    avg_loss_pips = result['total_losing_profit_pips'] / result['num_losing_trades'] if result['num_losing_trades'] > 0 else 0

    print(f"\n📈 Averages:")
    print(f"   Avg Win: {avg_win_pips:.2f} pips")
    print(f"   Avg Loss: {avg_loss_pips:.2f} pips")

    # Show first few trades with details
    print("\n" + "=" * 80)
    print("FIRST 3 TRADES DETAILED")
    print("=" * 80)

    for i, trade in enumerate(result['trades'][:3], 1):
        sl_dist = abs(trade['entry_price'] - trade['stop_loss']) / pip_value
        tp_dist = abs(trade['take_profit'] - trade['entry_price']) / pip_value

        print(f"\n📝 Trade #{i} ({trade['type'].upper()}):")
        print(f"   Entry: {trade['entry_price']:.5f}")
        print(f"   SL: {trade['stop_loss']:.5f} (distance: {sl_dist:.2f} pips)")
        print(f"   TP: {trade['take_profit']:.5f} (distance: {tp_dist:.2f} pips)")
        print(f"   Exit: {trade['exit_price']:.5f} ({trade['exit_reason']})")
        print(f"   Profit: {trade['profit_pips']:.2f} pips = ${trade['profit_currency']:.2f}")

        if sl_dist > 150:
            print(f"   ⚠️ SL distance is VERY LARGE ({sl_dist:.0f} pips)")
            print(f"   This is typical for D1 timeframe with swing-based SL")

        if tp_dist > 150:
            print(f"   ⚠️ TP distance is VERY LARGE ({tp_dist:.0f} pips)")

else:
    print("   No trades generated")

print("\n" + "=" * 80)
print("CONCLUSION")
print("=" * 80)

print("""
If you see large pip values (200+ pips per trade):

✅ This is NORMAL for D1 timeframe with swing-based SL/TP because:
   1. bars_check_swing = 5 means we look back 5 DAYS
   2. Price can move 200-500 pips in 5 days
   3. SL based on swing low/high → can be 200+ pips away
   4. TP = SL × Risk:Reward → also large

💡 But profit CURRENCY is correct:
   - 2000 pips × 0.0001 × 0.01 lot × 100000 = $200 ✓

⚠️ To reduce pip values, you can:
   1. Use smaller timeframe (H4, H1, M15)
   2. Reduce bars_check_swing (e.g., from 5 to 3)
   3. Add max SL limit in pips
   4. Use fixed SL/TP instead of swing-based
""")

print("=" * 80)
