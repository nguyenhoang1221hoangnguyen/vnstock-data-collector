# 🎯 BLUE-CHIP DETECTOR - User Guide

## 📊 Tổng quan

**Blue-chip Detector** là công cụ tự động phát hiện cổ phiếu blue-chip (cổ phiếu lớn, ổn định, chất lượng cao) trên thị trường Việt Nam.

---

## ✅ Tiêu chí Blue-chip

Một cổ phiếu được coi là **Blue-chip** khi đáp ứng **ít nhất 4/6 tiêu chí**:

| # | Tiêu chí | Ngưỡng | Mô tả |
|---|----------|--------|-------|
| 1 | **VN30** | Có trong rổ VN30 | Top 30 cổ phiếu lớn nhất |
| 2 | **P/E Ratio** | 5 < P/E < 20 | Định giá hợp lý |
| 3 | **ROE** | > 15% | Sinh lời vốn chủ sở hữu tốt |
| 4 | **Market Cap** | > 10,000 tỷ VND | Vốn hóa lớn |
| 5 | **Volume** | > 500,000 cp/ngày | Thanh khoản cao |
| 6 | **Volatility** | < 30% (1 năm) | Ổn định giá |

**Score:** 
- 6/6: ⭐⭐⭐ Perfect Blue-chip
- 5/6: ⭐⭐ Excellent
- 4/6: ⭐ Good
- <4/6: ❌ Not qualified

---

## 🚀 Cách sử dụng

### **1. Command Line (Standalone)**

```bash
cd "/Users/nguyenhoang/Desktop/2025/hoc-tap code/vscode/VNSTOCK 2"
source venv/bin/activate

# Scan VN30 (default)
python bluechip_detector.py

# Auto-add to watchlist
python bluechip_detector.py --auto
```

**Output:**
```
🎯 Scanning VN30 for Blue-chips...

🔍 Scanning 30 stocks for blue-chips...

[1/30] Checking ACB... ❌ Not qualified (Score: 3/6)
[2/30] Checking VCB... ✅ BLUE-CHIP! (Score: 5/6)
[3/30] Checking TCB... ✅ BLUE-CHIP! (Score: 4/6)
...

======================================================================
📊 BLUE-CHIP STOCKS REPORT
======================================================================

Total Blue-chips Found: 8
Scan Date: 2025-10-21 14:30:00

1. VCB - Score: 5/6
   ✓ VN30: Yes ✅
   ❌ P/E: N/A
   ✅ ROE: 16.22%
   ✅ Market Cap: 12.5 trillion VND
   ✅ Avg Volume: 1,500,000
   ✅ Volatility: 18.5%

2. TCB - Score: 4/6
   ...

📌 Add 8 blue-chips to watchlist? (y/n): y
✅ Added 8 stocks to watchlist!
```

---

### **2. API Endpoints**

#### **a) Scan Blue-chips**

```bash
# Scan VN30 (default)
curl "http://localhost:8501/bluechip/scan"

# Scan custom symbols
curl "http://localhost:8501/bluechip/scan?symbols=VCB,TCB,FPT,VNM,HPG"

# Adjust minimum score
curl "http://localhost:8501/bluechip/scan?min_score=5"
```

**Response:**
```json
{
  "success": true,
  "total": 8,
  "bluechips": [
    {
      "symbol": "VCB",
      "is_bluechip": true,
      "score": 5,
      "max_score": 6,
      "criteria_met": {
        "vn30": true,
        "pe": false,
        "roe": true,
        "market_cap": true,
        "volume": true,
        "volatility": true
      },
      "details": {
        "vn30": true,
        "roe": 16.22,
        "market_cap": 12500000000000,
        "avg_volume": 1500000,
        "volatility": 18.5
      }
    }
  ],
  "scan_date": "2025-10-21T14:30:00",
  "criteria": {
    "min_market_cap": 10000000000000,
    "min_pe": 5,
    "max_pe": 20,
    "min_roe": 15,
    "min_avg_volume": 500000,
    "max_volatility": 30
  }
}
```

#### **b) Auto-add to Watchlist**

```bash
# Scan and add to watchlist
curl -X POST "http://localhost:8501/bluechip/add-to-watchlist"

# Custom symbols
curl -X POST "http://localhost:8501/bluechip/add-to-watchlist?symbols=VCB,TCB,FPT"
```

