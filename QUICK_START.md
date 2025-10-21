# 🚀 VNStock - Hướng dẫn nhanh

## 📋 TỔNG QUAN HỆ THỐNG

VNStock là hệ thống phân tích cổ phiếu Việt Nam toàn diện với 3 thành phần chính:

```
┌─────────────────────────────────────────────────────────────┐
│                    VNSTOCK ECOSYSTEM                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. API SERVER (Port 8501)                                  │
│     • RESTful API                                           │
│     • FA Analysis (P/E, ROE, D/E)                          │
│     • TA Analysis (MA, RSI, MACD)                          │
│     • Stock Screener                                        │
│     • Backtesting                                           │
│                                                              │
│  2. DASHBOARD BASIC (Port 8502)                             │
│     • Biểu đồ nến (Candlestick)                            │
│     • Khối lượng giao dịch                                  │
│     • Metrics cơ bản                                        │
│                                                              │
│  3. DASHBOARD ADVANCED (Port 8503)                          │
│     • Technical Indicators (MA, RSI, MACD, BB)             │
│     • Multi-Stock Comparison                                │
│     • FA/TA Integration                                     │
│     • Personal Watchlist                                    │
│     • Price Alerts                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 CHỨC NĂNG CHI TIẾT

### 1️⃣ API SERVER (Backend)

#### Mô tả:
- RESTful API server để lấy dữ liệu cổ phiếu
- Phân tích FA (Fundamental Analysis)
- Phân tích TA (Technical Analysis)
- Sàng lọc cổ phiếu (Stock Screener)
- Kiểm thử chiến lược (Backtesting)

#### Khởi chạy:
```bash
# Activate virtual environment
source venv/bin/activate

# Chạy API server
python start_server.py
```

#### Truy cập:
- **URL**: `http://localhost:8501`
- **API Docs**: `http://localhost:8501/docs`
- **Health Check**: `http://localhost:8501/health`

#### Các API Endpoints:

##### 📊 Dữ liệu cổ phiếu:
```bash
# Lấy toàn bộ dữ liệu
GET /stock/{symbol}
curl "http://localhost:8501/stock/ACB"

# Lấy dữ liệu theo khoảng thời gian
GET /stock/{symbol}?start_date=2023-01-01&end_date=2024-01-01
curl "http://localhost:8501/stock/ACB?start_date=2023-01-01&end_date=2024-01-01"

# Lấy thông tin tổng quan
GET /stock/{symbol}/overview
curl "http://localhost:8501/stock/ACB/overview"

# Lấy dữ liệu lịch sử
GET /stock/{symbol}/historical
curl "http://localhost:8501/stock/ACB/historical"

# Lấy dữ liệu tài chính
GET /stock/{symbol}/financial
curl "http://localhost:8501/stock/ACB/financial"
```

##### 🧮 Phân tích FA (Fundamental Analysis):
```bash
# Tính toán các chỉ số FA
GET /stock/{symbol}/fa
curl "http://localhost:8501/stock/ACB/fa"

# Response:
# {
#   "ratios": {
#     "PE": null,
#     "ROE": 19.46,
#     "DE": 9.7
#   },
#   "data_quality": {...},
#   "completeness": {...}
# }

# Lấy giải thích FA
GET /stock/{symbol}/fa/interpret
curl "http://localhost:8501/stock/ACB/fa/interpret"
```

##### 📈 Phân tích TA (Technical Analysis):
```bash
# Tính toán các chỉ báo TA
GET /stock/{symbol}/ta
curl "http://localhost:8501/stock/FPT/ta"

# Response:
# {
#   "indicators": {
#     "MA50": 120500.0,
#     "MA200": 115000.0,
#     "RSI": 65.5,
#     "MACD": {...}
#   }
# }

# Phân tích tín hiệu TA
GET /stock/{symbol}/ta/analyze
curl "http://localhost:8501/stock/FPT/ta/analyze"

# Response:
# {
#   "indicators_analysis": {
#     "Moving_Averages": {...},
#     "RSI": {...},
#     "MACD": {...}
#   },
#   "signals": ["BULLISH: Golden Cross"],
#   "overall_trend": "BULLISH"
# }

# Vẽ biểu đồ TA (trả về image)
GET /stock/{symbol}/ta/chart
curl "http://localhost:8501/stock/FPT/ta/chart" --output chart.png
```

