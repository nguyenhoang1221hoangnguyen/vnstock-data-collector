# 🎯 STOCK CLASSIFICATION SYSTEM - Complete Guide

## 📊 Tổng quan

**Stock Classification System** là hệ thống phân loại cổ phiếu toàn diện, tự động quét và đánh giá toàn bộ thị trường chứng khoán Việt Nam theo **5 nhóm tiêu chí** khác nhau.

---

## 🏗️ Kiến trúc hệ thống

```
THỊ TRƯỜNG (HOSE + HNX + UPCOM)
    ↓
QUÉT & THU THẬP DỮ LIỆU
    ├── Fundamental Analysis (FA)
    ├── Technical Analysis (TA)
    └── Market Metrics
    ↓
PHÂN LOẠI 5 NHÓM
    ├── 1. Growth Potential
    ├── 2. Risk Level
    ├── 3. Market Cap
    ├── 4. Momentum
    └── 5. Overall Rating
    ↓
OUTPUT
    ├── JSON (API)
    ├── CSV (File)
    └── Console Report
```

---

## 📋 CÁC NHÓM PHÂN LOẠI

### **1. 🚀 Growth Potential (Tiềm năng tăng trưởng)**

Đánh giá khả năng tăng trưởng của công ty dựa trên các chỉ số tài chính.

| Nhóm | Điều kiện | Score | Mô tả |
|------|-----------|-------|-------|
| **High Growth** | ROE > 20%, P/E < 25, NPM > 15% | 9 | 🚀 Tăng trưởng mạnh, triển vọng tốt |
| **Growth** | ROE > 15%, P/E < 20 | 7 | 📈 Tăng trưởng ổn định |
| **Stable** | ROE > 10%, P/E < 15 | 6 | ➡️ Ổn định, cổ tức tốt |
| **Value** | P/E < 10 | 5 | 📊 Giá rẻ, tiềm năng đảo chiều |
| **Distressed** | ROE < 0 | 1 | ⚠️ Khó khăn, rủi ro cao |
| **Neutral** | Không thuộc nhóm trên | 4 | ➖ Trung lập |

**Ý nghĩa:**
- **High Growth:** Công ty có tốc độ tăng trưởng nhanh, ROE cao, lợi nhuận tốt → Phù hợp đầu tư tăng trưởng
- **Growth:** Tăng trưởng ổn định, chỉ số tốt → An toàn cho đầu tư dài hạn
- **Stable:** Công ty trưởng thành, cổ tức ổn định → Phù hợp nhà đầu tư bảo thủ
- **Value:** Định giá thấp, có thể bị đánh giá dưới giá trị → Cơ hội cho value investing
- **Distressed:** Đang gặp khó khăn → Tránh xa hoặc chờ tín hiệu phục hồi

---

### **2. ⚠️ Risk Level (Mức độ rủi ro)**

Đánh giá rủi ro dựa trên volatility, debt, và ROE.

| Nhóm | Điều kiện | Risk Score | Mô tả |
|------|-----------|------------|-------|
| **Low Risk** | Volatility < 20%, D/E < 1, ROE > 15% | 2 | 🟢 Rủi ro thấp, an toàn |
| **Medium Risk** | Volatility < 40%, D/E < 2, ROE > 5% | 5 | 🟡 Rủi ro trung bình |
| **High Risk** | Volatility < 60%, D/E < 3 | 8 | 🟠 Rủi ro cao |
| **Very High Risk** | Volatility > 60% hoặc D/E > 3 | 10 | 🔴 Rủi ro rất cao |

**Công thức Volatility:**
```
Volatility = StdDev(Daily Returns) × √252 × 100
```

**Ý nghĩa:**
- **Low Risk:** Giá ổn định, nợ thấp, sinh lời tốt → An toàn cho nhà đầu tư mới
- **Medium Risk:** Cân bằng risk/reward → Phù hợp đa số nhà đầu tư
- **High Risk:** Biến động lớn hoặc nợ cao → Cần kinh nghiệm
- **Very High Risk:** Rất biến động → Chỉ dành cho trader chuyên nghiệp

