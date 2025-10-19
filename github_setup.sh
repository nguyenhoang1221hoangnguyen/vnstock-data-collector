#!/bin/bash

# GitHub Setup Script for VNStock Data Collector
echo "🚀 GitHub Setup for VNStock Data Collector"
echo "=========================================="

# Kiểm tra Git config
echo "📧 Git configuration:"
echo "Email: $(git config user.email)"
echo "Name: $(git config user.name)"
echo ""

# Hướng dẫn tìm username
echo "🔍 Để tìm GitHub username của bạn:"
echo "1. Truy cập https://github.com và đăng nhập"
echo "2. Click vào avatar ở góc phải trên"
echo "3. Username sẽ hiển thị dưới tên (ví dụ: @your-username)"
echo "4. Hoặc xem trong URL: https://github.com/YOUR_USERNAME"
echo ""

# Yêu cầu nhập username
read -p "🔗 Nhập GitHub username của bạn (không có @): " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Vui lòng nhập username!"
    exit 1
fi

echo ""
echo "📊 Sẽ tạo repository: https://github.com/$GITHUB_USERNAME/vnstock-data-collector"
echo ""

# Kiểm tra xem đã có remote chưa
if git remote get-url origin 2>/dev/null; then
    echo "⚠️  Remote origin đã tồn tại. Xóa và tạo mới..."
    git remote remove origin
fi

# Thêm remote
echo "🔗 Thêm remote origin..."
git remote add origin "https://github.com/$GITHUB_USERNAME/vnstock-data-collector.git"

echo "✅ Remote đã được thêm!"
echo ""

# Hiển thị hướng dẫn tiếp theo
echo "📋 Các bước tiếp theo:"
echo "1. Tạo repository 'vnstock-data-collector' trên GitHub"
echo "2. Chạy lệnh: git push -u origin main"
echo ""

echo "📝 Repository info để thêm trên GitHub:"
echo "Name: vnstock-data-collector"
echo "Description: 🇻🇳 Professional Vietnam Stock Data Collector API - 15+ years historical data, n8n integration, AI-optimized"
echo "Topics: vietnam, stock, api, n8n, ai, fastapi, vnstock, financial-data, python, docker"
echo ""

# Tự động push nếu user đồng ý
read -p "🚀 Bạn đã tạo repository trên GitHub chưa? (y/N): " CREATE_REPO

if [[ $CREATE_REPO =~ ^[Yy]$ ]]; then
    echo "📤 Đang push lên GitHub..."
    if git push -u origin main; then
        echo ""
        echo "🎉 Upload thành công!"
        echo "🔗 Repository: https://github.com/$GITHUB_USERNAME/vnstock-data-collector"
        echo ""
        echo "⭐ Đừng quên:"
        echo "- Thêm description và topics"
        echo "- Enable Issues và Discussions"
        echo "- Star repository của bạn!"
    else
        echo ""
        echo "❌ Push thất bại. Kiểm tra:"
        echo "1. Repository đã được tạo trên GitHub chưa?"
        echo "2. Bạn có quyền push không?"
        echo "3. Username có đúng không?"
    fi
else
    echo ""
    echo "📋 Để push sau khi tạo repository:"
    echo "git push -u origin main"
fi

echo ""
echo "🎯 Repository URL: https://github.com/$GITHUB_USERNAME/vnstock-data-collector"
