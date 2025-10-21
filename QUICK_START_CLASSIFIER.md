# 🚀 QUICK START - Stock Classification System

## 📋 Cách sử dụng hệ thống phân loại cổ phiếu

Có **4 cách** để sử dụng Stock Classification System:

---

## 1️⃣ CÁCH 1: Script tự động (Dễ nhất) ⭐

### **Khởi chạy menu:**

```bash
./start_classifier.sh
```

**Menu sẽ hiện:**
```
🎯 STOCK CLASSIFICATION SYSTEM
==============================

Chọn chức năng:
1. Scan 20 stocks (nhanh - 2 phút)
2. Scan 50 stocks (vừa - 5 phút)
3. Scan 100 stocks (đầy đủ - 10 phút)
4. Quick test (5 stocks)
5. Classify 1 mã cụ thể

Nhập lựa chọn (1-5):
```

**Nhập số để chọn!**

---

## 2️⃣ CÁCH 2: Classify 1 mã cụ thể (Nhanh)

### **Command:**

```bash
# Activate venv
cd "/Users/nguyenhoang/Desktop/2025/hoc-tap code/vscode/VNSTOCK 2"
source venv/bin/activate

# Classify 1 stock
python classify_stock.py VNM
python classify_stock.py FPT
python classify_stock.py VCB
```

### **Output mẫu:**

```
======================================================================
📊 CLASSIFICATION RESULT: VNM
======================================================================

⭐ OVERALL RATING: F (3.7/10)
   🚫 Avoid - Tránh

📈 GROWTH POTENTIAL: neutral (Score: 4/10)
   ➖ Trung lập
   ROE: 24.01%
   P/E: 0.14
   NPM: 14.80%

⚠️  RISK LEVEL: high_risk (Score: 8/10)
   🟠 Rủi ro cao
   Volatility: 23.45%
   D/E Ratio: 0.55

💰 MARKET CAP: small_cap
   🏘️ Small Cap - Tiềm năng cao
   0.0 trillion VND

📊 MOMENTUM: sideways (Score: 5/10)
   ➡️ Đi ngang

🔢 COMPONENT SCORES:
   Growth:        4/10
   Risk Adjusted: 2/10
   Momentum:      5/10

📐 CALCULATION:
   Overall = (Growth × 0.4) + (Risk Adj × 0.3) + (Momentum × 0.3)
   3.7 = (4 × 0.4) + (2 × 0.3) + (5 × 0.3)

======================================================================
✅ Classification completed for VNM
======================================================================
```

**Thời gian:** ~7 seconds

---

## 3️⃣ CÁCH 3: Scan thị trường (Batch)

### **Command:**

```bash
# Activate venv
source venv/bin/activate

# Scan 20 stocks (mặc định)
python stock_classifier.py

# Scan 50 stocks
python stock_classifier.py 50

# Scan 100 stocks
python stock_classifier.py 100
```

### **Output mẫu:**

```
🔍 Scanning 20 stocks from ['HOSE']...

======================================================================
[1/20] VCB... ✅ F
[2/20] TCB... ✅ F
[3/20] FPT... ✅ F
[4/20] VNM... ✅ F
[5/20] HPG... ✅ B
...

======================================================================
✅ Completed: 20 stocks classified
❌ Errors: 0 stocks

======================================================================
📊 MARKET CLASSIFICATION SUMMARY
======================================================================

🚀 By Growth Potential:
growth          10
neutral         6
high_growth     3
stable          1

⚠️ By Risk Level:
medium_risk     12
high_risk       5
low_risk        3

💰 By Market Cap:
mid_cap         10
small_cap       8
large_cap       2

⭐ By Rating:
C     8
F     6
B     4
A     2

📈 Top 10 Recommendations:
symbol overall_rating  overall_score growth_category risk_category
FPT    A               7.5          high_growth      low_risk
VNM    A               7.2          growth           low_risk
VCB    B               6.8          growth           medium_risk
...

✅ Saved to stock_classification_20251021_143000.csv
```

**Output files:**
- CSV file: `stock_classification_YYYYMMDD_HHMMSS.csv`
- Console summary

