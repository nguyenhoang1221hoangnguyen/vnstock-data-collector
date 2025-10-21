# 🎯 Stock Screener Dashboard - Hướng dẫn sử dụng

## 📊 Tổng quan

**Stock Screener** là tab mới nhất trong **Advanced Dashboard**, cho phép bạn:
- 🔍 Quét toàn bộ thị trường chứng khoán VN
- 📊 Phân loại theo 5 tiêu chí
- 🎯 Lọc stocks theo nhiều điều kiện
- 📥 Download kết quả để phân tích

**Location:** Tab 6 trong Advanced Dashboard (Port 8503)

---

## 🚀 CÁCH KHỞI CHẠY

### **Bước 1: Start API Server**

```bash
cd "/Users/nguyenhoang/Desktop/2025/hoc-tap code/vscode/VNSTOCK 2"
source venv/bin/activate

# Terminal 1: Start API
python main.py
```

**API chạy tại:** http://localhost:8501

### **Bước 2: Start Dashboard**

```bash
# Terminal 2: Start Dashboard
python start_dashboard_advanced.py
```

**Dashboard chạy tại:** http://localhost:8503

### **Bước 3: Mở Dashboard**

```bash
# macOS
open http://localhost:8503

# Hoặc truy cập bằng browser
http://localhost:8503
```

### **Bước 4: Chọn Tab "Stock Screener"**

Click vào tab **"🎯 Stock Screener"** (tab cuối cùng)

---

## 💡 GIAO DIỆN

### **Layout:**

```
┌────────────────────────────────────────────────────────────┐
│  🎯 Stock Screener & Classification                        │
├──────────────────────┬─────────────────────────────────────┤
│ ⚙️ Settings (1/3)    │ 📊 Results (2/3)                    │
│                      │                                     │
│ 📍 Sàn giao dịch     │ [Empty state hoặc Results]          │
│ ☰ Số lượng mã quét  │                                     │
│                      │ • Summary metrics (4 cards)         │
│ 🔍 Bộ lọc            │ • Filtered table                    │
│ • Growth Potential   │ • Download CSV                      │
│ • Risk Level         │ • Distribution charts               │
│ • Overall Rating     │                                     │
│ • Min Score          │ ──── hoặc ────                      │
│                      │                                     │
│ 🚀 [Bắt đầu Scan]    │ • Single classify result            │
│                      │ • 3 metrics + details               │
│ 🔍 Classify 1 mã     │                                     │
│ [VD: FPT]            │ ──── hoặc ────                      │
│ [Classify]           │                                     │
│                      │ 📖 User Guide                       │
└──────────────────────┴─────────────────────────────────────┘
```

---

## 🎯 CÁCH SỬ DỤNG

### **OPTION 1: Scan thị trường**

#### **Bước 1: Chọn cài đặt**

**1.1 Chọn sàn:**
- HOSE (khuyến nghị)
- HNX
- HOSE+HNX (scan cả 2 sàn)

**1.2 Chọn số lượng:**
- 10-100 stocks
- Khuyến nghị: 20-50 để nhanh
- Slider để điều chỉnh

**1.3 Áp dụng bộ lọc (tùy chọn):**
- Growth: high_growth, growth, stable, value, neutral
- Risk: low_risk, medium_risk, high_risk
- Rating: A+, A, B, C, D, F
- Min Score: 0.0 - 10.0

#### **Bước 2: Click "Bắt đầu Scan"**

- Nút màu xanh (primary)
- Sẽ hiện progress indicator
- Thời gian tùy số lượng:
  - 10 stocks: ~1 phút
  - 20 stocks: ~2 phút
  - 50 stocks: ~5 phút
  - 100 stocks: ~10 phút

#### **Bước 3: Xem kết quả**

