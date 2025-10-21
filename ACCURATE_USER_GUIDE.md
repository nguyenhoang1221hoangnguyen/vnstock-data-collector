# 📚 HƯỚNG DẪN CHÍNH XÁC - VNSTOCK 2.0

> **Cập nhật:** 21/10/2025  
> **Phiên bản:** 2.0  
> **Trạng thái:** Đang chạy

---

## 🚀 HỆ THỐNG ĐANG CHẠY

### ✅ Services đang hoạt động:

| Service | Port | URL | Trạng thái |
|---------|------|-----|-----------|
| **API Server** | 8501 | http://localhost:8501 | ✅ Running |
| **API Documentation** | 8501 | http://localhost:8501/docs | ✅ Running |
| **Advanced Dashboard** | 8502 | http://localhost:8502 | ✅ Running |

### ❌ Services KHÔNG chạy:

| Service | Port | Ghi chú |
|---------|------|---------|
| Basic Dashboard | 8502 | Không cần thiết - Advanced Dashboard đã bao gồm tất cả |

---

## 📊 DASHBOARD HIỆN TẠI

### 🎯 Advanced Dashboard (Port 8502)

**URL:** http://localhost:8502

**File:** `dashboard_advanced.py`

**6 TABS chính:**

#### 1️⃣ Tab 1: 📈 Technical Analysis
**Chức năng:**
- ✅ Biểu đồ nến tương tác (Candlestick)
- ✅ Moving Averages: MA20, MA50, MA200, EMA12
- ✅ RSI (Relative Strength Index)
- ✅ MACD (Moving Average Convergence Divergence)
- ✅ Bollinger Bands
- ✅ Volume chart

**Cách sử dụng:**
1. Nhập mã cổ phiếu (VD: FPT, VCB, HPG)
2. Chọn khoảng thời gian (180 days, 365 days, 2 years)
3. Chọn indicators muốn hiển thị
4. Xem biểu đồ và phân tích

---

#### 2️⃣ Tab 2: 📊 Multi-Stock Comparison
**Chức năng:**
- ✅ So sánh đồng thời tối đa 6 mã cổ phiếu
- ✅ Normalized chart (base = 100)
- ✅ Performance summary table
- ✅ Price comparison

**Cách sử dụng:**
1. Nhập tối đa 6 mã cổ phiếu, cách nhau bằng dấu phẩy
   - Ví dụ: `FPT, VCB, HPG, VNM, MSN, VIC`
2. Chọn khoảng thời gian
3. Click "Compare Stocks"
4. Xem biểu đồ so sánh và bảng thống kê

---

#### 3️⃣ Tab 3: 🧮 FA/TA Integration
**Chức năng:**
- ✅ Fundamental Analysis (FA):
  - P/E Ratio, ROE, Net Profit Margin, D/E Ratio, EPS
- ✅ Technical Analysis (TA):
  - Trend signals, Momentum signals
- ✅ Overall Rating: A+, A, B, C, D, F
- ✅ Recommendation: Buy/Hold/Sell

**Cách sử dụng:**
1. Nhập mã cổ phiếu
2. Click "Analyze"
3. Xem FA ratios (bên trái)
4. Xem TA signals (bên phải)
5. Xem Overall Assessment

**⚠️ Lưu ý:**
- FA data phụ thuộc vào báo cáo tài chính công ty
- Một số mã có thể thiếu FA data → bình thường
- TA data luôn có sẵn từ giá lịch sử

---

#### 4️⃣ Tab 4: ⭐ Watchlist
**Chức năng:**
- ✅ Lưu danh sách cổ phiếu yêu thích
- ✅ Real-time price tracking
- ✅ Quick add/remove
- ✅ Persistent storage (SQLite database)

**Cách sử dụng:**
1. Nhập mã cổ phiếu và tên (VD: FPT - FPT Corporation)
2. Click "Add to Watchlist"
3. Xem danh sách theo dõi
4. Click "Remove" để xóa

**Database:** `vnstock.db` → table `watchlist`

---

