# VNStock Data Collector API

🇻🇳 **Ứng dụng Python chuyên nghiệp** sử dụng thư viện vnstock để thu thập **toàn bộ dữ liệu cổ phiếu Việt Nam**, được thiết kế đặc biệt để tích hợp với **n8n workflow** và **AI analysis systems**.

## 🚀 Tính năng chính

- **📊 Thu thập dữ liệu toàn diện**: 15+ năm dữ liệu lịch sử (3,940+ bản ghi) + 17+ năm báo cáo tài chính (51 báo cáo)
- **🔗 API RESTful hoàn chỉnh**: Tích hợp dễ dàng với n8n, AI agents và các hệ thống khác
- **🤖 Tối ưu cho AI**: Cấu trúc JSON rõ ràng, metadata phong phú, gợi ý phân tích tự động
- **⚡ Hiệu suất cao**: Không giới hạn thời gian hay số lượng bản ghi, dữ liệu real-time
- **🛡️ Ổn định**: Logging chi tiết, error handling, health check endpoint
- **🐳 Dễ triển khai**: Docker support, virtual environment, one-command setup
- **💰 Đơn vị tiền tệ VND chính xác**: Không làm tròn để tránh sai số, metadata đầy đủ cho currency tracking

## 📊 Dữ liệu thu thập (Toàn diện & Không giới hạn)

### 📈 **1. Dữ liệu lịch sử giá cổ phiếu**
- **Khoảng thời gian**: 2010 - hiện tại (15+ năm)
- **Tổng bản ghi**: 3,940+ ngày giao dịch
- **Tần suất**: Theo ngày (OHLCV)
- **Cập nhật**: Real-time đến T-1

### 💰 **2. Dữ liệu tài chính doanh nghiệp**
- **Khoảng thời gian**: 2008 - 2025 (17+ năm)
- **Tổng bản ghi**: 51 báo cáo tài chính
- **Bao gồm**: Bảng cân đối kế toán, KQKD, LCTT
- **Chỉ số**: P/E, ROE, ROA, Debt/Equity, etc.

### 🏢 **3. Thông tin doanh nghiệp**
- Thông tin cơ bản công ty
- Giá hiện tại và biến động
- Thông tin cổ đông và sự kiện

### 🤖 **4. AI Analysis Metadata**
- **Data completeness check**: Đánh giá tính đầy đủ
- **Analysis suggestions**: 5+ gợi ý phân tích tự động
- **Key metrics summary**: Tóm tắt chỉ số quan trọng
- **Structured format**: Tối ưu cho machine learning

### 💰 **5. Đơn vị tiền tệ & Độ chính xác**
- **Đơn vị**: VND (Đồng Việt Nam) - được ghi rõ trong metadata
- **Độ chính xác**: Không làm tròn - giữ nguyên giá trị gốc để tránh sai số
- **Format**: Số thực (float) hoặc số nguyên (int) tùy theo dữ liệu gốc
- **Currency tracking**: Metadata đầy đủ cho AI analysis và tính toán
- **Tương thích**: Hoàn toàn tương thích với các hệ thống tính toán tài chính

## 🛠 Cài đặt & Triển khai

### 🚀 **Cách 1: Setup tự động (Khuyến nghị)**

```bash
# Clone repository
git clone <repository-url>
cd vnstock-data-collector

# Chạy setup tự động
python setup.py

# Khởi chạy server
python start_server.py
```

### 🐍 **Cách 2: Manual setup**

```bash
# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc venv\Scripts\activate  # Windows

# Cài đặt dependencies
pip install -r requirements.txt

# Khởi chạy server
python start_server.py
```

### 🐳 **Cách 3: Docker (Coming soon)**

```bash
docker build -t vnstock-collector .
docker run -p 8501:8501 vnstock-collector
```

**Server sẽ chạy tại**: `http://localhost:8501`

## 📖 API Documentation

### Endpoints chính

#### 1. Lấy toàn bộ dữ liệu cổ phiếu
```
GET /stock/{symbol}?start_date=2023-01-01&end_date=2024-01-01
```

**Ví dụ:**
```bash
curl "http://localhost:8501/stock/VIC?start_date=2023-01-01&end_date=2024-01-01"
```

#### 2. Lấy thông tin tổng quan
```
GET /stock/{symbol}/overview
```

#### 3. Lấy dữ liệu lịch sử
```
GET /stock/{symbol}/historical?start_date=2023-01-01&end_date=2024-01-01
```

