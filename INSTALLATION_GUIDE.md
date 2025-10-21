# 🚀 VNSTOCK 2.0 - Installation Guide

## 📋 Yêu cầu hệ thống

### **Tối thiểu:**
- **OS:** macOS 10.15+, Ubuntu 18.04+, Windows 10+
- **Python:** 3.8 hoặc cao hơn
- **RAM:** 4GB+
- **Disk:** 1GB+ free space
- **Internet:** Broadband connection

### **Khuyến nghị:**
- **OS:** macOS 12+, Ubuntu 20.04+, Windows 11
- **Python:** 3.10+
- **RAM:** 8GB+
- **Disk:** 2GB+ SSD
- **Internet:** Stable connection (for API calls)

---

## 🔧 CÀI ĐẶT CHI TIẾT

### **Option 1: Cài đặt từ GitHub (Khuyến nghị)**

#### **Bước 1: Clone Repository**

```bash
# Clone project
git clone https://github.com/nguyenhoang1221hoangnguyen/vnstock-data-collector.git

# Di chuyển vào thư mục
cd vnstock-data-collector
```

#### **Bước 2: Kiểm tra Python**

```bash
# Kiểm tra Python version
python3 --version

# Nếu < 3.8, cài đặt Python mới:
# macOS:
brew install python@3.10

# Ubuntu:
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip

# Windows:
# Download từ https://www.python.org/downloads/
```

#### **Bước 3: Tạo Virtual Environment**

```bash
# Tạo virtual environment
python3 -m venv venv

# Activate virtual environment

# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Kiểm tra (should show venv path)
which python
```

#### **Bước 4: Cài đặt Dependencies**

```bash
# Upgrade pip
pip install --upgrade pip

# Cài đặt packages
pip install -r requirements.txt

# Verify installation
pip list | grep vnstock
```

**Nếu gặp lỗi:**

```bash
# Lỗi: externally-managed-environment
# → Đảm bảo đang trong venv (xem Bước 3)

# Lỗi: No module named 'pip'
python3 -m ensurepip --upgrade

# Lỗi: version conflicts
pip install --upgrade --force-reinstall -r requirements.txt
```

#### **Bước 5: Kiểm tra cài đặt**

```bash
# Test import
python3 -c "from vnstock import Vnstock; print('✅ vnstock OK')"
python3 -c "from fastapi import FastAPI; print('✅ FastAPI OK')"
python3 -c "import streamlit; print('✅ Streamlit OK')"

# Run tests
python3 test_all_modules.py
```

---

### **Option 2: Cài đặt qua Docker (Recommended for Production)**

#### **Bước 1: Cài đặt Docker**

```bash
# macOS:
brew install --cask docker

# Ubuntu:
sudo apt install docker.io docker-compose

# Windows:
# Download Docker Desktop từ https://www.docker.com/products/docker-desktop
```

#### **Bước 2: Build & Run**

```bash
# Clone repository
git clone https://github.com/nguyenhoang1221hoangnguyen/vnstock-data-collector.git
cd vnstock-data-collector

# Build image
docker build -t vnstock:latest .

# Run container
docker run -d \
  --name vnstock-api \
  -p 8501:8501 \
  -p 8502:8502 \
  -p 8503:8503 \
  vnstock:latest

# Check logs
docker logs -f vnstock-api

# Access API
curl http://localhost:8501/health
```

#### **Bước 3: Docker Compose (Multi-service)**

```bash
# Run all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

### **Option 3: Manual Installation (Advanced)**

#### **Bước 1: Download Source**

```bash
# Download ZIP
wget https://github.com/nguyenhoang1221hoangnguyen/vnstock-data-collector/archive/refs/heads/main.zip

# Extract
unzip main.zip
cd vnstock-data-collector-main
```

#### **Bước 2: Install System Dependencies**

```bash
# macOS:
brew install python@3.10 sqlite3

# Ubuntu:
sudo apt install python3.10 python3.10-venv python3-pip sqlite3

# Windows:
# Install Python from python.org
# SQLite: https://www.sqlite.org/download.html
```

#### **Bước 3: Install Python Packages**

```bash
# Create venv
python3.10 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install
pip install vnstock>=1.0.0
pip install fastapi uvicorn[standard]
pip install pandas numpy
pip install streamlit plotly
pip install mplfinance matplotlib
pip install backtesting
pip install beautifulsoup4 requests
pip install pytest pytest-asyncio

# Verify
pip list
```

---

## ⚙️ CẤU HÌNH HỆ THỐNG

### **1. Database Configuration**

Database được tự động tạo khi chạy lần đầu:

```bash
# Database file sẽ được tạo tại:
./vnstock.db