**Response:**
```json
{
  "success": true,
  "scanned": 8,
  "added": 8,
  "symbols": ["VCB", "TCB", "FPT", "VNM", "HPG", "MSN", "MWG", "VIC"],
  "timestamp": "2025-10-21T14:30:00"
}
```

#### **c) Get Detailed Report**

```bash
curl "http://localhost:8501/bluechip/report"
```

**Response:**
```json
{
  "success": true,
  "report": "...(full text report)...",
  "bluechips": [...],
  "timestamp": "2025-10-21T14:30:00"
}
```

---

### **3. Python Code**

```python
from bluechip_detector import BlueChipDetector

# Initialize detector
detector = BlueChipDetector()

# Scan VN30
bluechips = detector.scan_bluechips()

# Scan custom symbols
bluechips = detector.scan_bluechips(symbols=['VCB', 'TCB', 'FPT'])

# Get report
report = detector.get_bluechip_report(bluechips)
print(report)

# Add to watchlist
added = detector.auto_add_to_watchlist(bluechips)
print(f"Added {added} stocks")
```

---

### **4. Integration with n8n**

**Workflow Example:**

1. **Schedule Trigger** (Mỗi tuần 1 lần)
2. **HTTP Request Node:**
   - Method: POST
   - URL: `http://192.168.1.4:8501/bluechip/add-to-watchlist`
3. **IF Node** (Check success)
4. **Send Email/Telegram** (Thông báo kết quả)

**cURL for n8n:**
```bash
curl -X POST "http://192.168.1.4:8501/bluechip/add-to-watchlist?min_score=4"
```

---

## 🔧 Tùy chỉnh tiêu chí

Để thay đổi tiêu chí blue-chip, edit file `bluechip_detector.py`:

```python
# Trong __init__ method của BlueChipDetector
self.criteria = {
    'min_market_cap': 10_000_000_000_000,  # 10,000 tỷ → Thay đổi ở đây
    'min_pe': 5,                            # P/E min
    'max_pe': 20,                           # P/E max
    'min_roe': 15,                          # ROE min (%) → Thay đổi
    'min_avg_volume': 500_000,              # Volume TB/ngày
    'max_volatility': 30,                   # Biến động max (%)
}
```

**Ví dụ tiêu chí khắt khe hơn:**
```python
self.criteria = {
    'min_market_cap': 20_000_000_000_000,  # 20,000 tỷ (tăng gấp đôi)
    'min_pe': 8,
    'max_pe': 15,
    'min_roe': 18,                          # Tăng lên 18%
    'min_avg_volume': 1_000_000,            # Tăng lên 1M cp/ngày
    'max_volatility': 20,                   # Giảm xuống 20%
}
```

---

## 📊 Hiểu kết quả

### **Score Interpretation:**

| Score | Đánh giá | Hành động |
|-------|----------|-----------|
| 6/6 | ⭐⭐⭐ Perfect | ✅ MUA NGAY |
| 5/6 | ⭐⭐ Excellent | ✅ Cân nhắc mua |
| 4/6 | ⭐ Good | 👀 Theo dõi |
| 3/6 | ⚠️ Fair | ⏸️ Chờ đợi |
| 0-2/6 | ❌ Poor | 🚫 Tránh |

### **Criteria Analysis:**

**✅ VN30 = Yes:**
- Top 30 cổ phiếu lớn nhất
- Thanh khoản tốt
- Được tổ chức theo dõi

**✅ P/E = 5-20:**
- Định giá hợp lý
- Không quá rẻ (P/E < 5 = rủi ro)
- Không quá đắt (P/E > 20 = bong bóng)

**✅ ROE > 15%:**
- Sinh lời vốn chủ hiệu quả
- Quản lý tốt
- Lợi nhuận ổn định

**✅ Market Cap > 10,000 tỷ:**
- Công ty lớn, uy tín
- Khó thao túng giá
- Rủi ro thấp

**✅ Volume > 500,000:**
- Dễ mua/bán
- Giá minh bạch
- Thanh khoản tốt

**✅ Volatility < 30%:**
- Giá ổn định
- Rủi ro thấp
- Phù hợp đầu tư dài hạn

---

## ⚠️ Lưu ý quan trọng