**Summary Metrics:**
```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Total Stocks │  Avg Score   │ Top Rating   │    Count     │
│     50       │     6.2      │      B       │      18      │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

**Results Table:**
- 8 cột: Symbol, Rating, Score, Growth, Risk, Market Cap, Momentum, Recommendation
- Auto-sort theo Score (cao → thấp)
- Scroll để xem tất cả

**Distribution Charts:**
- Chart 1: Rating distribution (bar chart)
- Chart 2: Growth category distribution

#### **Bước 4: Lọc kết quả (tùy chọn)**

Sau khi scan xong, bạn có thể:
1. Thay đổi bộ lọc bên trái
2. Kết quả tự động filter
3. Số lượng hiển thị: "Showing X / Y stocks"

#### **Bước 5: Download**

- Click "📥 Download CSV"
- File tự động tải với tên: `stock_screener_YYYYMMDD_HHMMSS.csv`
- Encoding: UTF-8-sig (mở được bằng Excel)

---

### **OPTION 2: Classify 1 mã cụ thể**

#### **Bước 1: Nhập mã**

- Text box: "Nhập mã cổ phiếu"
- VD: FPT, VCB, VNM
- Không phân biệt hoa/thường

#### **Bước 2: Click "Classify"**

- Thời gian: ~7 seconds
- Progress indicator

#### **Bước 3: Xem kết quả chi tiết**

**3 Key Metrics:**
```
┌──────────────┬──────────────┬──────────────┐
│Overall Rating│ Growth Score │  Risk Score  │
│   F (3.7)    │  4/10        │   8/10       │
└──────────────┴──────────────┴──────────────┘
```

**Recommendation:**
```
🚫 Avoid - Tránh
```

**4 Expandable Sections:**

1. **📈 Growth Details**
   - Category, Score, Description
   - ROE, P/E, NPM (nếu có)

2. **⚠️ Risk Details**
   - Category, Score, Description
   - Volatility, D/E Ratio

3. **💰 Market Cap Details**
   - Category, Description
   - Market cap (trillion VND)

4. **📊 Momentum Details**
   - Category, Score, Description
   - Bullish/Bearish signals

#### **Bước 4: Clear Result**

- Click "🗑️ Clear Result" để xóa
- Quay về empty state

---

## 📊 HIỂU KẾT QUẢ

### **1. Overall Rating**

| Rating | Score | Meaning | Action |
|--------|-------|---------|--------|
| A+ | 8.0-10.0 | 🌟 Strong Buy | Mua mạnh |
| A | 7.0-7.9 | ✅ Buy | Mua |
| B | 6.0-6.9 | 👀 Hold/Accumulate | Giữ/Tích lũy |
| C | 5.0-5.9 | ⏸️ Hold | Giữ |
| D | 4.0-4.9 | ⚠️ Watch | Theo dõi |
| F | < 4.0 | 🚫 Avoid | Tránh |

**Công thức:**
```
Score = (Growth × 0.4) + (Risk Adjusted × 0.3) + (Momentum × 0.3)
```

---

### **2. Growth Categories**

- **high_growth** (9): ROE > 20%, P/E < 25
- **growth** (7): ROE > 15%, P/E < 20
- **stable** (6): ROE > 10%, P/E < 15
- **value** (5): P/E < 10 (undervalued)
- **neutral** (4): Không rõ ràng
- **distressed** (1): ROE < 0

---

### **3. Risk Levels**

- **low_risk** (2): Volatility < 20%, D/E < 1
- **medium_risk** (5): Volatility < 40%, D/E < 2
- **high_risk** (8): Volatility < 60%, D/E < 3
- **very_high_risk** (10): Rất biến động

---

### **4. Market Cap**

- **mega_cap**: > 100,000 tỷ VND
- **large_cap**: 10,000-100,000 tỷ
- **mid_cap**: 1,000-10,000 tỷ
- **small_cap**: < 1,000 tỷ

---

### **5. Momentum**

- **strong_uptrend** (9): 3+ bullish signals
- **uptrend** (7): 2 bullish signals
- **sideways** (5): Mixed signals
- **downtrend** (3): 2 bearish signals
- **strong_downtrend** (1): 3+ bearish signals

---

## 🎯 USE CASES

### **Case 1: Tìm cổ phiếu tăng trưởng cao, rủi ro thấp**

**Settings:**
- Exchange: HOSE
- Limit: 50
- Growth: high_growth
- Risk: low_risk
- Min Score: 7.0

**Kết quả:** Danh sách cổ phiếu tăng trưởng mạnh, an toàn

---

### **Case 2: Tìm value stocks (giá rẻ)**

**Settings:**
- Exchange: HOSE
- Limit: 50
- Growth: value
- Rating: B
- Min Score: 5.0

**Kết quả:** Cổ phiếu có thể bị đánh giá dưới giá trị

---

### **Case 3: Kiểm tra danh mục hiện tại**

**Cách 1:** Scan market → tìm mã của bạn trong table

**Cách 2:** Classify từng mã một:
- VCB → Classify
- TCB → Classify  
- FPT → Classify

---

### **Case 4: Top picks hàng tuần**

**Settings:**
- Exchange: HOSE+HNX
- Limit: 100
- Min Score: 7.0

**Action:**
1. Scan
2. Sort theo Score
3. Download top 10
4. Phân tích thủ công

---

## 💡 TIPS & TRICKS

### **1. Tăng tốc độ scan:**

- Scan 20-30 stocks thay vì 100
- Chỉ chọn 1 sàn (HOSE hoặc HNX)
- Scan trong giờ không cao điểm

### **2. Kết hợp bộ lọc:**

```
✅ GOOD: growth=high_growth + risk=low_risk
✅ GOOD: rating=A + risk=medium_risk
❌ TOO STRICT: growth=high_growth + risk=low_risk + rating=A+ + min_score=9
```

### **3. Sử dụng CSV:**

```bash
# Download CSV
# Mở bằng Excel/Google Sheets
# Sắp xếp, lọc, phân tích thêm
# Tạo charts riêng
```

### **4. Scheduled scanning:**

- Scan mỗi tuần 1 lần
- Track thay đổi rating
- Build watchlist

### **5. Kết hợp với tabs khác:**

1. Screener → Tìm top stocks
2. Technical Chart → Xem chart
3. FA/TA Analysis → Phân tích chi tiết
4. Watchlist → Add vào theo dõi
5. Price Alerts → Set alerts

---

## ⚠️ LƯU Ý

### **1. API Server phải chạy:**

```bash
# Check API
curl http://localhost:8501/health

