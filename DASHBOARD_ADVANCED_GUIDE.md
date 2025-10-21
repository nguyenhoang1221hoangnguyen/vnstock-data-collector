# 📊 VNStock Advanced Dashboard - Hướng dẫn chi tiết

Dashboard nâng cao với đầy đủ tính năng phân tích kỹ thuật, so sánh cổ phiếu, FA/TA analysis, watchlist và alerts.

## 🎯 Tính năng nổi bật

### 1. 📈 Technical Chart with Indicators
- **Biểu đồ nến (Candlestick)** với nhiều indicators tùy chọn
- **Moving Averages**: MA20, MA50, MA200, EMA12
- **RSI (14)**: Relative Strength Index với vùng overbought/oversold
- **MACD**: Moving Average Convergence Divergence với histogram
- **Bollinger Bands**: Upper/Lower bands với middle line
- **Multi-timeframe**: 30 ngày đến 2 năm

### 2. 📊 Multi-Stock Comparison
- So sánh **đồng thời tối đa 6 mã cổ phiếu**
- Normalized chart (base = 100) để so sánh hiệu suất
- Performance summary với metrics chi tiết
- Real-time data từ vnstock

### 3. 🧮 FA/TA Analysis Integration
- **Fundamental Analysis**:
  - P/E Ratio (Price to Earnings)
  - ROE (Return on Equity)
  - NPM (Net Profit Margin)
  - D/E (Debt to Equity)
  - Interpretation & recommendations
  
- **Technical Analysis**:
  - Trend analysis (MA crossovers)
  - Momentum indicators (RSI, MACD)
  - Overall signal: Bullish/Bearish/Neutral
  - API integration với backend server

### 4. ⭐ Personal Watchlist
- Lưu danh sách mã yêu thích
- Real-time price tracking
- Quick add/remove từ bất kỳ tab nào
- Session-based storage (giữ trong phiên làm việc)

### 5. 🔔 Price Alerts
- Thiết lập alerts khi giá đạt ngưỡng
- Điều kiện: Above (trên) hoặc Below (dưới)
- Notification tự động khi điều kiện được kích hoạt
- Quản lý alerts dễ dàng (add/delete)

## 🚀 Khởi chạy

### Cách 1: Sử dụng script (Khuyến nghị)
```bash
# Activate virtual environment
source venv/bin/activate

# Chạy advanced dashboard
python start_dashboard_advanced.py
```

### Cách 2: Chạy trực tiếp
```bash
source venv/bin/activate
streamlit run dashboard_advanced.py --server.port=8503 --server.address=0.0.0.0
```

### Cách 3: Chạy cùng API Server
```bash
# Terminal 1: API Server (cho FA/TA features)
python start_server.py &

# Terminal 2: Advanced Dashboard
python start_dashboard_advanced.py
```

## 🌐 Truy cập

- **Local**: `http://localhost:8503`
- **Network**: `http://192.168.1.4:8503`

## 📖 Hướng dẫn sử dụng chi tiết

### Tab 1: Technical Chart

#### Bước 1: Cấu hình
1. Nhập mã cổ phiếu (VD: ACB, VIC, FPT)
2. Chọn khoảng thời gian (30 ngày - 2 năm)
3. Chọn indicators muốn hiển thị:
   - ✅ MA20, MA50 (mặc định)
   - ✅ RSI, MACD (mặc định)
   - ⬜ MA200, EMA12, Bollinger Bands (tùy chọn)

#### Bước 2: Load Chart
- Nhấn nút "🔄 Load Chart"
- Xem metrics: Current Price, High, Low, Avg Volume
- Kiểm tra alerts (nếu có)

#### Bước 3: Phân tích
- **Biểu đồ nến**: Xác định xu hướng giá
- **RSI**: 
  - > 70: Overbought (quá mua)
  - < 30: Oversold (quá bán)
- **MACD**:
  - MACD > Signal: Bullish
  - MACD < Signal: Bearish
- **Moving Averages**:
  - Golden Cross: MA ngắn cắt lên MA dài → Tín hiệu mua
  - Death Cross: MA ngắn cắt xuống MA dài → Tín hiệu bán

#### Bước 4: Quick Stats
- Mở rộng "Quick Statistics"
- Xem RSI và MACD hiện tại
- Kiểm tra tín hiệu tự động

