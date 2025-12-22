# 📊 HƯỚNG DẪN SỬ DỤNG CHART VISUALIZATION

## 🎯 TỔNG QUAN

Tool **visualize_trades.py** giúp bạn **MÔ PHỎNG TRỰC QUAN** các trades từ backtest trên chart tương tác (interactive chart).

### Bạn Sẽ Thấy:
- 📈 **Candlestick Chart**: Giá nến OHLC
- 📊 **Ichimoku Lines**: Tenkan-sen (blue), Kijun-sen (red)
- 🟢 **Entry Points BUY**: Tam giác xanh hướng lên
- 🔴 **Entry Points SELL**: Tam giác đỏ hướng xuống
- 🎯 **Exit Points**: Dấu X (xanh = TP, đỏ = SL)
- 📏 **SL/TP Levels**: Đường ngang chấm chấm
- 📉 **RSI Subplot**: RSI indicator với threshold lines

---

## 🚀 CÁCH SỬ DỤNG

### **Cách 1: Chạy với file mặc định**
```bash
python visualize_trades.py
```
→ Sẽ dùng `CSV/AUDUSD5.csv` mặc định

### **Cách 2: Chỉ định file CSV**
```bash
python visualize_trades.py CSV/EURUSD60.csv
python visualize_trades.py CSV/GBPUSD240.csv
python visualize_trades.py your_data.csv
```

### **Cách 3: Sử dụng trong Python script**
```python
from visualize_trades import visualize_backtest

result, fig = visualize_backtest(
    csv_file="CSV/AUDUSD5.csv",
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
    max_candles=500  # Số nến hiển thị tối đa
)
```

---

## 📊 KẾT QUẢ

### **1. Console Output**
```
================================================================================
VISUALIZING ICHIMOKU BACKTEST: CSV/AUDUSD5.csv
================================================================================

✅ Loaded 2000 candles
   → Showing last 500 candles for better visualization

🔄 Running backtest...
   Tenkan: 9, Kijun: 26, Senkou: 52
   RSI: 14, Buy>=50.0, Sell<=50.0
   RR: 1.2, SL Buffer: 3.0 pips

✅ Backtest completed: 8 trades
   Profit: -34.48 pips
   Win Rate: 37.5%

📊 Creating interactive chart...

✅ Chart created successfully!
   Opening in browser...

💾 Chart saved to: CSV/AUDUSD5_visualization.html
```

### **2. File HTML Output**
File được lưu tại: `<CSV_FILENAME>_visualization.html`

Ví dụ:
- `CSV/AUDUSD5.csv` → `CSV/AUDUSD5_visualization.html`
- `CSV/EURUSD60.csv` → `CSV/EURUSD60_visualization.html`

### **3. Chart Tự Động Mở Trong Browser**
- Chart sẽ tự động mở trong trình duyệt mặc định
- Nếu không mở, double-click file HTML để xem

---

## 🎨 CÁC THÀNH PHẦN TRÊN CHART

### **Main Chart (Phần Trên):**

#### 1️⃣ **Candlestick (Nến)**
- **Xanh lá**: Nến tăng (close > open)
- **Đỏ**: Nến giảm (close < open)
- Hover để xem OHLC values

#### 2️⃣ **Tenkan-sen (Đường Xanh Dương)**
- Đường conversion line (9 periods mặc định)
- Cắt LÊN Kijun → Signal BUY
- Cắt XUỐNG Kijun → Signal SELL

#### 3️⃣ **Kijun-sen (Đường Đỏ)**
- Đường base line (26 periods mặc định)
- Là đường trung tâm cho crossover

#### 4️⃣ **Entry Points**
- **🟢 Tam giác xanh hướng lên**: Lệnh BUY
- **🔴 Tam giác đỏ hướng xuống**: Lệnh SELL
- Hover để xem:
  - Time: Thời gian vào lệnh
  - Price: Giá vào lệnh
  - SL: Stop Loss level
  - TP: Take Profit level

#### 5️⃣ **Exit Points**
- **✓ Dấu X màu xanh đậm**: Exit với lời (TP hoặc profit)
- **✗ Dấu X màu đỏ đậm**: Exit với lỗ (SL)
- Hover để xem:
  - Exit reason: TP/SL/EOD
  - Exit price
  - Profit/Loss (pips)

