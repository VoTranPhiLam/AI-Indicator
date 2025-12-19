# 🇻🇳 HƯỚNG DẪN SỬ DỤNG HỆ THỐNG BACKTESTING

## 📖 Mục Lục

1. [Cài Đặt](#1-cài-đặt)
2. [Chạy Test Nhanh](#2-chạy-test-nhanh)
3. [Chạy Tối Ưu Hóa Đầy Đủ](#3-chạy-tối-ưu-hóa-đầy-đủ)
4. [Sử Dụng Dữ Liệu Của Bạn](#4-sử-dụng-dữ-liệu-của-bạn)
5. [Hiểu Kết Quả](#5-hiểu-kết-quả)
6. [Tùy Chỉnh Tham Số](#6-tùy-chỉnh-tham-số)
7. [Xử Lý Lỗi](#7-xử-lý-lỗi)

---

## 1. Cài Đặt

### Bước 1.1: Kiểm tra Python

```bash
python --version
```

**Yêu cầu:** Python 3.7 trở lên

### Bước 1.2: Cài đặt thư viện

```bash
pip install pandas numpy
```

### Bước 1.3: Kiểm tra cài đặt

```bash
pip list | grep -E "pandas|numpy"
```

Bạn sẽ thấy:
```
numpy      2.x.x
pandas     2.x.x
```

---

## 2. Chạy Test Nhanh

### 🚀 Cách 1: Test Nhanh (16 combinations - ~1 giây)

```bash
python quick_test.py
```

**Đặc điểm:**
- ✅ Chạy rất nhanh (< 5 giây)
- ✅ Test 16 combinations
- ✅ Thích hợp để hiểu cách hệ thống hoạt động
- ✅ Tạo file `quick_test_results.csv`

**Kết quả mong đợi:**
```
🏆 Tham số tốt nhất:
   RSI Period:    22
   Overbought:    70
   Oversold:      20

💰 Hiệu suất:
   Profit:        13.00 pips
   Win Rate:      50.00%
   Số lệnh:       10
```

---

## 3. Chạy Tối Ưu Hóa Đầy Đủ

### 🎯 Cách 2: Tối Ưu Đầy Đủ (650 combinations - ~5-10 giây)

```bash
python backtest_optimizer.py
```

**Đặc điểm:**
- ✅ Test 650 combinations
- ✅ Tìm tham số tối ưu nhất
- ✅ Chính xác hơn
- ✅ Tạo file `results.csv` (86 KB)

**Tham số test:**
- RSI Period: 5 → 30 (26 giá trị)
- Overbought: 65 → 85 (5 giá trị)
- Oversold: 15 → 35 (5 giá trị)

**Kết quả mong đợi:**
```
★ BEST PARAMETERS ★
RSI Period:   18
Overbought:   85
Oversold:     25

Total Profit:   56.40 pips
Win Rate:       100.00%
Score:          1056.25
```

---

## 4. Sử Dụng Dữ Liệu Của Bạn

### Bước 4.1: Chuẩn bị dữ liệu CSV

File CSV cần có định dạng:

```csv
Date,Time,Open,High,Low,Close,Volume
2024.01.01,00:00,0.89500,0.89520,0.89480,0.89510,150
2024.01.01,00:15,0.89510,0.89530,0.89490,0.89520,200
2024.01.01,00:30,0.89520,0.89540,0.89500,0.89530,180
```

**Lưu ý:**
- ✅ Phân tách bằng dấu phẩy (,)
- ✅ Cột Date format: YYYY.MM.DD
- ✅ Cột Time format: HH:MM
- ✅ Giá phải là số thập phân (dùng dấu chấm .)

### Bước 4.2: Thay thế file dữ liệu

**Cách 1:** Đổi tên file của bạn thành `AUDCAD15.csv`

```bash
mv your_data.csv AUDCAD15.csv
```

**Cách 2:** Sửa tên file trong code

Mở file `backtest_optimizer.py` hoặc `quick_test.py`, tìm dòng:

```python
data_file = 'AUDCAD15.csv'
```

Đổi thành:

```python
data_file = 'TEN_FILE_CUA_BAN.csv'
```

### Bước 4.3: Chạy lại

```bash
python backtest_optimizer.py
```

---

## 5. Hiểu Kết Quả

### 📊 Các Chỉ Số Quan Trọng

| Chỉ số | Giải thích | Ý nghĩa |
|--------|-----------|---------|
| **Total Profit** | Tổng lợi nhuận (pips) | Càng cao càng tốt |
| **Win Rate** | Tỷ lệ lệnh thắng (%) | > 50% là tốt |
| **Profit Factor** | Tỷ số Lời/Lỗ | > 1.5 là tốt |
| **Max Drawdown** | Sụt giảm lớn nhất (%) | < 20% là tốt |
| **Number Trades** | Số lệnh giao dịch | Đủ để có ý nghĩa thống kê (> 30) |
| **Score** | Điểm tổng hợp | Càng cao càng tốt |

### 🎯 Cách Đọc Kết Quả

#### Ví dụ kết quả TỐT:
```
Total Profit:   56.40 pips  ✅ Lợi nhuận dương
Win Rate:       100.00%     ✅ Tỷ lệ thắng cao
Profit Factor:  56.40       ✅ Lời nhiều hơn lỗ
Max Drawdown:   0.00%       ✅ Rủi ro thấp
Number Trades:  3           ⚠️ Ít lệnh (cần nhiều data hơn)
Score:          1056.25     ✅ Điểm cao
```

#### Ví dụ kết quả TRUNG BÌNH:
```
Total Profit:   13.00 pips  ✅ Có lời nhưng ít
Win Rate:       50.00%      ⚠️ Trung bình
Profit Factor:  1.16        ⚠️ Lời/lỗ gần bằng nhau
Max Drawdown:   4.85%       ✅ Rủi ro thấp
Number Trades:  10          ⚠️ Đủ để tham khảo
Score:          478.48      ⚠️ Điểm trung bình
```

### 📁 File Kết Quả

#### 1. File `results.csv`
- Chứa **TẤT CẢ** kết quả test
- Mở bằng Excel/Google Sheets
- Có thể sắp xếp theo cột `score` để tìm tham số tốt nhất

#### 2. Console Output
- Hiển thị Top 10 tham số tốt nhất
- Rank #1 là **BEST PARAMETERS** (tham số tốt nhất)

---

## 6. Tùy Chỉnh Tham Số

### 🔧 Thay Đổi Trading Rules

Mở file `backtest_optimizer.py`, tìm phần:

```python
# Trading parameters
tp_pips = 20.0        # Take Profit
sl_pips = 15.0        # Stop Loss
spread_pips = 1.2     # Spread
lot_size = 0.1        # Kích thước lệnh
```

**Ví dụ tùy chỉnh:**

```python
tp_pips = 30.0        # Tăng TP lên 30 pips
sl_pips = 10.0        # Giảm SL xuống 10 pips
spread_pips = 2.0     # Spread cao hơn (broker kém)
lot_size = 0.5        # Lệnh lớn hơn
```

### 🎯 Thay Đổi Khoảng Tham Số RSI

Tìm phần:

```python
param_grid = {
    'rsi_period': list(range(5, 31)),      # 5 đến 30
    'overbought': list(range(65, 90, 5)),  # 65, 70, 75, 80, 85
    'oversold': list(range(15, 40, 5))     # 15, 20, 25, 30, 35
}
```

**Ví dụ: Test khoảng hẹp hơn (nhanh hơn):**

```python
param_grid = {
    'rsi_period': list(range(10, 21)),     # 10 đến 20
    'overbought': [70, 80],                # Chỉ test 2 giá trị
    'oversold': [20, 30]                   # Chỉ test 2 giá trị
}
# Tổng: 11 x 2 x 2 = 44 combinations
```

**Ví dụ: Test chi tiết hơn:**

```python
param_grid = {
    'rsi_period': list(range(5, 31)),      # 5 đến 30
    'overbought': list(range(65, 91, 1)),  # 65 đến 90 (step 1)
    'oversold': list(range(15, 36, 1))     # 15 đến 35 (step 1)
}
# Tổng: 26 x 26 x 21 = 14,196 combinations (chạy lâu!)
```

### 💡 Thay Đổi Scoring Function

Tìm hàm `calculate_score()`:

```python
def calculate_score(metrics: Dict) -> float:
    profit = metrics['total_profit_pips']
    max_dd = abs(metrics['max_drawdown'])
    win_rate = metrics['win_rate']
    num_trades = metrics['num_trades']

    # Tùy chỉnh trọng số ở đây
    score = (
        profit * 1.0          # Trọng số cho profit
        - max_dd * 0.7        # Phạt drawdown
        + win_rate * 10       # Thưởng win rate
        - num_trades * 0.05   # Phạt nhẹ overtrade
    )

    return score
```

**Ví dụ: Ưu tiên Win Rate hơn:**

```python
score = (
    profit * 0.5          # Giảm trọng số profit
    - max_dd * 0.7
    + win_rate * 20       # Tăng trọng số win rate
    - num_trades * 0.05
)
```

**Ví dụ: Ưu tiên Profit Factor:**

```python
profit_factor = metrics['profit_factor']

score = (
    profit * 1.0
    - max_dd * 0.5
    + profit_factor * 100  # Thêm profit factor
    - num_trades * 0.1
)
```

---

## 7. Xử Lý Lỗi

### ❌ Lỗi 1: "File not found"

```
❌ ERROR: File 'AUDCAD15.csv' not found!
```

**Nguyên nhân:** Không tìm thấy file dữ liệu

**Giải pháp:**
```bash
# Kiểm tra file có tồn tại không
ls *.csv

# Tạo dữ liệu mẫu
python generate_sample_data.py

# Hoặc đổi tên file của bạn
mv your_file.csv AUDCAD15.csv
```

---

### ❌ Lỗi 2: "No module named pandas"

```
ModuleNotFoundError: No module named 'pandas'
```

**Nguyên nhân:** Chưa cài thư viện

**Giải pháp:**
```bash
pip install pandas numpy
```

---

### ❌ Lỗi 3: "No valid results found"

```
⚠ WARNING: No valid results found!
```

**Nguyên nhân:** Không có tham số nào đạt tiêu chuẩn:
- Profit > 0
- Max Drawdown < 30%

**Giải pháp:**

1. **Nới lỏng tiêu chuẩn** - Mở file `backtest_optimizer.py`, tìm hàm `is_valid_result()`:

```python
def is_valid_result(metrics: Dict) -> bool:
    if metrics['total_profit_pips'] <= 0:
        return False

    if metrics['max_drawdown_pct'] >= 50.0:  # Thay 30.0 → 50.0
        return False

    return True
```

2. **Thử tham số khác:**
   - Thay đổi TP/SL
   - Thay đổi khoảng RSI
   - Sử dụng dữ liệu khác

---

### ❌ Lỗi 4: "Invalid CSV format"

```
❌ ERROR: Missing required column: close
```

**Nguyên nhân:** File CSV sai format

**Giải pháp:**

Đảm bảo CSV có đủ các cột:
- `Date` hoặc `date`
- `Time` hoặc `time`
- `Open` hoặc `open`
- `High` hoặc `high`
- `Low` hoặc `low`
- `Close` hoặc `close`
- `Volume` hoặc `volume`

---

## 📋 Checklist Test Nhanh

- [ ] Đã cài Python 3.7+
- [ ] Đã cài pandas và numpy
- [ ] Đã có file AUDCAD15.csv (hoặc dữ liệu của bạn)
- [ ] Chạy `python quick_test.py` thành công
- [ ] Hiểu được kết quả trong console
- [ ] Mở được file `quick_test_results.csv` bằng Excel

---

## 🎓 Tiến Trình Học Tập Đề Xuất

### Bước 1: Test Cơ Bản
```bash
python quick_test.py
```
→ Hiểu cách hệ thống hoạt động

### Bước 2: Test Đầy Đủ
```bash
python backtest_optimizer.py
```
→ Xem kết quả với 650 combinations

### Bước 3: Tùy Chỉnh Tham Số
→ Thay đổi TP/SL, spread, lot size

### Bước 4: Test Với Dữ Liệu Thật
→ Sử dụng dữ liệu trading của bạn

### Bước 5: Tối Ưu Scoring Function
→ Tùy chỉnh cách đánh giá tham số

---

## 💡 Tips & Tricks

### 1. Test với nhiều data hơn
- Dữ liệu càng nhiều → kết quả càng đáng tin
- Nên có ít nhất 1000+ candles
- Thử nhiều khoảng thời gian khác nhau

### 2. Kiểm tra overfitting
- Test tham số tốt nhất trên dữ liệu mới
- Nếu kết quả khác xa → overfitting
- Cần thêm validation set

### 3. Sử dụng out-of-sample testing
- Chia data: 70% train, 30% test
- Tìm tham số tốt trên 70% đầu
- Kiểm tra trên 30% cuối

### 4. Kết hợp nhiều chỉ số
- Không chỉ dựa vào profit
- Xem xét win rate, drawdown, profit factor
- Ưu tiên tham số ổn định hơn profit cao nhất

---

## 📞 Hỗ Trợ

Nếu gặp lỗi không có trong hướng dẫn:

1. Kiểm tra lại từng bước
2. Đọc thông báo lỗi kỹ
3. Google thông báo lỗi
4. Hỏi AI (ChatGPT, Claude) với đầy đủ thông tin lỗi

---

## ✅ Kết Luận

Bạn đã có:
- ✅ Hệ thống backtesting chuyên nghiệp
- ✅ Khả năng test 650+ tham số tự động
- ✅ Công cụ tìm tham số tối ưu
- ✅ Hướng dẫn chi tiết bằng tiếng Việt

**Chúc bạn tìm được bộ tham số hiệu quả! 🚀**

---

*Tài liệu này là phần của AI-Indicator Backtesting System*
*Cập nhật lần cuối: 2024*
