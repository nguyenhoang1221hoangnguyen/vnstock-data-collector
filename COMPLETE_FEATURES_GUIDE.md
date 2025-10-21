# 📚 HƯỚNG DẪN ĐẦY ĐỦ CÁC CHỨC NĂNG - VNSTOCK 2.0

## 🎯 Tổng quan hệ thống

**VNStock 2.0** là nền tảng phân tích chứng khoán Việt Nam toàn diện, bao gồm:
- ✅ **25+ API Endpoints** (FastAPI - Port 8501)
- ✅ **2 Dashboard tương tác** (Streamlit - Port 8502, 8503)
- ✅ **15+ Modules phân tích** (FA, TA, Classification, Portfolio, News...)
- ✅ **SQLite Database** (Persistent storage)
- ✅ **Multi-channel Notifications** (Telegram, Email, Discord)

---

## 📋 MỤC LỤC

1. [Thu thập dữ liệu (Data Collection)](#1-thu-thập-dữ-liệu)
2. [Phân tích cơ bản (Fundamental Analysis)](#2-phân-tích-cơ-bản-fa)
3. [Phân tích kỹ thuật (Technical Analysis)](#3-phân-tích-kỹ-thuật-ta)
4. [Phân loại cổ phiếu (Stock Classification)](#4-phân-loại-cổ-phiếu)
5. [Sàng lọc cổ phiếu (Stock Screener)](#5-sàng-lọc-cổ-phiếu)
6. [Phát hiện Blue-chip](#6-phát-hiện-blue-chip)
7. [Backtesting](#7-backtesting)
8. [Portfolio Management](#8-portfolio-management)
9. [News & Sentiment](#9-news--sentiment)
10. [Notifications](#10-notifications)
11. [Drawing Tools](#11-drawing-tools)
12. [Dashboard](#12-dashboard)
13. [Database](#13-database)

---

## 1. 📊 THU THẬP DỮ LIỆU

### Module: `vnstock_data_collector_simple.py`

### Chức năng:
- ✅ Thu thập 15+ năm dữ liệu OHLCV
- ✅ Lấy 17+ năm báo cáo tài chính
- ✅ Thông tin công ty và cổ đông
- ✅ Chuyển đổi VND chính xác (×1000)

### API Endpoints:

#### 1.1. Lấy toàn bộ dữ liệu
```bash
# GET - Single stock
curl "http://localhost:8501/stock/VIC?start_date=2023-01-01&end_date=2024-01-01"

# POST - Batch request (recommended for n8n)
curl -X POST "http://localhost:8501/stock/batch" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "VIC", "start_date": "2023-01-01", "end_date": "2024-01-01"}'
```

#### 1.2. Lấy từng loại dữ liệu
```bash
# Overview (thông tin tổng quan)
curl "http://localhost:8501/stock/VIC/overview"

# Historical data (dữ liệu lịch sử)
curl "http://localhost:8501/stock/VIC/historical?start_date=2023-01-01"

# Financial data (báo cáo tài chính)
curl "http://localhost:8501/stock/VIC/financial"

# Market data (dữ liệu thị trường)
curl "http://localhost:8501/stock/VIC/market"
```

### Response Format:
```json
{
  "success": true,
  "data": {
    "request_info": {
      "symbol": "VIC",
      "start_date": "2023-01-01",
      "end_date": "2024-01-01"
    },
    "overview": {...},
    "historical_data": {
      "daily_data": [...],  // 3940+ records
      "total_trading_days": 3940
    },
    "financial_data": {...},
    "ai_analysis_metadata": {
      "data_completeness": {...},
      "analysis_suggestions": [...],
      "currency_info": {
        "conversion": "Stock prices converted from thousands to full VND (×1000)"
      }
    }
  }
}
```

### Sử dụng trong Python:
```python
from vnstock_data_collector_simple import VNStockDataCollector

collector = VNStockDataCollector()
data = collector.get_full_stock_data('VIC', '2023-01-01', '2024-01-01')
```

---

## 2. 🧮 PHÂN TÍCH CƠ BẢN (FA)

### Module: `fa_calculator.py`

### Chức năng:
- ✅ Tính P/E Ratio
- ✅ Tính ROE (Return on Equity)
- ✅ Tính Net Profit Margin
- ✅ Tính Debt/Equity Ratio
- ✅ Tính EPS (Earnings Per Share)
- ✅ Đánh giá chất lượng dữ liệu
- ✅ Đưa ra khuyến nghị

### API Endpoints:

#### 2.1. Tính toán FA ratios
```bash
curl "http://localhost:8501/stock/FPT/fa"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "symbol": "FPT",
    "current_price": 93.0,
    "ratios": {
      "EPS": 581.6,
      "PE": 0.16,
      "ROE": 21.61,
      "NPM": 13.58,
      "DE": 1.04
    },
    "data_quality": {
      "EPS": "good",
      "PE": "good",
      "ROE": "good",
      "NPM": "good",
      "DE": "good"
    },
    "completeness": {
      "complete_ratios": 5,
      "total_ratios": 5,
      "percentage": 100.0
    }
  }
}
```

#### 2.2. Lấy interpretation (giải thích)
```bash
curl "http://localhost:8501/stock/FPT/fa/interpret"
```

### Sử dụng trong Python:
```python
from fa_calculator import calculate_fa_ratios, get_fa_interpretation

# Tính toán ratios
ratios = calculate_fa_ratios('FPT')
print(f"ROE: {ratios['ratios']['ROE']}%")

# Lấy giải thích
interpretation = get_fa_interpretation('FPT')
```

### Đánh giá:
- **P/E < 15**: Cổ phiếu được định giá hấp dẫn
- **ROE > 15%**: Hiệu quả sử dụng vốn tốt
- **NPM > 10%**: Biên lợi nhuận khỏe
- **D/E < 2.0**: Nợ ở mức an toàn

---

## 3. 📈 PHÂN TÍCH KỸ THUẬT (TA)

### Modules: `ta_analyzer.py`, `advanced_indicators.py`

### Chức năng:

#### Basic Indicators (4):
- ✅ Moving Averages (MA20, MA50, MA200, EMA12)
- ✅ RSI (14)
- ✅ MACD
- ✅ Bollinger Bands

#### Advanced Indicators (13+):
- ✅ Ichimoku Cloud
- ✅ ADX (Average Directional Index)
- ✅ Supertrend
- ✅ Parabolic SAR
- ✅ Stochastic Oscillator
- ✅ Williams %R
- ✅ CCI (Commodity Channel Index)
- ✅ OBV (On-Balance Volume)
- ✅ VWAP
- ✅ A/D Line
- ✅ ATR
- ✅ Keltner Channels
- ✅ Donchian Channels

### API Endpoints:

#### 3.1. Tính toán TA indicators
```bash
curl "http://localhost:8501/stock/FPT/ta"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "symbol": "FPT",
    "period_days": 365,
    "indicators": {
      "moving_averages": {
        "MA20": 88.5,
        "MA50": 85.2,
        "MA200": 82.1,
        "EMA12": 89.3
      },
      "rsi": {
        "current": 62.5,
        "status": "neutral"
      },
      "macd": {
        "MACD": 2.3,
        "Signal": 1.8,
        "Histogram": 0.5
      },
      "bollinger_bands": {
        "Upper": 95.2,
        "Middle": 88.5,
        "Lower": 81.8
      }
    }
  }
}
```

#### 3.2. Phân tích tín hiệu
```bash
curl "http://localhost:8501/stock/FPT/ta/analyze"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "signals": {
      "trend": {
        "status": "bullish",
        "strength": "strong",
        "details": [
          "Price above MA50",
          "MA20 > MA50 > MA200 (Golden Cross)",
          "MACD positive"
        ]
      },
      "momentum": {
        "status": "overbought",
        "RSI": 72.5
      }
    },
    "overall_assessment": "BULLISH: Strong uptrend but approaching overbought"
  }
}
```

#### 3.3. Vẽ biểu đồ TA
```bash
curl "http://localhost:8501/stock/FPT/ta/chart" --output FPT_chart.png
```

### Sử dụng trong Python:
```python
from ta_analyzer import calculate_ta_indicators, plot_technical_chart

# Tính indicators
ta_data = calculate_ta_indicators('FPT', period_days=365)
print(f"RSI: {ta_data['indicators']['rsi']['current']}")

# Vẽ biểu đồ
plot_technical_chart('FPT', period_days=365, save_path='FPT_chart.png')
```

---

## 4. 🎯 PHÂN LOẠI CỔ PHIẾU

### Module: `stock_classifier.py`

### Chức năng:
Phân loại cổ phiếu theo **5 tiêu chí**:

1. **Growth Potential** (Tiềm năng tăng trưởng)
   - High Growth (9), Growth (7), Stable (6), Value (5), Distressed (1)

2. **Risk Level** (Mức độ rủi ro)
   - Low (2), Medium (5), High (8), Very High (10)

3. **Market Cap** (Vốn hóa)
   - Mega Cap (>100,000 tỷ), Large Cap, Mid Cap, Small Cap

4. **Momentum** (Xu hướng)
   - Strong Uptrend (9), Uptrend (7), Sideways (5), Downtrend (3)

5. **Overall Rating** (Đánh giá tổng thể)
   - A+ (8.0+), A (7.0+), B (6.0+), C (5.0+), D (4.0+), F (<4.0)

### API Endpoints:

#### 4.1. Phân loại 1 cổ phiếu
```bash
curl "http://localhost:8501/classify/stock/FPT"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "symbol": "FPT",
    "classifications": {
      "growth": {
        "category": "growth",
        "score": 7,
        "description": "📈 Tăng trưởng ổn định",
        "roe": 21.61,
        "pe": 0.16,
        "npm": 13.58
      },
      "risk": {
        "category": "medium_risk",
        "risk_score": 5,
        "description": "🟡 Rủi ro trung bình",
        "volatility": 29.71,
        "debt_equity": 1.04
      },
      "market_cap": {
        "category": "small_cap",
        "market_cap_trillion": 0.0
      },
      "momentum": {
        "category": "sideways",
        "momentum_score": 5
      }
    },
    "overall_rating": {
      "score": 5.8,
      "rating": "C",
      "recommendation": "⏸️ Hold - Giữ"
    }
  }
}
```

#### 4.2. Quét toàn thị trường
```bash
curl "http://localhost:8501/classify/market?exchanges=HOSE&limit=20&delay=6.0"
```

#### 4.3. Lọc cổ phiếu theo tiêu chí
```bash
curl "http://localhost:8501/classify/filter?min_growth_score=7&max_risk_score=6&min_rating=B"
```

#### 4.4. Top picks (cổ phiếu tốt nhất)
```bash
curl "http://localhost:8501/classify/top-picks?min_rating=B&limit=10"
```

### Sử dụng trong Python:
```python
from stock_classifier import StockClassifier

classifier = StockClassifier()

# Phân loại 1 stock
result = classifier.classify_stock('FPT')
print(f"Rating: {result['overall_rating']['rating']}")

# Quét thị trường
df = classifier.scan_and_classify_market(exchanges=['HOSE'], limit=20, delay=6.0)
```

### Sử dụng CLI:
```bash
# Phân loại 1 stock
python classify_stock.py FPT

# Menu tương tác
./start_classifier.sh
```

---

## 5. 🔍 SÀNG LỌC CỔ PHIẾU

### Module: `stock_screener.py`

### Chức năng:
- ✅ Lọc theo FA criteria (ROE, P/E, NPM, D/E)
- ✅ Lọc theo TA criteria (MA, RSI, Price vs MA50)
- ✅ Kết hợp FA + TA
- ✅ Quét toàn bộ sàn HOSE/HNX

### API Endpoints:

#### 5.1. Lấy danh sách cổ phiếu
```bash
curl "http://localhost:8501/screener/list?exchange=HOSE"
```

#### 5.2. Sàng lọc với tiêu chí
```bash
curl -X POST "http://localhost:8501/screener/screen" \
  -H "Content-Type: application/json" \
  -d '{
    "min_roe": 15,
    "max_pe": 20,
    "min_price_vs_ma50": 0
  }'
```

#### 5.3. Kiểm tra 1 cổ phiếu
```bash
curl "http://localhost:8501/screener/FPT"
```

### Sử dụng trong Python:
```python
from stock_screener import run_screener

results = run_screener(
    exchanges=['HOSE'],
    min_roe=15,
    max_pe=20,
    min_price_vs_ma50=0,
    limit=20
)

print(f"Found {len(results)} stocks matching criteria")
```

---

## 6. 💎 PHÁT HIỆN BLUE-CHIP

### Module: `bluechip_detector.py`

### Chức năng:
Tự động phát hiện cổ phiếu blue-chip dựa trên:
- ✅ Market cap > 10,000 tỷ
- ✅ ROE > 12%
- ✅ P/E < 25 (nếu có)
- ✅ Average volume > 100,000
- ✅ Volatility < 40%
- ✅ VN30 member (bonus)

### API Endpoints:

#### 6.1. Quét blue-chip
```bash
curl "http://localhost:8501/bluechip/scan?limit=10"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_scanned": 10,
    "bluechips_found": 3,
    "bluechips": [
      {
        "symbol": "FPT",
        "score": 85,
        "market_cap": 15000,
        "roe": 21.61,
        "pe": 15.2,
        "avg_volume": 250000,
        "volatility": 28.5,
        "is_vn30": true
      }
    ]
  }
}
```

#### 6.2. Thêm vào watchlist
```bash
curl -X POST "http://localhost:8501/bluechip/add-to-watchlist"
```

#### 6.3. Báo cáo chi tiết
```bash
curl "http://localhost:8501/bluechip/report"
```

### Sử dụng trong Python:
```python
from bluechip_detector import BlueChipDetector

detector = BlueChipDetector()
bluechips = detector.scan_bluechips(limit=20)

for stock in bluechips:
    print(f"{stock['symbol']}: Score {stock['score']}")
```

---

## 7. 🔄 BACKTESTING

### Module: `backtesting_strategy.py`

### Chức năng:
- ✅ MA Crossover strategy (Golden/Death Cross)
- ✅ 3 years historical data
- ✅ Performance metrics (Win rate, Sharpe, Drawdown)
- ✅ Equity curve visualization

### API Endpoint:
```bash
curl "http://localhost:8501/backtest/TCB?initial_capital=100000000"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "symbol": "TCB",
    "strategy": "MA Crossover (20/50)",
    "period": "3 years",
    "initial_capital": 100000000,
    "results": {
      "Equity Final [VND]": 125000000,
      "Return [%]": 25.0,
      "Win Rate [%]": 58.5,
      "Max Drawdown [%]": -12.3,
      "Sharpe Ratio": 1.45,
      "Total Trades": 24
    }
  }
}
```

### Sử dụng trong Python:
```python
from backtesting_strategy import run_ma_crossover_backtest

results = run_ma_crossover_backtest('TCB', initial_capital=100_000_000)
print(f"Return: {results['Return [%]']}%")
```

---

## 8. 💼 PORTFOLIO MANAGEMENT

### Module: `portfolio_manager.py`

### Chức năng:
- ✅ Paper trading (mô phỏng giao dịch)
- ✅ Track positions & P&L
- ✅ Performance metrics
- ✅ Trade history
- ✅ Portfolio summary

### Sử dụng trong Python:
```python
from portfolio_manager import PortfolioManager

# Khởi tạo portfolio
portfolio = PortfolioManager(initial_capital=100_000_000)

# Mua cổ phiếu
portfolio.buy('FPT', quantity=1000, price=93_000)

# Bán cổ phiếu
portfolio.sell('FPT', quantity=500, price=95_000)

# Xem summary
summary = portfolio.get_summary()
print(f"Total P&L: {summary['total_pnl']:,} VND")

# Performance metrics
metrics = portfolio.calculate_performance_metrics()
print(f"Win Rate: {metrics['win_rate']}%")
```

### Database tables:
- `portfolio`: Current positions
- `transactions`: Trade history
- `settings`: User preferences

---

## 9. 📰 NEWS & SENTIMENT

### Module: `news_sentiment.py`

### Chức năng:
- ✅ Aggregate news từ nhiều nguồn
- ✅ Sentiment analysis (Vietnamese NLP)
- ✅ Market sentiment score
- ✅ Stock-specific news

### Sử dụng trong Python:
```python
from news_sentiment import NewsAnalyzer

analyzer = NewsAnalyzer()

# Lấy news cho 1 stock
news = analyzer.fetch_stock_news('FPT', limit=10)
for article in news:
    print(f"{article['title']}: {article['sentiment']}")

# Market sentiment
sentiment = analyzer.get_market_sentiment()
print(f"Market: {sentiment['overall']}")
```

### News sources:
- Cafef.vn
- VnExpress
- CafeF
- Vietstock

---

## 10. 🔔 NOTIFICATIONS

### Module: `notifications.py`

### Chức năng:
- ✅ Multi-channel (Telegram, Email, Discord)
- ✅ Price alerts
- ✅ Trade notifications
- ✅ Technical signals
- ✅ Portfolio summary

### Setup:
```bash
# 1. Copy config template
cp notification_config_example.json notification_config.json

# 2. Edit config
nano notification_config.json
```

**Config format:**
```json
{
  "telegram": {
    "enabled": true,
    "bot_token": "YOUR_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID"
  },
  "email": {
    "enabled": true,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your@email.com",
    "sender_password": "your_app_password",
    "recipient_email": "recipient@email.com"
  },
  "discord": {
    "enabled": true,
    "webhook_url": "YOUR_WEBHOOK_URL"
  }
}
```

### Sử dụng trong Python:
```python
from notifications import NotificationManager

notif = NotificationManager(config_file='notification_config.json')

# Price alert
notif.send_price_alert('FPT', current_price=95000, target_price=93000, condition='above')

# Trade notification
notif.send_trade_notification('FPT', action='BUY', quantity=1000, price=93000)

# Start background monitoring
notif.start_alert_monitoring(watchlist=['FPT', 'VCB', 'HPG'])
```

---

## 11. ✏️ DRAWING TOOLS

### Module: `drawing_tools.py`

### Chức năng:
- ✅ Horizontal lines
- ✅ Trend lines
- ✅ Fibonacci retracement
- ✅ Rectangle zones
- ✅ Text annotations
- ✅ Save/Load drawings

### Sử dụng trong Python:
```python
from drawing_tools import DrawingManager

manager = DrawingManager()

# Add horizontal line (support/resistance)
manager.add_horizontal_line(
    symbol='FPT',
    price=90000,
    label='Support Level',
    color='green'
)

# Add trend line
manager.add_trend_line(
    symbol='FPT',
    start_date='2024-01-01',
    start_price=85000,
    end_date='2024-10-21',
    end_price=95000,
    label='Uptrend'
)

# Save drawings
manager.save_drawings('FPT', 'fpt_drawings.json')

# Load drawings
manager.load_drawings('FPT', 'fpt_drawings.json')
```

---

## 12. 📊 DASHBOARD

### Có 2 loại Dashboard:

### A. Basic Dashboard (Port 8502)

**Module:** `dashboard.py`

**Chức năng:**
- ✅ Candlestick chart
- ✅ Volume chart
- ✅ Real-time metrics
- ✅ Data table with export

**Khởi chạy:**
```bash
python start_dashboard.py
# → http://localhost:8502
```

---

### B. Advanced Dashboard (Port 8503) **⭐ RECOMMENDED**

**Module:** `dashboard_advanced.py`

**Chức năng - 6 TABS:**

#### Tab 1: 📈 Technical Analysis
- Moving Averages (MA20, MA50, MA200)
- RSI, MACD, Bollinger Bands
- Multi-indicator charts
- Signal detection

#### Tab 2: 📊 Multi-Stock Comparison
- Compare up to 6 stocks
- Normalized performance chart
- Side-by-side metrics
- Performance summary

#### Tab 3: 🧮 FA/TA Integration
- Fundamental Analysis (P/E, ROE, NPM, D/E)
- Technical Signals
- Overall rating
- Combined assessment

#### Tab 4: ⭐ Watchlist
- Personal watchlist management
- Real-time price tracking
- Quick add/remove
- Persistent storage (SQLite)

#### Tab 5: 🔔 Price Alerts
- Set price alerts
- Above/Below conditions
- Multi-alert management
- Notification integration

#### Tab 6: 🎯 Stock Screener **🆕**
- Market scan (HOSE, HNX)
- Classification filters
- Real-time results
- Download CSV

**Khởi chạy:**
```bash
python start_dashboard_advanced.py
# → http://localhost:8503
```

### Dashboard Settings:
- **Exchange**: HOSE, HNX
- **Limit**: 5-50 stocks
- **Delay**: 6-10 giây (recommended: 8s)
- **Filters**: Growth score, Risk level, Rating

---

## 13. 🗄️ DATABASE

### Module: `database.py`

### SQLite Database: `vnstock.db`

### Tables (6):

1. **watchlist**: Danh sách theo dõi
   - symbol, name, added_date

2. **alerts**: Price alerts
   - symbol, condition, target_price, status

3. **chart_layouts**: Chart configurations
   - symbol, layout_data

4. **portfolio**: Current positions
   - symbol, quantity, avg_price, current_value

5. **transactions**: Trade history
   - symbol, action, quantity, price, timestamp

6. **settings**: User preferences
   - key, value

### Sử dụng trong Python:
```python
from database import DatabaseManager

db = DatabaseManager()

# Add to watchlist
db.add_to_watchlist('FPT', 'FPT Corporation')

# Get watchlist
watchlist = db.get_watchlist()

# Add alert
db.add_alert('FPT', 'above', 95000)

# Get active alerts
alerts = db.get_alerts(active_only=True)
```

---

## 🚀 KHỞI ĐỘNG HỆ THỐNG

### Cách 1: Management Script (Recommended)
```bash
./manage_system.sh

# Menu:
# 1. Start All Services
# 2. Stop All Services
# 3. Restart All Services
# 4. Check Status
# 5. View Logs
# 6. Exit
```

### Cách 2: Manual
```bash
# Terminal 1: API Server
python3 main.py

# Terminal 2: Advanced Dashboard
streamlit run dashboard_advanced.py --server.port 8503

# Terminal 3: Basic Dashboard (optional)
streamlit run dashboard.py --server.port 8502
```

### Cách 3: Background
```bash
# Start all services in background
python3 main.py > logs_api.txt 2>&1 &
streamlit run dashboard_advanced.py --server.port 8503 > logs_dashboard.txt 2>&1 &
```

---

## 🔗 TRUY CẬP HỆ THỐNG

| Service | URL | Port |
|---------|-----|------|
| **API Server** | http://localhost:8501 | 8501 |
| **API Docs** | http://localhost:8501/docs | 8501 |
| **Basic Dashboard** | http://localhost:8502 | 8502 |
| **Advanced Dashboard** | http://localhost:8503 | 8503 |

**Network Access:**
- Replace `localhost` with your machine's IP (e.g., `192.168.1.4`)
- Example: `http://192.168.1.4:8503`

---

## 📖 TÀI LIỆU CHI TIẾT

### Guides có sẵn:
1. `README.md` - Overview
2. `QUICK_START.md` - Quick start guide
3. `DASHBOARD_GUIDE.md` - Basic dashboard
4. `DASHBOARD_ADVANCED_GUIDE.md` - Advanced dashboard
5. `FA_ANALYSIS_GUIDE.md` - Fundamental analysis
6. `CLASSIFICATION_GUIDE.md` - Stock classification
7. `BLUECHIP_DETECTOR_GUIDE.md` - Blue-chip detection
8. `SCREENER_DASHBOARD_GUIDE.md` - Stock screener
9. `INSTALLATION_GUIDE.md` - Installation
10. `DOCKER_DEPLOYMENT.md` - Docker deployment
11. `BUGFIX_HISTORY.md` - Bug fix history
12. `SUCCESS_REPORT.md` - Success report
13. `TIMEOUT_FIX.md` - Timeout troubleshooting

---

## ⚠️ LƯU Ý QUAN TRỌNG

### 1. Rate Limits
- **VNStock API có rate limit nghiêm ngặt**
- **Recommended delay**: 6-8 giây giữa các requests
- **Large scans**: Dùng delay 8-10 giây

### 2. Timeout
- Dashboard tự động tính timeout dựa trên:
  - `timeout = stocks × (4 + delay) × 1.5`
- Ví dụ: 20 stocks, 8s delay → 360s timeout

### 3. Data Quality
- Một số stocks thiếu FA data → bình thường
- Check `data_quality` field trong response
- Rating "F" không phải lúc nào cũng là bug

### 4. Currency
- Tất cả giá cả theo VND (Đồng Việt Nam)
- Stock prices: Đã chuyển từ nghìn đồng sang VND đầy đủ (×1000)
- Financial data: Giữ nguyên đơn vị gốc

---

## 🎯 USE CASES

### 1. AI & Machine Learning
```python
# Lấy 15+ năm dữ liệu cho training
collector = VNStockDataCollector()
data = collector.get_full_stock_data('VIC')
# → 3940+ records cho ML models
```

### 2. Automated Trading
```python
# Daily stock scan → auto trading signals
classifier = StockClassifier()
df = classifier.scan_and_classify_market(exchanges=['HOSE'], limit=50)
top_stocks = df[df['overall_rating'].isin(['A+', 'A', 'B'])]
# → Buy signals
```

### 3. Portfolio Monitoring
```python
# Track portfolio performance
portfolio = PortfolioManager(initial_capital=100_000_000)
portfolio.buy('FPT', 1000, 93000)
summary = portfolio.get_summary()
# → Real-time P&L tracking
```

### 4. Research & Analysis
```bash
# Export data for research
curl "http://localhost:8501/stock/VIC/historical" > vic_data.json
# → Analysis in Excel, Python, R
```

---

## 📊 PERFORMANCE

| Operation | Time | Records |
|-----------|------|---------|
| Single stock data | 3-5s | 3940+ |
| FA calculation | 2-3s | 5 ratios |
| TA indicators | 2-3s | 15+ indicators |
| Classification | 4-5s | Full analysis |
| Market scan (10 stocks) | 60s | With 6s delay |
| Backtest (3 years) | 5-10s | Full strategy |

---

## 🆘 TROUBLESHOOTING

### Timeout errors
```bash
# Giảm số stocks hoặc tăng delay
curl "http://localhost:8501/classify/market?limit=5&delay=10.0"
```

### Rate limit (502/429)
```bash
# Tăng delay lên 10+ giây
# Hoặc chờ 1-2 phút rồi thử lại
```

### API không response
```bash
# Check health
curl http://localhost:8501/health

# Restart
./manage_system.sh → Option 3 (Restart)
```

### Dashboard không load
```bash
# Clear cache và restart
pkill -f streamlit
streamlit run dashboard_advanced.py --server.port 8503
```

---

## 📝 LOGS

### Log files:
- `logs_api.txt` - API server logs
- `logs_dashboard.txt` - Dashboard logs

### View logs:
```bash
# Real-time API logs
tail -f logs_api.txt

# Real-time Dashboard logs
tail -f logs_dashboard.txt

# Last 100 lines
tail -100 logs_api.txt
```

---

## 🎉 KẾT LUẬN

**VNStock 2.0** là hệ thống phân tích cổ phiếu **TOÀN DIỆN NHẤT** cho thị trường Việt Nam với:

✅ **25+ API Endpoints** - RESTful API hoàn chỉnh  
✅ **15+ Modules** - FA, TA, Classification, Portfolio, News...  
✅ **2 Dashboards** - Basic + Advanced với 6 tabs  
✅ **SQLite Database** - Persistent storage  
✅ **Multi-channel Notifications** - Telegram, Email, Discord  
✅ **Production Ready** - Tested, documented, deployed  

**Hệ thống sẵn sàng cho:**
- 🤖 AI & Machine Learning
- 📊 Automated Trading
- 💼 Portfolio Management
- 🔬 Research & Analytics
- 🔗 n8n Integration

---

**Happy Trading!** 🚀📈

_Cập nhật: 21/10/2025_  
_Version: 2.0_