# Để reset database:
rm vnstock.db
python3 -c "from database import get_db; get_db()"
```

### **2. Notification Configuration**

```bash
# Copy config template
cp notification_config_example.json notification_config.json

# Edit với credentials của bạn
nano notification_config.json
```

**notification_config.json:**
```json
{
  "enabled_channels": ["telegram"],
  "telegram": {
    "bot_token": "YOUR_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID"
  },
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your@email.com",
    "sender_password": "your_app_password",
    "receiver_email": "your@email.com"
  }
}
```

**Get Telegram credentials:**
```
1. Chat với @BotFather on Telegram
2. /newbot → Đặt tên bot
3. Copy Bot Token
4. Chat với @userinfobot để lấy Chat ID
```

### **3. Environment Variables (Optional)**

```bash
# Create .env file
cat > .env << EOF
VNSTOCK_API_PORT=8501
VNSTOCK_DB_PATH=./vnstock.db
VNSTOCK_LOG_LEVEL=INFO
EOF

# Load env vars
export $(cat .env | xargs)
```

---

## 🚀 KHỞI CHẠY HỆ THỐNG

### **1. Start API Server**

```bash
# Activate venv
source venv/bin/activate

# Start server
python3 main.py

# Server chạy tại:
# - API: http://localhost:8501
# - Docs: http://localhost:8501/docs
```

**Run in background (macOS/Linux):**
```bash
# Start
nohup python3 main.py > api.log 2>&1 &

# Check
ps aux | grep main.py

# Stop
pkill -f main.py
```

### **2. Start Basic Dashboard**

```bash
# Terminal mới
source venv/bin/activate
python3 start_dashboard.py

# Access: http://localhost:8502
```

### **3. Start Advanced Dashboard**

```bash
# Terminal mới
source venv/bin/activate
python3 start_dashboard_advanced.py

# Access: http://localhost:8503
```

### **4. Start All Services (Recommended)**

```bash
# Install tmux (optional but recommended)
brew install tmux  # macOS
sudo apt install tmux  # Ubuntu

# Create startup script
cat > start_all.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate

# Start API in background
python3 main.py > logs/api.log 2>&1 &
echo "✅ API started (port 8501)"

# Start Basic Dashboard
python3 start_dashboard.py > logs/dashboard.log 2>&1 &
echo "✅ Basic Dashboard started (port 8502)"

# Start Advanced Dashboard
python3 start_dashboard_advanced.py > logs/dashboard_advanced.log 2>&1 &
echo "✅ Advanced Dashboard started (port 8503)"

echo ""
echo "🎉 All services started!"
echo "API: http://localhost:8501/docs"
echo "Basic Dashboard: http://localhost:8502"
echo "Advanced Dashboard: http://localhost:8503"
EOF

chmod +x start_all.sh

# Run
./start_all.sh
```

### **5. Stop All Services**

```bash
# Create stop script
cat > stop_all.sh << 'EOF'
#!/bin/bash
pkill -f "python3 main.py"
pkill -f "streamlit run"
echo "✅ All services stopped"
EOF

chmod +x stop_all.sh

# Run
./stop_all.sh
```

---

## 🧪 KIỂM TRA HỆ THỐNG

### **Test Suite**

```bash
# Run all tests
python3 test_all_modules.py

# Expected output:
# ============================================================
# TEST SUMMARY
# ============================================================
# Database................................ ✅ PASSED
# Drawing Tools........................... ✅ PASSED
# Portfolio Manager....................... ✅ PASSED
# News & Sentiment........................ ✅ PASSED
# Notifications........................... ✅ PASSED
# Advanced Indicators..................... ✅ PASSED
#
# Total: 6/6 passed (100%)
# 🎉 ALL TESTS PASSED! 🎉
```

### **Test Individual Features**

```bash
# Test Blue-chip Detector
python3 test_bluechip_quick.py

# Test Stock Classifier
python3 test_classifier_quick.py

# Test API
curl http://localhost:8501/health
curl http://localhost:8501/stock/VCB/overview
```

---

## 🔧 TROUBLESHOOTING

### **Problem 1: Python version conflicts**

```bash
# Solution: Use python3 explicitly
python3 --version  # Check version
python3 -m venv venv  # Create venv with python3
```

### **Problem 2: ModuleNotFoundError**

```bash
# Solution: Install missing package
pip install <package-name>

