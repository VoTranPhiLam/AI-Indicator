"""
Quick test for Ichimoku strategy
"""
from backtest_optimizer import load_data, backtest_strategy
import sys

# Test with one CSV file
csv_file = "CSV/AUDUSD5.csv"

print(f"Testing Ichimoku strategy with {csv_file}...")
print("=" * 60)

try:
    # Load data
    data = load_data(csv_file, has_header=False)
    print(f"✅ Loaded {len(data)} candles")
    print(f"   Date range: {data['timestamp'].min()} to {data['timestamp'].max()}")
    print()

    # Test with default EA parameters
    print("Running backtest with EA default parameters...")
    print("  Tenkan: 9, Kijun: 26, Senkou B: 52")
    print("  RSI Period: 14, Buy >= 50, Sell <= 50")
    print("  Risk:Reward: 1.2, SL Buffer: 3 pips, Swing Bars: 5")
    print()

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
        symbol="AUDUSD"  # Auto-detect pip value
    )

    print("RESULTS:")
    print("-" * 60)
    print(f"  Total Trades:      {result['num_trades']}")
    print(f"  Win Rate:          {result['win_rate']:.1f}%")
    print(f"  Total Profit:      {result['total_profit_pips']:.2f} pips")
    print(f"  Profit Factor:     {result['profit_factor']:.2f}")
    print(f"  Max Drawdown:      {result['max_drawdown_pct']:.2f}%")
    print()

    # Show first 3 trades
    if result['trades']:
        print("First 3 trades:")
        for i, trade in enumerate(result['trades'][:3]):
            print(f"  {i+1}. {trade['type'].upper()}: "
                  f"Entry={trade['entry_price']:.5f}, "
                  f"Exit={trade['exit_price']:.5f}, "
                  f"Profit={trade['profit_pips']:.2f} pips, "
                  f"Reason={trade['exit_reason']}")

    print()
    print("✅ Test completed successfully!")

except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
