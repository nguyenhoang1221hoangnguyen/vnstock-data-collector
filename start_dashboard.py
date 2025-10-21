#!/usr/bin/env python3
"""
Script khởi chạy VNStock Dashboard
"""

import os
import sys
import subprocess

def main():
    """Khởi chạy Streamlit dashboard"""
    
    print("=" * 60)
    print("🚀 Đang khởi chạy VNStock Dashboard...")
    print("=" * 60)
    print()
    print("📊 Dashboard sẽ chạy tại: http://localhost:8502")
    print("🔗 Hoặc truy cập: http://192.168.1.4:8502 (từ máy khác trong mạng)")
    print()
    print("💡 Tips:")
    print("   - Nhấn Ctrl+C để dừng dashboard")
    print("   - Dashboard sẽ tự động reload khi bạn thay đổi code")
    print()
    print("=" * 60)
    print()
    
    try:
        # Chạy streamlit
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "dashboard.py",
            "--server.port=8502",
            "--server.address=0.0.0.0",
            "--browser.serverAddress=localhost",
            "--server.headless=true"
        ])
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard đã dừng")
    except Exception as e:
        print(f"\n❌ Lỗi khi khởi chạy dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

