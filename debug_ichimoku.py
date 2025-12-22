"""
Debug script để tìm lỗi Ichimoku strategy
"""
from backtest_optimizer import load_data, compute_ichimoku, compute_rsi
import pandas as pd
import sys

# Test với file CSV thực tế
csv_file = "CSV/AUDUSD5.csv"  # Thay bằng file của bạn

print("=" * 80)
print(f"DEBUGGING ICHIMOKU STRATEGY: {csv_file}")
print("=" * 80)

try:
    # Load data
    data = load_data(csv_file, has_header=False)
    print(f"\n✅ Loaded {len(data)} candles")
    print(f"   Date range: {data['timestamp'].min()} to {data['timestamp'].max()}")

    # Calculate indicators với parameters của bạn
    tenkan_period = 9
    kijun_period = 26
    senkou_b_period = 52
    rsi_period = 14
    rsi_buy_threshold = 50.0
    rsi_sell_threshold = 50.0

    print(f"\n📊 Parameters:")
    print(f"   Tenkan: {tenkan_period}, Kijun: {kijun_period}, Senkou: {senkou_b_period}")
    print(f"   RSI: {rsi_period}, Buy >= {rsi_buy_threshold}, Sell <= {rsi_sell_threshold}")

    # Calculate Ichimoku
    data['tenkan'], data['kijun'], data['senkou_a'], data['senkou_b'], data['chikou'] = compute_ichimoku(
        data['high'], data['low'], tenkan_period, kijun_period, senkou_b_period
    )

    # Calculate RSI
    data['rsi'] = compute_rsi(data['close'], rsi_period)

    # Drop NaN ONLY from columns used for signals
    print(f"\n🔍 Before dropna: {len(data)} candles")
    print(f"   Tenkan NaN: {data['tenkan'].isna().sum()}")
    print(f"   Kijun NaN: {data['kijun'].isna().sum()}")
    print(f"   RSI NaN: {data['rsi'].isna().sum()}")
    print(f"   Senkou B NaN: {data['senkou_b'].isna().sum()}")

    data = data.dropna(subset=['tenkan', 'kijun', 'rsi']).reset_index(drop=True)
    print(f"\n✅ After dropna (subset): {len(data)} candles")

    # Tìm crossover signals
    buy_signals = []
    sell_signals = []

    for i in range(1, len(data)):
        current = data.iloc[i]
        prev = data.iloc[i-1]

        tenkan_curr = current['tenkan']
        kijun_curr = current['kijun']
        tenkan_prev = prev['tenkan']
        kijun_prev = prev['kijun']
        rsi_curr = current['rsi']

        # Check BUY crossover
        if tenkan_curr > kijun_curr and tenkan_prev <= kijun_prev:
            buy_signals.append({
                'index': i,
                'timestamp': current['timestamp'],
                'tenkan': tenkan_curr,
                'kijun': kijun_curr,
                'rsi': rsi_curr,
                'rsi_pass': rsi_curr >= rsi_buy_threshold
            })

        # Check SELL crossover
        if tenkan_curr < kijun_curr and tenkan_prev >= kijun_prev:
            sell_signals.append({
                'index': i,
                'timestamp': current['timestamp'],
                'tenkan': tenkan_curr,
                'kijun': kijun_curr,
                'rsi': rsi_curr,
                'rsi_pass': rsi_curr <= rsi_sell_threshold
            })

    print(f"\n🔍 CROSSOVER SIGNALS:")
    print(f"   BUY Crossovers (Tenkan cắt LÊN Kijun): {len(buy_signals)}")
    print(f"   SELL Crossovers (Tenkan cắt XUỐNG Kijun): {len(sell_signals)}")

    # Show first 5 BUY signals
    if buy_signals:
        print(f"\n✅ First {min(5, len(buy_signals))} BUY Crossovers:")
        for sig in buy_signals[:5]:
            status = "✓ PASS" if sig['rsi_pass'] else "✗ FAIL"
            print(f"   [{sig['index']}] {sig['timestamp']} | RSI={sig['rsi']:.2f} {status}")

        # Count how many pass RSI filter
        buy_pass = sum(1 for s in buy_signals if s['rsi_pass'])
        print(f"\n   → {buy_pass}/{len(buy_signals)} BUY signals PASS RSI filter (>= {rsi_buy_threshold})")
    else:
        print("   ❌ NO BUY CROSSOVERS FOUND!")

    # Show first 5 SELL signals
    if sell_signals:
        print(f"\n✅ First {min(5, len(sell_signals))} SELL Crossovers:")
        for sig in sell_signals[:5]:
            status = "✓ PASS" if sig['rsi_pass'] else "✗ FAIL"
            print(f"   [{sig['index']}] {sig['timestamp']} | RSI={sig['rsi']:.2f} {status}")

        # Count how many pass RSI filter
        sell_pass = sum(1 for s in sell_signals if s['rsi_pass'])
        print(f"\n   → {sell_pass}/{len(sell_signals)} SELL signals PASS RSI filter (<= {rsi_sell_threshold})")
    else:
        print("   ❌ NO SELL CROSSOVERS FOUND!")

    # Total valid signals
    total_valid = sum(1 for s in buy_signals if s['rsi_pass']) + sum(1 for s in sell_signals if s['rsi_pass'])
    print(f"\n📊 TOTAL VALID SIGNALS: {total_valid}")

    if total_valid == 0:
        print("\n⚠️ PHÁT HIỆN VẤN ĐỀ!")
        print("   Nguyên nhân có thể:")
        if len(buy_signals) == 0 and len(sell_signals) == 0:
            print("   1. KHÔNG CÓ CROSSOVER NÀO trong dữ liệu")
            print("      → Dữ liệu quá ngắn hoặc Kijun period quá lớn")
            print("      → Thử giảm Kijun xuống 15-20")
        else:
            print("   1. CÓ CROSSOVER nhưng TẤT CẢ đều bị chặn bởi RSI filter")
            print(f"      → RSI Buy >= {rsi_buy_threshold} quá strict")
            print(f"      → RSI Sell <= {rsi_sell_threshold} quá strict")
            print("      → Thử mở rộng: Buy >= 30, Sell <= 70")

except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