---

### **3. 💰 Market Cap (Vốn hóa thị trường)**

Phân loại theo quy mô công ty.

| Nhóm | Vốn hóa | Tier | Mô tả |
|------|---------|------|-------|
| **Mega Cap** | > 100,000 tỷ VND | 1 | 🏢 Siêu lớn (VCB, VIC, VHM) |
| **Large Cap** | 10,000 - 100,000 tỷ | 2 | 🏪 Blue-chip, ổn định |
| **Mid Cap** | 1,000 - 10,000 tỷ | 3 | 🏠 Tăng trưởng ổn định |
| **Small Cap** | < 1,000 tỷ | 4 | 🏘️ Tiềm năng cao, rủi ro cao |

**Ý nghĩa:**
- **Mega Cap:** Công ty top đầu, thanh khoản cao, rủi ro thấp
- **Large Cap:** Đa số là blue-chips, phù hợp đầu tư dài hạn
- **Mid Cap:** Cân bằng tăng trưởng & rủi ro
- **Small Cap:** Tiềm năng gấp bội nhưng rủi ro cao

---

### **4. 📊 Momentum (Xu hướng kỹ thuật)**

Đánh giá xu hướng giá dựa trên technical signals.

| Nhóm | Điều kiện | Score | Mô tả |
|------|-----------|-------|-------|
| **Strong Uptrend** | 3+ bullish signals | 9 | 🔥 Xu hướng tăng mạnh |
| **Uptrend** | 2 bullish signals | 7 | 📈 Xu hướng tăng |
| **Sideways** | Mixed signals | 5 | ➡️ Đi ngang |
| **Downtrend** | 2 bearish signals | 3 | 📉 Xu hướng giảm |
| **Strong Downtrend** | 3+ bearish signals | 1 | 💥 Xu hướng giảm mạnh |

**Signals được tính:**
- MACD (bullish/bearish)
- RSI (overbought/oversold)
- MA Crossover
- Bollinger Bands
- Volume trends

**Ý nghĩa:**
- **Strong Uptrend:** Đang tăng mạnh → Cơ hội mua/giữ
- **Uptrend:** Tăng ổn → An toàn để vào
- **Sideways:** Chưa rõ hướng → Chờ đợi
- **Downtrend:** Đang giảm → Cẩn thận
- **Strong Downtrend:** Giảm mạnh → Tránh xa

---

### **5. ⭐ Overall Rating (Đánh giá tổng thể)**

Tổng hợp từ 3 nhóm: Growth (40%), Risk (30%), Momentum (30%)

| Rating | Score Range | Recommendation | Ý nghĩa |
|--------|-------------|----------------|---------|
| **A+** | 8.0 - 10.0 | 🌟 Strong Buy - Mua mạnh | Xuất sắc, mua ngay |
| **A** | 7.0 - 7.9 | ✅ Buy - Mua | Tốt, đáng mua |
| **B** | 6.0 - 6.9 | 👀 Hold/Accumulate | Giữ hoặc tích lũy |
| **C** | 5.0 - 5.9 | ⏸️ Hold - Giữ | Trung bình, giữ |
| **D** | 4.0 - 4.9 | ⚠️ Watch - Theo dõi | Cẩn thận, theo dõi |
| **F** | < 4.0 | 🚫 Avoid - Tránh | Kém, tránh xa |

**Công thức:**
```
Overall Score = (Growth × 0.4) + ((10 - Risk) × 0.3) + (Momentum × 0.3)
```

---

## 🚀 HƯỚNG DẪN SỬ DỤNG

### **1. Command Line**

#### **Scan toàn thị trường:**
```bash
cd "/Users/nguyenhoang/Desktop/2025/hoc-tap code/vscode/VNSTOCK 2"
source venv/bin/activate

# Scan 20 mã (default)
python stock_classifier.py

# Scan 50 mã
python stock_classifier.py 50

# Scan 100 mã (tốn ~5 phút với delay 3s)
python stock_classifier.py 100
```

