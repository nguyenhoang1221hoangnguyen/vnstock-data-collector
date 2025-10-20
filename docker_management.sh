#!/bin/bash

# VNStock Data Collector - Docker Management Script
# Script quản lý container Docker

case "$1" in
    "start")
        echo "🚀 Khởi chạy VNStock Data Collector..."
        docker-compose up -d
        echo "✅ Container đã khởi chạy"
        ;;
    "stop")
        echo "🛑 Dừng VNStock Data Collector..."
        docker-compose down
        echo "✅ Container đã dừng"
        ;;
    "restart")
        echo "🔄 Khởi động lại VNStock Data Collector..."
        docker-compose restart
        echo "✅ Container đã khởi động lại"
        ;;
    "status")
        echo "📊 Trạng thái VNStock Data Collector:"
        docker-compose ps
        echo ""
        echo "🏥 Health Check:"
        curl -s http://localhost:8501/health || echo "❌ API không phản hồi"
        ;;
    "logs")
        echo "📋 Logs VNStock Data Collector:"
        docker-compose logs -f
        ;;
    "build")
        echo "🔨 Build lại Docker image..."
        docker-compose build --no-cache
        echo "✅ Build hoàn tất"
        ;;
    "clean")
        echo "🧹 Dọn dẹp Docker..."
        docker-compose down
        docker system prune -f
        echo "✅ Dọn dẹp hoàn tất"
        ;;
    "test")
        echo "🧪 Test API endpoints:"
        echo "====================="
        echo "🏥 Health Check:"
        curl -s http://localhost:8501/health | jq . 2>/dev/null || curl -s http://localhost:8501/health
        echo ""
        echo "📖 API Info:"
        curl -s http://localhost:8501/ | jq . 2>/dev/null || curl -s http://localhost:8501/
        echo ""
        echo "📊 Test với mã VIC:"
        curl -s "http://localhost:8501/stock/VIC/overview" | jq . 2>/dev/null || curl -s "http://localhost:8501/stock/VIC/overview"
        ;;
    *)
        echo "🐳 VNStock Data Collector - Docker Management"
        echo "============================================="
        echo ""
        echo "📋 Các lệnh có sẵn:"
        echo "  start    - Khởi chạy container"
        echo "  stop     - Dừng container"
        echo "  restart  - Khởi động lại container"
        echo "  status   - Xem trạng thái container"
        echo "  logs     - Xem logs real-time"
        echo "  build    - Build lại Docker image"
        echo "  clean    - Dọn dẹp Docker"
        echo "  test     - Test API endpoints"
        echo ""
        echo "💡 Ví dụ sử dụng:"
        echo "  ./docker_management.sh start"
        echo "  ./docker_management.sh status"
        echo "  ./docker_management.sh logs"
        ;;
esac