##### 🔍 Stock Screener:
```bash
# Lấy danh sách tất cả cổ phiếu HOSE
GET /screener/list
curl "http://localhost:8501/screener/list"

# Sàng lọc cổ phiếu (20 mã đầu tiên)
GET /screener/screen
curl "http://localhost:8501/screener/screen"

# Response:
# {
#   "total_screened": 20,
#   "matched_stocks": [
#     {
#       "symbol": "ACB",
#       "pe": 12.5,
#       "roe": 18.5,
#       "price_vs_ma50": "above"
#     }
#   ]
# }

# Sàng lọc 1 mã cụ thể
GET /screener/{symbol}
curl "http://localhost:8501/screener/ACB"
```

##### 🔙 Backtesting:
```bash
# Chạy backtest với chiến lược MA crossover
GET /backtest/{symbol}
curl "http://localhost:8501/backtest/TCB"

# Response:
# {
#   "symbol": "TCB",
#   "strategy": "MA Crossover",
#   "results": {
#     "initial_capital": 100000000,
#     "final_equity": 120500000,
#     "return_pct": 20.5,
#     "win_rate": 65.5,
#     "max_drawdown": -15.2,
#     "total_trades": 45
#   }
# }
```

##### 📦 Batch Request (cho n8n):
```bash
# POST request để lấy nhiều loại dữ liệu
POST /stock/batch
curl -X POST "http://localhost:8501/stock/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "VIC",
    "start_date": "2023-01-01",
    "end_date": "2024-01-01"
  }'
```

---

### 2️⃣ DASHBOARD BASIC (Simple UI)

#### Mô tả:
- Giao diện web đơn giản để xem biểu đồ cổ phiếu
- Biểu đồ nến (Candlestick) tương tác
- Biểu đồ khối lượng giao dịch
- Metrics cơ bản (giá, volume, biến động)

#### Khởi chạy:
```bash
# Activate virtual environment
source venv/bin/activate

# Chạy dashboard basic
python start_dashboard.py
```

#### Truy cập:
- **URL**: `http://localhost:8502`
- **Network**: `http://192.168.1.4:8502`

#### Cách sử dụng:

1. **Nhập mã cổ phiếu**
   - Gõ mã: VD: ACB, VIC, FPT, TCB
   - Sidebar bên trái

2. **Chọn khoảng thời gian**
   - 30 ngày
   - 90 ngày (3 tháng)
   - 180 ngày (6 tháng)
   - 365 ngày (1 năm) - Mặc định
   - 730 ngày (2 năm)
   - 1095 ngày (3 năm)

3. **Nhấn "Tải dữ liệu"**
   - Hệ thống sẽ load dữ liệu từ vnstock
   - Hiển thị metrics và biểu đồ

4. **Phân tích biểu đồ**
   - **Zoom**: Click và kéo trên biểu đồ
   - **Pan**: Shift + Click và kéo
   - **Reset**: Double-click
   - **Hover**: Di chuột để xem chi tiết

5. **Xem dữ liệu chi tiết**
   - Mở expander "Xem dữ liệu chi tiết"
   - Export CSV nếu cần

#### Tính năng:
- ✅ Biểu đồ nến Plotly tương tác
- ✅ Khối lượng giao dịch với màu sắc
- ✅ Metrics: Giá, High/Low, Volume
- ✅ Thống kê: Volatility, Total Volume
- ✅ Export data to CSV

---

### 3️⃣ DASHBOARD ADVANCED (Professional Trading Platform)

#### Mô tả:
- Platform phân tích chuyên nghiệp
- Technical indicators đầy đủ
- So sánh nhiều cổ phiếu
- Tích hợp FA/TA analysis
- Quản lý watchlist
- Price alerts

#### Khởi chạy:
```bash
# Activate virtual environment
source venv/bin/activate

# Chạy dashboard advanced
python start_dashboard_advanced.py

# LƯU Ý: Cần API server chạy (port 8501) để FA/TA hoạt động
```