# Or reinstall all
pip install -r requirements.txt
```

### **Problem 3: Port already in use**

```bash
# Check what's using the port
lsof -i :8501  # macOS/Linux
netstat -ano | findstr :8501  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or change port in main.py
```

### **Problem 4: Rate limit from VCI API**

```bash
# Solution: Increase delay between requests
# Edit stock_classifier.py:
# delay=3.0 → delay=5.0
```

### **Problem 5: Database locked**

```bash
# Solution: Close all connections and restart
rm vnstock.db
python3 -c "from database import get_db; get_db()"
```

### **Problem 6: Streamlit error**

```bash
# Solution: Clear Streamlit cache
rm -rf ~/.streamlit/cache

# Restart dashboard
python3 start_dashboard_advanced.py
```

---

## 📊 POST-INSTALLATION

### **1. Verify Installation**

```bash
# Check all endpoints
curl http://localhost:8501/health
curl http://localhost:8501/stock/VCB/overview
curl http://localhost:8501/bluechip/scan
curl http://localhost:8501/classify/stock/VCB

# Check dashboards
open http://localhost:8502  # macOS
open http://localhost:8503  # macOS
```

### **2. Setup n8n Integration**

```bash
# Get your local IP
ipconfig getifaddr en0  # macOS
hostname -I  # Linux

# Use this IP in n8n instead of localhost
# Example: http://192.168.1.4:8501
```

### **3. Setup Automated Scans (Cron)**

```bash
# Edit crontab
crontab -e

# Add jobs:
# Run bluechip scan every Sunday at 8AM
0 8 * * 0 cd /path/to/vnstock && source venv/bin/activate && python3 bluechip_detector.py --auto

# Run market classification every Monday at 8AM
0 8 * * 1 cd /path/to/vnstock && source venv/bin/activate && python3 stock_classifier.py 100
```

### **4. Setup Logging**

```bash
# Create logs directory
mkdir -p logs

# Edit logging config in Python files:
logging.basicConfig(
    level=logging.INFO,
    filename='logs/vnstock.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## 🔄 UPDATE & MAINTENANCE

### **Update to Latest Version**

```bash
# Pull latest changes
git pull origin main

# Update dependencies
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Restart services
./stop_all.sh
./start_all.sh
```

### **Backup Database**

```bash
# Backup
cp vnstock.db vnstock_backup_$(date +%Y%m%d).db

# Restore
cp vnstock_backup_20251021.db vnstock.db
```

### **Clean Up**

```bash
# Remove cache
rm -rf __pycache__
rm -rf .pytest_cache
rm -rf *.pyc

# Remove old CSVs
rm stock_classification_*.csv

# Remove old logs
rm logs/*.log
```

---

## 📚 NEXT STEPS

После cài đặt thành công:

1. ✅ **Đọc Documentation:**
   - README.md
   - QUICK_START.md
   - CLASSIFICATION_GUIDE.md
   - BLUECHIP_DETECTOR_GUIDE.md

2. ✅ **Try Examples:**
   ```bash
   # Scan market
   python3 stock_classifier.py 20
   
   # Detect blue-chips
   python3 bluechip_detector.py
   
   # Open dashboard
   open http://localhost:8503
   ```

3. ✅ **Setup Notifications:**
   - Configure Telegram/Email
   - Test alerts
   
4. ✅ **Integrate with n8n:**
   - Import workflow example
   - Test API calls

---

## 💡 TIPS

### **Performance Optimization:**

```bash
# Use SSD for database
# Increase memory allocation
# Use faster internet connection
# Reduce scan frequency
```

### **Security:**

```bash
# Don't expose API to internet without authentication
# Keep notification credentials secure
# Backup database regularly
# Use HTTPS in production
```

### **Best Practices:**

```bash
# Use virtual environment
# Keep dependencies updated
# Monitor logs regularly
# Test before deploying
# Document custom changes
```

---

## 📞 SUPPORT

**Issues:** https://github.com/nguyenhoang1221hoangnguyen/vnstock-data-collector/issues

**Email:** nguyenhoang1221hoangnguyen@gmail.com

**Documentation:** See all `*.md` files in project root

---

## ✅ CHECKLIST

Sau khi cài đặt, kiểm tra:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] All dependencies installed
- [ ] Database created (vnstock.db)
- [ ] API server running (port 8501)
- [ ] Dashboards accessible (8502, 8503)
- [ ] All tests passing (6/6)
- [ ] Notifications configured (optional)
- [ ] n8n integration tested (optional)

---

**🎉 Chúc mừng! VNStock 2.0 đã sẵn sàng sử dụng!**

*Version: 2.0*  
*Last Updated: 2025-10-21*

