#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VNStock Data Collector - Web Interface Launcher
Script khởi chạy giao diện web
"""

import uvicorn
import sys
import os

def main():
    print("🚀 Đang khởi chạy VNStock Web Interface...")
    print("📊 Giao diện web sẽ chạy tại: http://localhost:8502")
    print("🔍 API Documentation: http://localhost:8502/docs")
    print("🏠 Trang chủ: http://localhost:8502")
    print("=" * 60)
    print("✨ Tính năng:")
    print("   • Tìm kiếm thông minh với gợi ý")
    print("   • Hiển thị đầy đủ thông tin tài chính")
    print("   • Giao diện đẹp mắt, thân thiện")
    print("   • Đơn vị tiền tệ VND")
    print("   • Responsive design")
    print("=" * 60)
    
    try:
        uvicorn.run(
            "web_interface:app",
            host="0.0.0.0",
            port=8502,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Đã dừng VNStock Web Interface!")
    except Exception as e:
        print(f"❌ Lỗi khởi chạy: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