#### Truy cập:
- **URL**: `http://localhost:8503`
- **Network**: `http://192.168.1.4:8503`

#### Các Tab chức năng:

##### 📈 TAB 1: TECHNICAL CHART

**Chức năng:**
- Biểu đồ nến với technical indicators
- Tùy chọn indicators: MA20, MA50, MA200, EMA12, RSI, MACD, Bollinger Bands
- Multi-subplot layout chuyên nghiệp
- Quick statistics

**Cách sử dụng:**

1. **Cấu hình (Sidebar bên trái)**
   ```
   • Nhập mã: ACB, VIC, FPT...
   • Chọn timeframe: 30 ngày - 2 năm
   • Chọn indicators:
     ☑ MA20 (Moving Average 20)
     ☑ MA50 (Moving Average 50)
     ☐ MA200 (Moving Average 200)
     ☐ EMA12 (Exponential MA 12)
     ☑ RSI (Relative Strength Index)
     ☑ MACD (Moving Average Convergence Divergence)
     ☐ BB (Bollinger Bands)
   ```

2. **Load Chart**
   - Nhấn "🔄 Load Chart"
   - Xem metrics: Current Price, High, Low, Avg Volume
   - Kiểm tra price alerts (nếu có)

3. **Phân tích**
   - **Biểu đồ nến**: Xác định xu hướng
   - **RSI**: 
     - > 70: Overbought (quá mua) ⚠️
     - < 30: Oversold (quá bán) ✅
     - 30-70: Neutral
   - **MACD**:
     - MACD > Signal: Bullish ✅
     - MACD < Signal: Bearish ⚠️
   - **Moving Averages**:
     - Golden Cross (MA ngắn > MA dài): Buy signal
     - Death Cross (MA ngắn < MA dài): Sell signal

4. **Quick Stats**
   - Mở expander "Quick Statistics"
   - Xem RSI và MACD hiện tại
   - Tín hiệu tự động

5. **Add to Watchlist**
   - Nhấn "⭐ Add to Watchlist"
   - Mã sẽ được lưu vào watchlist

**Use Case:**
```
Ví dụ: Phân tích ACB
1. Nhập "ACB"
2. Chọn 180 ngày
3. Check: MA20, MA50, RSI, MACD
4. Load Chart
5. Phân tích:
   - RSI = 41 → Neutral
   - MACD < Signal → Bearish
   - MA20 < MA50 → Downtrend
   → Kết luận: Đợi tín hiệu mua rõ ràng hơn
```

##### 📊 TAB 2: MULTI-STOCK COMPARISON

**Chức năng:**
- So sánh tối đa 6 mã cổ phiếu
- Normalized chart (base = 100)
- Performance summary table

**Cách sử dụng:**

1. **Nhập danh sách mã**
   ```
   Enter stock symbols: ACB,VCB,TCB,MBB
   (Cách nhau bởi dấu phẩy)
   ```

2. **Chọn timeframe**
   - 30, 90, 180, 365 ngày

3. **Nhấn "📈 Compare"**

4. **Phân tích biểu đồ**
   - Biểu đồ normalized (tất cả bắt đầu từ 100)
   - Mã nào tăng cao nhất = outperformer
   - Mã nào giảm = underperformer

5. **Xem Performance Summary**
   - % Change của từng mã
   - High, Low prices
   - Average Volume

**Use Case:**
```
Ví dụ: So sánh ngân hàng
1. Nhập: ACB,VCB,TCB,MBB
2. Timeframe: 365 ngày
3. Compare
4. Kết quả:
   VCB: +25% → Best performer
   TCB: +18%
   ACB: +12%
   MBB: +8% → Worst performer
→ Quyết định: Nên đầu tư VCB
```

##### 🧮 TAB 3: FA/TA ANALYSIS

**Chức năng:**
- Fundamental Analysis (P/E, ROE, D/E)
- Technical Analysis (MA, RSI, MACD)
- Overall signals

**Cách sử dụng:**

1. **Nhập mã cổ phiếu**
   ```
   Stock Symbol: ACB
   ```

