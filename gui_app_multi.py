"""
Multi-Symbol Multi-Timeframe Backtesting GUI
Giao diện đồ họa cho tối ưu hóa đa sản phẩm, đa khung thời gian
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path
import time
from datetime import datetime
import os
import re

# Import backtesting functions
from backtest_optimizer import (
    load_data,
    compute_rsi,
    backtest_strategy,
    evaluate_metrics,
    calculate_score,
    is_valid_result
)
from itertools import product

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_filename(filename):
    """
    Parse filename to extract symbol and timeframe.

    Examples:
        AUDUSD5.csv -> (AUDUSD, M5)
        EURUSD15.csv -> (EURUSD, M15)
        GBPUSD30.csv -> (GBPUSD, M30)
        USDJPY60.csv -> (USDJPY, H1)
        EURUSD1440.csv -> (EURUSD, D1)

    Args:
        filename: CSV filename

    Returns:
        (symbol, timeframe) tuple
    """
    # Remove .csv extension
    name = filename.replace('.csv', '')

    # Extract number at the end
    match = re.match(r'([A-Z]+)(\d+)', name)

    if match:
        symbol = match.group(1)
        minutes = int(match.group(2))

        # Convert minutes to timeframe label
        if minutes < 60:
            timeframe = f"M{minutes}"
        elif minutes == 60:
            timeframe = "H1"
        elif minutes < 1440:
            hours = minutes // 60
            timeframe = f"H{hours}"
        elif minutes == 1440:
            timeframe = "D1"
        else:
            days = minutes // 1440
            timeframe = f"D{days}"

        return symbol, timeframe

    return None, None


def scan_csv_folder(folder_path):
    """
    Scan CSV folder and return list of files with metadata.

    Args:
        folder_path: Path to CSV folder

    Returns:
        List of dicts with file info
    """
    csv_folder = Path(folder_path)

    if not csv_folder.exists():
        return []

    files_info = []

    for csv_file in csv_folder.glob('*.csv'):
        symbol, timeframe = parse_filename(csv_file.name)

        if symbol and timeframe:
            # Get file size
            size_kb = csv_file.stat().st_size / 1024

            files_info.append({
                'filename': csv_file.name,
                'path': str(csv_file),
                'symbol': symbol,
                'timeframe': timeframe,
                'size_kb': size_kb
            })

    # Sort by symbol then timeframe
    files_info.sort(key=lambda x: (x['symbol'], x['timeframe']))

    return files_info


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Multi-Symbol Optimizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .file-item {
        padding: 0.5rem;
        margin: 0.25rem 0;
        background-color: #f0f2f6;
        border-radius: 0.3rem;
        border-left: 3px solid #1f77b4;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st.markdown('<h1 class="main-header">📊 Multi-Symbol Multi-Timeframe Optimizer</h1>', unsafe_allow_html=True)
st.markdown("### 🚀 Tối ưu hóa đồng thời nhiều sản phẩm và khung thời gian")
st.markdown("---")

# ============================================================================
# SIDEBAR - CONFIGURATION
# ============================================================================

with st.sidebar:
    st.header("⚙️ Cấu Hình")

    # CSV Folder Path
    st.subheader("📁 Thư Mục CSV")
    csv_folder = st.text_input(
        "Đường dẫn folder CSV:",
        value="CSV",
        help="Thư mục chứa các file CSV (tương đối hoặc tuyệt đối)"
    )

    # Scan folder
    if st.button("🔍 Scan Folder", use_container_width=True):
        st.session_state.files_scanned = True

    st.markdown("---")

    # File Selection
    if 'files_scanned' not in st.session_state:
        st.session_state.files_scanned = False

    if st.session_state.files_scanned or Path(csv_folder).exists():
        files_info = scan_csv_folder(csv_folder)

        if files_info:
            st.subheader("📊 Chọn Files")

            # Group by symbol
            symbols = sorted(set(f['symbol'] for f in files_info))

            # Select all checkbox
            select_all = st.checkbox("✅ Chọn tất cả", value=True)

            selected_files = []

            for symbol in symbols:
                with st.expander(f"💱 {symbol}", expanded=True):
                    symbol_files = [f for f in files_info if f['symbol'] == symbol]

                    for file_info in symbol_files:
                        default_value = select_all

                        if st.checkbox(
                            f"{file_info['timeframe']} ({file_info['size_kb']:.1f} KB)",
                            value=default_value,
                            key=f"file_{file_info['filename']}"
                        ):
                            selected_files.append(file_info)

            st.session_state.selected_files = selected_files
            st.info(f"📌 Đã chọn: {len(selected_files)} file(s)")
        else:
            st.warning(f"⚠️ Không tìm thấy file CSV nào trong folder '{csv_folder}'")
            st.session_state.selected_files = []
    else:
        st.info("👆 Nhấn 'Scan Folder' để tìm files")
        st.session_state.selected_files = []

    st.markdown("---")

    # Indicator Selection
    st.subheader("📊 Chiến Lược")
    indicator = st.selectbox("Chọn indicator:", ["ICHIMOKU + RSI"])

    st.markdown("---")

    # ICHIMOKU Parameters
    if indicator == "ICHIMOKU + RSI":
        st.subheader("🎯 Tham Số ICHIMOKU")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Tenkan-sen**")
            tenkan_min = st.number_input("Tenkan Min", 3, 30, 9, 1)
            tenkan_max = st.number_input("Tenkan Max", 3, 30, 9, 1)
            tenkan_step = st.number_input("Tenkan Step", 1, 10, 1, 1)

        with col2:
            st.markdown("**Kijun-sen**")
            kijun_min = st.number_input("Kijun Min", 10, 60, 26, 1)
            kijun_max = st.number_input("Kijun Max", 10, 60, 26, 1)
            kijun_step = st.number_input("Kijun Step", 1, 10, 1, 1)

        with col3:
            st.markdown("**Senkou Span B**")
            senkou_min = st.number_input("Senkou Min", 20, 100, 52, 1)
            senkou_max = st.number_input("Senkou Max", 20, 100, 52, 1)
            senkou_step = st.number_input("Senkou Step", 1, 10, 1, 1)

        st.markdown("---")
        st.subheader("🔍 Tham Số RSI Filter")

        col4, col5, col6 = st.columns(3)
        with col4:
            rsi_period_min = st.number_input("RSI Period Min", 5, 30, 14, 1)
            rsi_period_max = st.number_input("RSI Period Max", 5, 30, 14, 1)
            rsi_period_step = st.number_input("RSI Period Step", 1, 10, 1, 1)

        with col5:
            rsi_buy_min = st.number_input("RSI Buy Min", 30.0, 70.0, 50.0, 5.0)
            rsi_buy_max = st.number_input("RSI Buy Max", 30.0, 70.0, 50.0, 5.0)
            rsi_buy_step = st.number_input("RSI Buy Step", 1.0, 10.0, 5.0, 1.0)

        with col6:
            rsi_sell_min = st.number_input("RSI Sell Min", 30.0, 70.0, 50.0, 5.0)
            rsi_sell_max = st.number_input("RSI Sell Max", 30.0, 70.0, 50.0, 5.0)
            rsi_sell_step = st.number_input("RSI Sell Step", 1.0, 10.0, 5.0, 1.0)

        # Calculate total combinations
        total_combos = (
            len(range(tenkan_min, tenkan_max + 1, tenkan_step)) *
            len(range(kijun_min, kijun_max + 1, kijun_step)) *
            len(range(senkou_min, senkou_max + 1, senkou_step)) *
            len(range(rsi_period_min, rsi_period_max + 1, rsi_period_step)) *
            len([x / 10 for x in range(int(rsi_buy_min * 10), int(rsi_buy_max * 10) + 1, int(rsi_buy_step * 10))]) *
            len([x / 10 for x in range(int(rsi_sell_min * 10), int(rsi_sell_max * 10) + 1, int(rsi_sell_step * 10))])
        )

        st.info(f"📊 Tests per file: **{total_combos:,}**")

    st.markdown("---")

    # Trading Parameters
    st.subheader("💰 Tham Số Trading")

    col7, col8 = st.columns(2)
    with col7:
        risk_reward_ratio = st.number_input("Risk:Reward Ratio", 0.5, 5.0, 1.2, 0.1)
        sl_buffer_pips = st.number_input("SL Buffer (pips)", 0.0, 10.0, 3.0, 0.5)
    with col8:
        bars_check_swing = st.number_input("Bars Check Swing", 1, 20, 5, 1)
        spread_pips = st.number_input("Spread (pips)", 0.1, 10.0, 1.2, 0.1)

    lot_size = st.number_input("Lot Size", 0.01, 10.0, 0.01, 0.01)

    st.markdown("---")

    # Optimization Settings
    st.subheader("🔧 Cài Đặt")

    max_dd_threshold = st.slider("Max DD Threshold (%)", 10, 50, 30, 5)

    st.markdown("---")

    # Run Button
    run_optimization = st.button(
        "🚀 Chạy Tối Ưu Hóa",
        use_container_width=True,
        type="primary",
        disabled=not st.session_state.get('selected_files', [])
    )

# ============================================================================
# MAIN AREA
# ============================================================================

# Initialize session state
if 'all_results' not in st.session_state:
    st.session_state.all_results = None
if 'optimization_done' not in st.session_state:
    st.session_state.optimization_done = False

# ============================================================================
# RUN OPTIMIZATION
# ============================================================================

if run_optimization and st.session_state.get('selected_files'):
    st.session_state.optimization_done = False

    selected_files = st.session_state.selected_files

    st.header(f"🔄 Đang Tối Ưu Hóa {len(selected_files)} File(s)...")

    # Build parameter grid for Ichimoku
    param_grid = {
        'tenkan_period': list(range(tenkan_min, tenkan_max + 1, tenkan_step)),
        'kijun_period': list(range(kijun_min, kijun_max + 1, kijun_step)),
        'senkou_b_period': list(range(senkou_min, senkou_max + 1, senkou_step)),
        'rsi_period': list(range(rsi_period_min, rsi_period_max + 1, rsi_period_step)),
        'rsi_buy_threshold': [x / 10 for x in range(int(rsi_buy_min * 10), int(rsi_buy_max * 10) + 1, int(rsi_buy_step * 10))],
        'rsi_sell_threshold': [x / 10 for x in range(int(rsi_sell_min * 10), int(rsi_sell_max * 10) + 1, int(rsi_sell_step * 10))]
    }

    # Generate all combinations
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())
    combinations = list(product(*param_values))
    total_combinations = len(combinations)

    # Progress tracking
    total_tasks = len(selected_files) * total_combinations
    overall_progress = st.progress(0)
    status_text = st.empty()

    all_results_list = []
    task_count = 0

    # Process each file
    for file_idx, file_info in enumerate(selected_files):
        st.subheader(f"📊 {file_info['symbol']} - {file_info['timeframe']}")

        try:
            # Load data
            data = load_data(file_info['path'], has_header=False)

            st.info(f"✅ Loaded {len(data)} candles from {data['timestamp'].min()} to {data['timestamp'].max()}")

            # Test each combination
            for idx, combo in enumerate(combinations):
                params = dict(zip(param_names, combo))

                # Update progress
                task_count += 1
                progress = task_count / total_tasks
                overall_progress.progress(progress)
                status_text.text(
                    f"File {file_idx+1}/{len(selected_files)}: {file_info['symbol']} {file_info['timeframe']} | "
                    f"Test {idx+1}/{total_combinations} ({progress*100:.1f}%)"
                )

                # Run backtest with Ichimoku strategy
                backtest_result = backtest_strategy(
                    data=data,
                    tenkan_period=params['tenkan_period'],
                    kijun_period=params['kijun_period'],
                    senkou_b_period=params['senkou_b_period'],
                    rsi_period=params['rsi_period'],
                    rsi_buy_threshold=params['rsi_buy_threshold'],
                    rsi_sell_threshold=params['rsi_sell_threshold'],
                    risk_reward_ratio=risk_reward_ratio,
                    sl_buffer_pips=sl_buffer_pips,
                    bars_check_swing=bars_check_swing,
                    spread_pips=spread_pips,
                    lot_size=lot_size,
                    symbol=file_info['symbol']  # Pass symbol to auto-detect JPY pairs
                )

                # Calculate score
                score = calculate_score(backtest_result)
                valid = (
                    backtest_result['total_profit_pips'] > 0 and
                    backtest_result['max_drawdown_pct'] < max_dd_threshold
                )

                # Store result with file info
                result = {
                    'symbol': file_info['symbol'],
                    'timeframe': file_info['timeframe'],
                    'filename': file_info['filename'],
                    'tenkan_period': params['tenkan_period'],
                    'kijun_period': params['kijun_period'],
                    'senkou_b_period': params['senkou_b_period'],
                    'rsi_period': params['rsi_period'],
                    'rsi_buy_threshold': params['rsi_buy_threshold'],
                    'rsi_sell_threshold': params['rsi_sell_threshold'],
                    'risk_reward_ratio': risk_reward_ratio,
                    'total_profit_pips': backtest_result['total_profit_pips'],
                    'num_trades': backtest_result['num_trades'],
                    'win_rate': backtest_result['win_rate'],
                    'profit_factor': backtest_result['profit_factor'],
                    'max_drawdown_pct': backtest_result['max_drawdown_pct'],
                    'score': score,
                    'valid': valid
                }

                all_results_list.append(result)

            st.success(f"✅ {file_info['symbol']} {file_info['timeframe']}: Hoàn thành {total_combinations} tests")

        except Exception as e:
            st.error(f"❌ Lỗi khi xử lý {file_info['filename']}: {str(e)}")

    # Convert to DataFrame
    all_results_df = pd.DataFrame(all_results_list)
    all_results_df = all_results_df.sort_values('score', ascending=False).reset_index(drop=True)

    # Store in session state
    st.session_state.all_results = all_results_df
    st.session_state.optimization_done = True

    # Clear progress
    overall_progress.empty()
    status_text.empty()

    st.success(f"✅ Đã tối ưu hóa {len(selected_files)} file(s) với tổng {len(all_results_df)} kết quả!")

# ============================================================================
# DISPLAY RESULTS
# ============================================================================

if st.session_state.optimization_done and st.session_state.all_results is not None:
    all_results_df = st.session_state.all_results

    st.markdown("---")
    st.header("📊 Kết Quả Tổng Hợp")

    # Overall Statistics
    st.subheader("📈 Thống Kê Tổng Quan")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Tổng Tests", f"{len(all_results_df):,}")
    with col2:
        valid_count = len(all_results_df[all_results_df['valid'] == True])
        st.metric("Kết Quả Hợp Lệ", f"{valid_count:,}", delta=f"{valid_count/len(all_results_df)*100:.1f}%")
    with col3:
        # Count results with 0 trades
        zero_trades = len(all_results_df[all_results_df['num_trades'] == 0])
        st.metric("Không Có Trade", f"{zero_trades:,}", delta=f"{zero_trades/len(all_results_df)*100:.1f}%")
    with col4:
        unique_symbols = all_results_df['symbol'].nunique()
        st.metric("Số Sản Phẩm", unique_symbols)
    with col5:
        unique_files = all_results_df['filename'].nunique()
        st.metric("Số Files", unique_files)

    # Warning if most results have no trades
    if zero_trades > len(all_results_df) * 0.8:
        st.warning(f"⚠️ **{zero_trades/len(all_results_df)*100:.0f}% kết quả không có trade nào!**\n\n"
                   "Nguyên nhân: Ichimoku crossover rất hiếm với dữ liệu ngắn.\n\n"
                   "**Giải pháp:**\n"
                   "1. Sử dụng dữ liệu DÀI HƠN (>6 tháng)\n"
                   "2. Giảm Kijun/Senkou periods để tín hiệu nhạy hơn\n"
                   "3. Hoặc test trên khung thời gian LỚN HƠN (H1, H4, D1)")

    st.markdown("---")

    # Best Results Per Symbol/Timeframe
    st.subheader("🏆 Kết Quả Tốt Nhất Theo File")

    valid_results = all_results_df[all_results_df['valid'] == True]

    if len(valid_results) > 0:
        # Group by file and get best result
        best_per_file = valid_results.groupby(['symbol', 'timeframe', 'filename']).apply(
            lambda x: x.nlargest(1, 'score')
        ).reset_index(drop=True)

        # Display in grid
        for _, row in best_per_file.iterrows():
            col1, col2, col3 = st.columns([1, 2, 2])

            with col1:
                st.markdown(f"### {row['symbol']}")
                st.markdown(f"**{row['timeframe']}**")

            with col2:
                st.markdown("**Tham Số:**")
                st.write(f"Tenkan: {int(row['tenkan_period'])}, Kijun: {int(row['kijun_period'])}, Senkou: {int(row['senkou_b_period'])}")
                st.write(f"RSI: {int(row['rsi_period'])}, Buy>={row['rsi_buy_threshold']:.0f}, Sell<={row['rsi_sell_threshold']:.0f}")

            with col3:
                st.markdown("**Hiệu Suất:**")
                st.write(f"Profit: {row['total_profit_pips']:.2f} pips | WR: {row['win_rate']:.1f}% | Score: {row['score']:.2f}")

            st.markdown("---")
    else:
        st.warning("⚠️ Không có kết quả hợp lệ")

    # Detailed Results Table
    st.subheader("📋 Bảng Kết Quả Chi Tiết")

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        filter_symbol = st.multiselect(
            "Lọc theo Symbol:",
            options=sorted(all_results_df['symbol'].unique()),
            default=sorted(all_results_df['symbol'].unique())
        )

    with col2:
        filter_timeframe = st.multiselect(
            "Lọc theo Timeframe:",
            options=sorted(all_results_df['timeframe'].unique()),
            default=sorted(all_results_df['timeframe'].unique())
        )

    with col3:
        show_all = st.checkbox("Hiển thị TẤT CẢ (bao gồm invalid)", value=False)

    # Apply filters
    filtered_df = all_results_df[
        (all_results_df['symbol'].isin(filter_symbol)) &
        (all_results_df['timeframe'].isin(filter_timeframe))
    ]

    # Filter by valid status if needed
    if not show_all:
        filtered_df = filtered_df[filtered_df['valid'] == True]
        if len(filtered_df) == 0:
            st.info("💡 Không có kết quả hợp lệ. Tick 'Hiển thị TẤT CẢ' để xem tất cả kết quả (bao gồm invalid).")

    # Display
    display_df = filtered_df.copy()
    display_df = display_df.sort_values('score', ascending=False).head(100)

    st.dataframe(
        display_df[[
            'symbol', 'timeframe',
            'tenkan_period', 'kijun_period', 'senkou_b_period',
            'rsi_period', 'rsi_buy_threshold', 'rsi_sell_threshold',
            'total_profit_pips', 'win_rate', 'num_trades',
            'max_drawdown_pct', 'score', 'valid'
        ]],
        use_container_width=True,
        height=400
    )

    # Charts
    st.markdown("---")
    st.subheader("📊 Biểu Đồ Phân Tích")

    # Only show charts if there are valid results
    if len(valid_results) > 0:
        tab1, tab2, tab3 = st.tabs(["📊 By Symbol/Timeframe", "💰 Profit Distribution", "📈 Score Comparison"])

        with tab1:
            # Best score by symbol and timeframe
            fig = px.bar(
                best_per_file,
                x='symbol',
                y='score',
                color='timeframe',
                barmode='group',
                title="Best Score by Symbol and Timeframe",
                labels={'score': 'Score', 'symbol': 'Symbol', 'timeframe': 'Timeframe'}
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            # Profit distribution
            fig = px.box(
                valid_results,
                x='symbol',
                y='total_profit_pips',
                color='timeframe',
                title="Profit Distribution by Symbol and Timeframe",
                labels={'total_profit_pips': 'Profit (pips)', 'symbol': 'Symbol'}
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            # Score comparison scatter
            fig = px.scatter(
                valid_results,
                x='win_rate',
                y='total_profit_pips',
                color='symbol',
                size='score',
                hover_data=['timeframe', 'tenkan_period', 'kijun_period', 'rsi_period', 'rsi_buy_threshold'],
                title="Win Rate vs Profit (Size = Score)",
                labels={'win_rate': 'Win Rate (%)', 'total_profit_pips': 'Profit (pips)'}
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("💡 Không có kết quả hợp lệ để hiển thị biểu đồ. Thử giảm Max DD Threshold hoặc điều chỉnh parameters.")

    # Download
    st.markdown("---")
    st.subheader("💾 Tải Kết Quả")

    csv_data = all_results_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download All Results (CSV)",
        data=csv_data,
        file_name=f"multi_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )

else:
    # Instructions
    st.info("👈 Vui lòng chọn files và nhấn '🚀 Chạy Tối Ưu Hóa' để bắt đầu!")

    st.markdown("### 📚 Hướng Dẫn")

    with st.expander("🎯 Cách Sử Dụng", expanded=True):
        st.markdown("""
        1. **Chuẩn bị files CSV:**
           - Đặt tất cả files vào folder `CSV`
           - Format tên: `SYMBOL` + `TIMEFRAME_MINUTES` + `.csv`
           - Ví dụ: `AUDUSD5.csv`, `EURUSD15.csv`, `GBPUSD30.csv`

        2. **Format CSV:**
           - Không có dòng header
           - Cột: Date, Time, Open, High, Low, Close, Volume
           - Ví dụ: `2025.12.19  3:00  0.66423  0.6643  0.66399  0.6642  156`

        3. **Scan & Select:**
           - Nhấn "Scan Folder" để tìm files
           - Chọn files muốn test (theo symbol/timeframe)

        4. **Cấu hình & Run:**
           - Điều chỉnh tham số RSI và Trading
           - Nhấn "Chạy Tối Ưu Hóa"

        5. **Xem kết quả:**
           - Bảng tổng hợp theo symbol/timeframe
           - Biểu đồ so sánh
           - Download CSV
        """)

    with st.expander("💡 Timeframe Mapping"):
        st.markdown("""
        | File | Timeframe | Mô tả |
        |------|-----------|-------|
        | AUDUSD5.csv | M5 | 5 phút |
        | AUDUSD15.csv | M15 | 15 phút |
        | AUDUSD30.csv | M30 | 30 phút |
        | AUDUSD60.csv | H1 | 1 giờ |
        | AUDUSD240.csv | H4 | 4 giờ |
        | AUDUSD1440.csv | D1 | 1 ngày |
        """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>📊 Multi-Symbol Multi-Timeframe Backtesting System</p>
    <p>Built with Streamlit & Plotly | © 2024</p>
</div>
""", unsafe_allow_html=True)