#### 6️⃣ **SL/TP Lines** (10 trades đầu tiên)
- **Đường đỏ chấm chấm**: Stop Loss level
- **Đường xanh chấm chấm**: Take Profit level
- Hiển thị từ entry → exit time

### **RSI Subplot (Phần Dưới):**

- **Đường tím**: RSI values
- **Đường xanh chấm**: RSI Buy threshold (default 50)
- **Đường đỏ chấm**: RSI Sell threshold (default 50)
- **Đường xám chấm**: RSI 50 midline

---

## 🖱️ TƯƠNG TÁC VỚI CHART

### **Zoom & Pan:**
- **Scroll chuột**: Zoom in/out
- **Click & drag**: Pan (di chuyển chart)
- **Double click**: Reset zoom

### **Legend (Chú thích):**
- **Single click**: Ẩn/hiện một line
- **Double click**: Chỉ hiện line đó (ẩn tất cả các line khác)

### **Toolbar (Góc phải trên):**
- 📷 **Camera**: Download chart as PNG
- 🔍 **Zoom**: Zoom to selection
- 📐 **Pan**: Pan mode
- 🏠 **Home**: Reset view
- ↔️ **Autoscale**: Auto-fit to data

### **Hover Mode:**
- Di chuột qua chart để xem chi tiết từng điểm
- Unified hover: Thấy tất cả values tại cùng thời điểm

---

## 📐 TÙY CHỈNH PARAMETERS

### **Thay Đổi Ichimoku Parameters:**

Sửa trong script hoặc gọi hàm:
```python
visualize_backtest(
    csv_file="your_file.csv",
    tenkan_period=7,      # Thay đổi từ 9
    kijun_period=20,      # Thay đổi từ 26
    senkou_b_period=40,   # Thay đổi từ 52
    # ...
)
```

### **Thay Đổi RSI Parameters:**
```python
visualize_backtest(
    csv_file="your_file.csv",
    rsi_period=10,              # Thay đổi từ 14
    rsi_buy_threshold=45.0,     # Thay đổi từ 50
    rsi_sell_threshold=55.0,    # Thay đổi từ 50
    # ...
)
```

### **Thay Đổi Trading Parameters:**
```python
visualize_backtest(
    csv_file="your_file.csv",
    risk_reward_ratio=1.5,    # Thay đổi từ 1.2
    sl_buffer_pips=5.0,       # Thay đổi từ 3.0
    bars_check_swing=10,      # Thay đổi từ 5
    # ...
)
```

### **Thay Đổi Số Nến Hiển Thị:**
```python
visualize_backtest(
    csv_file="your_file.csv",
    max_candles=1000,  # Default 500
    # ...
)
```

**Lưu ý**: Quá nhiều nến (>1000) sẽ làm chart nặng và chậm!

---

## 💡 TIPS & TRICKS

### **1. Phân Tích Entry Points**
- Nhìn vào màu tam giác entry:
  - 🟢 **Xanh** = BUY khi Tenkan cắt LÊN Kijun
  - 🔴 **Đỏ** = SELL khi Tenkan cắt XUỐNG Kijun
- Check RSI subplot để xác nhận:
  - BUY phải có RSI >= 50 (trên đường xanh)
  - SELL phải có RSI <= 50 (dưới đường đỏ)

### **2. Kiểm Tra Win/Loss Ratio**
- Đếm số **X xanh** (win) vs **X đỏ** (loss)
- Xem exit reason: Nhiều TP hay SL?

### **3. Đánh Giá SL/TP Placement**
- Xem đường SL/TP có hợp lý không?
- SL có quá gần (bị hit dễ)?
- TP có quá xa (không đạt được)?

### **4. Tìm Pattern**
- Zoom vào từng cặp entry-exit
- Xem trend khi vào lệnh:
  - Có đang trong uptrend mạnh?
  - Có bị chop (sideway)?

### **5. So Sánh Timeframes**
Chạy visualization cho cùng symbol, nhiều timeframes:
```bash
python visualize_trades.py CSV/EURUSD5.csv   # M5
python visualize_trades.py CSV/EURUSD60.csv  # H1
python visualize_trades.py CSV/EURUSD240.csv # H4
```
Mở 3 tabs để compare!

---

## 🎯 VÍ DỤ PHÂN TÍCH

### **Ví Dụ 1: Trade Thành Công (TP)**

