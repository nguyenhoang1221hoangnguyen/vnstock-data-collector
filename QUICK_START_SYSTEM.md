# 🚀 VNStock - Hướng Dẫn Khởi Động Nhanh

## ✅ HỆ THỐNG ĐÃ KHỞI ĐỘNG THÀNH CÔNG!

### 📡 **Truy cập hệ thống:**

| Service | URL | Mô tả |
|---------|-----|-------|
| **FastAPI Server** | http://localhost:8501 | Backend API |
| **API Documentation** | http://localhost:8501/docs | Swagger UI - Test API |
| **Advanced Dashboard** | http://localhost:8503 | Web Dashboard chính |

---

## 🎯 CHỨC NĂNG CHÍNH

### 1️⃣ **Web Dashboard** (Khuyến nghị)
**URL:** http://localhost:8503

**6 TAB CHỨC NĂNG:**

#### 📊 **Tab 1: Technical Analysis**
- Nhập mã cổ phiếu (VD: VCB, FPT, VNM)
- Chọn khoảng thời gian (7 ngày - 5 năm)
- Xem biểu đồ nến với các chỉ báo:
  - MA (50, 200)
  - RSI (14)
  - MACD
  - Bollinger Bands
  - Volume

#### 📈 **Tab 2: Multi-Stock Comparison**
- So sánh tối đa 5 mã cổ phiếu
- Xem xu hướng giá tương đối
- So sánh hiệu suất

#### 💰 **Tab 3: Fundamental Analysis**
- Phân tích cơ bản chi tiết
- Các chỉ số: P/E, ROE, NPM, D/E, EPS
- Đánh giá chất lượng dữ liệu
- Khuyến nghị đầu tư

#### 🔍 **Tab 4: Technical + Fundamental**
- Kết hợp phân tích kỹ thuật và cơ bản
- Tín hiệu mua/bán
- Khuyến nghị tổng hợp

#### ⭐ **Tab 5: Watchlist & Alerts**
- Tạo danh sách theo dõi
- Thiết lập cảnh báo giá
- Quản lý cổ phiếu yêu thích

#### 🎯 **Tab 6: Stock Screener** (MỚI!)
- Quét thị trường tự động
- Phân loại cổ phiếu:
  - **Growth**: Tiềm năng tăng trưởng
  - **Risk**: Mức độ rủi ro
  - **Market Cap**: Vốn hóa
  - **Momentum**: Xu hướng
  - **Rating**: Xếp hạng tổng thể (A+ → F)
- Lọc theo tiêu chí
- Xuất CSV
- Top picks

---

### 2️⃣ **API Endpoints** (Cho lập trình viên)

**Base URL:** http://localhost:8501

#### 📦 **Data Collection**
```bash
# Lấy tất cả dữ liệu 1 mã
curl -X POST "http://localhost:8501/stock/batch" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "VCB"}'
```

#### 💹 **Fundamental Analysis**
```bash
# Tính toán FA ratios
curl "http://localhost:8501/stock/VCB/fa"
```

#### 📊 **Technical Analysis**
```bash
# Tính toán TA indicators
curl "http://localhost:8501/stock/VCB/ta?period_days=365"

# Phân tích tín hiệu
curl "http://localhost:8501/stock/VCB/ta/analyze?period_days=365"
```

#### 🔍 **Stock Screener**
```bash
# Danh sách cổ phiếu HOSE
curl "http://localhost:8501/screener/list?exchange=HOSE"

# Screen 1 mã cụ thể
curl "http://localhost:8501/screener/VCB?pe_max=15&roe_min=18"
```

#### 🧪 **Backtesting**
```bash
# Backtest chiến lược MA crossover
curl "http://localhost:8501/backtest/TCB?initial_cash=100000000&ma_fast=20&ma_slow=50&period_days=1095"
```

#### 💎 **Blue-chip Detector**
```bash
# Quét blue-chip stocks
curl "http://localhost:8501/bluechip/scan?min_score=4"

# Báo cáo chi tiết
curl "http://localhost:8501/bluechip/report?min_score=4"
```

#### 🎯 **Stock Classification** (MỚI!)
```bash
# Phân loại 1 mã
curl "http://localhost:8501/classify/stock/VCB"

# Quét thị trường (3 mã test)
curl "http://localhost:8501/classify/market?limit=3&exchanges=HOSE&delay=3.0"

# Quét thị trường (50 mã)
curl "http://localhost:8501/classify/market?limit=50&exchanges=HOSE&delay=3.0"

# Lọc theo tiêu chí
curl "http://localhost:8501/classify/filter?growth=high_growth&risk=low_risk&min_score=7.0&limit=20"

# Top picks
curl "http://localhost:8501/classify/top-picks?limit=10"
```

---

## 🛠️ QUẢN LÝ HỆ THỐNG

### **Cách 1: Dùng Script Quản Lý (Khuyến nghị)**

```bash
cd "/Users/nguyenhoang/Desktop/2025/hoc-tap code/vscode/VNSTOCK 2"
./manage_system.sh
```

**Menu:**
- `1` - Start tất cả services
- `2` - Stop tất cả services
- `3` - Restart tất cả services
- `4` - Kiểm tra trạng thái
- `5` - Xem logs
- `6` - Test API
- `7` - Thoát

### **Cách 2: Thủ công**

#### Start hệ thống:
```bash
cd "/Users/nguyenhoang/Desktop/2025/hoc-tap code/vscode/VNSTOCK 2"
source venv/bin/activate

# Start API
nohup python main.py > logs_api.txt 2>&1 &

# Start Dashboard
nohup streamlit run dashboard_advanced.py --server.port 8503 > logs_dashboard.txt 2>&1 &
```

