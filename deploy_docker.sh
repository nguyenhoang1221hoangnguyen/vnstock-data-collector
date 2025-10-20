#!/bin/bash

# VNStock Data Collector - Docker Deployment Script
# Script tự động deploy ứng dụng lên Docker Desktop

echo "🐳 VNStock Data Collector - Docker Deployment"
echo "=============================================="
echo ""

# Kiểm tra Docker Desktop
echo "🔍 Kiểm tra Docker Desktop..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker chưa được cài đặt hoặc không có trong PATH"
    echo "📥 Vui lòng cài đặt Docker Desktop từ: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Docker Desktop chưa chạy"
    echo "🚀 Vui lòng khởi động Docker Desktop và thử lại"
    exit 1
fi

echo "✅ Docker Desktop đang chạy"
echo ""

# Kiểm tra Docker Compose
echo "🔍 Kiểm tra Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose chưa được cài đặt"
    echo "📥 Vui lòng cài đặt Docker Compose"
    exit 1
fi

echo "✅ Docker Compose có sẵn"
echo ""

# Dừng container cũ nếu có
echo "🛑 Dừng container cũ (nếu có)..."
docker-compose down 2>/dev/null || true
docker stop vnstock-data-collector 2>/dev/null || true
docker rm vnstock-data-collector 2>/dev/null || true
echo "✅ Đã dọn dẹp container cũ"
echo ""

# Build Docker image
echo "🔨 Building Docker image..."
docker-compose build --no-cache
if [ $? -ne 0 ]; then
    echo "❌ Lỗi khi build Docker image"
    exit 1
fi
echo "✅ Build Docker image thành công"
echo ""

# Tạo thư mục logs
echo "📁 Tạo thư mục logs..."
mkdir -p logs
echo "✅ Thư mục logs đã sẵn sàng"
echo ""

# Khởi chạy container
echo "🚀 Khởi chạy VNStock Data Collector..."
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "❌ Lỗi khi khởi chạy container"
    exit 1
fi
echo "✅ Container đã khởi chạy thành công"
echo ""

# Kiểm tra trạng thái
echo "⏳ Đợi container khởi động hoàn toàn..."
sleep 10

echo "🔍 Kiểm tra trạng thái container..."
docker-compose ps

echo ""
echo "🏥 Kiểm tra health check..."
for i in {1..10}; do
    if curl -f http://localhost:8501/health &>/dev/null; then
        echo "✅ API đã sẵn sàng!"
        break
    else
        echo "⏳ Đang đợi API khởi động... ($i/10)"
        sleep 5
    fi
done

echo ""
echo "📊 Thông tin deployment:"
echo "========================="
echo "🌐 API URL: http://localhost:8501"
echo "📖 API Documentation: http://localhost:8501/docs"
echo "🏥 Health Check: http://localhost:8501/health"
echo "📋 Container Name: vnstock-data-collector"
echo "🔧 Network: vnstock-network"
echo ""

echo "🧪 Test API..."
echo "curl http://localhost:8501/health"
curl -s http://localhost:8501/health | head -3

echo ""
echo "📝 Các lệnh quản lý:"
echo "===================="
echo "📊 Xem logs: docker-compose logs -f"
echo "🛑 Dừng: docker-compose down"
echo "🔄 Restart: docker-compose restart"
echo "📈 Status: docker-compose ps"
echo "🧹 Clean up: docker system prune -f"
echo ""

echo "🎉 Deployment hoàn tất!"
echo "🚀 VNStock Data Collector đã sẵn sàng sử dụng!"