#### 5️⃣ Tab 5: 🔔 Price Alerts
**Chức năng:**
- ✅ Thiết lập cảnh báo giá
- ✅ Điều kiện: Above (trên) / Below (dưới)
- ✅ Multi-alert management
- ✅ Notification integration (Telegram/Email/Discord)

**Cách sử dụng:**
1. Nhập mã cổ phiếu
2. Chọn điều kiện (Above/Below)
3. Nhập giá mục tiêu (VD: 95000)
4. Click "Set Alert"
5. Xem danh sách alerts
6. Click "Delete" để xóa alert

**⚠️ Lưu ý:**
- Cần cấu hình `notification_config.json` để nhận thông báo
- Alerts được lưu trong database
- Monitoring tự động kiểm tra giá theo thời gian thực

**Database:** `vnstock.db` → table `alerts`

---

#### 6️⃣ Tab 6: 🎯 Stock Screener & Classification **🆕**
**Chức năng:**
- ✅ Quét toàn thị trường (HOSE, HNX, UPCOM)
- ✅ Phân loại theo 5 tiêu chí:
  1. **Growth Potential** (Tiềm năng tăng trưởng)
  2. **Risk Level** (Mức độ rủi ro)
  3. **Market Cap** (Vốn hóa)
  4. **Momentum** (Xu hướng)
  5. **Overall Rating** (A+, A, B, C, D, F)
- ✅ Lọc theo tiêu chí
- ✅ Download kết quả CSV
- ✅ Single stock classification

**Cách sử dụng:**

**A. Quét thị trường (Market Scan):**
1. **Settings Panel (Sidebar):**
   - **Exchange**: Chọn sàn (HOSE/HNX/UPCOM)
   - **Stock Limit**: Số lượng mã quét (5-50)
     - Khuyến nghị: 10-20 mã cho lần đầu
   - **Scan Delay**: Thời gian chờ giữa các requests (6-10s)
     - Khuyến nghị: 8 giây để tránh rate limit

2. **Filters (Optional):**
   - Min Growth Score: 1-9
   - Max Risk Score: 1-10
   - Min Rating: F, D, C, B, A, A+
   - Min Overall Score: 0-10

3. Click **"🔍 Scan Market"**

4. **Results:**
   - Bảng kết quả với tất cả thông tin phân loại
   - Summary metrics (tổng số stocks, trung bình scores)
   - Distribution charts (phân bố rating, risk level)
   - Download CSV button

**B. Phân loại 1 cổ phiếu (Single Stock):**
1. Nhập mã cổ phiếu (VD: FPT)
2. Click "🔍 Classify Stock"
3. Xem kết quả chi tiết:
   - Growth category & score
   - Risk level & score
   - Market cap category
   - Momentum category
   - Overall rating & recommendation

**⚠️ Lưu ý QUAN TRỌNG:**

### Rate Limit & Timeout:
- **VNStock API có rate limit nghiêm ngặt**
- **Recommended settings:**
  - Stock Limit: 10-20 mã
  - Delay: 8-10 giây
  - Timeout tự động tính: `stocks × (4 + delay) × 1.5`
  
  Ví dụ: 20 stocks, 8s delay → 360s timeout

### Estimated Time:
- 5 stocks: ~60 giây
- 10 stocks: ~120 giây (2 phút)
- 20 stocks: ~240 giây (4 phút)
- 50 stocks: ~600 giây (10 phút)

### Errors thường gặp:
1. **"Read timed out"** → Giảm Stock Limit hoặc tăng Delay
2. **"API Error 500"** → Rate limit, chờ 2-3 phút rồi thử lại
3. **"No stocks classified"** → Check API server đang chạy
4. **FA data = 0** → Một số stocks thiếu báo cáo tài chính (bình thường)

### Best Practices:
1. **Lần đầu test:** Quét 5-10 mã với delay 8s
2. **Production:** Quét 20-30 mã với delay 8-10s
3. **Full scan:** Chia nhỏ thành nhiều lần (50 mã/lần)
4. **Nếu bị rate limit:** Chờ 5-10 phút rồi tiếp tục

---

## 🔌 API SERVER

### URL: http://localhost:8501

### Swagger UI: http://localhost:8501/docs

### 25+ Endpoints:

