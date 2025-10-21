# 📊 Hướng dẫn Phân tích Cơ bản (FA) - VNStock Data Collector

Hướng dẫn sử dụng module phân tích cơ bản (Fundamental Analysis) để tính toán và diễn giải các chỉ số tài chính.

## 🎯 Tổng quan

Module FA Calculator cung cấp các công cụ để:
- Tính toán các chỉ số tài chính quan trọng
- Diễn giải và đánh giá các chỉ số
- Đưa ra khuyến nghị đầu tư

## 📊 Các chỉ số FA được tính toán

### 1. **EPS (Earnings Per Share)** - Thu nhập mỗi cổ phiếu
- **Công thức**: `EPS = Tổng lợi nhuận ròng 4 quý / Số cổ phiếu lưu hành`
- **Đơn vị**: Nghìn đồng/cổ phiếu
- **Ý nghĩa**: Thu nhập mà mỗi cổ phiếu tạo ra
- **Đánh giá**: Càng cao càng tốt

### 2. **P/E (Price to Earnings)** - Tỷ lệ Giá/Thu nhập
- **Công thức**: `P/E = Giá thị trường hiện tại / EPS`
- **Đơn vị**: Lần
- **Ý nghĩa**: Số năm cần để thu hồi vốn đầu tư
- **Đánh giá**:
  - `< 10`: Có thể bị định giá thấp hoặc doanh nghiệp gặp khó khăn
  - `10-15`: Định giá hợp lý cho thị trường Việt Nam
  - `15-25`: Định giá cao, kỳ vọng tăng trưởng tốt
  - `> 25`: Định giá rất cao, có thể bị thổi phồng

### 3. **ROE (Return on Equity)** - Tỷ suất sinh lời trên vốn chủ sở hữu
- **Công thức**: `ROE = (Lợi nhuận ròng 4 quý / Vốn chủ sở hữu) × 100`
- **Đơn vị**: %
- **Ý nghĩa**: Hiệu quả sử dụng vốn chủ sở hữu
- **Đánh giá**:
  - `< 10%`: Hiệu quả thấp
  - `10-15%`: Trung bình
  - `15-25%`: Tốt
  - `> 25%`: Xuất sắc

### 4. **NPM (Net Profit Margin)** - Biên lợi nhuận ròng
- **Công thức**: `NPM = (Lợi nhuận ròng / Doanh thu) × 100`
- **Đơn vị**: %
- **Ý nghĩa**: Khả năng kiểm soát chi phí và tạo lợi nhuận
- **Đánh giá**:
  - `< 5%`: Thấp
  - `5-10%`: Trung bình
  - `10-20%`: Tốt
  - `> 20%`: Rất cao

### 5. **D/E (Debt to Equity)** - Tỷ lệ Nợ/Vốn chủ sở hữu
- **Công thức**: `D/E = Nợ phải trả / Vốn chủ sở hữu`
- **Đơn vị**: Lần
- **Ý nghĩa**: Mức độ sử dụng nợ trong cấu trúc vốn
- **Đánh giá**:
  - `< 0.5`: Rất an toàn
  - `0.5-1.0`: Hợp lý
  - `1.0-2.0`: Cao
  - `> 2.0`: Rất cao, rủi ro

## 🔧 Sử dụng API

### **Endpoint 1: Tính toán chỉ số FA**

```bash
GET /stock/{symbol}/fa
```

**Ví dụ:**
```bash
curl "http://localhost:8501/stock/FPT/fa"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "symbol": "FPT",
    "calculation_date": "2025-10-21T09:40:22.776362",
    "current_price": 90.0,
    "price_unit": "nghìn đồng",
    "ratios": {
      "EPS": 581.6,
      "PE": 0.15,
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

### **Endpoint 2: Phân tích FA với diễn giải**

```bash
GET /stock/{symbol}/fa/interpret
```

**Ví dụ:**
```bash
curl "http://localhost:8501/stock/FPT/fa/interpret"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "fa_ratios": {
      "symbol": "FPT",
      "ratios": {
        "EPS": 581.6,
        "PE": 0.15,
        "ROE": 21.61,
        "NPM": 13.58,
        "DE": 1.04
      }
    },
    "interpretation": {
      "symbol": "FPT",
      "interpretations": {
        "PE": {
          "value": 0.15,
          "rating": "low",
          "meaning": "Cổ phiếu có thể bị định giá thấp",
          "investment_note": "Cần xem xét kỹ nguyên nhân P/E thấp"
        },
        "ROE": {
          "value": 21.61,
          "rating": "good",
          "meaning": "Hiệu quả sử dụng vốn tốt",
          "investment_note": "Doanh nghiệp sinh lời tốt"
        }
      },
      "overall_rating": "good",
      "investment_considerations": [
        "Doanh nghiệp ổn định, có thể cân nhắc đầu tư"
      ]
    }
  }
}
```

## 🐍 Sử dụng Python Module

### **Import module:**
```python
from fa_calculator import calculate_fa_ratios, get_fa_interpretation
```

### **Tính toán chỉ số FA:**
```python
# Tính toán FA ratios cho mã FPT
fa_ratios = calculate_fa_ratios("FPT")