#### Stop hệ thống:
```bash
pkill -f "python main.py"
pkill -f "streamlit run dashboard_advanced.py"
```

#### Xem logs:
```bash
# API logs
tail -f logs_api.txt

# Dashboard logs
tail -f logs_dashboard.txt
```

---

## 📊 USE CASES

### 1. **Phân tích 1 mã cổ phiếu cụ thể**
1. Mở Dashboard: http://localhost:8503
2. Tab "Technical + Fundamental"
3. Nhập mã (VD: VCB)
4. Xem phân tích tổng hợp

### 2. **Tìm cổ phiếu tiềm năng**
1. Tab "Stock Screener"
2. Chọn sàn HOSE, Limit 50
3. Click "Bắt đầu Scan"
4. Lọc theo:
   - Growth: High Growth
   - Risk: Low/Medium Risk
   - Rating: A+, A, B
   - Score: ≥ 7.0
5. Xem Top Picks

### 3. **Theo dõi danh mục**
1. Tab "Watchlist & Alerts"
2. Thêm các mã vào watchlist
3. Thiết lập cảnh báo giá
4. Nhận thông báo khi đạt ngưỡng

### 4. **Backtest chiến lược**
API:
```bash
curl "http://localhost:8501/backtest/VCB?initial_cash=100000000&ma_fast=20&ma_slow=50&period_days=1095"
```

### 5. **Tích hợp với n8n**
- Import workflow từ `n8n_workflow_example.json`
- Cấu hình HTTP Request node với URL: http://localhost:8501
- Tự động hóa phân tích định kỳ

---

## 🎓 TIPS & TRICKS

### **Stock Screener**
- **Limit=5**: Test nhanh (20 giây)
- **Limit=20**: Phân tích vừa (80 giây)
- **Limit=50**: Quét đầy đủ (3-4 phút)
- Delay=3.0: Tránh rate limit API

### **Đọc Rating**
- **A+, A**: Rất tốt - Mua
- **B**: Tốt - Xem xét
- **C**: Trung bình - Thận trọng
- **D, F**: Kém - Tránh

### **Lọc hiệu quả**
Kết hợp tiêu chí:
```
Growth: high_growth hoặc growth
Risk: low_risk hoặc medium_risk
Min Score: ≥ 7.0
```

### **Xuất dữ liệu**
- Click "📥 Download CSV" trong Stock Screener
- Phân tích thêm bằng Excel/Google Sheets

---

## 🐛 TROUBLESHOOTING

### **Dashboard không load**
```bash
# Restart dashboard
pkill -f "streamlit"
cd "/Users/nguyenhoang/Desktop/2025/hoc-tap code/vscode/VNSTOCK 2"
source venv/bin/activate
streamlit run dashboard_advanced.py --server.port 8503
```

### **API không phản hồi**
```bash
# Check API status
curl http://localhost:8501/health

# Restart API
pkill -f "python main.py"
cd "/Users/nguyenhoang/Desktop/2025/hoc-tap code/vscode/VNSTOCK 2"
source venv/bin/activate
python main.py
```

### **Stock Screener lỗi "No stocks classified"**
- Đã được fix! Restart hệ thống.
- Nếu vẫn lỗi, giảm limit xuống 5 để test.

### **Lỗi rate limit**
```
Rate limit exceeded. Vui lòng thử lại sau X giây.
```
- Tăng delay: `delay=5.0` hoặc `delay=10.0`
- Giảm số lượng mã quét

---

## 📚 TÀI LIỆU KHÁC

- **README.md**: Tổng quan dự án
- **CLASSIFICATION_GUIDE.md**: Hướng dẫn phân loại chi tiết
- **INSTALLATION_GUIDE.md**: Hướng dẫn cài đặt
- **PROJECT_SUMMARY.md**: Tổng kết dự án
- **API Docs**: http://localhost:8501/docs

---

## ⚡ QUICK COMMANDS

```bash
# Quản lý hệ thống
./manage_system.sh

# Test API nhanh
curl http://localhost:8501/health
curl "http://localhost:8501/classify/stock/VCB"

# Quét 5 mã test
curl "http://localhost:8501/classify/market?limit=5&exchanges=HOSE&delay=3.0"

# Xem logs
tail -f logs_api.txt
tail -f logs_dashboard.txt
```

---

## 🎯 ROADMAP ĐÃ HOÀN THÀNH

✅ Data Collection (OHLCV, FA, TA, News)
✅ Fundamental Analysis (P/E, ROE, NPM, D/E, EPS)
✅ Technical Analysis (15+ indicators)
✅ Stock Screener (FA + TA filters)
✅ Backtesting (MA crossover strategy)
✅ Dashboard (6 tabs, full features)
✅ Blue-chip Detector
✅ **Stock Classification System** (Growth, Risk, Market Cap, Momentum, Rating)
✅ Database (SQLite - Watchlist, Alerts, Portfolio)
✅ Notifications (Telegram, Email, Discord)
✅ Drawing Tools (Lines, Fibonacci, Rectangles)
✅ Portfolio Manager (Paper trading, P&L tracking)
✅ News & Sentiment Analysis
✅ n8n Integration

---

## 💡 HỖ TRỢ

Nếu gặp vấn đề:
1. Kiểm tra logs: `logs_api.txt` và `logs_dashboard.txt`
2. Restart hệ thống: `./manage_system.sh` → Option 3
3. Check GitHub Issues: https://github.com/nguyenhoang1221hoangnguyen/vnstock-data-collector

---

**🎉 Chúc bạn đầu tư thành công với VNStock!**

_Cập nhật lần cuối: 21/10/2025_

