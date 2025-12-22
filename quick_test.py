"""
TEST NHANH - Chạy với ít tham số hơn để test nhanh
Quick Test - Run with fewer parameters for faster testing
"""

import pandas as pd
import sys
from backtest_optimizer import (
    load_data,
    optimize_parameters,
    print_top_results,
    save_results
)

def main():
    print("\n" + "="*80)
    print("🧪 TEST NHANH - QUICK TEST")
    print("="*80)
    print("\n📌 Test này sẽ chạy nhanh hơn với ít tham số hơn")
    print("   This test runs faster with fewer parameters\n")

    # ========================================================================
    # CẤU HÌNH TEST - TEST CONFIGURATION
    # ========================================================================

    # File dữ liệu
    data_file = 'AUDCAD15.csv'

    # Tham số RSI (ít hơn để test nhanh)
    # RSI parameters (fewer for quick testing)
    param_grid = {
        'rsi_period': [10, 14, 18, 22],        # Chỉ test 4 giá trị
        'overbought': [70, 80],                # Chỉ test 2 giá trị
        'oversold': [20, 30]                   # Chỉ test 2 giá trị
    }
    # Tổng: 4 x 2 x 2 = 16 combinations (instead of 650)

    # Tham số trading
    tp_pips = 20.0
    sl_pips = 15.0
    spread_pips = 1.2
    lot_size = 0.1

    # File kết quả
    results_file = 'quick_test_results.csv'

    print("Cấu hình test:")
    print(f"  📁 File dữ liệu:     {data_file}")
    print(f"  🎯 Take Profit:      {tp_pips} pips")
    print(f"  🛑 Stop Loss:        {sl_pips} pips")
    print(f"  💱 Spread:           {spread_pips} pips")
    print(f"  💰 Lot Size:         {lot_size}")
    print(f"\n  📊 Tổng combinations: 4 x 2 x 2 = 16")
    print(f"  💾 File kết quả:     {results_file}\n")

    # ========================================================================
    # LOAD DATA
    # ========================================================================

    try:
        print("⏳ Đang load dữ liệu...")
        data = load_data(data_file)
        print(f"✅ Đã load {len(data)} candles")
    except FileNotFoundError:
        print(f"\n❌ LỖI: Không tìm thấy file '{data_file}'!")
        return
    except Exception as e:
        print(f"\n❌ LỖI khi load data: {e}")
        return

    # ========================================================================
    # OPTIMIZE
    # ========================================================================

    print("\n" + "="*80)
    print("🔍 BẮT ĐẦU TỐI ƯU HÓA THAM SỐ")
    print("="*80 + "\n")

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
        print(f"\n❌ LỖI trong quá trình tối ưu: {e}")
        import traceback
        traceback.print_exc()
        return

    # ========================================================================
    # HIỂN THỊ KẾT QUẢ - DISPLAY RESULTS
    # ========================================================================

    print_top_results(results_df, top_n=5)  # Chỉ hiển thị top 5

    # ========================================================================
    # LƯU KẾT QUẢ - SAVE RESULTS
    # ========================================================================

    save_results(results_df, results_file)

    # ========================================================================
    # TỔNG KẾT - SUMMARY
    # ========================================================================

    print("\n" + "="*80)
    print("✅ TEST HOÀN THÀNH - TEST COMPLETE")
    print("="*80)

    valid_count = len(results_df[results_df['valid'] == True])
    total_count = len(results_df)

    print(f"\n📊 Thống kê:")
    print(f"   Tổng số test:        {total_count}")
    print(f"   Kết quả hợp lệ:      {valid_count}")
    print(f"   Không hợp lệ:        {total_count - valid_count}")

    if valid_count > 0:
        best = results_df[results_df['valid'] == True].iloc[0]
        print(f"\n🏆 Tham số tốt nhất:")
        print(f"   RSI Period:    {int(best['rsi_period'])}")
        print(f"   Overbought:    {int(best['overbought'])}")
        print(f"   Oversold:      {int(best['oversold'])}")
        print(f"\n💰 Hiệu suất:")
        print(f"   Profit:        {best['total_profit_pips']:.2f} pips")
        print(f"   Win Rate:      {best['win_rate']:.2f}%")
        print(f"   Số lệnh:       {int(best['num_trades'])}")
        print(f"   Max Drawdown:  {best['max_drawdown_pct']:.2f}%")
        print(f"   Score:         {best['score']:.2f}")
    else:
        print("\n⚠️  Không có kết quả hợp lệ")

    print("\n" + "="*80)
    print(f"💾 Kết quả chi tiết đã lưu vào: {results_file}")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