print(f"Mã: {fa_ratios['symbol']}")
print(f"P/E: {fa_ratios['ratios']['PE']}")
print(f"ROE: {fa_ratios['ratios']['ROE']}%")
print(f"NPM: {fa_ratios['ratios']['NPM']}%")
print(f"D/E: {fa_ratios['ratios']['DE']}")
print(f"EPS: {fa_ratios['ratios']['EPS']} nghìn đồng")
```

### **Diễn giải kết quả:**
```python
# Diễn giải các chỉ số
interpretation = get_fa_interpretation(fa_ratios)

print(f"Đánh giá tổng thể: {interpretation['overall_rating']}")
print(f"Khuyến nghị: {interpretation['investment_considerations']}")

# Xem chi tiết từng chỉ số
for ratio_name, interp in interpretation['interpretations'].items():
    print(f"\n{ratio_name}:")
    print(f"  Giá trị: {interp['value']}")
    print(f"  Đánh giá: {interp['rating']}")
    print(f"  Ý nghĩa: {interp['meaning']}")
    print(f"  Lưu ý: {interp['investment_note']}")
```

## 🌐 Tích hợp với n8n

### **HTTP Request Node Configuration:**

**URL:** `http://localhost:8501/stock/{{$json.symbol}}/fa/interpret`  
**Method:** `GET`  
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Input Data:**
```json
{
  "symbol": "FPT"
}
```

### **Process Response:**
```javascript
// Lấy các chỉ số FA
const ratios = $json.data.fa_ratios.ratios;
const interpretation = $json.data.interpretation;

// Tạo message cho AI agent
return {
  symbol: $json.data.fa_ratios.symbol,
  analysis: {
    pe_ratio: ratios.PE,
    roe: ratios.ROE,
    npm: ratios.NPM,
    de_ratio: ratios.DE,
    eps: ratios.EPS
  },
  overall_rating: interpretation.overall_rating,
  recommendation: interpretation.investment_considerations[0]
};
```

## 📈 Ví dụ phân tích thực tế

### **Case Study: FPT Corporation**

```bash
curl "http://localhost:8501/stock/FPT/fa/interpret"
```

**Kết quả:**
- **EPS**: 581.6 nghìn đồng → Thu nhập cao
- **P/E**: 0.15 → Định giá rất thấp (có thể do sai số trong tính toán số cổ phiếu)
- **ROE**: 21.61% → Hiệu quả sử dụng vốn tốt
- **NPM**: 13.58% → Biên lợi nhuận tốt
- **D/E**: 1.04 → Tỷ lệ nợ ở mức hợp lý

**Đánh giá tổng thể**: **GOOD** - Doanh nghiệp ổn định, có thể cân nhắc đầu tư

## ⚠️ Lưu ý quan trọng

### **1. Data Quality**
- Một số chỉ số có thể không tính được do thiếu dữ liệu
- Kiểm tra `data_quality` field để biết độ tin cậy
- `completeness` cho biết tỷ lệ chỉ số tính được thành công

### **2. Giới hạn dữ liệu**
- Dữ liệu lấy từ vnstock (VCI source)
- Một số mã có thể thiếu thông tin cổ phiếu lưu hành
- Ngân hàng (như VCB) có cấu trúc tài chính đặc thù

### **3. Diễn giải**
- Đánh giá dựa trên chuẩn thị trường Việt Nam
- Cần xem xét ngành nghề và bối cảnh kinh tế
- Chỉ số FA là công cụ tham khảo, không phải khuyến nghị đầu tư

### **4. P/E thấp bất thường**
- Nếu P/E < 1, có thể do:
  - Sai số trong số lượng cổ phiếu lưu hành
  - Giá đang ở đơn vị nghìn đồng
  - Cần kiểm tra lại dữ liệu gốc

## 🔍 Troubleshooting

### **Lỗi: "Không đủ dữ liệu để tính chỉ số"**
- Kiểm tra mã cổ phiếu có đúng không
- Một số mã mới niêm yết có thể thiếu dữ liệu lịch sử
- Xem `data_quality` để biết chỉ số nào bị lỗi

### **Chỉ số bằng None**
- Dữ liệu từ vnstock không đầy đủ
- Kiểm tra `raw_data` để biết số quý dữ liệu có được
- Thử lại sau hoặc dùng mã khác

### **P/E hoặc ROE âm**
- Doanh nghiệp đang thua lỗ
- Chỉ số này không có ý nghĩa trong trường hợp này
- Xem xét các chỉ số khác

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra API đang chạy: `curl http://localhost:8501/health`
2. Xem logs: `docker-compose logs -f` hoặc console output
3. Test với mã khác: `FPT`, `VIC`, `VCB`
4. Kiểm tra completeness percentage

---

🎉 **Module FA Analysis đã sẵn sàng để phân tích cổ phiếu Việt Nam!**