**Thời gian:**
- 20 stocks: ~2 phút
- 50 stocks: ~5 phút
- 100 stocks: ~10 phút

---

## 4️⃣ CÁCH 4: API REST (Tích hợp hệ thống)

### **Khởi chạy API server:**

```bash
# Terminal 1: Start API
python main.py

# API chạy tại: http://localhost:8501
```

### **Sử dụng API:**

#### **A. Classify 1 stock:**

```bash
curl "http://localhost:8501/classify/stock/VNM"
```

#### **B. Scan market:**

```bash
# Scan 50 stocks
curl "http://localhost:8501/classify/market?limit=50"

# Scan nhiều sàn
curl "http://localhost:8501/classify/market?exchanges=HOSE,HNX&limit=100"
```

#### **C. Filter stocks:**

```bash
# High growth + Low risk
curl "http://localhost:8501/classify/filter?growth=high_growth&risk=low_risk"

# Rating A+
curl "http://localhost:8501/classify/filter?rating=A%2B"

# Min score 7.0
curl "http://localhost:8501/classify/filter?min_score=7.0"
```

#### **D. Top picks:**

```bash
# Top 10 cổ phiếu tốt nhất
curl "http://localhost:8501/classify/top-picks?count=10&min_rating=B"
```

### **API Documentation:**

```bash
# Mở browser
open http://localhost:8501/docs
```

---

## 5️⃣ CÁCH 5: Python Code (Advanced)

### **Code mẫu:**

```python
from stock_classifier import StockClassifier, scan_market

# ========== Option 1: Classify 1 stock ==========
classifier = StockClassifier()
result = classifier.classify_stock('VNM')

print(f"Rating: {result['overall_rating']['rating']}")
print(f"Score: {result['overall_rating']['score']}")
print(f"Recommendation: {result['overall_rating']['recommendation']}")

# ========== Option 2: Scan market ==========
df = scan_market(exchanges=['HOSE'], limit=50)

# Filter results
high_growth = df[df['growth_category'] == 'high_growth']
print(f"High growth stocks: {len(high_growth)}")

# ========== Option 3: Custom filter ==========
filtered = classifier.get_stocks_by_filter(
    df,
    growth='high_growth',
    risk='low_risk',
    min_score=7.0
)

print(f"Found {len(filtered)} stocks matching criteria")
```

---

## 📊 OUTPUT GIẢI THÍCH

### **Các nhóm phân loại:**

#### **1. Growth Potential (Tiềm năng tăng trưởng):**
- `high_growth` - Tăng trưởng mạnh (Score: 9)
- `growth` - Tăng trưởng ổn định (Score: 7)
- `stable` - Ổn định (Score: 6)
- `value` - Giá rẻ (Score: 5)
- `neutral` - Trung lập (Score: 4)
- `distressed` - Khó khăn (Score: 1)

#### **2. Risk Level (Rủi ro):**
- `low_risk` - Rủi ro thấp (Score: 2)
- `medium_risk` - Rủi ro TB (Score: 5)
- `high_risk` - Rủi ro cao (Score: 8)
- `very_high_risk` - Rủi ro rất cao (Score: 10)

#### **3. Market Cap (Vốn hóa):**
- `mega_cap` - Siêu lớn (>100,000 tỷ)
- `large_cap` - Blue-chip (10,000-100,000 tỷ)
- `mid_cap` - Vừa (1,000-10,000 tỷ)
- `small_cap` - Nhỏ (<1,000 tỷ)

#### **4. Momentum (Xu hướng):**
- `strong_uptrend` - Tăng mạnh (Score: 9)
- `uptrend` - Tăng (Score: 7)
- `sideways` - Ngang (Score: 5)
- `downtrend` - Giảm (Score: 3)
- `strong_downtrend` - Giảm mạnh (Score: 1)

#### **5. Overall Rating (Tổng hợp):**
- `A+` (8.0-10.0) - 🌟 Strong Buy
- `A` (7.0-7.9) - ✅ Buy
- `B` (6.0-6.9) - 👀 Hold/Accumulate
- `C` (5.0-5.9) - ⏸️ Hold
- `D` (4.0-4.9) - ⚠️ Watch
- `F` (<4.0) - 🚫 Avoid