#### 1. Data Collection
```bash
# Lấy toàn bộ dữ liệu
GET /stock/{symbol}
GET /stock/{symbol}/overview
GET /stock/{symbol}/historical
GET /stock/{symbol}/financial
GET /stock/{symbol}/market

# Batch request
POST /stock/batch
```

#### 2. Fundamental Analysis (FA)
```bash
GET /stock/{symbol}/fa
GET /stock/{symbol}/fa/interpret
```

#### 3. Technical Analysis (TA)
```bash
GET /stock/{symbol}/ta
GET /stock/{symbol}/ta/analyze
GET /stock/{symbol}/ta/chart
```

#### 4. Stock Classification
```bash
GET /classify/stock/{symbol}
GET /classify/market?exchanges=HOSE&limit=20&delay=6.0
GET /classify/filter?min_growth_score=7&max_risk_score=6
GET /classify/top-picks?min_rating=B&limit=10
```

#### 5. Stock Screener
```bash
GET /screener/list?exchange=HOSE
POST /screener/screen
GET /screener/{symbol}
```

#### 6. Blue-chip Detector
```bash
GET /bluechip/scan?limit=10
POST /bluechip/add-to-watchlist
GET /bluechip/report
```

#### 7. Backtesting
```bash
GET /backtest/{symbol}?initial_capital=100000000
```

#### 8. Health Check
```bash
GET /health
```

---

## 🛠️ PYTHON MODULES (15+)

### Core Modules:

1. **vnstock_data_collector_simple.py**
   - Thu thập dữ liệu OHLCV, Financial, Overview
   - 15+ năm dữ liệu lịch sử
   - VND currency conversion

2. **fa_calculator.py**
   - Tính P/E, ROE, NPM, D/E, EPS
   - Data quality assessment
   - Interpretation

3. **ta_analyzer.py**
   - Basic indicators (MA, RSI, MACD, BB)
   - Signal detection
   - Chart plotting

4. **advanced_indicators.py**
   - 15+ advanced indicators
   - Ichimoku, ADX, Supertrend, etc.

5. **stock_classifier.py**
   - 5-dimensional classification
   - Market scanning
   - Filtering & top picks

6. **stock_screener.py**
   - FA/TA criteria screening
   - Multi-exchange support

7. **bluechip_detector.py**
   - Auto blue-chip detection
   - Scoring system

8. **backtesting_strategy.py**
   - MA Crossover strategy
   - Performance metrics

9. **portfolio_manager.py**
   - Paper trading
   - P&L tracking
   - Performance metrics

10. **news_sentiment.py**
    - News aggregation
    - Vietnamese NLP sentiment

11. **notifications.py**
    - Multi-channel (Telegram/Email/Discord)
    - Price alerts, Trade notifications

12. **drawing_tools.py**
    - Chart annotations
    - Save/Load drawings

13. **database.py**
    - SQLite management
    - 6 tables (watchlist, alerts, portfolio, etc.)

14. **main.py**
    - FastAPI application
    - 25+ endpoints

15. **dashboard_advanced.py**
    - Streamlit dashboard
    - 6 tabs interface

---

## 💾 DATABASE

### File: `vnstock.db` (SQLite)

### Tables:

1. **watchlist**
   ```sql
   - symbol (TEXT)
   - name (TEXT)
   - added_date (TIMESTAMP)
   ```

2. **alerts**
   ```sql
   - symbol (TEXT)
   - condition (TEXT: 'above'/'below')
   - target_price (REAL)
   - current_price (REAL)
   - status (TEXT: 'active'/'triggered'/'cancelled')
   - created_at (TIMESTAMP)
   ```

3. **chart_layouts**
   ```sql
   - symbol (TEXT)
   - layout_name (TEXT)
   - layout_data (TEXT: JSON)
   - created_at (TIMESTAMP)
   ```

4. **portfolio**
   ```sql
   - symbol (TEXT)
   - quantity (INTEGER)
   - avg_price (REAL)
   - current_price (REAL)
   - current_value (REAL)
   - pnl (REAL)
   - updated_at (TIMESTAMP)
   ```