#### Tips:
- Sử dụng **⭐ Add to Watchlist** để theo dõi mã này
- Zoom/Pan trên biểu đồ để xem chi tiết
- Hover để xem giá trị chính xác

### Tab 2: Multi-Stock Comparison

#### Bước 1: Nhập danh sách mã
- Nhập các mã cách nhau bởi dấu phẩy
- Ví dụ: `ACB,VCB,TCB,MBB`
- Tối đa 6 mã

#### Bước 2: Chọn thời gian
- 30, 90, 180, hoặc 365 ngày

#### Bước 3: Compare
- Nhấn "📈 Compare"
- Xem biểu đồ normalized (base = 100)
- So sánh hiệu suất tương đối

#### Bước 4: Phân tích Performance Summary
- Xem % thay đổi của từng mã
- So sánh High/Low
- Kiểm tra Volume

#### Use Cases:
- So sánh các ngân hàng: ACB, VCB, TCB
- So sánh các công ty bất động sản: VHM, VIC, NVL
- So sánh cổ phiếu cùng ngành

### Tab 3: FA/TA Analysis

#### Fundamental Analysis:
1. Nhập mã cổ phiếu
2. Chọn "Fundamental (FA)" hoặc "Both"
3. Nhấn "🔍 Analyze"
4. Xem các chỉ số:
   - **P/E < 15**: Undervalued
   - **ROE > 15%**: Good profitability
   - **NPM > 10%**: Healthy margin
   - **D/E < 1**: Safe leverage

#### Technical Analysis:
1. Chọn "Technical (TA)" hoặc "Both"
2. Xem Trend Analysis:
   - MA signals
   - Price position vs MAs
3. Xem Momentum:
   - RSI signals
   - MACD signals
4. Overall Signal:
   - ✅ Bullish: Nhiều tín hiệu tích cực
   - ⚠️ Bearish: Nhiều tín hiệu tiêu cực
   - ℹ️ Neutral: Tín hiệu trung lập

#### Note:
- Cần API server chạy (port 8501) để FA/TA hoạt động
- Nếu API offline: Dashboard vẫn hoạt động nhưng FA/TA sẽ không có dữ liệu

### Tab 4: Watchlist

#### Thêm mã vào watchlist:
1. Nhập mã cổ phiếu
2. Nhấn "➕ Add"
3. Hoặc từ Tab 1: Nhấn "⭐ Add to Watchlist"

#### Theo dõi:
- Xem giá real-time
- Kiểm tra % thay đổi
- Monitor volume

#### Xóa khỏi watchlist:
- Nhấn "❌" bên cạnh mã muốn xóa

#### Tips:
- Watchlist được lưu trong session
- Refresh page sẽ mất watchlist
- Tương lai: Sẽ lưu vào database hoặc local storage

### Tab 5: Price Alerts

#### Tạo Alert:
1. Nhập mã cổ phiếu
2. Chọn điều kiện:
   - **Above**: Alert khi giá vượt ngưỡng
   - **Below**: Alert khi giá xuống dưới ngưỡng
3. Nhập giá ngưỡng (VND)
4. Nhấn "➕ Add Alert"

#### Kiểm tra Alerts:
- Quay lại Tab 1 (Technical Chart)
- Load mã cổ phiếu có alert
- Nếu điều kiện đạt → Hiển thị warning

#### Quản lý Alerts:
- Xem danh sách active alerts
- Nhấn "🗑️ Delete" để xóa

#### Use Cases:
- Alert mua: `ACB below 24000` → Mua khi giá giảm
- Alert bán: `VIC above 50000` → Bán khi đạt target
- Alert breakout: `FPT above 120000` → Theo dõi đột phá

## 💡 Tips & Best Practices

### 1. Workflow hiệu quả
```
1. Thêm mã vào Watchlist
2. Theo dõi giá ở Tab Watchlist
3. Khi có biến động → Tab Technical Chart để phân tích
4. Check FA/TA để xác nhận
5. Set Price Alert cho entry/exit points
```

### 2. Technical Analysis
- Kết hợp nhiều indicators
- MA + RSI + MACD cho tín hiệu mạnh hơn
- Xác nhận với volume

### 3. Fundamental Analysis
- Check P/E so với ngành
- ROE > 15% là tốt
- D/E < 1 là an toàn

### 4. Multi-Stock Comparison
- So sánh cổ phiếu cùng ngành
- Tìm outperformer
- Xác định xu hướng sector

