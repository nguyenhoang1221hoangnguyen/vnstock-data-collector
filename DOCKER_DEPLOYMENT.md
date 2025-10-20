# 🐳 Docker Deployment Guide - VNStock Data Collector

Hướng dẫn chi tiết deploy ứng dụng VNStock Data Collector lên Docker Desktop.

## 📋 Yêu cầu hệ thống

### ✅ **Docker Desktop**
- **Windows**: Docker Desktop for Windows
- **macOS**: Docker Desktop for Mac  
- **Linux**: Docker Engine + Docker Compose

### 🔗 **Download Docker Desktop**
- **Windows**: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
- **macOS**: https://desktop.docker.com/mac/main/amd64/Docker.dmg
- **Linux**: https://docs.docker.com/engine/install/

## 🚀 Cách 1: Deploy tự động (Khuyến nghị)

### 1. **Chuẩn bị**
```bash
# Đảm bảo Docker Desktop đang chạy
# Mở Terminal/Command Prompt trong thư mục project
```

### 2. **Chạy script deploy**
```bash
# Cấp quyền thực thi
chmod +x deploy_docker.sh

# Chạy deploy
./deploy_docker.sh
```

### 3. **Kiểm tra kết quả**
- ✅ Container sẽ tự động build và khởi chạy
- ✅ API sẽ có sẵn tại: http://localhost:8501
- ✅ Health check sẽ được thực hiện tự động

## 🔧 Cách 2: Deploy thủ công

### 1. **Build Docker image**
```bash
docker-compose build --no-cache
```

### 2. **Khởi chạy container**
```bash
docker-compose up -d
```

### 3. **Kiểm tra trạng thái**
```bash
docker-compose ps
```

## 📊 Quản lý Container

### 🎮 **Sử dụng script quản lý**
```bash
# Cấp quyền thực thi
chmod +x docker_management.sh

# Các lệnh có sẵn
./docker_management.sh start     # Khởi chạy
./docker_management.sh stop      # Dừng
./docker_management.sh restart   # Khởi động lại
./docker_management.sh status    # Xem trạng thái
./docker_management.sh logs      # Xem logs
./docker_management.sh test      # Test API
./docker_management.sh clean     # Dọn dẹp
```

### 🔧 **Lệnh Docker thủ công**
```bash
# Xem logs
docker-compose logs -f

# Dừng container
docker-compose down

# Khởi động lại
docker-compose restart

# Xem trạng thái
docker-compose ps

# Dọn dẹp
docker system prune -f
```

## 🧪 Test API

### 1. **Health Check**
```bash
curl http://localhost:8501/health
```

### 2. **API Documentation**
Mở trình duyệt: http://localhost:8501/docs

### 3. **Test với mã cổ phiếu**
```bash
# Lấy thông tin VIC
curl "http://localhost:8501/stock/VIC/overview"

# Lấy dữ liệu lịch sử
curl "http://localhost:8501/stock/VIC/historical?start_date=2024-01-01&end_date=2024-01-31"
```

## 🌐 Tích hợp với n8n

### **Cấu hình HTTP Request Node**
- **URL**: `http://localhost:8501/stock/batch`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:
```json
{
  "symbol": "VIC",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

## 📁 Cấu trúc Docker

### **Dockerfile**
- Base image: Python 3.11-slim
- Port: 8501
- Health check: Tự động
- User: Non-root (bảo mật)

### **docker-compose.yml**
- Service: vnstock-collector
- Network: vnstock-network
- Volumes: ./logs:/app/logs
- Restart: unless-stopped

## 🔍 Troubleshooting

### ❌ **Container không khởi động**
```bash
# Kiểm tra logs
docker-compose logs

# Kiểm tra Docker Desktop
docker info
```

### ❌ **API không phản hồi**
```bash
# Kiểm tra port
netstat -an | grep 8501

# Restart container
docker-compose restart
```

### ❌ **Lỗi build**
```bash
# Clean build
docker-compose down
docker system prune -f
docker-compose build --no-cache
```

## 📊 Monitoring

### **Health Check**
- URL: http://localhost:8501/health
- Interval: 30s
- Timeout: 30s
- Retries: 3

### **Logs**
```bash
# Xem logs real-time
docker-compose logs -f

# Xem logs của service cụ thể
docker-compose logs vnstock-collector
```

## 🎯 Production Deployment

### **Cấu hình Production**
1. **Thay đổi port** trong docker-compose.yml
2. **Thêm reverse proxy** (nginx)
3. **Cấu hình SSL/TLS**
4. **Setup monitoring** (Prometheus/Grafana)
5. **Backup logs** định kỳ

### **Security**
- ✅ Non-root user
- ✅ Health checks
- ✅ Resource limits
- ✅ Network isolation

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra Docker Desktop đang chạy
2. Xem logs: `docker-compose logs`
3. Test health check: `curl http://localhost:8501/health`
4. Restart container: `docker-compose restart`

---

🎉 **Chúc mừng!** VNStock Data Collector đã sẵn sàng trên Docker Desktop!
