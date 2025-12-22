"""
Interactive Chart Visualization for Ichimoku Backtest
Hiển thị chart với entry/exit points và Ichimoku indicators
"""
from backtest_optimizer import load_data, backtest_strategy
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import sys

def visualize_backtest(csv_file: str,
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
                       max_candles: int = 500,
                       symbol: str = None):
    """
    Tạo interactive chart visualization cho backtest

    Args:
        csv_file: Đường dẫn file CSV
        max_candles: Số candles tối đa để hiển thị (tránh chart quá dày)
    """
    print("=" * 80)
    print(f"VISUALIZING ICHIMOKU BACKTEST: {csv_file}")
    print("=" * 80)

    # Auto-detect symbol from filename if not provided
    if symbol is None:
        import re
        filename = csv_file.split('/')[-1].replace('.csv', '')
        # Extract symbol from filename (e.g., AUDUSD5.csv -> AUDUSD)
        match = re.match(r'([A-Z]+)\d+', filename)
        if match:
            symbol = match.group(1)
        else:
            symbol = "EURUSD"  # Default
        print(f"   Auto-detected symbol: {symbol}")

    # Load data
    data = load_data(csv_file, has_header=False)
    print(f"\n✅ Loaded {len(data)} candles")

    # Lấy max_candles cuối cùng để chart không quá dày
    if len(data) > max_candles:
        print(f"   → Showing last {max_candles} candles for better visualization")
        data = data.tail(max_candles).reset_index(drop=True)

    # Run backtest
    print(f"\n🔄 Running backtest...")
    print(f"   Symbol: {symbol} (pip value: {'0.01' if 'JPY' in symbol else '0.0001'})")
    print(f"   Tenkan: {tenkan_period}, Kijun: {kijun_period}, Senkou: {senkou_b_period}")
    print(f"   RSI: {rsi_period}, Buy>={rsi_buy_threshold}, Sell<={rsi_sell_threshold}")
    print(f"   RR: {risk_reward_ratio}, SL Buffer: {sl_buffer_pips} pips")

    result = backtest_strategy(
        data=data,
        tenkan_period=tenkan_period,
        kijun_period=kijun_period,
        senkou_b_period=senkou_b_period,
        rsi_period=rsi_period,
        rsi_buy_threshold=rsi_buy_threshold,
        rsi_sell_threshold=rsi_sell_threshold,
        risk_reward_ratio=risk_reward_ratio,
        sl_buffer_pips=sl_buffer_pips,
        bars_check_swing=bars_check_swing,
        spread_pips=spread_pips,
        lot_size=lot_size,
        symbol=symbol  # Auto-detect pip value for JPY pairs
    )

    trades = result['trades']
    print(f"\n✅ Backtest completed: {len(trades)} trades")
    print(f"   Profit: {result['total_profit_pips']:.2f} pips")
    print(f"   Win Rate: {result['win_rate']:.1f}%")

    # Load data lại để có indicators
    from backtest_optimizer import compute_ichimoku, compute_rsi

    data_full = load_data(csv_file, has_header=False)
    if len(data_full) > max_candles:
        data_full = data_full.tail(max_candles).reset_index(drop=True)

    data_full['tenkan'], data_full['kijun'], _, _, _ = compute_ichimoku(
        data_full['high'], data_full['low'], tenkan_period, kijun_period, senkou_b_period
    )
    data_full['rsi'] = compute_rsi(data_full['close'], rsi_period)
    data_full = data_full.dropna(subset=['tenkan', 'kijun', 'rsi']).reset_index(drop=True)

    print(f"\n📊 Creating interactive chart...")

    # Create subplots: Main chart + RSI
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3],
        subplot_titles=('Price Chart with Ichimoku & Trades', 'RSI Indicator')
    )

    # 1. Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=data_full['timestamp'],
            open=data_full['open'],
            high=data_full['high'],
            low=data_full['low'],
            close=data_full['close'],
            name='Price',
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350'
        ),
        row=1, col=1
    )

    # 2. Tenkan-sen (Conversion Line)
    fig.add_trace(
        go.Scatter(
            x=data_full['timestamp'],
            y=data_full['tenkan'],
            name='Tenkan-sen',
            line=dict(color='#2962FF', width=1.5),
            opacity=0.8
        ),
        row=1, col=1
    )

    # 3. Kijun-sen (Base Line)
    fig.add_trace(
        go.Scatter(
            x=data_full['timestamp'],
            y=data_full['kijun'],
            name='Kijun-sen',
            line=dict(color='#F23645', width=1.5),
            opacity=0.8
        ),
        row=1, col=1
    )

    # 4. Mark entry points
    for i, trade in enumerate(trades):
        entry_time = trade['entry_timestamp']
        entry_price = trade['entry_price']
        exit_time = trade['exit_timestamp']
        exit_price = trade['exit_price']
        sl = trade['stop_loss']
        tp = trade['take_profit']

        is_buy = trade['type'] == 'long'
        color = '#00E676' if is_buy else '#FF1744'  # Green for BUY, Red for SELL
        symbol_shape = 'triangle-up' if is_buy else 'triangle-down'

        # Entry point
        fig.add_trace(
            go.Scatter(
                x=[entry_time],
                y=[entry_price],
                mode='markers',
                name=f"{'BUY' if is_buy else 'SELL'} Entry #{i+1}",
                marker=dict(
                    symbol=symbol_shape,
                    size=15,
                    color=color,
                    line=dict(color='white', width=2)
                ),
                hovertemplate=f"<b>{'BUY' if is_buy else 'SELL'} Entry</b><br>" +
                              f"Time: %{{x}}<br>" +
                              f"Price: {entry_price:.5f}<br>" +
                              f"SL: {sl:.5f}<br>" +
                              f"TP: {tp:.5f}<br>" +
                              "<extra></extra>",
                showlegend=(i == 0)  # Only show legend for first trade
            ),
            row=1, col=1
        )

        # Exit point
        exit_color = '#00C853' if trade['profit_pips'] > 0 else '#D50000'
        fig.add_trace(
            go.Scatter(
                x=[exit_time],
                y=[exit_price],
                mode='markers',
                name=f"Exit #{i+1} ({trade['exit_reason']})",
                marker=dict(
                    symbol='x',
                    size=12,
                    color=exit_color,
                    line=dict(width=2)
                ),
                hovertemplate=f"<b>Exit - {trade['exit_reason']}</b><br>" +
                              f"Time: %{{x}}<br>" +
                              f"Price: {exit_price:.5f}<br>" +
                              f"Profit: {trade['profit_pips']:.2f} pips<br>" +
                              "<extra></extra>",
                showlegend=(i == 0)
            ),
            row=1, col=1
        )

        # Draw SL and TP horizontal lines (only for first few trades to avoid cluttering)
        if i < 10:  # Only show for first 10 trades
            # SL line
            fig.add_trace(
                go.Scatter(
                    x=[entry_time, exit_time],
                    y=[sl, sl],
                    mode='lines',
                    name='Stop Loss' if i == 0 else None,
                    line=dict(color='red', width=1, dash='dot'),
                    opacity=0.5,
                    showlegend=(i == 0),
                    hoverinfo='skip'
                ),
                row=1, col=1
            )

            # TP line
            fig.add_trace(
                go.Scatter(
                    x=[entry_time, exit_time],
                    y=[tp, tp],
                    mode='lines',
                    name='Take Profit' if i == 0 else None,
                    line=dict(color='green', width=1, dash='dot'),
                    opacity=0.5,
                    showlegend=(i == 0),
                    hoverinfo='skip'
                ),
                row=1, col=1
            )

    # 5. RSI Indicator
    fig.add_trace(
        go.Scatter(
            x=data_full['timestamp'],
            y=data_full['rsi'],
            name='RSI',
            line=dict(color='#9C27B0', width=1.5),
        ),
        row=2, col=1
    )

    # RSI threshold lines
    fig.add_hline(y=rsi_buy_threshold, line_dash="dash", line_color="green", opacity=0.5, row=2, col=1)
    fig.add_hline(y=rsi_sell_threshold, line_dash="dash", line_color="red", opacity=0.5, row=2, col=1)
    fig.add_hline(y=50, line_dash="dot", line_color="gray", opacity=0.3, row=2, col=1)

    # Update layout
    fig.update_layout(
        title=f"Ichimoku Backtest Visualization - {csv_file}<br>" +
              f"<sub>Trades: {len(trades)} | Profit: {result['total_profit_pips']:.2f} pips | " +
              f"Win Rate: {result['win_rate']:.1f}% | PF: {result['profit_factor']:.2f}</sub>",
        xaxis_title="Time",
        yaxis_title="Price",
        xaxis2_title="Time",
        yaxis2_title="RSI",
        height=900,
        template="plotly_dark",
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Update xaxis for better formatting
    fig.update_xaxes(rangeslider_visible=False)

    print(f"\n✅ Chart created successfully!")
    print(f"   Opening in browser...")

    # Save and show
    output_file = csv_file.replace('.csv', '_visualization.html')
    fig.write_html(output_file)
    print(f"\n💾 Chart saved to: {output_file}")

    # Show in browser
    fig.show()

    return result, fig


if __name__ == "__main__":
    # Mặc định test với AUDUSD5.csv
    csv_file = "CSV/AUDUSD5.csv"

    if len(sys.argv) > 1:
        csv_file = sys.argv[1]

    print(f"\n🎨 Ichimoku Backtest Visualizer")
    print(f"   Usage: python visualize_trades.py [CSV_FILE]")
    print(f"   Using: {csv_file}\n")

    # Run visualization với EA default parameters
    visualize_backtest(
        csv_file=csv_file,
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
        max_candles=500  # Show last 500 candles
    )