### **1. Rate Limit:**
- API VCI có giới hạn requests
- **Khuyến nghị:** Scan không quá 10 mã/phút
- Sử dụng `time.sleep(3)` giữa các mã

### **2. Dữ liệu:**
- P/E có thể không có với một số mã (do API)
- Market Cap là ước tính (dựa trên Equity × 2)
- Dữ liệu cập nhật theo quý/năm

### **3. Tiêu chí:**
- Tiêu chí mặc định là **tham khảo**
- Cần điều chỉnh theo mục tiêu cá nhân
- Nên kết hợp phân tích thủ công

### **4. Không phải lời khuyên tài chính:**
- Đây là công cụ **hỗ trợ** phân tích
- Không thay thế nghiên cứu thủ công
- Luôn DYOR (Do Your Own Research)

---

## 🎯 Use Cases

### **1. Đầu tư dài hạn:**
```bash
# Tìm blue-chips ổn định
python bluechip_detector.py
# Chọn mã có Score 5-6/6
# Mua và giữ 3-5 năm
```

### **2. Diversification:**
```bash
# Scan toàn bộ VN30
curl "http://localhost:8501/bluechip/scan"
# Chọn 8-10 mã để đa dạng hóa
```

### **3. Tự động hóa:**
```bash
# Cron job mỗi tuần
0 8 * * 0 cd /path && python bluechip_detector.py --auto
```

### **4. Watchlist Management:**
```python
# Python script
detector = BlueChipDetector()
bluechips = detector.scan_bluechips()
detector.auto_add_to_watchlist(bluechips)

# Xem trong Advanced Dashboard
# Tab "Watchlist"
```

---

## 🔍 Troubleshooting

### **Problem: Rate limit exceeded**
**Solution:**
```python
# Edit bluechip_detector.py
# Thêm delay trong scan_bluechips:
import time
for symbol in symbols:
    result = self.check_bluechip_criteria(symbol)
    time.sleep(3)  # Add 3 second delay
```

### **Problem: P/E = N/A**
**Reason:** API không trả về số lượng cổ phiếu lưu hành  
**Solution:** Tiêu chí vẫn hoạt động, P/E bị bỏ qua

### **Problem: No blue-chips found**
**Reason:** Tiêu chí quá khắt khe  
**Solution:** Giảm `min_score` xuống 3 hoặc điều chỉnh `criteria`

---

## 📚 API Documentation

### **GET /bluechip/scan**
**Parameters:**
- `symbols` (optional): "ACB,VCB,TCB"
- `min_score` (optional): 1-6 (default: 4)

**Returns:** List of blue-chips with details

---

### **POST /bluechip/add-to-watchlist**
**Parameters:**
- `symbols` (optional): "ACB,VCB,TCB"
- `min_score` (optional): 1-6 (default: 4)

**Returns:** Number of stocks added

---

### **GET /bluechip/report**
**Parameters:**
- `symbols` (optional): "ACB,VCB,TCB"
- `min_score` (optional): 1-6 (default: 4)

**Returns:** Text report + JSON data

---

## 💡 Tips & Best Practices

✅ **DO:**
- Chạy scan định kỳ (1 tuần 1 lần)
- Kết hợp với phân tích tin tức
- Kiểm tra báo cáo tài chính
- Đa dạng hóa danh mục

❌ **DON'T:**
- Scan quá nhiều mã cùng lúc (rate limit)
- Dựa 100% vào tool (cần nghiên cứu thêm)
- Mua tất cả blue-chips cùng lúc
- Bỏ qua quản lý rủi ro

---

## 🎓 Example Workflow

**Weekly Blue-chip Review:**

1. **Monday 8AM:** Run scan
   ```bash
   python bluechip_detector.py
   ```

2. **Review results:** Check scores + details

3. **Research top 5:** Read news, financials

4. **Select 2-3:** For purchase

5. **Add alerts:** Set price alerts

6. **Monitor weekly:** Track performance

---

## 📞 Support

**Issues:** https://github.com/nguyenhoang1221hoangnguyen/vnstock-data-collector/issues

**Documentation:** See README.md, QUICK_START.md

---

**🎯 Happy Blue-chip Hunting! 📈**

*Version: 1.0*  
*Last Updated: 2025-10-21*

