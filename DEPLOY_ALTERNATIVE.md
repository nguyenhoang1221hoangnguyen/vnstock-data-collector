# 🚀 Alternative Deployment Guide - VNStock Data Collector

Do Docker Hub đang gặp sự cố (503 Service Unavailable), đây là các cách deploy thay thế:

## 🔧 Cách 1: Deploy Local (Khuyến nghị khi Docker Hub gặp sự cố)

### **Chạy trực tiếp với Python**
```bash
# 1. Tạo virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# hoặc
venv\Scripts\activate     # Windows

# 2. Cài đặt dependencies
pip install -r requirements.txt

# 3. Chạy ứng dụng
python start_server.py
```

### **Kết quả**
- ✅ API sẽ chạy tại: http://localhost:8501
- ✅ Documentation: http://localhost:8501/docs
- ✅ Health Check: http://localhost:8501/health

## 🐳 Cách 2: Docker với Image có sẵn

### **Sử dụng Python image có sẵn**
```bash
# Kiểm tra images có sẵn
docker images | grep python

# Nếu có python image, sửa Dockerfile
# Thay FROM python:3.11-slim thành FROM python:3.9-slim (hoặc version có sẵn)
```

### **Build với image local**
```bash
# Build với image có sẵn
docker build -t vnstock-collector .
docker run -d -p 8501:8501 --name vnstock-data-collector vnstock-collector
```

## 🌐 Cách 3: Deploy lên Cloud

### **Railway.app**
```bash
# 1. Tạo tài khoản Railway
# 2. Connect GitHub repository
# 3. Deploy tự động
```

### **Heroku**
```bash
# 1. Tạo Procfile
echo "web: python start_server.py" > Procfile

# 2. Deploy
heroku create vnstock-collector
git push heroku main
```

### **DigitalOcean App Platform**
```bash
# 1. Tạo app từ GitHub
# 2. Cấu hình build command: pip install -r requirements.txt
# 3. Cấu hình run command: python start_server.py
```

## 🔄 Cách 4: Chờ Docker Hub khôi phục

### **Kiểm tra trạng thái Docker Hub**
```bash
# Kiểm tra kết nối
curl -I https://hub.docker.com

# Thử lại sau 15-30 phút
docker pull python:3.11-slim
```

### **Khi Docker Hub hoạt động trở lại**
```bash
# Chạy script deploy
./deploy_docker.sh
```

## 🧪 Test Local Deployment

### **1. Khởi chạy local**
```bash
cd "/Users/nguyenhoang/Desktop/2025/hoc-tap code/vscode/VNSTOCK 2"
source venv/bin/activate
python start_server.py
```

### **2. Test API**
```bash
# Health check
curl http://localhost:8501/health

# API info
curl http://localhost:8501/

# Test với VIC
curl "http://localhost:8501/stock/VIC/overview"
```

### **3. Tích hợp n8n**
- **URL**: `http://localhost:8501/stock/batch`
- **Method**: `POST`
- **Body**: `{"symbol": "VIC"}`

## 📊 Monitoring Local

### **Logs**
```bash
# Xem logs real-time
tail -f logs/app.log

# Hoặc xem trong terminal khi chạy
python start_server.py
```

### **Process Management**
```bash
# Tìm process
ps aux | grep python

# Kill process
pkill -f start_server.py
```

## 🎯 Khuyến nghị

### **Hiện tại (Docker Hub gặp sự cố)**
1. ✅ **Sử dụng Local Deployment** - Nhanh nhất
2. ✅ **Test đầy đủ chức năng**
3. ✅ **Tích hợp với n8n**

### **Khi Docker Hub khôi phục**
1. ✅ **Chuyển sang Docker** - Dễ quản lý
2. ✅ **Production deployment**
3. ✅ **Scaling và monitoring**

## 🆘 Troubleshooting

### **Port 8501 đã được sử dụng**
```bash
# Tìm process sử dụng port
lsof -i :8501

# Kill process
kill -9 <PID>
```

### **Dependencies lỗi**
```bash
# Cài đặt lại
pip install --upgrade -r requirements.txt
```

### **vnstock API lỗi**
```bash
# Cập nhật vnstock
pip install --upgrade vnstock
```

---

🎉 **Kết luận**: Sử dụng Local Deployment để tiếp tục phát triển, chuyển sang Docker khi Docker Hub khôi phục!