2. **Chọn loại phân tích**
   - ◉ Fundamental (FA)
   - ◯ Technical (TA)
   - ◯ Both

3. **Nhấn "🔍 Analyze"**

4. **Xem kết quả FA**
   ```
   P/E Ratio: N/A (insufficient data)
   ROE: 19.46% ✅ Good
   D/E: 9.7 ⚠️ High
   
   Data Quality: ████████░░ 66.7%
   
   Quick Analysis:
   ℹ️ Good profitability, check debt levels
   ```

5. **Xem kết quả TA**
   ```
   Moving Averages:
   MA50: 26,375 VND (Price: below)
   MA200: 22,675 VND (Price: above)
   ✅ Golden Cross
   
   RSI: 41.11 - ℹ️ Neutral
   MACD: -122.24 - ⚠️ Bearish
   
   Signals:
   ✅ BULLISH: Golden Cross detected
   ⚠️ BEARISH: MACD below Signal
   
   Overall Trend: ℹ️ NEUTRAL
   ```

**Giải thích chỉ số:**

**Fundamental Analysis:**
- **P/E < 15**: Undervalued (rẻ)
- **ROE > 15%**: Good profitability (lợi nhuận tốt)
- **D/E < 1**: Safe leverage (đòn bẩy an toàn)
- **D/E > 2**: High risk (rủi ro cao)

**Technical Analysis:**
- **Golden Cross**: MA ngắn cắt lên MA dài → Tín hiệu mua
- **Death Cross**: MA ngắn cắt xuống MA dài → Tín hiệu bán
- **RSI > 70**: Overbought → Có thể giảm
- **RSI < 30**: Oversold → Có thể tăng
- **MACD > Signal**: Bullish → Xu hướng tăng
- **MACD < Signal**: Bearish → Xu hướng giảm

**Use Case:**
```
Ví dụ: Quyết định mua ACB
1. Analyze: Both
2. FA: ROE = 19.46% (Good) ✅
        D/E = 9.7 (High) ⚠️
3. TA: Golden Cross ✅
        MACD Bearish ⚠️
4. Overall: NEUTRAL
→ Quyết định: Đợi thêm tín hiệu rõ ràng
```

##### ⭐ TAB 4: WATCHLIST

**Chức năng:**
- Lưu danh sách mã yêu thích
- Track giá real-time
- Quick add/remove

**Cách sử dụng:**

1. **Thêm mã vào watchlist**
   ```
   Add new stock: [ACB]
   Nhấn "➕ Add"
   ```

2. **Xem bảng watchlist**
   ```
   Symbol | Price      | Change (%) | Volume
   -------|------------|------------|--------
   ACB    | 25,100     | +2.00%     | 10.5M
   VCB    | 82,500     | -1.50%     | 5.2M
   TCB    | 25,300     | +0.80%     | 8.9M
   ```

3. **Xóa khỏi watchlist**
   - Nhấn "❌ [Symbol]" để xóa

**Use Case:**
```
Workflow hàng ngày:
1. Morning: Check watchlist
2. Nếu có mã tăng/giảm mạnh → Tab 1 để phân tích
3. Nếu có tín hiệu mua → Tab 3 để confirm FA/TA
4. Set price alert ở Tab 5
```

##### 🔔 TAB 5: PRICE ALERTS

**Chức năng:**
- Thiết lập alerts khi giá đạt ngưỡng
- Auto-notification
- Multi-alert management

**Cách sử dụng:**

1. **Tạo alert**
   ```
   Stock Symbol: ACB
   Condition: [above] hoặc [below]
   Price (VND): 25000
   Nhấn "➕ Add Alert"
   ```

2. **Xem danh sách alerts**
   ```
   ACB - Alert when price goes above 25,000 VND
   Created: 2025-10-21 10:30
   [🗑️ Delete]
   
   VCB - Alert when price goes below 80,000 VND
   Created: 2025-10-21 10:35
   [🗑️ Delete]
   ```

3. **Nhận notification**
   - Quay lại Tab 1 (Technical Chart)
   - Load mã có alert
   - Nếu điều kiện đạt → Hiển thị warning:
     ```
     🔔 Alert! ACB is above 25,000 VND
     ```