```
Entry: 🟢 BUY at 1.0500
Exit:  ✓ TP at 1.0560
Profit: +60 pips

Quan sát:
- Tenkan vừa cắt lên Kijun → Signal BUY
- RSI = 55 (>50) → Xác nhận uptrend
- SL = 1.0450 (-50 pips)
- TP = 1.0560 (+60 pips) với RR = 1:1.2
- Price đi thẳng lên TP, không test SL
→ Trade hoàn hảo!
```

### **Ví Dụ 2: Trade Thất Bại (SL)**

```
Entry: 🔴 SELL at 1.0500
Exit:  ✗ SL at 1.0565
Loss: -65 pips

Quan sát:
- Tenkan cắt xuống Kijun → Signal SELL
- RSI = 48 (<50) → Xác nhận downtrend
- SL = 1.0565 (+65 pips)
- TP = 1.0435 (-65 pips)
- Price đảo chiều đi lên, hit SL ngay
→ False signal, market đảo chiều
```

### **Ví Dụ 3: Whipsaw (Nhiều Losses Liên Tiếp)**

```
Trade 1: SELL → SL → -50 pips
Trade 2: BUY  → SL → -50 pips
Trade 3: SELL → SL → -50 pips

Quan sát trên chart:
- Price đang sideway (chop)
- Tenkan và Kijun cắt nhau liên tục
- Không có trend rõ ràng
→ Nên tránh trade khi market sideway!
```

---

## ⚠️ LƯU Ý

### **1. Giới Hạn Hiển Thị**
- Default: **500 nến cuối cùng**
- Lý do: Chart quá nhiều nến sẽ chậm
- Nếu muốn xem tất cả, tăng `max_candles`:
  ```python
  max_candles=2000  # Hiển thị hết
  ```

### **2. SL/TP Lines**
- Chỉ hiển thị cho **10 trades đầu tiên**
- Lý do: Tránh chart quá rối với nhiều đường
- Nếu muốn xem tất cả, sửa code:
  ```python
  if i < 10:  # Thay 10 thành số lớn hơn
  ```

### **3. Performance**
- File HTML có thể nặng (2-5MB) với nhiều trades
- Browser có thể chậm với >1000 nến
- Khuyến nghị: max_candles <= 500

### **4. Dữ Liệu**
- Cần file CSV với format đúng (tab-separated, no header)
- Cột: Date, Time, Open, High, Low, Close, Volume

---

## 🔧 TROUBLESHOOTING

### **Lỗi: "FileNotFoundError"**
```
Solution: Kiểm tra đường dẫn file CSV
Đúng:  python visualize_trades.py CSV/AUDUSD5.csv
Sai:   python visualize_trades.py AUDUSD5.csv
```

### **Lỗi: "No trades found"**
```
Solution:
- Dữ liệu quá ngắn, không có crossover
- Thử giảm Kijun period (26 → 15)
- Hoặc dùng timeframe lớn hơn (H1, H4)
```

### **Chart không mở trong browser**
```
Solution:
1. Tìm file *_visualization.html
2. Double-click để mở thủ công
3. Hoặc drag & drop vào browser
```

### **Chart quá chậm/lag**
```
Solution:
- Giảm max_candles xuống 300-500
- Tắt SL/TP lines (comment code if i < 10:)
- Đóng các tab browser khác
```

---

## 📚 TÀI LIỆU THAM KHẢO

- **Plotly Documentation**: https://plotly.com/python/
- **Candlestick Charts**: https://plotly.com/python/candlestick-charts/
- **Ichimoku Strategy**: Xem `HUONG_DAN_ICHIMOKU.md`

---

## 🎓 KẾT LUẬN

### ✅ **Ưu Điểm:**
1. **Trực quan**: Thấy rõ entry/exit trên chart
2. **Interactive**: Zoom, pan, hover để analyze
3. **Chi tiết**: SL/TP levels, RSI confirmation
4. **Dễ dùng**: Chỉ cần 1 lệnh

### 🎯 **Sử Dụng Cho:**
- Debug strategy logic
- Hiểu tại sao trades thắng/thua
- Optimize parameters (thấy ngay impact)
- Present results (chart đẹp, professional)

### 🚀 **Next Steps:**
1. Chạy visualization cho file CSV của bạn
2. Phân tích entry/exit patterns
3. Điều chỉnh parameters
4. So sánh results

---

**Happy Visualizing!** 📊🎯
