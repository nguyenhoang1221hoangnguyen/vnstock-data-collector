#!/usr/bin/env python3
"""
Script khởi chạy VNStock Advanced Dashboard
Dashboard nâng cao với: Technical Indicators, Multi-Stock Comparison, FA/TA Analysis, Watchlist, Alerts
"""

import os
import sys
import subprocess

def main():
    """Khởi chạy Streamlit advanced dashboard"""
    
    print("=" * 70)
    print("🚀 Đang khởi chạy VNStock Advanced Dashboard...")
    print("=" * 70)
    print()
    print("📊 Dashboard sẽ chạy tại: http://localhost:8503")
    print("🔗 Hoặc truy cập: http://192.168.1.4:8503 (từ máy khác trong mạng)")
    print()
    print("✨ Tính năng:")
    print("   • Technical Indicators (MA, RSI, MACD, BB)")
    print("   • Multi-Stock Comparison")
    print("   • FA/TA Analysis Integration")
    print("   • Personal Watchlist")
    print("   • Price Alerts")
    print()
    print("💡 Tips:")
    print("   - Nhấn Ctrl+C để dừng dashboard")
    print("   - Dashboard sẽ tự động reload khi bạn thay đổi code")
    print("   - Đảm bảo API server đang chạy (port 8501) cho FA/TA features")
    print()
    print("=" * 70)
    print()
    
    try:
        # Chạy streamlit
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "dashboard_advanced.py",
            "--server.port=8503",
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

