#!/usr/bin/env python3
"""
Script khởi chạy server VNStock Data Collector
"""

import uvicorn
import sys
import os
from pathlib import Path

def main():
    """Khởi chạy server"""
    print("🚀 Đang khởi chạy VNStock Data Collector API...")
    print("📊 Server sẽ chạy tại: http://localhost:8501")
    print("📖 API Documentation: http://localhost:8501/docs")
    print("🔍 Health Check: http://localhost:8501/health")
    print("=" * 50)
    
    try:
        # Chạy server với uvicorn
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8501,
            reload=True,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n⏹️  Server đã được dừng bởi người dùng")
    except Exception as e:
        print(f"❌ Lỗi khi khởi chạy server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