**Use Case:**
```
Ví dụ: Set alerts cho ACB

Strategy: Buy dip
1. Current price: 25,100 VND
2. Set alert: ACB below 24,000 (support level)
3. Khi giá về 24,000 → Notification
4. Vào Tab 1 check RSI/MACD
5. Nếu oversold → Mua

Strategy: Take profit
1. Buy price: 24,000 VND
2. Set alert: ACB above 26,000 (target +8%)
3. Khi giá lên 26,000 → Notification
4. Vào Tab 3 check TA
5. Nếu overbought → Bán
```

---

## 🔄 WORKFLOW THỰC TẾ

### Workflow 1: Day Trading

```
Buổi sáng (9:00 AM):
├─ 1. Mở Dashboard Advanced → Tab Watchlist
├─ 2. Check giá và % change
├─ 3. Chọn mã có biến động lớn (VD: ACB +3%)
├─ 4. Tab Technical Chart:
│     • Load ACB, timeframe 30 ngày
│     • Check indicators: MA20, RSI, MACD
│     • RSI = 68 (gần overbought)
│     • MACD bullish
├─ 5. Tab FA/TA Analysis:
│     • Check overall signal
│     • Confirm bullish trend
└─ 6. Quyết định: Mua ACB
      Set alert: ACB above 26,000 (target)
      Set alert: ACB below 24,000 (stop-loss)

Trong ngày:
├─ Monitor alerts
└─ Khi alert trigger → Tab 1 để re-analyze

Buổi chiều:
└─ Alert triggered: ACB above 26,000
   → Tab 1: Check RSI = 72 (overbought)
   → Quyết định: Bán để take profit
```

### Workflow 2: Swing Trading (3-5 ngày)

```
Day 1 - Research:
├─ 1. Tab Multi-Stock Comparison
│     Compare: ACB,VCB,TCB,MBB (90 ngày)
│     → VCB outperformer (+15%)
├─ 2. Tab FA/TA Analysis (VCB)
│     FA: P/E = 12, ROE = 18%, D/E = 0.8
│     → Fundamentals tốt
│     TA: Golden Cross, RSI = 55
│     → Technical tốt
└─ 3. Quyết định: Add VCB to Watchlist

Day 2 - Entry:
├─ Check Watchlist: VCB -2% (pullback)
├─ Tab Technical Chart:
│     RSI = 48 (từ 55 xuống, healthy pullback)
│     MACD vẫn bullish
└─ Quyết định: Mua VCB
   Set alert: VCB above 85,000 (target +3%)
   Set alert: VCB below 80,000 (stop -3%)

Day 3-4:
└─ Monitor watchlist daily

Day 5:
└─ Alert: VCB above 85,000
   → Tab 1: Check indicators
   → Quyết định: Bán (+3% profit)
```

### Workflow 3: Long-term Investment

```
Monthly Review:
├─ 1. Tab Stock Screener (API):
│     curl "http://localhost:8501/screener/screen"
│     → Danh sách mã có FA/TA tốt
├─ 2. Chọn top 3-5 mã
├─ 3. Tab FA/TA Analysis:
│     Phân tích chi tiết từng mã
│     Check ROE, D/E, P/E
└─ 4. Add selected stocks to Watchlist

Weekly Check:
├─ Tab Watchlist: Monitor prices
├─ Nếu giá giảm > 10%:
│     → Tab FA/TA để re-analyze
│     → Buy more hoặc Hold
└─ Set alerts cho từng mã

Yearly Rebalance:
├─ Tab Multi-Stock Comparison (365 ngày)
├─ Review performance
├─ Sell underperformers
└─ Buy outperformers
```

---

## 🚀 KHỞI CHẠY TOÀN BỘ HỆ THỐNG

### Option 1: Chạy riêng lẻ

```bash
# Terminal 1: API Server
source venv/bin/activate
python start_server.py
# Truy cập: http://localhost:8501

# Terminal 2: Dashboard Basic
source venv/bin/activate
python start_dashboard.py
# Truy cập: http://localhost:8502

# Terminal 3: Dashboard Advanced
source venv/bin/activate
python start_dashboard_advanced.py
# Truy cập: http://localhost:8503
```