5. **transactions**
   ```sql
   - symbol (TEXT)
   - action (TEXT: 'BUY'/'SELL')
   - quantity (INTEGER)
   - price (REAL)
   - total_amount (REAL)
   - timestamp (TIMESTAMP)
   ```

6. **settings**
   ```sql
   - key (TEXT)
   - value (TEXT)
   - updated_at (TIMESTAMP)
   ```

---

## 🚀 KHỞI ĐỘNG HỆ THỐNG

### Hiện tại đang chạy:

```bash
# API Server (port 8501)
Process ID: 83135, 86734
Command: python3 main.py

# Advanced Dashboard (port 8502)
Process ID: 86792
Command: streamlit run dashboard_advanced.py --server.port 8502
```

### Restart hệ thống:

#### Cách 1: Sử dụng Management Script
```bash
./manage_system.sh

# Menu options:
# 1. Start All Services
# 2. Stop All Services
# 3. Restart All Services
# 4. Check Status
# 5. View Logs
# 6. Exit
```

#### Cách 2: Manual
```bash
# Stop tất cả
pkill -f "python3 main.py"
pkill -f "streamlit run dashboard_advanced.py"

# Start lại
cd "/Users/nguyenhoang/Desktop/2025/hoc-tap code/vscode/VNSTOCK 2"
source venv/bin/activate

# Terminal 1: API
python3 main.py > logs_api.txt 2>&1 &

# Terminal 2: Dashboard
streamlit run dashboard_advanced.py --server.port 8502 > logs_dashboard.txt 2>&1 &
```

#### Cách 3: Start từ đầu
```bash
cd "/Users/nguyenhoang/Desktop/2025/hoc-tap code/vscode/VNSTOCK 2"
source venv/bin/activate

# API Server
python3 main.py

# Dashboard (terminal mới)
python start_dashboard_advanced.py
# → Sẽ chạy trên port 8503 (theo thiết kế)
```

---

## 📖 CÁC FILE HƯỚNG DẪN

| File | Nội dung |
|------|----------|
| `README.md` | Overview tổng quan |
| `COMPLETE_FEATURES_GUIDE.md` | Hướng dẫn đầy đủ 13 modules |
| **`ACCURATE_USER_GUIDE.md`** | **Hướng dẫn chính xác (file này)** ⭐ |
| `DASHBOARD_ADVANCED_GUIDE.md` | Chi tiết Advanced Dashboard |
| `CLASSIFICATION_GUIDE.md` | Hệ thống phân loại cổ phiếu |
| `SCREENER_DASHBOARD_GUIDE.md` | Stock Screener guide |
| `FA_ANALYSIS_GUIDE.md` | Fundamental Analysis guide |
| `BLUECHIP_DETECTOR_GUIDE.md` | Blue-chip detection |
| `QUICK_START.md` | Quick start guide |
| `INSTALLATION_GUIDE.md` | Cài đặt hệ thống |
| `BUGFIX_HISTORY.md` | Lịch sử sửa lỗi |
| `TIMEOUT_FIX.md` | Sửa lỗi timeout |

---

## 🎯 WORKFLOW THỰC TẾ

### Kịch bản 1: Phân tích 1 cổ phiếu
1. Mở http://localhost:8502
2. Vào Tab 1 (Technical Analysis)
3. Nhập mã: FPT
4. Xem biểu đồ và indicators
5. Vào Tab 3 (FA/TA Integration)
6. Click "Analyze" → Xem FA ratios + TA signals
7. Vào Tab 4 (Watchlist) → Add to Watchlist

### Kịch bản 2: So sánh nhiều cổ phiếu
1. Vào Tab 2 (Multi-Stock Comparison)
2. Nhập: `FPT, VCB, HPG, VNM, MSN, VIC`
3. Click "Compare Stocks"
4. Xem performance chart
5. Xem bảng so sánh

### Kịch bản 3: Tìm cổ phiếu tốt
1. Vào Tab 6 (Stock Screener)
2. Settings:
   - Exchange: HOSE
   - Limit: 20
   - Delay: 8s
3. Filters:
   - Min Growth Score: 7
   - Max Risk Score: 6
   - Min Rating: B
