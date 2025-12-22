# 🖥️ HƯỚNG DẪN SỬ DỤNG GUI - AI-Indicator Optimizer

## 📋 Mục Lục

1. [Giới Thiệu](#giới-thiệu)
2. [Cài Đặt](#cài-đặt)
3. [Khởi Động GUI](#khởi-động-gui)
4. [Sử Dụng Giao Diện](#sử-dụng-giao-diện)
5. [Các Tính Năng](#các-tính-năng)
6. [Ví Dụ Minh Họa](#ví-dụ-minh-họa)
7. [Xử Lý Lỗi](#xử-lý-lỗi)

---

## 🎯 Giới Thiệu

**AI-Indicator GUI** là giao diện đồ họa trực quan cho hệ thống backtesting, giúp bạn:

✅ Chọn file dữ liệu dễ dàng từ dropdown
✅ Cấu hình tham số qua slider và input box
✅ Xem kết quả với biểu đồ tương tác đẹp mắt
✅ Phân tích với nhiều loại chart (Bar, Scatter, Heatmap)
✅ Tải kết quả về CSV chỉ với 1 click

**Công nghệ:** Streamlit + Plotly (Modern Web UI)

---

## 📦 Cài Đặt

### Bước 1: Cài Đặt Thư Viện

```bash
pip install -r requirements.txt
```

Hoặc cài thủ công:

```bash
pip install streamlit plotly pandas numpy
```

### Bước 2: Kiểm Tra Cài Đặt

```bash
streamlit --version
```

Bạn sẽ thấy: `Streamlit, version 1.52.x`

---

## 🚀 Khởi Động GUI

### Cách 1: Sử Dụng Script (Khuyến nghị)

```bash
./run_gui.sh
```

hoặc

```bash
bash run_gui.sh
```

### Cách 2: Chạy Trực Tiếp

```bash
streamlit run gui_app.py
```

### Kết Quả

Sau khi chạy, bạn sẽ thấy:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

**Mở trình duyệt và vào:** `http://localhost:8501`

---

## 🖱️ Sử Dụng Giao Diện

### Layout Tổng Quan

```
┌─────────────────────────────────────────────────────────────┐
│  📈 AI-Indicator Backtesting & Optimization System          │
├──────────────┬──────────────────────────────────────────────┤
│              │                                              │
│   SIDEBAR    │           MAIN CONTENT AREA                  │
│              │                                              │
│  ⚙️ Cấu Hình │  📊 Data Preview                            │
│              │  🏆 Best Parameters                          │
│  📁 File     │  📋 Top N Results Table                      │
│  📊 Indicator│  📊 Charts (Ranking, Profit, Heatmap...)    │
│  🎯 Params   │  💾 Download Buttons                         │
│  💰 Trading  │                                              │
│  🚀 Run Btn  │                                              │
│              │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

---

## 📖 Hướng Dẫn Từng Bước

### Bước 1: Chọn File Dữ Liệu 📁

**Vị trí:** Sidebar → "📁 Chọn File Dữ Liệu"

1. Click vào dropdown "File CSV:"
2. Chọn file dữ liệu của bạn (ví dụ: `AUDCAD15.csv`)
3. Hệ thống tự động load và hiển thị preview

**Xem trước dữ liệu:**
- Click "📊 Xem Trước Dữ Liệu" để mở rộng
- Xem số lượng candles, khoảng thời gian
- Xem biểu đồ giá

---

### Bước 2: Chọn Indicator 📊

**Vị trí:** Sidebar → "📊 Chọn Indicator"

Hiện tại hỗ trợ:
- ✅ **RSI** (Relative Strength Index)
- 🔜 MACD (Coming Soon)
- 🔜 Bollinger Bands (Coming Soon)

Chọn **RSI** để tiếp tục.

---

### Bước 3: Cấu Hình Tham Số RSI 🎯

**Vị trí:** Sidebar → "🎯 Tham Số RSI"

#### RSI Period

| Tham số | Giá trị mặc định | Ý nghĩa |
|---------|------------------|---------|
| **Period Min** | 5 | Giá trị RSI period nhỏ nhất |
| **Period Max** | 30 | Giá trị RSI period lớn nhất |
| **Period Step** | 1 | Bước nhảy giữa các giá trị |

**Ví dụ:**
- Min=10, Max=20, Step=2 → Test: 10, 12, 14, 16, 18, 20 (6 giá trị)

#### Overbought

| Tham số | Giá trị mặc định | Ý nghĩa |
|---------|------------------|---------|
| **OB Min** | 65 | Ngưỡng overbought thấp nhất |
| **OB Max** | 85 | Ngưỡng overbought cao nhất |
| **OB Step** | 5 | Bước nhảy |

#### Oversold

| Tham số | Giá trị mặc định | Ý nghĩa |
|---------|------------------|---------|
| **OS Min** | 15 | Ngưỡng oversold thấp nhất |
| **OS Max** | 35 | Ngưỡng oversold cao nhất |
| **OS Step** | 5 | Bước nhảy |

**💡 Tips:**
- **Test nhanh:** Dùng Step lớn (5-10) → ít combinations hơn
- **Test chi tiết:** Dùng Step nhỏ (1-2) → nhiều combinations hơn

**Hiển thị tổng combinations:**
```
📊 Tổng combinations: 650
```

---

### Bước 4: Cấu Hình Trading 💰

**Vị trí:** Sidebar → "💰 Tham Số Trading"

| Tham số | Mặc định | Mô tả |
|---------|----------|-------|
| **Take Profit** | 20.0 pips | Mục tiêu lời |
| **Stop Loss** | 15.0 pips | Cắt lỗ |
| **Spread** | 1.2 pips | Chi phí giao dịch |
| **Lot Size** | 0.1 | Khối lượng lệnh |

**Điều chỉnh:** Click vào số và nhập giá trị mới, hoặc dùng nút +/-

---

### Bước 5: Cài Đặt Tối Ưu 🔧

**Vị trí:** Sidebar → "🔧 Cài Đặt Tối Ưu"

| Tham số | Mặc định | Mô tả |
|---------|----------|-------|
| **Max Drawdown Threshold** | 30% | Ngưỡng rủi ro chấp nhận được |
| **Top N Results** | 10 | Số lượng kết quả hiển thị |

**Max Drawdown Threshold:**
- Chỉ chấp nhận kết quả có drawdown < ngưỡng này
- Tăng lên nếu không có kết quả hợp lệ

---

### Bước 6: Chạy Tối Ưu Hóa 🚀

**Vị trí:** Sidebar → Bottom

1. Click nút **"🚀 Chạy Tối Ưu Hóa"** (màu xanh)
2. Đợi progress bar chạy
3. Kết quả sẽ hiển thị trong main area

**Progress tracking:**
```
🔄 Đang tối ưu hóa...
Đang test: 325/650 (50.0%)
[████████████░░░░░░░░░░░░] 50%
```

**Thời gian:** ~5-10 giây cho 650 combinations

---

## 📊 Xem Kết Quả

### 1. Tổng Quan (Summary) 📈

5 metrics cards hiển thị ngay đầu:

```
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│ Tổng Số     │ Kết Quả     │ Profit      │ Win Rate    │ Score       │
│ Tests       │ Hợp Lệ      │ Tốt Nhất    │ Tốt Nhất    │ Cao Nhất    │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│   650       │  169        │  56.40 pips │  100.00%    │  1056.25    │
│             │  ▲26.0%     │             │             │             │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

---

### 2. Tham Số Tốt Nhất 🏆

3 boxes màu xanh hiển thị:

#### Box 1: 🎯 Tham Số
```
RSI Period:   18
Overbought:   85
Oversold:     25
```

#### Box 2: 💰 Hiệu Suất
```
Total Profit:   56.40 pips
Win Rate:       100.00%
Profit Factor:  56.40
```

#### Box 3: 📊 Thống Kê
```
Number of Trades:  3
Max Drawdown:      0.00%
Score:             1056.25
```

---

### 3. Bảng Top N Kết Quả 📋

Bảng đầy đủ với cột:

| Rank | RSI Period | OB | OS | Profit | Win Rate | PF | Trades | Max DD | Score | Valid |
|------|-----------|----|----|--------|----------|----|----|--------|-------|-------|
| 1 | 18 | 85 | 25 | 56.40 | 100.00% | 56.40 | 3 | 0.00% | 1056.25 | ✓ |
| 2 | 19 | 85 | 25 | 37.60 | 100.00% | 37.60 | 2 | 0.00% | 1037.50 | ✓ |

**Tính năng:**
- Sắp xếp theo Score
- Có thể scroll ngang/dọc
- Highlight valid results

---

### 4. Biểu Đồ Phân Tích 📊

4 tabs biểu đồ tương tác:

#### Tab 1: 📊 Ranking (Biểu đồ cột)

**Hiển thị:** Top 20 parameter sets, sắp xếp theo score

**Màu sắc:**
- 🟢 Xanh lá: Valid results
- 🔴 Đỏ: Invalid results

**Tương tác:**
- Hover để xem chi tiết
- Zoom in/out
- Pan (kéo trái phải)
- Download chart as PNG

---

#### Tab 2: 💰 Profit Analysis (Scatter plot)

**Trục:**
- **X-axis:** Max Drawdown (%)
- **Y-axis:** Total Profit (pips)
- **Size:** Number of Trades (bong bóng lớn = nhiều lệnh)
- **Color:** Win Rate (màu đậm hơn = win rate cao)

**Reference lines:**
- Đường đỏ ngang: Profit = 0 (break-even)
- Đường cam dọc: Max DD Threshold

**Cách đọc:**
- 🎯 Vùng tốt: Góc trên bên trái (profit cao, DD thấp)
- ⚠️ Vùng xấu: Góc dưới bên phải (lỗ, DD cao)

---

#### Tab 3: 🎯 Parameter Heatmap

**Hiển thị:** Average score theo Overbought x Oversold

**Màu sắc:**
- 🟢 Xanh lá đậm: Score cao
- 🟡 Vàng: Score trung bình
- 🔴 Đỏ: Score thấp

**Cách dùng:**
- Tìm ô màu xanh đậm nhất → Tổ hợp OB/OS tốt nhất
- Hover để xem giá trị chính xác

---

#### Tab 4: 📈 Scatter Plot (Win Rate vs Profit Factor)

**Trục:**
- **X-axis:** Win Rate (%)
- **Y-axis:** Profit Factor
- **Size:** Total Profit
- **Color:** Valid/Invalid

**Reference lines:**
- Đường ngang: PF = 1.0 (break-even)
- Đường dọc: Win Rate = 50%

**Vùng lý tưởng:** Góc trên bên phải (WR > 50%, PF > 1.5)

---

### 5. Tải Kết Quả 💾

2 nút download:

#### Nút 1: 📥 Tải Tất Cả Kết Quả (CSV)
- Tải toàn bộ 650 kết quả
- Bao gồm cả valid và invalid

#### Nút 2: 📥 Tải Kết Quả Hợp Lệ (CSV)
- Chỉ tải kết quả valid
- Chỉ có nếu có ≥1 kết quả hợp lệ

**File format:**
```csv
rsi_period,overbought,oversold,total_profit_pips,win_rate,...
18,85,25,56.40,100.00,...
19,85,25,37.60,100.00,...
```

**Mở bằng:** Excel, Google Sheets, hoặc text editor

---

## 💡 Các Tính Năng

### ✨ Tính Năng Nổi Bật

| Tính năng | Mô tả |
|-----------|-------|
| **Multi-file support** | Chọn bất kỳ CSV nào trong thư mục |
| **Real-time progress** | Progress bar cập nhật theo thời gian thực |
| **Interactive charts** | Zoom, pan, hover tooltip với Plotly |
| **Responsive UI** | Tự động điều chỉnh theo kích thước màn hình |
| **Dark mode ready** | Tương thích với dark mode của Streamlit |
| **One-click download** | Tải kết quả về máy ngay lập tức |
| **Parameter validation** | Kiểm tra tham số hợp lệ trước khi chạy |

---

### 🎨 Giao Diện Đẹp

- **Gradient headers** với màu sắc chuyên nghiệp
- **Color-coded metrics** dễ phân biệt valid/invalid
- **Success boxes** highlight kết quả tốt nhất
- **Modern charts** với Plotly (smooth animations)
- **Clean layout** không bị rối mắt

---

## 📚 Ví Dụ Minh Họa

### Ví Dụ 1: Test Nhanh

**Mục tiêu:** Test nhanh để xem hệ thống hoạt động

**Cấu hình:**
```
RSI Period:  10 → 20 (step 5)  → 3 giá trị
Overbought:  70 → 80 (step 10) → 2 giá trị
Oversold:    20 → 30 (step 10) → 2 giá trị
Total: 3 × 2 × 2 = 12 combinations
```

**Kết quả:** ~2 giây

---

### Ví Dụ 2: Test Đầy Đủ

**Mục tiêu:** Tìm tham số tối ưu nhất

**Cấu hình:**
```
RSI Period:  5 → 30 (step 1)  → 26 giá trị
Overbought:  65 → 85 (step 5) → 5 giá trị
Oversold:    15 → 35 (step 5) → 5 giá trị
Total: 26 × 5 × 5 = 650 combinations
```

**Kết quả:** ~10 giây

---

### Ví Dụ 3: Fine-tuning

**Mục tiêu:** Tinh chỉnh quanh tham số tốt từ test trước

Giả sử test trước cho kết quả tốt: RSI(18, 85, 25)

**Cấu hình:**
```
RSI Period:  16 → 20 (step 1)  → 5 giá trị
Overbought:  80 → 90 (step 2)  → 6 giá trị
Oversold:    20 → 30 (step 2)  → 6 giá trị
Total: 5 × 6 × 6 = 180 combinations
```

**Kết quả:** ~5 giây, độ phân giải cao hơn

---

## ❌ Xử Lý Lỗi

### Lỗi 1: "No CSV files found"

**Nguyên nhân:** Không có file CSV trong thư mục

**Giải pháp:**
```bash
python generate_sample_data.py
```

---

### Lỗi 2: "No valid results found"

**Hiển thị:** Warning box màu vàng

**Nguyên nhân:**
- Tất cả kết quả đều có profit < 0 HOẶC
- Tất cả kết quả đều có max DD > threshold

**Giải pháp:**

1. **Tăng Max Drawdown Threshold:**
   - Sidebar → "Max Drawdown Threshold"
   - Tăng từ 30% → 50%

2. **Thay đổi TP/SL:**
   - Tăng TP: 20 → 30 pips
   - Giảm SL: 15 → 10 pips

3. **Thử khoảng tham số khác:**
   - Thử RSI period khác (ví dụ: 10-25)

---

### Lỗi 3: "Module not found: streamlit"

**Nguyên nhân:** Chưa cài Streamlit

**Giải pháp:**
```bash
pip install -r requirements.txt
```

---

### Lỗi 4: Browser không tự động mở

**Nguyên nhân:** Firewall hoặc cấu hình

**Giải pháp:**
1. Mở browser thủ công
2. Vào: `http://localhost:8501`

---

### Lỗi 5: Port 8501 đã được sử dụng

**Hiển thị:**
```
Address already in use
```

**Giải pháp:**

**Cách 1:** Đóng app Streamlit cũ (Ctrl+C)

**Cách 2:** Dùng port khác:
```bash
streamlit run gui_app.py --server.port 8502
```

---

## 🎯 Tips & Tricks

### 1. Tăng Tốc Độ Test

✅ Dùng Step lớn hơn (5-10 thay vì 1)
✅ Thu hẹp khoảng tham số (10-20 thay vì 5-30)
✅ Test trên dữ liệu ngắn hơn trước

### 2. Phân Tích Kết Quả

✅ Không chỉ nhìn profit, xem cả drawdown
✅ Ưu tiên kết quả có nhiều trades (>30)
✅ So sánh nhiều metrics với scatter plot
✅ Dùng heatmap để tìm vùng tham số tốt

### 3. Tránh Overfitting

✅ Test trên nhiều khoảng thời gian khác nhau
✅ Chia data: 70% train, 30% test
✅ Không tin hoàn toàn vào 1 kết quả

### 4. Tối Ưu Trải Nghiệm

✅ Dùng màn hình lớn (≥1920x1080) để xem biểu đồ
✅ Mở full-screen mode (F11)
✅ Zoom biểu đồ để xem chi tiết
✅ Download chart as PNG để lưu lại

---

## 🔄 So Sánh GUI vs Command Line

| Tiêu chí | GUI (Streamlit) | Command Line |
|----------|-----------------|--------------|
| **Dễ sử dụng** | ⭐⭐⭐⭐⭐ Rất dễ | ⭐⭐⭐ Cần biết code |
| **Trực quan** | ⭐⭐⭐⭐⭐ Biểu đồ đẹp | ⭐⭐ Chỉ có text |
| **Tốc độ** | ⭐⭐⭐⭐ Nhanh | ⭐⭐⭐⭐⭐ Hơi nhanh hơn |
| **Linh hoạt** | ⭐⭐⭐⭐ Tốt | ⭐⭐⭐⭐⭐ Rất linh hoạt |
| **Xuất kết quả** | ⭐⭐⭐⭐⭐ 1 click | ⭐⭐⭐ Tự động lưu |

**Khuyến nghị:**
- 🆕 **Người mới:** Dùng GUI
- 💻 **Chuyên nghiệp:** Kết hợp cả 2
- 🤖 **Tự động hóa:** Dùng Command Line

---

## 📞 Hỗ Trợ

### Các File Hướng Dẫn

| File | Nội dung |
|------|----------|
| `HUONG_DAN_GUI.md` | Hướng dẫn GUI (file này) |
| `HUONG_DAN.md` | Hướng dẫn Command Line |
| `QUICK_START.txt` | Hướng dẫn nhanh |
| `README.md` | Tài liệu kỹ thuật |

### Video Demo (Tưởng tượng)

```
📹 Coming soon: Video hướng dẫn từng bước
🎬 Screencast: Cách sử dụng GUI hiệu quả
📺 Tutorial: Phân tích kết quả với charts
```

---

## ✅ Checklist Sử Dụng GUI

- [ ] Đã cài đặt `streamlit` và `plotly`
- [ ] Chạy `streamlit run gui_app.py` thành công
- [ ] Mở được trình duyệt vào `localhost:8501`
- [ ] Chọn được file CSV
- [ ] Xem được preview dữ liệu
- [ ] Chạy optimization thành công
- [ ] Xem được kết quả và biểu đồ
- [ ] Download được file CSV

---

## 🎓 Kết Luận

**GUI AI-Indicator** giúp bạn:

✅ Tối ưu hóa tham số indicator một cách trực quan
✅ Phân tích kết quả với biểu đồ tương tác chuyên nghiệp
✅ Tiết kiệm thời gian với giao diện thân thiện
✅ Ra quyết định tốt hơn với nhiều góc nhìn dữ liệu

**Bắt đầu ngay:**

```bash
streamlit run gui_app.py
```

---

**🚀 Chúc bạn tìm được bộ tham số tối ưu nhất!**

---

*Tài liệu GUI - AI-Indicator Backtesting System*
*Cập nhật: 2024*