#### 4. Lấy dữ liệu tài chính
```
GET /stock/{symbol}/financial
```

#### 5. Lấy dữ liệu thị trường
```
GET /stock/{symbol}/market
```

#### 6. Batch request (POST) - Phù hợp cho n8n
```
POST /stock/batch
Content-Type: application/json

{
    "symbol": "VIC",
    "start_date": "2023-01-01",
    "end_date": "2024-01-01"
}
```

### Response Format

Tất cả endpoint trả về cấu trúc JSON chuẩn:

```json
{
    "success": true,
    "data": {
        "request_info": {
            "symbol": "VIC",
            "start_date": "2023-01-01",
            "end_date": "2024-01-01",
            "collection_timestamp": "2024-01-01T10:00:00",
            "data_source": "vnstock"
        },
        "overview": { ... },
        "historical_data": { ... },
        "financial_data": { ... },
        "market_data": { ... },
        "ai_analysis_metadata": { ... }
    },
    "timestamp": "2024-01-01T10:00:00"
}
```

## 🔗 Tích hợp với n8n & AI Systems

### 🤖 **n8n Workflow Integration**

#### **Cấu hình HTTP Request Node:**
```json
{
  "method": "POST",
  "url": "http://192.168.1.4:8501/stock/batch",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "symbol": "{{$json['stock_symbol']}}",
    "start_date": "{{$json['start_date']}}",
    "end_date": "{{$json['end_date']}}"
  }
}
```

#### **Workflow mẫu có sẵn:**
- Import file `n8n_workflow_example.json`
- Tự động xử lý lỗi và notification
- Tích hợp database và AI analysis

### 🧠 **AI Analysis Integration**

Response được tối ưu cho AI systems:
```json
{
  "ai_analysis_metadata": {
    "data_completeness": {
      "has_overview": true,
      "has_historical_data": true,
      "has_financial_data": true,
      "overall_complete": true
    },
    "analysis_suggestions": [
      "Phân tích xu hướng giá trong 15 năm qua",
      "So sánh hiệu suất với VN-Index",
      "Đánh giá tình hình tài chính qua các quý"
    ],
    "key_metrics_summary": {
      "current_price": 204.0,
      "total_trading_days": 3940,
      "price_change_percent": 15.2
    }
  }
}
```

## 🎯 Ví dụ sử dụng thực tế

### 📊 **1. Lấy toàn bộ dữ liệu cổ phiếu VIC (15+ năm)**

```bash
curl -X POST http://localhost:8501/stock/batch \
  -H 'Content-Type: application/json' \
  -d '{"symbol": "VIC"}'

# Response: 3,940+ bản ghi lịch sử + 51 báo cáo tài chính
```

### 📈 **2. Lấy dữ liệu khoảng thời gian cụ thể**

```bash
curl -X POST http://localhost:8501/stock/batch \
  -H 'Content-Type: application/json' \
  -d '{
    "symbol": "VCB",
    "start_date": "2020-01-01",
    "end_date": "2024-12-31"
  }'
```

### 🔍 **3. Lấy từng loại dữ liệu riêng biệt**

```bash
# Chỉ dữ liệu lịch sử
curl "http://localhost:8501/stock/VIC/historical"

# Chỉ dữ liệu tài chính
curl "http://localhost:8501/stock/VIC/financial"

# Thông tin tổng quan
curl "http://localhost:8501/stock/VIC/overview"
```

### 🤖 **4. Kết quả mẫu cho AI Analysis**

```json
{
  "success": true,
  "data": {
    "request_info": {
      "symbol": "VIC",
      "start_date": "2010-01-01",
      "end_date": "2025-10-19",
      "collection_timestamp": "2025-10-19T22:59:02"
    },
    "historical_data": {
      "daily_data": [/* 3,940+ records */],
      "total_trading_days": 3940
    },
    "financial_data": {
      "balance_sheet": [/* 51 records from 2008-2025 */]
    },
    "ai_analysis_metadata": {
      "data_completeness": {
        "overall_complete": true
      },
      "analysis_suggestions": [
        "Phân tích xu hướng giá trong 15 năm qua",
        "Đánh giá biến động và rủi ro",
        "So sánh với chỉ số VN-Index"
      ]
    }
  }
}
```

## 🔍 Monitoring và Debugging

### 1. Health Check
```bash
curl "http://localhost:8501/health"
```

### 2. API Documentation
Truy cập: `http://localhost:8501/docs` để xem Swagger UI