**Output:**
```
🔍 Scanning 20 stocks from ['HOSE']...
======================================================================
[1/20] VCB... ✅ B
[2/20] TCB... ✅ C
[3/20] FPT... ✅ A
...

📊 MARKET CLASSIFICATION SUMMARY
======================================================================

🚀 By Growth Potential:
growth          8
stable          6
high_growth     3

⭐ By Rating:
B     8
C     6
A     4

📈 Top 10 Recommendations:
symbol overall_rating  overall_score
FPT    A               7.5
VNM    A               7.2
VCB    B               6.8

✅ Saved to stock_classification_20251021_143000.csv
```

#### **Quick Test:**
```bash
# Test với 5 mã (nhanh)
python test_classifier_quick.py
```

---

### **2. API Usage**

#### **2.1. Classify Single Stock**

```bash
# Basic
curl "http://localhost:8501/classify/stock/VCB"

# From n8n
curl -X GET "http://192.168.1.4:8501/classify/stock/{{$json["symbol"]}}"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "symbol": "VCB",
    "timestamp": "2025-10-21T14:30:00",
    "classifications": {
      "growth": {
        "category": "growth",
        "score": 7,
        "description": "📈 Tăng trưởng ổn định",
        "roe": 16.22,
        "pe": 0
      },
      "risk": {
        "category": "medium_risk",
        "risk_score": 5,
        "description": "🟡 Rủi ro trung bình",
        "volatility": 25.3,
        "debt_equity": 9.37
      },
      "market_cap": {
        "category": "large_cap",
        "tier": 2,
        "description": "🏪 Large Cap - Blue-chip",
        "market_cap_trillion": 450.5
      },
      "momentum": {
        "category": "uptrend",
        "momentum_score": 7,
        "description": "📈 Xu hướng tăng"
      }
    },
    "overall_rating": {
      "score": 6.8,
      "rating": "B",
      "recommendation": "👀 Hold/Accumulate - Giữ/Tích lũy"
    }
  }
}
```

---

#### **2.2. Scan Market**

```bash
# Scan 50 stocks from HOSE
curl "http://localhost:8501/classify/market?exchanges=HOSE&limit=50&delay=3.0"

# Scan from multiple exchanges
curl "http://localhost:8501/classify/market?exchanges=HOSE,HNX&limit=100&delay=3.0"
```

**Response:**
```json
{
  "success": true,
  "summary": {
    "total_stocks": 50,
    "by_growth": {
      "growth": 20,
      "stable": 15,
      "high_growth": 8,
      "value": 5,
      "distressed": 2
    },
    "by_risk": {
      "medium_risk": 25,
      "low_risk": 15,
      "high_risk": 10
    },
    "by_rating": {
      "B": 18,
      "C": 15,
      "A": 10,
      "D": 5,
      "A+": 2
    },
    "avg_score": 6.2,
    "top_rated": [
      {"symbol": "FPT", "overall_rating": "A", "overall_score": 7.5}
    ]
  },
  "stocks": [...]
}
```

---

#### **2.3. Filter Stocks**

```bash
# High growth + Low risk
curl "http://localhost:8501/classify/filter?growth=high_growth&risk=low_risk&limit=100"

# A+ rated stocks
curl "http://localhost:8501/classify/filter?rating=A%2B&limit=100"

# Min score 7.0
curl "http://localhost:8501/classify/filter?min_score=7.0&limit=100"

# Combine filters
curl "http://localhost:8501/classify/filter?growth=growth&risk=low_risk&min_score=6.5&limit=100"
```

**Response:**
```json
{
  "success": true,
  "filters": {
    "growth": "high_growth",
    "risk": "low_risk",
    "rating": null,
    "min_score": null
  },
  "total_found": 8,
  "stocks": [
    {
      "symbol": "FPT",
      "growth_category": "high_growth",
      "risk_category": "low_risk",
      "overall_rating": "A",
      "overall_score": 7.5,
      "recommendation": "✅ Buy - Mua"
    }
  ]
}
```