# Nếu lỗi, start lại
python main.py
```

### **2. Timeout:**

- Scan 100 stocks có thể mất ~10 phút
- Nếu timeout, giảm limit xuống

### **3. Rate Limit:**

- VCI API có giới hạn requests
- Delay mặc định: 3 seconds
- Nếu bị block, chờ vài phút

### **4. Data Quality:**

- Một số mã có thể thiếu data
- P/E calculation có thể N/A
- Market cap là ước tính

---

## 🐛 TROUBLESHOOTING

### **Problem: "API Error: 500"**

**Solution:**
```bash
# Restart API server
pkill -f "python main.py"
python main.py
```

---

### **Problem: "No stocks classified successfully"**

**Causes:**
- API server chưa chạy
- Rate limit exceeded
- Network issues

**Solution:**
1. Check API: `curl http://localhost:8501/health`
2. Giảm limit xuống 10-20
3. Đợi 1-2 phút rồi thử lại

---

### **Problem: Scan quá lâu**

**Solution:**
- Giảm limit xuống 20-30
- Check network connection
- Close other applications

---

### **Problem: Filter không có kết quả**

**Solution:**
- Nới lỏng tiêu chí
- Bỏ bớt filters
- Giảm min_score

---

## 📚 ADDITIONAL RESOURCES

**Documentation:**
- [CLASSIFICATION_GUIDE.md](CLASSIFICATION_GUIDE.md) - Chi tiết 5 nhóm phân loại
- [QUICK_START_CLASSIFIER.md](QUICK_START_CLASSIFIER.md) - Quick start guide
- [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) - Cài đặt hệ thống

**API Docs:**
```
http://localhost:8501/docs
```

**Dashboard Guide:**
- [DASHBOARD_ADVANCED_GUIDE.md](DASHBOARD_ADVANCED_GUIDE.md) - Full advanced dashboard guide

---

## 🎓 VIDEO TUTORIAL (Coming Soon)

- [ ] Cách sử dụng Stock Screener
- [ ] Tips & tricks
- [ ] Use cases thực tế

---

## 📞 SUPPORT

**Issues:** Report bugs tại GitHub

**Email:** nguyenhoang1221hoangnguyen@gmail.com

---

## ✅ CHECKLIST SỬ DỤNG

Trước khi scan, check:

- [ ] API server đang chạy (port 8501)
- [ ] Dashboard đang chạy (port 8503)
- [ ] Browser mở tab Stock Screener
- [ ] Đã chọn settings phù hợp
- [ ] Network connection ổn định

---

**🎉 Chúc bạn tìm được những cổ phiếu tốt nhất! 📊**

*Version: 1.0*  
*Last Updated: 2025-10-21*  
*Dashboard: Advanced Dashboard v2.0*