### 3. Logs
Ứng dụng sẽ ghi log chi tiết về quá trình thu thập dữ liệu và các lỗi xảy ra.

## 📝 Lưu ý quan trọng

### 1. Mã cổ phiếu hợp lệ
- Sử dụng mã cổ phiếu chính xác (VD: VIC, VCB, FPT)
- Hệ thống tự động chuyển về chữ hoa

### 2. Định dạng ngày tháng
- Sử dụng format: `YYYY-MM-DD`
- Ví dụ: `2023-01-01`

### 3. Giới hạn dữ liệu
- Dữ liệu lịch sử mặc định từ 2010-01-01
- Có thể tùy chỉnh khoảng thời gian theo nhu cầu

### 4. Performance
- API có thể mất vài giây để thu thập đầy đủ dữ liệu
- Nên cache kết quả cho các request lặp lại

## 🚨 Xử lý lỗi

API sẽ trả về thông tin lỗi chi tiết:

```json
{
    "success": false,
    "error": "Mô tả lỗi chi tiết",
    "timestamp": "2024-01-01T10:00:00"
}
```

Các lỗi thường gặp:
- Mã cổ phiếu không tồn tại
- Định dạng ngày tháng không hợp lệ
- Lỗi kết nối đến nguồn dữ liệu
- Thiếu dữ liệu cho khoảng thời gian yêu cầu

## 🚀 Production Deployment

### 🌐 **Network Configuration**
- **Local**: `http://localhost:8501`
- **Network**: `http://192.168.1.4:8501` (thay IP theo máy host)
- **Docker**: `http://0.0.0.0:8501`

### 📊 **Performance Metrics**
- **Response time**: < 5s cho toàn bộ dữ liệu
- **Data volume**: 3,940+ records/request
- **Concurrent requests**: Hỗ trợ multiple requests
- **Memory usage**: ~200MB với full dataset

### 🔧 **Troubleshooting**

#### **Lỗi thường gặp:**
```bash
# Lỗi kết nối n8n
ECONNREFUSED ::1:8501 → Sử dụng IP thay localhost

# Lỗi timeout
Tăng timeout trong n8n > 60s

# Lỗi memory
Giảm khoảng thời gian hoặc tăng RAM
```

## 📁 Cấu trúc Project

```
vnstock-data-collector/
├── 📄 main.py                     # FastAPI server chính
├── 📄 vnstock_data_collector_simple.py  # Data collector engine
├── 📄 start_server.py             # Script khởi chạy
├── 📄 setup.py                    # Auto setup script
├── 📄 test_api.py                 # API testing script
├── 📄 requirements.txt            # Dependencies
├── 📄 n8n_workflow_example.json   # n8n workflow mẫu
├── 📄 README.md                   # Documentation
├── 📄 .gitignore                  # Git ignore rules
└── 📁 venv/                       # Virtual environment
```

## 🎯 Use Cases

### 🤖 **AI & Machine Learning**
- **Stock price prediction**: 15+ năm dữ liệu lịch sử
- **Financial analysis**: 17+ năm báo cáo tài chính
- **Risk assessment**: Volatility và correlation analysis
- **Portfolio optimization**: Multi-stock comparison

### 📊 **Business Intelligence**
- **Automated reporting**: Tích hợp n8n workflows
- **Real-time monitoring**: Price alerts và notifications
- **Data warehousing**: ETL pipeline cho data lake
- **Dashboard integration**: Power BI, Tableau, Grafana

### 🔬 **Research & Analytics**
- **Academic research**: Vietnam stock market analysis
- **Quantitative trading**: Algorithm development
- **Market research**: Sector và industry analysis
- **Economic modeling**: Macro-economic indicators

## 🤝 Contributing

Chúng tôi hoan nghênh mọi đóng góp! 

### **Cách đóng góp:**
1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

### **Báo cáo lỗi:**
- Sử dụng GitHub Issues
- Cung cấp log chi tiết
- Mô tả steps to reproduce

## 📄 License

**MIT License** - Xem file [LICENSE](LICENSE) để biết thêm chi tiết.

## 📞 Support & Contact

- **GitHub Issues**: [Báo cáo lỗi & feature requests](https://github.com/your-repo/issues)
- **Documentation**: [API Docs](http://localhost:8501/docs)
- **Email**: your-email@domain.com

---

⭐ **Nếu project hữu ích, hãy cho chúng tôi một star!** ⭐