---

#### **2.4. Get Top Picks**

```bash
# Top 10 picks, min rating B
curl "http://localhost:8501/classify/top-picks?count=10&min_rating=B&max_risk=medium_risk"

# Top 5 A+ stocks
curl "http://localhost:8501/classify/top-picks?count=5&min_rating=A%2B"
```

**Response:**
```json
{
  "success": true,
  "criteria": {
    "min_rating": "B",
    "max_risk": "medium_risk",
    "count": 10
  },
  "total_candidates": 35,
  "top_picks": [
    {
      "symbol": "FPT",
      "overall_rating": "A",
      "overall_score": 7.5,
      "growth_category": "high_growth",
      "risk_category": "low_risk",
      "recommendation": "✅ Buy - Mua"
    }
  ]
}
```

---

### **3. Python Code**

```python
from stock_classifier import StockClassifier, scan_market

# ========== QUICK SCAN ==========
df = scan_market(exchanges=['HOSE'], limit=50)

# ========== SINGLE CLASSIFICATION ==========
classifier = StockClassifier()
result = classifier.classify_stock('VCB')

print(f"Symbol: {result['symbol']}")
print(f"Rating: {result['overall_rating']['rating']}")
print(f"Score: {result['overall_rating']['score']}")
print(f"Recommendation: {result['overall_rating']['recommendation']}")

# ========== FILTER STOCKS ==========
high_growth_low_risk = classifier.get_stocks_by_filter(
    df,
    growth='high_growth',
    risk='low_risk',
    min_score=7.0
)

print(f"\nFound {len(high_growth_low_risk)} stocks:")
print(high_growth_low_risk[['symbol', 'overall_rating', 'overall_score']])

# ========== SAVE TO CSV ==========
df.to_csv('my_analysis.csv', index=False, encoding='utf-8-sig')
```

---

## 📊 USE CASES

### **1. Portfolio Construction**

**Mục tiêu:** Xây dựng danh mục đa dạng

```python
# Lấy 5 high growth + 5 stable + 5 value
high_growth = classifier.get_stocks_by_filter(df, growth='high_growth', risk='low_risk')
stable = classifier.get_stocks_by_filter(df, growth='stable', risk='low_risk')
value = classifier.get_stocks_by_filter(df, growth='value')

portfolio = pd.concat([
    high_growth.head(5),
    stable.head(5),
    value.head(5)
])
```

---

### **2. Risk Assessment**

**Mục tiêu:** Đánh giá rủi ro danh mục hiện tại

```python
my_portfolio = ['VCB', 'TCB', 'FPT', 'VNM', 'HPG']

for symbol in my_portfolio:
    result = classifier.classify_stock(symbol)
    risk = result['classifications']['risk']
    print(f"{symbol}: {risk['category']} - {risk['description']}")
```

---

### **3. Stock Screening**

**Mục tiêu:** Tìm cổ phiếu theo tiêu chí cụ thể

```bash
# API: Tìm cổ phiếu tăng trưởng cao, rủi ro thấp
curl "http://localhost:8501/classify/filter?growth=high_growth&risk=low_risk&min_score=7"
```

---

### **4. Market Overview**

**Mục tiêu:** Tổng quan thị trường

```python
df = scan_market(limit=200)

print("Market Statistics:")
print(f"Total stocks: {len(df)}")
print(f"Avg score: {df['overall_score'].mean():.2f}")
print(f"\nRating distribution:")
print(df['overall_rating'].value_counts())
print(f"\nRisk distribution:")
print(df['risk_category'].value_counts())
```

---

## 🔧 TÙY CHỈNH

### **Thay đổi thresholds:**

Edit file `stock_classifier.py`:

```python
self.thresholds = {
    'growth': {
        'high_growth': {
            'roe': 20,           # Thay đổi ở đây
            'pe_max': 25
        },
        'growth': {
            'roe': 15,           # Thay đổi ở đây
            'pe_max': 20
        }
    },
    'risk': {
        'low': {
            'volatility_max': 20,  # Thay đổi ở đây
            'de_max': 1,
            'roe_min': 15
        }
    }
}
```