---

## 🎯 USE CASES

### **1. Tìm cổ phiếu tăng trưởng cao:**

```bash
# Command line
python stock_classifier.py 100 > results.txt
grep "high_growth" results.txt

# API
curl "http://localhost:8501/classify/filter?growth=high_growth&min_score=7"
```

### **2. Tìm cổ phiếu an toàn (low risk):**

```bash
# API
curl "http://localhost:8501/classify/filter?risk=low_risk&rating=A"
```

### **3. So sánh nhiều mã:**

```bash
# Classify từng mã
python classify_stock.py VCB
python classify_stock.py TCB
python classify_stock.py FPT
```

### **4. Portfolio analysis:**

```python
# Python
my_portfolio = ['VCB', 'TCB', 'FPT', 'VNM', 'HPG']

for symbol in my_portfolio:
    result = classifier.classify_stock(symbol)
    print(f"{symbol}: {result['overall_rating']['rating']}")
```

---

## ⚡ TIPS & TRICKS

### **1. Tăng tốc độ:**

```bash
# Giảm delay (có thể bị rate limit)
# Edit stock_classifier.py line 493:
delay=1.0  # thay vì 3.0
```

### **2. Lưu kết quả:**

```bash
# Redirect output
python stock_classifier.py 50 > results.txt

# CSV tự động lưu
# File: stock_classification_YYYYMMDD_HHMMSS.csv
```

### **3. Filter CSV:**

```python
import pandas as pd

# Load CSV
df = pd.read_csv('stock_classification_20251021_143000.csv')

# Filter A+ stocks
a_plus = df[df['overall_rating'] == 'A+']
print(a_plus[['symbol', 'overall_score', 'recommendation']])
```

### **4. Scheduled scanning (Cron):**

```bash
# Edit crontab
crontab -e

# Add job (chạy mỗi thứ 2 lúc 8h sáng)
0 8 * * 1 cd /path/to/vnstock && source venv/bin/activate && python stock_classifier.py 100
```

---

## ❓ FAQ

**Q: Mất bao lâu để scan?**  
A: ~7 seconds/stock. 50 stocks = ~5 phút.

**Q: Có giới hạn số lượng không?**  
A: Không, nhưng khuyến nghị ≤ 100 mã/lần để tránh rate limit.

**Q: CSV lưu ở đâu?**  
A: Cùng thư mục, tên: `stock_classification_YYYYMMDD_HHMMSS.csv`

**Q: Làm sao xem full documentation?**  
A: Đọc `CLASSIFICATION_GUIDE.md`

**Q: API chạy ở port nào?**  
A: Port 8501 (có thể thay đổi trong `main.py`)

---

## 🆘 TROUBLESHOOTING

**Problem: "ModuleNotFoundError"**  
**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Problem: "Rate limit exceeded"**  
**Solution:**
```bash
# Tăng delay lên 5s (edit stock_classifier.py)
# Hoặc scan ít mã hơn
python stock_classifier.py 20
```

**Problem: "Permission denied: start_classifier.sh"**  
**Solution:**
```bash
chmod +x start_classifier.sh
```

---

## 📚 NEXT STEPS

1. ✅ Đọc kết quả classification
2. ✅ Filter theo tiêu chí của bạn
3. ✅ Kết hợp với phân tích thủ công
4. ✅ Track stocks theo thời gian
5. ✅ Integrate với n8n workflow

---

## 📞 SUPPORT

**Documentation:**
- [CLASSIFICATION_GUIDE.md](CLASSIFICATION_GUIDE.md) - Hướng dẫn chi tiết
- [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) - Cài đặt
- [TEST_RESULTS.md](TEST_RESULTS.md) - Kết quả test

**API Docs:**
```bash
# Start API server
python main.py

# Open browser
open http://localhost:8501/docs
```

---

**🎉 Happy Stock Screening! 📊**

*Version: 2.0 | Updated: 2025-10-21*

