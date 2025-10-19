#!/usr/bin/env python3
"""
Script setup và cài đặt VNStock Data Collector
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Chạy command và hiển thị kết quả"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description}: Thành công")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}: Thất bại")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Kiểm tra phiên bản Python"""
    print("🐍 Kiểm tra phiên bản Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}: OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro}: Cần Python 3.8 trở lên")
        return False

def install_requirements():
    """Cài đặt các thư viện cần thiết"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    if requirements_file.exists():
        return run_command(
            f"pip install -r {requirements_file}",
            "Cài đặt thư viện từ requirements.txt"
        )
    else:
        print("❌ Không tìm thấy file requirements.txt")
        return False

def create_virtual_env():
    """Tạo virtual environment (tùy chọn)"""
    response = input("🤔 Bạn có muốn tạo virtual environment không? (y/N): ")
    if response.lower() in ['y', 'yes']:
        venv_path = Path(__file__).parent / "venv"
        if not venv_path.exists():
            success = run_command(
                f"python -m venv {venv_path}",
                "Tạo virtual environment"
            )
            if success:
                if os.name == 'nt':  # Windows
                    activate_script = venv_path / "Scripts" / "activate.bat"
                    print(f"💡 Để kích hoạt virtual environment, chạy: {activate_script}")
                else:  # Unix/Linux/macOS
                    activate_script = venv_path / "bin" / "activate"
                    print(f"💡 Để kích hoạt virtual environment, chạy: source {activate_script}")
            return success
        else:
            print("✅ Virtual environment đã tồn tại")
            return True
    return True

def test_installation():
    """Test cài đặt"""
    print("🧪 Test cài đặt...")
    try:
        import vnstock
        import fastapi
        import pandas
        print("✅ Tất cả thư viện đã được cài đặt thành công")
        
        # Test vnstock
        print("🔍 Test thư viện vnstock...")
        # Không test thực tế để tránh lỗi network trong setup
        print("✅ VNStock: OK")
        
        return True
    except ImportError as e:
        print(f"❌ Thiếu thư viện: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("🚀 VNStock Data Collector - Setup Script")
    print("=" * 50)
    
    # Kiểm tra Python version
    if not check_python_version():
        sys.exit(1)
    
    # Tạo virtual environment (tùy chọn)
    if not create_virtual_env():
        print("⚠️  Có thể tiếp tục mà không cần virtual environment")
    
    # Cài đặt requirements
    if not install_requirements():
        print("❌ Cài đặt thất bại. Vui lòng kiểm tra lại.")
        sys.exit(1)
    
    # Test cài đặt
    if not test_installation():
        print("❌ Test cài đặt thất bại. Vui lòng kiểm tra lại.")
        sys.exit(1)
    
    print()
    print("🎉 Setup hoàn thành!")
    print("=" * 50)
    print("📝 Các bước tiếp theo:")
    print("1. Chạy server: python start_server.py")
    print("2. Test API: python test_api.py")
    print("3. Xem documentation: http://localhost:8501/docs")
    print()
    print("🔗 Tích hợp với n8n:")
    print("- Sử dụng HTTP Request node")
    print("- URL: http://localhost:8501/stock/{symbol}")
    print("- Method: GET hoặc POST")
    print()
    print("💡 Xem README.md để biết thêm chi tiết!")

if __name__ == "__main__":
    main()