4. Click "Scan Market"
5. Đợi ~4 phút
6. Xem results → Lọc → Download CSV

### Kịch bản 4: Set price alert
1. Vào Tab 5 (Price Alerts)
2. Nhập:
   - Symbol: FPT
   - Condition: Above
   - Target Price: 95000
3. Click "Set Alert"
4. Hệ thống sẽ notify khi FPT > 95,000 VND

---

## 🔧 TROUBLESHOOTING

### 1. Dashboard không load
```bash
# Check process
ps aux | grep streamlit

# Restart
pkill -f streamlit
streamlit run dashboard_advanced.py --server.port 8502
```

### 2. API không response
```bash
# Check health
curl http://localhost:8501/health

# Check process
ps aux | grep "main.py"

# Restart
pkill -f "main.py"
python3 main.py
```

### 3. Stock Screener timeout
**Triệu chứng:** "Read timed out (read timeout=60)"

**Giải pháp:**
1. Giảm Stock Limit xuống 10
2. Tăng Delay lên 10s
3. Nếu vẫn lỗi → Chờ 5 phút rồi thử lại

### 4. FA data = 0
**Triệu chứng:** ROE=0, PE=0 trong kết quả

**Giải thích:**
- Một số stocks thiếu báo cáo tài chính
- API chưa cập nhật
- Công ty chưa công bố

**Không phải bug!** TA data vẫn có.

### 5. Rate Limit (API Error 500/502)
**Triệu chứng:** API trả về 500 hoặc 502

**Giải pháp:**
1. **Chờ 5-10 phút**
2. Tăng Delay lên 10s
3. Giảm số lượng stocks
4. Không quét quá nhanh

### 6. AuthSessionMissingError (Console)
**Triệu chứng:** Lỗi trong browser console

**Giải thích:**
- Lỗi NGOÀI hệ thống VNStock
- Thường từ n8n hoặc ứng dụng khác
- **Bỏ qua, không ảnh hưởng VNStock**

---

## 📊 HIỆU NĂNG

| Operation | Time | Notes |
|-----------|------|-------|
| Single stock data | 3-5s | Full 15+ years |
| FA calculation | 2-3s | 5 ratios |
| TA indicators | 2-3s | 15+ indicators |
| Classification | 4-5s | Full analysis |
| Market scan (10 stocks) | ~120s | With 8s delay |
| Market scan (20 stocks) | ~240s | With 8s delay |
| Market scan (50 stocks) | ~600s | With 8s delay |

---

## ✅ CHECKLIST HẰNG NGÀY

### Sáng (Trước giờ giao dịch):
- [ ] Check API health: `curl http://localhost:8501/health`
- [ ] Check Dashboard: http://localhost:8502
- [ ] Xem Watchlist (Tab 4)
- [ ] Check Price Alerts (Tab 5)

### Trong giờ giao dịch:
- [ ] Monitor real-time prices
- [ ] Check TA signals (Tab 1)
- [ ] Update Watchlist nếu cần

### Chiều (Sau giờ giao dịch):
- [ ] Scan market (Tab 6) - 20 stocks
- [ ] Review FA/TA (Tab 3)
- [ ] Update Portfolio nếu có giao dịch
- [ ] Set alerts cho ngày mai

---

## 🎯 KẾT LUẬN

**Hệ thống hiện tại:**
- ✅ API Server: http://localhost:8501 ✓
- ✅ Advanced Dashboard: http://localhost:8502 ✓
- ✅ 25+ API Endpoints ✓
- ✅ 6 Dashboard Tabs ✓
- ✅ SQLite Database ✓
- ✅ Full functionality ✓

**Không cần:**
- ❌ Basic Dashboard (đã được thay thế bởi Advanced)
- ❌ Port 8503 (đang dùng 8502)

**Ready for:**
- 🤖 AI Analysis
- 📊 Trading
- 💼 Portfolio Management
- 🔍 Stock Screening

---

**Happy Trading!** 🚀📈

_Last updated: 21/10/2025 - 21:45_  
_Version: 2.0 (Production)_  
_Status: Running on Port 8502_