### Option 2: Chạy tất cả trong background

```bash
# Activate venv
source venv/bin/activate

# Start all services
python start_server.py &
python start_dashboard.py &
python start_dashboard_advanced.py &

# Check status
ps aux | grep python

# View logs
tail -f *.log

# Stop all
pkill -f "start_server.py"
pkill -f "start_dashboard.py"
pkill -f "start_dashboard_advanced.py"
```

### Option 3: Script tự động

```bash
#!/bin/bash
# Tạo file: start_all.sh

echo "🚀 Starting VNStock Ecosystem..."

# Activate venv
source venv/bin/activate

# Start API Server
echo "Starting API Server (port 8501)..."
python start_server.py > api.log 2>&1 &
API_PID=$!

# Wait 5 seconds
sleep 5

# Start Dashboard Basic
echo "Starting Dashboard Basic (port 8502)..."
python start_dashboard.py > dashboard_basic.log 2>&1 &
BASIC_PID=$!

# Start Dashboard Advanced
echo "Starting Dashboard Advanced (port 8503)..."
python start_dashboard_advanced.py > dashboard_advanced.log 2>&1 &
ADVANCED_PID=$!

echo "✅ All services started!"
echo "API Server PID: $API_PID"
echo "Dashboard Basic PID: $BASIC_PID"
echo "Dashboard Advanced PID: $ADVANCED_PID"
echo ""
echo "Access:"
echo "  API: http://localhost:8501"
echo "  Basic: http://localhost:8502"
echo "  Advanced: http://localhost:8503"

# Chạy:
chmod +x start_all.sh
./start_all.sh
```

---

## 📚 TÀI LIỆU CHI TIẾT

- **README.md**: Tổng quan hệ thống
- **DASHBOARD_GUIDE.md**: Hướng dẫn Dashboard Basic
- **DASHBOARD_ADVANCED_GUIDE.md**: Hướng dẫn Dashboard Advanced
- **FA_ANALYSIS_GUIDE.md**: Hướng dẫn Fundamental Analysis
- **DOCKER_DEPLOYMENT.md**: Triển khai Docker

---

## 💡 TIPS & BEST PRACTICES

### Trading Tips:

1. **Luôn kết hợp FA + TA**
   - FA để chọn cổ phiếu chất lượng
   - TA để timing vào lệnh

2. **Sử dụng Multi-Stock Comparison**
   - So sánh trong cùng ngành
   - Chọn outperformer

3. **Set Price Alerts**
   - Entry points (support levels)
   - Exit points (resistance levels)
   - Stop-loss levels

4. **Watchlist Management**
   - Track 10-20 mã
   - Daily review
   - Remove non-performers

### Technical Tips:

1. **Cache hiệu quả**
   - Dashboard cache 5 phút
   - Tránh spam API

2. **Network access**
   - Basic: localhost:8502
   - Advanced: localhost:8503
   - LAN: 192.168.1.4:8503

3. **API integration**
   - FA/TA cần API server running
   - Graceful fallback nếu API offline

---

## 🆘 TROUBLESHOOTING

### Lỗi thường gặp:

**1. Port already in use**
```bash
# Check port
lsof -i :8501
lsof -i :8502
lsof -i :8503

# Kill process
kill -9 <PID>
```

**2. Module not found**
```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt
```

**3. API connection error (Dashboard Advanced)**
```bash
# Make sure API server is running
curl http://localhost:8501/health

# If not running, start it
python start_server.py
```

**4. No data for symbol**
- Check mã cổ phiếu đúng chưa
- Thử mã khác (ACB, VCB, FPT)
- Check internet connection

---

## 🎯 KẾT LUẬN

VNStock cung cấp đầy đủ công cụ cho:
- ✅ **Day traders**: Technical indicators & alerts
- ✅ **Swing traders**: Multi-stock comparison & FA/TA
- ✅ **Long-term investors**: Fundamental analysis & screener
- ✅ **Portfolio managers**: Watchlist & monitoring

**Happy Trading! 📈💰**

