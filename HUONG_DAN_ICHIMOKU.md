# 📊 HƯỚNG DẪN CHIẾN LƯỢC ICHIMOKU + RSI FILTER

## 🎯 TỔNG QUAN

Hệ thống đã được **THAY ĐỔI HOÀN TOÀN** từ chiến lược RSI sang **Ichimoku Kinko Hyo + RSI Filter** dựa trên logic của `EA_ICHIMOKU_MT4.mq4`.

### Điểm Khác Biệt So Với Phiên Bản RSI Cũ:

| Tiêu Chí | Phiên Bản Cũ (RSI) | Phiên Bản Mới (ICHIMOKU) |
|----------|---------------------|--------------------------|
| **Entry Signal** | RSI oversold/overbought | Ichimoku crossover + RSI filter |
| **SL Calculation** | Fixed pips | Dynamic (swing high/low) |
| **TP Calculation** | Fixed pips | Dynamic (Risk:Reward ratio) |
| **Parameters** | 3 (RSI period, OB, OS) | 9 (Ichimoku, RSI, RR, etc.) |
| **Tín hiệu/năm** | Nhiều (50-200) | Ít hơn (10-50) |

---

## 📐 CÔNG THỨC ICHIMOKU

### 1️⃣ **Tenkan-sen (Đường Chuyển Đổi)**
```
Tenkan-sen = (Highest High + Lowest Low) / 2 trong N candles
Default: N = 9
```

### 2️⃣ **Kijun-sen (Đường Chuẩn)**
```
Kijun-sen = (Highest High + Lowest Low) / 2 trong N candles
Default: N = 26
```

### 3️⃣ **Senkou Span B (Đường Chậm)**
```
Senkou Span B = (Highest High + Lowest Low) / 2 trong N candles
Default: N = 52
```

### 4️⃣ **RSI (Bộ Lọc Xu Hướng)**
```
RSI = 100 - (100 / (1 + RS))
RS = Average Gain / Average Loss
Default: Period = 14
```

---

## 🔔 ĐIỀU KIỆN VÀO LỆNH

### ✅ **LỆNH BUY**

```python
IF (Tenkan[1] > Kijun[1] AND Tenkan[2] <= Kijun[2]):  # Tenkan VỪA cắt LÊN Kijun
    IF (RSI[1] >= 50):  # Xu hướng tăng
        → MỞ LỆNH BUY
```

**Giải thích:**
1. Tenkan cắt lên Kijun → Tín hiệu đảo chiều tăng
2. RSI >= 50 → Xác nhận xu hướng mạnh
3. Entry: Close + Spread
4. SL: Swing Low - 3 pips
5. TP: Entry + (SL Distance × 1.2)

### ❌ **LỆNH SELL**

```python
IF (Tenkan[1] < Kijun[1] AND Tenkan[2] >= Kijun[2]):  # Tenkan VỪA cắt XUỐNG Kijun
    IF (RSI[1] <= 50):  # Xu hướng giảm
        → MỞ LỆNH SELL
```

**Giải thích:**
1. Tenkan cắt xuống Kijun → Tín hiệu đảo chiều giảm
2. RSI <= 50 → Xác nhận xu hướng yếu
3. Entry: Close - Spread
4. SL: Swing High + 3 pips
5. TP: Entry - (SL Distance × 1.2)

---

## 🎯 TÍNH TOÁN SL VÀ TP

### **Stop Loss (Dynamic)**

**Cho lệnh BUY:**
```python
1. Tìm Swing Low = Lowest Low trong 5 nến gần nhất
2. SL = Swing Low - (3 pips × Point)
```

**Cho lệnh SELL:**
```python
1. Tìm Swing High = Highest High trong 5 nến gần nhất
2. SL = Swing High + (3 pips × Point)
```

### **Take Profit (Risk:Reward)**

**Cho lệnh BUY:**
```python
SL_Distance = Entry - SL
TP = Entry + (SL_Distance × 1.2)
```

**Ví dụ:**
- Entry: 1.0500
- SL: 1.0450 (50 pips)
- TP: 1.0500 + (50 × 1.2) = 1.0560 (60 pips)
- **RR = 1:1.2** ✅

---

## ⚙️ CÁC THAM SỐ CÓ THỂ TỐI ƯU HÓA

### 📊 **Tham Số Ichimoku**

