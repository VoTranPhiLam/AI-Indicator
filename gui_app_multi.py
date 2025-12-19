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
    st.subheader("📊 Indicator")
    indicator = st.selectbox("Chọn indicator:", ["RSI"])

    st.markdown("---")

    # RSI Parameters
    if indicator == "RSI":
        st.subheader("🎯 Tham Số RSI")

        col1, col2 = st.columns(2)
        with col1:
            rsi_period_min = st.number_input("Period Min", 5, 50, 10, 1)
            rsi_period_max = st.number_input("Period Max", 5, 50, 20, 1)
        with col2:
            rsi_period_step = st.number_input("Period Step", 1, 10, 2, 1)

        col3, col4 = st.columns(2)
        with col3:
            overbought_min = st.number_input("OB Min", 60, 90, 70, 5)
            overbought_max = st.number_input("OB Max", 60, 90, 80, 5)
        with col4:
            overbought_step = st.number_input("OB Step", 1, 10, 10, 1)

        col5, col6 = st.columns(2)
        with col5:
            oversold_min = st.number_input("OS Min", 10, 40, 20, 5)
            oversold_max = st.number_input("OS Max", 10, 40, 30, 5)
        with col6:
            oversold_step = st.number_input("OS Step", 1, 10, 10, 1)

        # Calculate total combinations
        total_combos = (
            len(range(rsi_period_min, rsi_period_max + 1, rsi_period_step)) *
            len(range(overbought_min, overbought_max + 1, overbought_step)) *
            len(range(oversold_min, oversold_max + 1, oversold_step))
        )

        st.info(f"📊 Tests per file: **{total_combos}**")

    st.markdown("---")

    # Trading Parameters
    st.subheader("💰 Tham Số Trading")

    tp_pips = st.number_input("Take Profit (pips)", 5.0, 100.0, 20.0, 1.0)
    sl_pips = st.number_input("Stop Loss (pips)", 5.0, 100.0, 15.0, 1.0)
    spread_pips = st.number_input("Spread (pips)", 0.1, 10.0, 1.2, 0.1)
    lot_size = st.number_input("Lot Size", 0.01, 10.0, 0.1, 0.01)

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

    # Build parameter grid
    param_grid = {
        'rsi_period': list(range(rsi_period_min, rsi_period_max + 1, rsi_period_step)),
        'overbought': list(range(overbought_min, overbought_max + 1, overbought_step)),
        'oversold': list(range(oversold_min, oversold_max + 1, oversold_step))
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
                valid = (
                    backtest_result['total_profit_pips'] > 0 and
                    backtest_result['max_drawdown_pct'] < max_dd_threshold
                )

                # Store result with file info
                result = {
                    'symbol': file_info['symbol'],
                    'timeframe': file_info['timeframe'],
                    'filename': file_info['filename'],
                    'rsi_period': params['rsi_period'],
                    'overbought': params['overbought'],
                    'oversold': params['oversold'],
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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Tổng Tests", f"{len(all_results_df):,}")
    with col2:
        valid_count = len(all_results_df[all_results_df['valid'] == True])
        st.metric("Kết Quả Hợp Lệ", f"{valid_count:,}", delta=f"{valid_count/len(all_results_df)*100:.1f}%")
    with col3:
        unique_symbols = all_results_df['symbol'].nunique()
        st.metric("Số Sản Phẩm", unique_symbols)
    with col4:
        unique_files = all_results_df['filename'].nunique()
        st.metric("Số Files", unique_files)

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
                st.write(f"Period: {int(row['rsi_period'])}, OB: {int(row['overbought'])}, OS: {int(row['oversold'])}")

            with col3:
                st.markdown("**Hiệu Suất:**")
                st.write(f"Profit: {row['total_profit_pips']:.2f} pips | WR: {row['win_rate']:.1f}% | Score: {row['score']:.2f}")

            st.markdown("---")
    else:
        st.warning("⚠️ Không có kết quả hợp lệ")

    # Detailed Results Table
    st.subheader("📋 Bảng Kết Quả Chi Tiết")

    # Filters
    col1, col2 = st.columns(2)

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

    # Apply filters
    filtered_df = all_results_df[
        (all_results_df['symbol'].isin(filter_symbol)) &
        (all_results_df['timeframe'].isin(filter_timeframe))
    ]

    # Display
    display_df = filtered_df.copy()
    display_df = display_df.sort_values('score', ascending=False).head(100)

    st.dataframe(
        display_df[[
            'symbol', 'timeframe', 'rsi_period', 'overbought', 'oversold',
            'total_profit_pips', 'win_rate', 'num_trades',
            'max_drawdown_pct', 'score', 'valid'
        ]],
        use_container_width=True,
        height=400
    )

    # Charts
    st.markdown("---")
    st.subheader("📊 Biểu Đồ Phân Tích")

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
            hover_data=['timeframe', 'rsi_period', 'overbought', 'oversold'],
            title="Win Rate vs Profit (Size = Score)",
            labels={'win_rate': 'Win Rate (%)', 'total_profit_pips': 'Profit (pips)'}
        )
        st.plotly_chart(fig, use_container_width=True)

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
