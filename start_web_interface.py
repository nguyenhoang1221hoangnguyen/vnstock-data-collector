#!/usr/bin/env python3
"""
VNStock Data Collector - Web Interface Launcher
Script để khởi chạy giao diện web Streamlit
"""

import subprocess
import sys
import os
import time

def check_dependencies():
    """Kiểm tra các thư viện cần thiết"""
    required_packages = ['streamlit', 'plotly']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Thiếu các thư viện: {', '.join(missing_packages)}")
        print("🔧 Đang cài đặt...")
        
        for package in missing_packages:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        
        print("✅ Đã cài đặt xong các thư viện!")
    
    return len(missing_packages) == 0

def start_web_interface():
    """Khởi chạy giao diện web"""
    print("🚀 Đang khởi chạy VNStock Data Collector Web Interface...")
    print("📊 Giao diện web sẽ mở tại: http://localhost:8502")
    print("🔍 Đảm bảo API server đang chạy tại: http://localhost:8501")
    print("=" * 60)
    
    try:
        # Chạy Streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'web_interface.py',
            '--server.port=8502',
            '--server.address=0.0.0.0',
            '--browser.gatherUsageStats=false'
        ])
    except KeyboardInterrupt:
        print("\n👋 Đã dừng giao diện web!")
    except Exception as e:
        print(f"❌ Lỗi khi khởi chạy: {e}")

def main():
    """Hàm chính"""
    print("🎯 VNStock Data Collector - Web Interface")
    print("=" * 50)
    
    # Kiểm tra file web_interface.py
    if not os.path.exists('web_interface.py'):
        print("❌ Không tìm thấy file web_interface.py")
        return
    
    # Kiểm tra dependencies
    if not check_dependencies():
        print("❌ Không thể cài đặt dependencies")
        return
    
    # Khởi chạy
    start_web_interface()

if __name__ == "__main__":
    main()