| Tham Số | Mặc Định | Min | Max | Bước Nhảy | Ý Nghĩa |
|---------|----------|-----|-----|-----------|---------|
| **Tenkan Period** | 9 | 3 | 30 | 1 | Độ nhạy tín hiệu |
| **Kijun Period** | 26 | 10 | 60 | 1 | Đường xu hướng |
| **Senkou B Period** | 52 | 20 | 100 | 1 | Đường chậm |

### 🔍 **Tham Số RSI Filter**

| Tham Số | Mặc Định | Min | Max | Bước Nhảy | Ý Nghĩa |
|---------|----------|-----|-----|-----------|---------|
| **RSI Period** | 14 | 5 | 30 | 1 | Độ nhạy RSI |
| **RSI Buy >=** | 50 | 30 | 70 | 5 | Ngưỡng mua |
| **RSI Sell <=** | 50 | 30 | 70 | 5 | Ngưỡng bán |

### 💰 **Tham Số Trading**

| Tham Số | Mặc Định | Min | Max | Bước Nhảy | Ý Nghĩa |
|---------|----------|-----|-----|-----------|---------|
| **Risk:Reward** | 1.2 | 0.5 | 5.0 | 0.1 | Tỷ lệ TP/SL |
| **SL Buffer** | 3 pips | 0 | 10 | 0.5 | Khoảng cách SL từ swing |
| **Bars Check Swing** | 5 | 1 | 20 | 1 | Số nến tìm swing |

---

## 🚀 CÁCH SỬ DỤNG GUI

### **Bước 1: Chạy GUI**
```bash
streamlit run gui_app_multi.py
# hoặc
./run_multi_gui.bat   # (Windows)
```

### **Bước 2: Chọn Files**
1. Nhập đường dẫn folder CSV (mặc định: `CSV`)
2. Nhấn **"Scan Folder"**
3. Chọn các files muốn backtest (AUDUSD5, EURUSD15, ...)

### **Bước 3: Cấu Hình Tham Số**

**Ichimoku Parameters:**
- Để **default (9, 26, 52)** để test theo EA gốc
- Hoặc thiết lập range để tối ưu hóa:
  - Tenkan: Min=7, Max=11, Step=2 → [7, 9, 11]
  - Kijun: Min=20, Max=30, Step=5 → [20, 25, 30]
  - Senkou: Min=40, Max=60, Step=10 → [40, 50, 60]

**RSI Filter:**
- RSI Period: 14 (default EA)
- Buy >= 50, Sell <= 50 (default EA)

**Trading:**
- Risk:Reward: 1.2 (default EA)
- SL Buffer: 3 pips (default EA)
- Bars Check Swing: 5 (default EA)

### **Bước 4: Chạy Optimization**
1. Nhấn **"Chạy Tối Ưu Hóa"**
2. Hệ thống sẽ test TẤT CẢ combinations
3. Xem kết quả theo Score, Profit, Win Rate

---

## 📈 DIỄN GIẢI KẾT QUẢ

### **Kết Quả Tốt:**
```
Symbol: EURUSD
Timeframe: H1
Tenkan: 9, Kijun: 26, Senkou: 52
RSI: 14, Buy>=50, Sell<=50
Profit: 450.00 pips
Win Rate: 65.0%
Profit Factor: 2.3
Max DD: 12.5%
Score: 723.45
```

**Ý nghĩa:**
- ✅ Profit > 0
- ✅ Win Rate > 60%
- ✅ Profit Factor > 2.0
- ✅ Max DD < 20%
- ✅ Score cao → Kết hợp tốt nhiều metrics

### **Kết Quả Xấu:**
```
Profit: -120.00 pips
Win Rate: 35.0%
Profit Factor: 0.7
Max DD: 35.2%
Score: -250.12
```

**Ý nghĩa:**
- ❌ Profit < 0 → Lỗ
- ❌ Win Rate < 50% → Thua nhiều hơn thắng
- ❌ Profit Factor < 1.0 → Lỗ nhiều hơn lời
- ❌ Max DD > 30% → Rủi ro cao

---

## ⚠️ LƯU Ý QUAN TRỌNG

### 1️⃣ **Số Lượng Tín Hiệu**
- Ichimoku crossover **ÍT XẢY RA** hơn RSI nhiều
- Với dữ liệu 2000 nến M5 (7 ngày):
  - RSI: 50-100 trades
  - Ichimoku: 5-20 trades