### 5. Watchlist Management
- Nhóm theo ngành
- Track 10-20 mã
- Daily review

### 6. Price Alerts
- Set multiple alerts
- Conservative entry
- Aggressive exit
- Risk management

## 🎨 Tùy chỉnh

### Theme
- Settings (góc trên phải) → Theme
- Light/Dark mode
- Wide mode cho nhiều data hơn

### Indicators
- Customize theo strategy
- Scalping: MA20, RSI
- Swing: MA50, MA200, MACD
- Long-term: MA200, Bollinger Bands

### Timeframes
- Day trading: 30-90 ngày
- Swing trading: 180-365 ngày
- Position trading: 730+ ngày

## 🐛 Troubleshooting

### Dashboard không load được
```bash
# Kiểm tra port 8503
lsof -i :8503

# Kill nếu đã được sử dụng
kill -9 <PID>

# Restart dashboard
python start_dashboard_advanced.py
```

### FA/TA Analysis không có data
```bash
# Kiểm tra API server
curl http://localhost:8501/health

# Nếu API offline, start server
python start_server.py
```

### Lỗi "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Indicators không hiển thị
- Check đủ dữ liệu (MA200 cần ít nhất 200 ngày)
- Chọn timeframe dài hơn

### Chart lag/slow
- Giảm số lượng indicators
- Chọn timeframe ngắn hơn
- Close các tabs không dùng

## 📊 Ví dụ Use Cases

### Use Case 1: Scalping Strategy
```
1. Tab Technical Chart
2. Timeframe: 30 ngày
3. Indicators: MA20, RSI, MACD
4. Watch cho oversold (RSI < 30)
5. Confirm với MACD crossover
6. Set alert below current support
```

### Use Case 2: Sector Rotation
```
1. Tab Multi-Stock Comparison
2. Compare: VCB, TCB, ACB, MBB (Banking)
3. Identify outperformer
4. Check FA in Tab 3
5. Add winner to Watchlist
6. Set alert for entry
```

### Use Case 3: Swing Trading
```
1. Tab Technical Chart
2. Timeframe: 180 ngày
3. Indicators: MA50, MA200, Bollinger Bands
4. Wait cho Golden Cross
5. Confirm with FA (P/E, ROE)
6. Set alert at MA50 for stop-loss
```

### Use Case 4: Portfolio Review
```
1. Add all holdings to Watchlist
2. Daily check in Watchlist tab
3. If any drops > 5% → Tab Technical Chart
4. Analyze with indicators
5. Decision: Hold/Sell based on signals
```

## 🔄 Tích hợp với hệ thống

### Với API Server
```python
# Dashboard tự động call API endpoints:
GET /stock/{symbol}/fa           # Fundamental data
GET /stock/{symbol}/ta/analyze   # Technical analysis
GET /stock/{symbol}/historical   # Price data
```

### Với n8n Workflow
```
1. n8n trigger: Price alert từ dashboard
2. n8n action: Send notification
3. n8n action: Log to database
4. n8n action: Update portfolio
```

## 📈 Roadmap

### Upcoming Features:
- [ ] Save Watchlist to local storage
- [ ] Export charts as images
- [ ] Email/Telegram notifications for alerts
- [ ] Backtesting integration
- [ ] Portfolio tracking
- [ ] News sentiment analysis
- [ ] Dark theme by default
- [ ] Mobile app version

## 📞 Support

### Logs:
```bash
# Nếu có lỗi, check terminal output
# Hoặc check Streamlit logs
~/.streamlit/logs/
```

### API Health:
```bash
curl http://localhost:8501/health
```

### Dashboard Health:
```bash
curl http://localhost:8503
```

## 📝 Notes

- Dashboard sử dụng **session state** để lưu Watchlist và Alerts
- Refresh page sẽ mất data → Cần implement persistent storage
- Cache data 5 phút để tăng tốc độ
- API integration cần server chạy ở port 8501

## 🎯 Kết luận

VNStock Advanced Dashboard là công cụ mạnh mẽ cho:
- ✅ Day traders: Technical indicators & alerts
- ✅ Swing traders: Multi-stock comparison & FA/TA
- ✅ Long-term investors: Fundamental analysis & watchlist
- ✅ Portfolio managers: Multi-stock tracking & alerts

**Happy Trading! 📈💰**

