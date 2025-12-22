# 🌐 HƯỚNG DẪN MULTI-SYMBOL MULTI-TIMEFRAME GUI

## 📋 Mục Lục

1. [Giới Thiệu](#giới-thiệu)
2. [Chuẩn Bị Files CSV](#chuẩn-bị-files-csv)
3. [Khởi Động GUI](#khởi-động-gui)
4. [Sử Dụng Giao Diện](#sử-dụng-giao-diện)
5. [Hiểu Kết Quả](#hiểu-kết-quả)
6. [Tips & Tricks](#tips--tricks)

---

## 🎯 Giới Thiệu

**Multi-Symbol Multi-Timeframe Optimizer** cho phép bạn:

✅ Chạy tối ưu hóa đồng thời nhiều sản phẩm (AUDUSD, EURUSD, GBPUSD, ...)
✅ Test trên nhiều khung thời gian (M5, M15, M30, H1, H4, D1, ...)
✅ So sánh kết quả giữa các symbol và timeframe
✅ Tìm tham số tối ưu cho từng cặp symbol-timeframe

---

## 📁 Chuẩn Bị Files CSV

### Bước 1: Tạo Folder CSV

Tạo folder `CSV` cùng cấp với các file Python:

```
AI-Indicator/
├── CSV/                  ← Folder chứa files CSV
│   ├── AUDUSD5.csv
│   ├── AUDUSD15.csv
│   ├── EURUSD5.csv
│   └── ...
├── gui_app_multi.py
└── ...
```

### Bước 2: Format File CSV

**QUAN TRỌNG:** Files CSV **KHÔNG CÓ HEADER** (dòng đầu tiên)

**Format:**
- Cột 1: Date (YYYY.MM.DD)
- Cột 2: Time (HH:MM)
- Cột 3: Open
- Cột 4: High
- Cột 5: Low
- Cột 6: Close
- Cột 7: Volume
- **Phân tách:** Tab hoặc khoảng trắng

**Ví dụ:**
```
2025.12.19	3:00	0.66423	0.6643	0.66399	0.6642	156
2025.12.19	3:05	0.66421	0.66426	0.66377	0.66378	178
2025.12.19	3:10	0.66377	0.66386	0.66362	0.66385	159
```

### Bước 3: Quy Tắc Đặt Tên File

**Format:** `SYMBOL` + `TIMEFRAME_MINUTES` + `.csv`

| File | Symbol | Timeframe | Minutes |
|------|--------|-----------|---------|
| `AUDUSD5.csv` | AUDUSD | M5 | 5 |
| `AUDUSD15.csv` | AUDUSD | M15 | 15 |
| `AUDUSD30.csv` | AUDUSD | M30 | 30 |
| `AUDUSD60.csv` | AUDUSD | H1 | 60 |
| `AUDUSD240.csv` | AUDUSD | H4 | 240 |
| `AUDUSD1440.csv` | AUDUSD | D1 | 1440 |
| `EURUSD5.csv` | EURUSD | M5 | 5 |
| `GBPUSD15.csv` | GBPUSD | M15 | 15 |

**Lưu ý:**
- Symbol phải viết HOA (AUDUSD, EURUSD, GBPUSD, ...)
- Số phút phải chính xác (5, 15, 30, 60, 240, 1440, ...)

### Bước 4: Tạo Sample Files (Optional)

Chạy script để tạo files mẫu:

```bash
python generate_multi_csv.py
```

Kết quả: 16 files mẫu trong folder `CSV/`:
- 4 symbols: AUDUSD, EURUSD, GBPUSD, USDJPY
- 4 timeframes: M5, M15, M30, H1

---

## 🚀 Khởi Động GUI

### Cách 1: Dùng File .BAT (Windows - Dễ nhất)

Double-click file:
```
run_multi_gui.bat
```

### Cách 2: Command Line

```bash
streamlit run gui_app_multi.py
```

### Kết Quả

Browser tự động mở:
```
http://localhost:8501
```

---

## 🖱️ Sử Dụng Giao Diện

### Bước 1: Scan Folder CSV 📁

1. Trong sidebar, kiểm tra đường dẫn folder:
   ```
   Đường dẫn folder CSV: CSV
   ```

2. Nhấn nút **"🔍 Scan Folder"**

3. Hệ thống sẽ tìm và hiển thị tất cả files CSV

### Bước 2: Chọn Files 📊

**Option A: Chọn tất cả**

Tick vào checkbox **"✅ Chọn tất cả"**

**Option B: Chọn theo symbol**

Mở rộng từng symbol và chọn timeframe:

```
┌─────────────────────────────────┐
│ 💱 AUDUSD                       │
│   ☑ M5 (102.4 KB)              │
│   ☑ M15 (102.4 KB)             │
│   ☑ M30 (76.8 KB)              │
│   ☐ H1 (51.2 KB)               │
│                                  │
│ 💱 EURUSD                       │
│   ☑ M5 (102.4 KB)              │
│   ☑ M15 (102.4 KB)             │
│   ...                            │
└─────────────────────────────────┘
```

Số file đã chọn hiển thị ở dưới:
```
📌 Đã chọn: 12 file(s)
```

### Bước 3: Cấu Hình Tham Số 🎯

#### RSI Parameters

```
Period Min:  10
Period Max:  20
Period Step: 2
→ Test: 10, 12, 14, 16, 18, 20 (6 giá trị)

Overbought Min:  70
Overbought Max:  80
OB Step:         10
→ Test: 70, 80 (2 giá trị)

Oversold Min:    20
Oversold Max:    30
OS Step:         10
→ Test: 20, 30 (2 giá trị)
```

**Tổng combinations:** 6 × 2 × 2 = **24 tests per file**

#### Trading Parameters

```
Take Profit:  20.0 pips
Stop Loss:    15.0 pips
Spread:       1.2 pips
Lot Size:     0.1
```

#### Optimization Settings

```
Max DD Threshold: 30%
```

### Bước 4: Chạy Tối Ưu Hóa 🚀

Nhấn nút **"🚀 Chạy Tối Ưu Hóa"**

**Progress tracking:**
```
🔄 Đang Tối Ưu Hóa 12 File(s)...

File 3/12: AUDUSD M30 | Test 18/24 (37.5%)
[████████░░░░░░░░░░░░░] 37.5%

📊 AUDUSD - M5
✅ Loaded 2000 candles from 2025-11-19 to 2025-12-19
✅ AUDUSD M5: Hoàn thành 24 tests

📊 AUDUSD - M15
✅ Loaded 2000 candles from 2025-11-19 to 2025-12-19
✅ AUDUSD M15: Hoàn thành 24 tests

...
```

**Thời gian ước tính:**
- 12 files × 24 tests = 288 total tests
- ~2-5 giây

---

## 📊 Hiểu Kết Quả

### 1. Thống Kê Tổng Quan 📈

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Tổng Tests  │ KQ Hợp Lệ   │ Số Sản Phẩm │ Số Files    │
├─────────────┼─────────────┼─────────────┼─────────────┤
│    288      │  156 (54%)  │     4       │     12      │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

**Giải thích:**
- **Tổng Tests:** Tổng số parameter combinations đã test
- **KQ Hợp Lệ:** Số kết quả có profit > 0 và DD < threshold
- **Số Sản Phẩm:** Số symbol khác nhau
- **Số Files:** Số file (symbol-timeframe combinations)

### 2. Kết Quả Tốt Nhất Theo File 🏆

Hiển thị tham số tốt nhất cho từng symbol-timeframe:

```
╔══════════════════════════════════════════════════════════╗
║  AUDUSD                                                  ║
║  M5                                                      ║
╠══════════════════════════════════════════════════════════╣
║  Tham Số:                    Hiệu Suất:                 ║
║  Period: 14, OB: 70, OS: 30  Profit: 45.2 pips          ║
║                               WR: 65.5%                  ║
║                               Score: 856.3               ║
╚══════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════╗
║  AUDUSD                                                  ║
║  M15                                                     ║
╠══════════════════════════════════════════════════════════╣
║  Tham Số:                    Hiệu Suất:                 ║
║  Period: 16, OB: 80, OS: 20  Profit: 62.8 pips          ║
║                               WR: 72.1%                  ║
║                               Score: 1024.7              ║
╚══════════════════════════════════════════════════════════╝
```

**Cách đọc:**
- Mỗi box = 1 file (symbol + timeframe)
- **Tham Số:** Best parameters tìm được
- **Hiệu Suất:** Profit, Win Rate, Score

### 3. Bảng Kết Quả Chi Tiết 📋

**Filters:**

```
Lọc theo Symbol:     [AUDUSD] [EURUSD] [GBPUSD] [USDJPY]
Lọc theo Timeframe:  [M5] [M15] [M30] [H1]
```

**Bảng:**

| Symbol | TF | Period | OB | OS | Profit | WR | Trades | DD | Score | Valid |
|--------|----|----|----|----|--------|-----|--------|-----|-------|-------|
| EURUSD | M15 | 16 | 80 | 20 | 62.8 | 72.1% | 18 | 8.5% | 1024.7 | ✓ |
| AUDUSD | M5 | 14 | 70 | 30 | 45.2 | 65.5% | 22 | 12.3% | 856.3 | ✓ |

**Sắp xếp:** Theo Score (cao nhất trước)

### 4. Biểu Đồ 📊

#### Tab 1: By Symbol/Timeframe (Bar Chart)

```
Score
1200 │         ██
1000 │      ██ ██ ██
 800 │   ██ ██ ██ ██ ██
 600 │ ██ ██ ██ ██ ██ ██
     └─┴──┴──┴──┴──┴──┴──
      AUDUSD  EURUSD  GBPUSD
       M5 M15 M5 M15 M5 M15
```

**Màu sắc:** Mỗi timeframe một màu

**Cách đọc:**
- So sánh score giữa các symbol
- So sánh score giữa các timeframe

#### Tab 2: Profit Distribution (Box Plot)

```
Profit
(pips)
  80 │    ●
     │   ┌─┐
  60 │   │▓│  ●
     │ ┌─┼─┼─┐
  40 │ │▓│▓│▓│
     │ └─┴─┴─┘
  20 │    ●
     └─┴──┴──┴──
      AUDUSD EURUSD GBPUSD
```

**Cách đọc:**
- Box: Q1 - Q3 (50% giữa)
- Line: Median
- Whiskers: Min-Max
- Dots: Outliers

#### Tab 3: Score Comparison (Scatter)

```
Profit
(pips)
  80 │         ●  ← Large bubble = High score
     │       ●   ●
  60 │     ●   ●
     │   ●       ● ← Color = Symbol
  40 │ ●   ●
     └─────────────────► Win Rate (%)
       0  20  40  60  80
```

**Màu sắc:** Mỗi symbol một màu
**Size:** Bubble lớn hơn = Score cao hơn

### 5. Download Kết Quả 💾

Nhấn **"📥 Download All Results (CSV)"**

File tải về: `multi_optimization_YYYYMMDD_HHMMSS.csv`

**Columns:**
```csv
symbol,timeframe,filename,rsi_period,overbought,oversold,
total_profit_pips,num_trades,win_rate,profit_factor,
max_drawdown_pct,score,valid
EURUSD,M15,EURUSD15.csv,16,80,20,62.8,18,72.1,2.45,8.5,1024.7,True
AUDUSD,M5,AUDUSD5.csv,14,70,30,45.2,22,65.5,1.89,12.3,856.3,True
...
```

**Mở bằng:** Excel, Google Sheets

---

## 💡 Tips & Tricks

### 1. Chọn Files Hiệu Quả

**Test nhanh:**
- Chọn 1-2 symbols
- Chọn 1-2 timeframes
- Dùng khoảng tham số nhỏ (step lớn)

**Test đầy đủ:**
- Chọn tất cả files
- Dùng step nhỏ (1-2) để chi tiết hơn

### 2. Phân Tích Kết Quả

**So sánh theo Symbol:**
- Symbol nào có nhiều kết quả valid nhất?
- Symbol nào có profit cao nhất?

**So sánh theo Timeframe:**
- Timeframe nào ổn định hơn (ít DD)?
- Timeframe nào có win rate cao hơn?

**Tìm Pattern:**
- Tham số nào xuất hiện nhiều ở top results?
- Có tham số "vàng" chung cho nhiều symbol/TF không?

### 3. Tối Ưu Hiệu Suất

**Giảm thời gian test:**
- Dùng step lớn hơn (5-10)
- Test ít files hơn
- Thu hẹp khoảng tham số

**Tăng độ chính xác:**
- Dùng step nhỏ (1-2)
- Test trên nhiều files
- Khoảng tham số rộng hơn

### 4. Xử Lý "No Valid Results"

Nếu không có kết quả hợp lệ:

1. **Nới lỏng Max DD Threshold:**
   - Tăng từ 30% → 50%

2. **Điều chỉnh TP/SL:**
   - TP quá cao → Giảm xuống
   - SL quá thấp → Tăng lên

3. **Thử khoảng tham số khác:**
   - RSI period: 5-30
   - Overbought: 60-90
   - Oversold: 10-40

### 5. Best Practices

**Trước khi chạy:**
- ✅ Kiểm tra format CSV đúng (no header)
- ✅ Kiểm tra tên file đúng quy tắc
- ✅ Test với 1-2 files trước khi chạy toàn bộ

**Sau khi có kết quả:**
- ✅ Download CSV để backup
- ✅ So sánh với các lần test trước
- ✅ Ghi chú lại tham số tốt nhất

---

## ❌ Xử Lý Lỗi

### Lỗi 1: "Không tìm thấy file CSV"

**Nguyên nhân:** Folder CSV không tồn tại hoặc sai đường dẫn

**Giải pháp:**
```bash
# Tạo folder CSV
mkdir CSV

# Hoặc sửa đường dẫn trong GUI
Đường dẫn folder CSV: D:\AI-Indicator\CSV
```

### Lỗi 2: "Error parsing filename"

**Nguyên nhân:** Tên file không đúng format

**Giải pháp:**

❌ SAI:
- `audusd_5.csv` (lowercase)
- `AUDUSD-5.csv` (có dấu -)
- `AUDUSD_M5.csv` (có chữ M)

✅ ĐÚNG:
- `AUDUSD5.csv`
- `EURUSD15.csv`
- `GBPUSD30.csv`

### Lỗi 3: "Missing required column"

**Nguyên nhân:** CSV format sai

**Giải pháp:**

Kiểm tra CSV:
- ✅ 7 cột (Date Time Open High Low Close Volume)
- ✅ Không có header
- ✅ Phân tách bằng tab/space
- ✅ Date format: YYYY.MM.DD
- ✅ Time format: HH:MM

### Lỗi 4: "No files selected"

**Nguyên nhân:** Chưa chọn file nào

**Giải pháp:**
1. Nhấn "Scan Folder"
2. Tick vào các checkbox để chọn files
3. Nhấn "Chạy Tối Ưu Hóa"

---

## 📚 Ví Dụ Workflow

### Workflow 1: Test Nhanh (2 phút)

```
1. Scan folder
2. Chọn: AUDUSD M5, AUDUSD M15 (2 files)
3. Cấu hình:
   - Period: 10-20, step 5 (3 giá trị)
   - OB: 70-80, step 10 (2 giá trị)
   - OS: 20-30, step 10 (2 giá trị)
   → 3×2×2 = 12 tests/file = 24 total
4. Chạy
5. Xem kết quả
```

### Workflow 2: Test Đầy Đủ (5-10 phút)

```
1. Scan folder
2. Chọn tất cả files (16 files)
3. Cấu hình:
   - Period: 5-30, step 1 (26 giá trị)
   - OB: 65-85, step 5 (5 giá trị)
   - OS: 15-35, step 5 (5 giá trị)
   → 26×5×5 = 650 tests/file = 10,400 total
4. Chạy (5-10 phút)
5. Download CSV
6. Phân tích trong Excel
```

### Workflow 3: Fine-tuning (3 phút)

```
1. Từ kết quả test đầy đủ, chọn best parameters
   Ví dụ: Period=14, OB=75, OS=25

2. Test lại với khoảng hẹp:
   - Period: 12-16, step 1 (5 giá trị)
   - OB: 70-80, step 2 (6 giá trị)
   - OS: 20-30, step 2 (6 giá trị)
   → 5×6×6 = 180 tests/file

3. So sánh kết quả
```

---

## ✅ Checklist

- [ ] Folder CSV đã tạo
- [ ] Files CSV đúng format (no header, 7 cột)
- [ ] Tên files đúng quy tắc (SYMBOL + MINUTES)
- [ ] Đã cài streamlit (`pip install streamlit`)
- [ ] Chạy được GUI (`streamlit run gui_app_multi.py`)
- [ ] Scan folder thành công
- [ ] Chọn được files
- [ ] Chạy optimization thành công
- [ ] Xem được kết quả và biểu đồ
- [ ] Download được CSV

---

## 🎓 Kết Luận

**Multi-Symbol Multi-Timeframe Optimizer** giúp bạn:

✅ Tối ưu hóa hàng trăm tests đồng thời
✅ So sánh kết quả across symbols & timeframes
✅ Tìm tham số phù hợp cho từng sản phẩm
✅ Phân tích với biểu đồ trực quan
✅ Export kết quả để phân tích sâu hơn

**Bắt đầu ngay:**

```bash
streamlit run gui_app_multi.py
```

---

**🚀 Chúc bạn tìm được bộ tham số tối ưu cho tất cả các sản phẩm!**

---

*Multi-Symbol Multi-Timeframe Backtesting System*
*© 2024*