- **→ CẦN DỮ LIỆU DÀI HƠN** để có đủ trades

### 2️⃣ **Độ Tin Cậy**
- Ít nhất **30 trades** để kết quả có ý nghĩa thống kê
- Nếu < 10 trades → Không đủ dữ liệu để đánh giá

### 3️⃣ **Tối Ưu Hóa**
- Tránh **over-fitting**: Quá nhiều parameters → quá tối ưu cho dữ liệu mẫu
- Nên test với **out-of-sample data** (dữ liệu chưa thấy)

### 4️⃣ **Dynamic SL/TP**
- SL và TP **THAY ĐỔI** theo từng trade
- Không giống RSI strategy (fixed SL/TP)
- Phù hợp hơn với market dynamics

---

## 🔬 TEST NHANH

### Chạy Test Script:
```bash
python test_ichimoku.py
```

**Kết quả mong đợi:**
```
Testing Ichimoku strategy with CSV/AUDUSD5.csv...
============================================================
✅ Loaded 2000 candles
   Date range: 2025-11-19 00:00:00 to 2025-11-27 22:35:00

Running backtest with EA default parameters...
  Tenkan: 9, Kijun: 26, Senkou B: 52
  RSI Period: 14, Buy >= 50, Sell <= 50
  Risk:Reward: 1.2, SL Buffer: 3 pips, Swing Bars: 5

RESULTS:
------------------------------------------------------------
  Total Trades:      0-15 (tùy dữ liệu)
  Win Rate:          XX.X%
  Total Profit:      XXX.XX pips
  Profit Factor:     X.XX
  Max Drawdown:      XX.XX%

✅ Test completed successfully!
```

---

## 📊 VÍ DỤ OPTIMIZATION GRID

### **Conservative (Ít combinations):**
```
Tenkan: 9-9 (step 1) → 1 value
Kijun: 26-26 (step 1) → 1 value
Senkou: 52-52 (step 1) → 1 value
RSI Period: 14-14 (step 1) → 1 value
RSI Buy: 50-50 (step 5) → 1 value
RSI Sell: 50-50 (step 5) → 1 value

Total: 1 × 1 × 1 × 1 × 1 × 1 = 1 test/file
```

### **Moderate (Medium combinations):**
```
Tenkan: 7-11 (step 2) → 3 values [7, 9, 11]
Kijun: 20-30 (step 5) → 3 values [20, 25, 30]
Senkou: 40-60 (step 10) → 3 values [40, 50, 60]
RSI Period: 10-18 (step 4) → 3 values [10, 14, 18]
RSI Buy: 45-55 (step 5) → 3 values [45, 50, 55]
RSI Sell: 45-55 (step 5) → 3 values [45, 50, 55]

Total: 3^6 = 729 tests/file
```

### **Aggressive (Nhiều combinations):**
```
Tenkan: 5-15 (step 1) → 11 values
Kijun: 20-35 (step 1) → 16 values
Senkou: 40-70 (step 2) → 16 values
RSI Period: 10-20 (step 2) → 6 values
RSI Buy: 40-60 (step 5) → 5 values
RSI Sell: 40-60 (step 5) → 5 values

Total: 11 × 16 × 16 × 6 × 5 × 5 = 211,200 tests/file
⚠️ Warning: Có thể mất NHIỀU GIỜ!
```

---

## 🎓 KẾT LUẬN

### ✅ **Ưu Điểm:**
1. Logic dựa trên EA đã được verify
2. Dynamic SL/TP phù hợp với market
3. RSI filter giảm false signals
4. Có thể tối ưu hóa 9 parameters

### ⚠️ **Nhược Điểm:**
1. Ít tín hiệu hơn RSI strategy
2. Cần dữ liệu dài hơn (>6 tháng)
3. Optimization mất nhiều thời gian hơn
4. Có thể không trade trong nhiều ngày

### 🚀 **Khuyến Nghị:**
- Test với **dữ liệu thật ít nhất 6 tháng**
- Sử dụng **moderate optimization** (500-1000 tests)
- Forward test trên **out-of-sample data**
- Kết hợp với **risk management** (max DD, max trades/day)

---

**Chúc bạn backtest thành công!** 🎯
