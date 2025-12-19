"""
AI-Indicator Backtesting GUI Application
Giao diện đồ họa cho hệ thống tối ưu hóa indicator
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
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="AI-Indicator Optimizer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st.markdown('<h1 class="main-header">📈 AI-Indicator Backtesting & Optimization System</h1>', unsafe_allow_html=True)
st.markdown("### 🚀 Tối ưu hóa tham số Indicator tự động với giao diện trực quan")
st.markdown("---")

# ============================================================================
# SIDEBAR - CONFIGURATION
# ============================================================================

with st.sidebar:
    st.header("⚙️ Cấu Hình")

    # File Selection
    st.subheader("📁 Chọn File Dữ Liệu")

    # List available CSV files
    csv_files = list(Path('.').glob('*.csv'))
    csv_filenames = [f.name for f in csv_files]

    if csv_filenames:
        selected_file = st.selectbox(
            "File CSV:",
            csv_filenames,
            index=csv_filenames.index('AUDCAD15.csv') if 'AUDCAD15.csv' in csv_filenames else 0
        )
    else:
        st.error("❌ Không tìm thấy file CSV nào!")
        st.stop()

    st.markdown("---")

    # Indicator Selection
    st.subheader("📊 Chọn Indicator")
    indicator = st.selectbox(
        "Indicator:",
        ["RSI", "MACD (Coming Soon)", "Bollinger Bands (Coming Soon)"],
        disabled=False
    )

    st.markdown("---")

    # RSI Parameters (only if RSI selected)
    if indicator == "RSI":
        st.subheader("🎯 Tham Số RSI")

        col1, col2 = st.columns(2)
        with col1:
            rsi_period_min = st.number_input("Period Min", 5, 50, 5, 1)
            rsi_period_max = st.number_input("Period Max", 5, 50, 30, 1)

        with col2:
            rsi_period_step = st.number_input("Period Step", 1, 10, 1, 1)

        col3, col4 = st.columns(2)
        with col3:
            overbought_min = st.number_input("Overbought Min", 60, 90, 65, 5)
            overbought_max = st.number_input("Overbought Max", 60, 90, 85, 5)

        with col4:
            overbought_step = st.number_input("OB Step", 1, 10, 5, 1)

        col5, col6 = st.columns(2)
        with col5:
            oversold_min = st.number_input("Oversold Min", 10, 40, 15, 5)
            oversold_max = st.number_input("Oversold Max", 10, 40, 35, 5)

        with col6:
            oversold_step = st.number_input("OS Step", 1, 10, 5, 1)

        # Calculate total combinations
        total_combos = (
            len(range(rsi_period_min, rsi_period_max + 1, rsi_period_step)) *
            len(range(overbought_min, overbought_max + 1, overbought_step)) *
            len(range(oversold_min, oversold_max + 1, oversold_step))
        )

        st.info(f"📊 Tổng combinations: **{total_combos}**")

    st.markdown("---")

    # Trading Parameters
    st.subheader("💰 Tham Số Trading")

    tp_pips = st.number_input("Take Profit (pips)", 5.0, 100.0, 20.0, 1.0)
    sl_pips = st.number_input("Stop Loss (pips)", 5.0, 100.0, 15.0, 1.0)
    spread_pips = st.number_input("Spread (pips)", 0.1, 10.0, 1.2, 0.1)
    lot_size = st.number_input("Lot Size", 0.01, 10.0, 0.1, 0.01)

    st.markdown("---")

    # Optimization Settings
    st.subheader("🔧 Cài Đặt Tối Ưu")

    max_dd_threshold = st.slider("Max Drawdown Threshold (%)", 10, 50, 30, 5)
    top_n_results = st.slider("Top N Results to Display", 5, 20, 10, 1)

    st.markdown("---")

    # Run Button
    run_optimization = st.button("🚀 Chạy Tối Ưu Hóa", use_container_width=True, type="primary")

# ============================================================================
# MAIN AREA
# ============================================================================

# Initialize session state
if 'results_df' not in st.session_state:
    st.session_state.results_df = None
if 'data' not in st.session_state:
    st.session_state.data = None
if 'optimization_done' not in st.session_state:
    st.session_state.optimization_done = False

# ============================================================================
# LOAD DATA (always load selected file to show preview)
# ============================================================================

try:
    data = load_data(selected_file)
    st.session_state.data = data

    # Data Preview
    with st.expander("📊 Xem Trước Dữ Liệu", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📅 Tổng Candles", f"{len(data):,}")
        with col2:
            st.metric("📆 Từ ngày", data['timestamp'].min().strftime('%Y-%m-%d'))
        with col3:
            st.metric("📆 Đến ngày", data['timestamp'].max().strftime('%Y-%m-%d'))

        st.dataframe(data.head(10), use_container_width=True)

        # Simple price chart
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(
            x=data['timestamp'],
            y=data['close'],
            mode='lines',
            name='Close Price',
            line=dict(color='#1f77b4', width=2)
        ))
        fig_price.update_layout(
            title="📈 Biểu Đồ Giá",
            xaxis_title="Thời gian",
            yaxis_title="Giá",
            height=300,
            hovermode='x unified'
        )
        st.plotly_chart(fig_price, use_container_width=True)

except Exception as e:
    st.error(f"❌ Lỗi khi load dữ liệu: {str(e)}")
    st.stop()

# ============================================================================
# RUN OPTIMIZATION
# ============================================================================

if run_optimization:
    st.session_state.optimization_done = False

    with st.spinner("🔄 Đang tối ưu hóa..."):
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Build parameter grid
        if indicator == "RSI":
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

        status_text.text(f"Tổng số combinations: {total_combinations}")

        results = []

        # Run optimization
        for idx, combo in enumerate(combinations):
            params = dict(zip(param_names, combo))

            # Update progress
            progress = (idx + 1) / total_combinations
            progress_bar.progress(progress)
            status_text.text(f"Đang test: {idx + 1}/{total_combinations} ({progress*100:.1f}%)")

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

            # Calculate score with custom max_dd threshold
            score = calculate_score(backtest_result)

            # Check validity with custom threshold
            valid = (
                backtest_result['total_profit_pips'] > 0 and
                backtest_result['max_drawdown_pct'] < max_dd_threshold
            )

            # Store result
            result = {
                'rsi_period': params['rsi_period'],
                'overbought': params['overbought'],
                'oversold': params['oversold'],
                'total_profit_pips': backtest_result['total_profit_pips'],
                'total_profit_currency': backtest_result['total_profit_currency'],
                'num_trades': backtest_result['num_trades'],
                'win_rate': backtest_result['win_rate'],
                'profit_factor': backtest_result['profit_factor'],
                'max_drawdown': backtest_result['max_drawdown'],
                'max_drawdown_pct': backtest_result['max_drawdown_pct'],
                'score': score,
                'valid': valid
            }

            results.append(result)

        # Convert to DataFrame and sort
        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values('score', ascending=False).reset_index(drop=True)

        # Store in session state
        st.session_state.results_df = results_df
        st.session_state.optimization_done = True

        # Clear progress
        progress_bar.empty()
        status_text.empty()

        st.success("✅ Tối ưu hóa hoàn tất!")

# ============================================================================
# DISPLAY RESULTS
# ============================================================================

if st.session_state.optimization_done and st.session_state.results_df is not None:
    results_df = st.session_state.results_df

    st.markdown("---")
    st.header("📊 Kết Quả Tối Ưu Hóa")

    # Summary Statistics
    st.subheader("📈 Tổng Quan")

    col1, col2, col3, col4, col5 = st.columns(5)

    valid_results = results_df[results_df['valid'] == True]

    with col1:
        st.metric("Tổng Số Tests", f"{len(results_df):,}")
    with col2:
        st.metric("Kết Quả Hợp Lệ", f"{len(valid_results):,}",
                 delta=f"{len(valid_results)/len(results_df)*100:.1f}%")
    with col3:
        if len(valid_results) > 0:
            best_profit = valid_results.iloc[0]['total_profit_pips']
            st.metric("Profit Tốt Nhất", f"{best_profit:.2f} pips")
        else:
            st.metric("Profit Tốt Nhất", "N/A")
    with col4:
        if len(valid_results) > 0:
            best_wr = valid_results.iloc[0]['win_rate']
            st.metric("Win Rate Tốt Nhất", f"{best_wr:.1f}%")
        else:
            st.metric("Win Rate Tốt Nhất", "N/A")
    with col5:
        if len(valid_results) > 0:
            best_score = valid_results.iloc[0]['score']
            st.metric("Score Cao Nhất", f"{best_score:.2f}")
        else:
            st.metric("Score Cao Nhất", "N/A")

    st.markdown("---")

    # Best Parameters
    if len(valid_results) > 0:
        st.subheader("🏆 Tham Số Tốt Nhất")

        best = valid_results.iloc[0]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("### 🎯 Tham Số")
            st.markdown(f"**RSI Period:** {int(best['rsi_period'])}")
            st.markdown(f"**Overbought:** {int(best['overbought'])}")
            st.markdown(f"**Oversold:** {int(best['oversold'])}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("### 💰 Hiệu Suất")
            st.markdown(f"**Total Profit:** {best['total_profit_pips']:.2f} pips")
            st.markdown(f"**Win Rate:** {best['win_rate']:.2f}%")
            st.markdown(f"**Profit Factor:** {best['profit_factor']:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("### 📊 Thống Kê")
            st.markdown(f"**Number of Trades:** {int(best['num_trades'])}")
            st.markdown(f"**Max Drawdown:** {best['max_drawdown_pct']:.2f}%")
            st.markdown(f"**Score:** {best['score']:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Không có kết quả hợp lệ. Thử điều chỉnh tham số hoặc ngưỡng Max Drawdown.")

    st.markdown("---")

    # Top N Results Table
    st.subheader(f"📋 Top {top_n_results} Kết Quả")

    display_df = valid_results.head(top_n_results) if len(valid_results) > 0 else results_df.head(top_n_results)
    display_df = display_df.copy()
    display_df.insert(0, 'Rank', range(1, len(display_df) + 1))

    # Format columns
    display_df['total_profit_pips'] = display_df['total_profit_pips'].apply(lambda x: f"{x:.2f}")
    display_df['win_rate'] = display_df['win_rate'].apply(lambda x: f"{x:.2f}%")
    display_df['profit_factor'] = display_df['profit_factor'].apply(lambda x: f"{x:.2f}")
    display_df['max_drawdown_pct'] = display_df['max_drawdown_pct'].apply(lambda x: f"{x:.2f}%")
    display_df['score'] = display_df['score'].apply(lambda x: f"{x:.2f}")

    st.dataframe(
        display_df[[
            'Rank', 'rsi_period', 'overbought', 'oversold',
            'total_profit_pips', 'win_rate', 'profit_factor',
            'num_trades', 'max_drawdown_pct', 'score', 'valid'
        ]],
        use_container_width=True,
        height=400
    )

    st.markdown("---")

    # Charts
    st.subheader("📊 Biểu Đồ Phân Tích")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Ranking", "💰 Profit Analysis", "🎯 Parameter Heatmap", "📈 Scatter Plot"])

    with tab1:
        # Ranking Bar Chart
        st.markdown("#### Biểu Đồ Cột - Top Results by Score")

        top_data = valid_results.head(20) if len(valid_results) > 0 else results_df.head(20)
        top_data = top_data.copy()
        top_data['param_label'] = top_data.apply(
            lambda x: f"RSI({int(x['rsi_period'])}, {int(x['overbought'])}, {int(x['oversold'])})",
            axis=1
        )

        fig_rank = px.bar(
            top_data,
            x='param_label',
            y='score',
            color='valid',
            title="Top 20 Parameter Sets by Score",
            labels={'param_label': 'Parameters', 'score': 'Score', 'valid': 'Valid'},
            color_discrete_map={True: '#2ecc71', False: '#e74c3c'},
            height=500
        )
        fig_rank.update_layout(xaxis_tickangle=-45, hovermode='x unified')
        st.plotly_chart(fig_rank, use_container_width=True)

    with tab2:
        # Profit vs Drawdown Scatter
        st.markdown("#### Profit vs Max Drawdown")

        fig_profit = px.scatter(
            results_df,
            x='max_drawdown_pct',
            y='total_profit_pips',
            size='num_trades',
            color='win_rate',
            hover_data=['rsi_period', 'overbought', 'oversold', 'score'],
            title="Profit vs Drawdown (Size = Number of Trades, Color = Win Rate)",
            labels={
                'max_drawdown_pct': 'Max Drawdown (%)',
                'total_profit_pips': 'Total Profit (pips)',
                'win_rate': 'Win Rate (%)'
            },
            height=500
        )
        fig_profit.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)
        fig_profit.add_vline(x=max_dd_threshold, line_dash="dash", line_color="orange", opacity=0.5,
                           annotation_text=f"Max DD Threshold ({max_dd_threshold}%)")
        st.plotly_chart(fig_profit, use_container_width=True)

    with tab3:
        # Parameter Heatmap
        st.markdown("#### Heatmap - Score by Parameters")

        # Create pivot table for heatmap
        if 'overbought' in results_df.columns and 'oversold' in results_df.columns:
            # Group by overbought and oversold, average score
            heatmap_data = results_df.groupby(['overbought', 'oversold'])['score'].mean().reset_index()
            heatmap_pivot = heatmap_data.pivot(index='oversold', columns='overbought', values='score')

            fig_heatmap = px.imshow(
                heatmap_pivot,
                labels=dict(x="Overbought", y="Oversold", color="Avg Score"),
                x=heatmap_pivot.columns,
                y=heatmap_pivot.index,
                color_continuous_scale='RdYlGn',
                title="Average Score by Overbought/Oversold Levels",
                height=500
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)

    with tab4:
        # Multi-dimensional scatter
        st.markdown("#### Win Rate vs Profit Factor")

        fig_scatter = px.scatter(
            results_df,
            x='win_rate',
            y='profit_factor',
            size='total_profit_pips',
            color='valid',
            hover_data=['rsi_period', 'overbought', 'oversold', 'score', 'num_trades'],
            title="Win Rate vs Profit Factor (Size = Total Profit)",
            labels={
                'win_rate': 'Win Rate (%)',
                'profit_factor': 'Profit Factor',
                'valid': 'Valid Result'
            },
            color_discrete_map={True: '#2ecc71', False: '#e74c3c'},
            height=500
        )
        fig_scatter.add_hline(y=1.0, line_dash="dash", line_color="gray", opacity=0.5,
                            annotation_text="Break-even PF")
        fig_scatter.add_vline(x=50, line_dash="dash", line_color="gray", opacity=0.5,
                            annotation_text="50% Win Rate")
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    # Download Results
    st.subheader("💾 Tải Kết Quả")

    col1, col2 = st.columns(2)

    with col1:
        # Download full results
        csv_full = results_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Tải Tất Cả Kết Quả (CSV)",
            data=csv_full,
            file_name=f"optimization_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:
        # Download valid results only
        if len(valid_results) > 0:
            csv_valid = valid_results.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Tải Kết Quả Hợp Lệ (CSV)",
                data=csv_valid,
                file_name=f"valid_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.button("📥 Tải Kết Quả Hợp Lệ (CSV)", disabled=True, use_container_width=True)

else:
    # Show instructions when no optimization has been run
    st.info("👈 Vui lòng cấu hình tham số bên trái và nhấn '🚀 Chạy Tối Ưu Hóa' để bắt đầu!")

    st.markdown("### 📚 Hướng Dẫn Sử Dụng")

    with st.expander("🎯 Các Bước Thực Hiện", expanded=True):
        st.markdown("""
        1. **Chọn File CSV**: Chọn file dữ liệu OHLCV từ dropdown
        2. **Chọn Indicator**: Hiện tại hỗ trợ RSI (sẽ có thêm MACD, Bollinger Bands)
        3. **Cấu Hình Tham Số**:
           - Đặt khoảng giá trị cho RSI period, overbought, oversold
           - Điều chỉnh Take Profit, Stop Loss, Spread
        4. **Chạy Tối Ưu**: Nhấn nút "🚀 Chạy Tối Ưu Hóa"
        5. **Xem Kết Quả**:
           - Bảng top results
           - Biểu đồ phân tích
           - Tải về file CSV
        """)

    with st.expander("💡 Tips & Tricks"):
        st.markdown("""
        - **Test nhanh**: Dùng khoảng tham số nhỏ (ví dụ: Period 10-20, step 5) để test nhanh
        - **Test đầy đủ**: Dùng khoảng rộng hơn (Period 5-30, step 1) để tìm tham số tối ưu
        - **Max Drawdown Threshold**: Tăng lên nếu không có kết quả hợp lệ
        - **Biểu đồ**: Sử dụng các tab biểu đồ để phân tích mối quan hệ giữa các metric
        - **Download**: Tải kết quả về để phân tích thêm trong Excel
        """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>📈 AI-Indicator Backtesting & Optimization System</p>
    <p>Built with Streamlit & Plotly | © 2024</p>
</div>
""", unsafe_allow_html=True)