---

### **Thay đổi scoring weights:**

```python
def _calculate_overall_rating(self, classifications: Dict) -> Dict:
    # Thay đổi weights
    weights = {
        'growth': 0.4,      # 40% → Thay đổi
        'risk': 0.3,        # 30% → Thay đổi
        'momentum': 0.3     # 30% → Thay đổi
    }
    
    total_score = (
        growth_score * weights['growth'] +
        risk_score * weights['risk'] +
        momentum_score * weights['momentum']
    )
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

### **1. Rate Limit:**
- VCI API có giới hạn requests
- **Default delay:** 3 seconds giữa các requests
- **Khuyến nghị:** Không scan quá 100 mã/lần

### **2. Thời gian thực thi:**
```
20 mã  = ~1 phút
50 mã  = ~3 phút
100 mã = ~6 phút
200 mã = ~12 phút
```

### **3. Độ chính xác:**
- **Market Cap:** Ước tính (Equity × 2)
- **P/E:** Có thể N/A với một số mã
- **Volatility:** Tính từ 1 năm dữ liệu

### **4. Cập nhật dữ liệu:**
- Dữ liệu FA: Cập nhật theo quý
- Dữ liệu TA: Real-time
- **Khuyến nghị:** Re-scan mỗi tuần 1 lần

---

## 📈 BEST PRACTICES

### ✅ **DO:**
1. Re-scan định kỳ (1 tuần 1 lần)
2. Kết hợp với phân tích thủ công
3. Kiểm tra tin tức công ty
4. Diversify across categories
5. Use filters to narrow down choices
6. Save results to CSV for comparison

### ❌ **DON'T:**
1. Scan quá nhiều mã cùng lúc (rate limit)
2. Dựa 100% vào classification
3. Bỏ qua risk category
4. Trade dựa chỉ trên momentum
5. Ignore fundamental changes
6. Overlook market conditions

---

## 🎯 CHIẾN LƯỢC ĐẦU TƯ

### **1. Conservative (Bảo thủ):**
```
Filter: growth=stable, risk=low_risk, min_score=6.0
→ Cổ phiếu ổn định, rủi ro thấp
```

### **2. Balanced (Cân bằng):**
```
Filter: growth=growth, risk=medium_risk, rating=B
→ Tăng trưởng tốt, rủi ro chấp nhận được
```

### **3. Aggressive (Tích cực):**
```
Filter: growth=high_growth, min_score=7.0
→ Tăng trưởng cao, chấp nhận rủi ro
```

### **4. Value Investing:**
```
Filter: growth=value, risk=low_risk
→ Giá rẻ, tiềm năng phục hồi
```

---

## 📞 SUPPORT

**Issues:** https://github.com/nguyenhoang1221hoangnguyen/vnstock-data-collector/issues

**Documentation:**
- README.md
- QUICK_START.md
- CLASSIFICATION_GUIDE.md (this file)
- API Docs: http://localhost:8501/docs

---

## 🎓 FAQ

**Q: Tại sao một số mã có P/E = 0?**  
A: VCI API không trả về số lượng cổ phiếu lưu hành. Tiêu chí P/E sẽ bị bỏ qua.

**Q: Làm sao để scan nhanh hơn?**  
A: Giảm delay xuống 1s (có thể bị rate limit) hoặc scan batch nhỏ hơn.

**Q: Kết quả có chính xác không?**  
A: Kết quả dựa trên data từ VCI và công thức tính toán. Nên kết hợp phân tích thủ công.

**Q: Có thể lưu vào database không?**  
A: Có, code đã có sẵn `get_db()`. Bạn có thể extend để save results.

**Q: Tích hợp với dashboard?**  
A: Dashboard integration sẽ được thêm trong version tiếp theo.

---

**🎯 Happy Stock Screening! 📊**

*Version: 1.0*  
*Last Updated: 2025-10-21*  
*Author: VNStock Team*

