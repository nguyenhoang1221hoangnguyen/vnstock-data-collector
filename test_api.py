#!/usr/bin/env python3
"""
Script test API VNStock Data Collector
"""

import requests
import json
from datetime import datetime, timedelta

def test_api():
    """Test các endpoint của API"""
    base_url = "http://localhost:8501"
    test_symbol = "VIC"  # Mã cổ phiếu test
    
    print("🧪 Bắt đầu test API VNStock Data Collector")
    print("=" * 50)
    
    # Test 1: Health check
    print("1️⃣ Test Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check: OK")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
    
    print()
    
    # Test 2: Root endpoint
    print("2️⃣ Test Root Endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint: OK")
            data = response.json()
            print(f"   API Version: {data.get('version')}")
            print(f"   Available endpoints: {len(data.get('endpoints', {}))}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {str(e)}")
    
    print()
    
    # Test 3: Stock overview
    print(f"3️⃣ Test Stock Overview ({test_symbol})...")
    try:
        response = requests.get(f"{base_url}/stock/{test_symbol}/overview")
        if response.status_code == 200:
            print("✅ Stock overview: OK")
            data = response.json()
            if data.get('success'):
                print(f"   Symbol: {data['data'].get('symbol')}")
                print(f"   Data collection time: {data['data'].get('data_collection_time')}")
            else:
                print(f"   Error in response: {data.get('error')}")
        else:
            print(f"❌ Stock overview failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Stock overview error: {str(e)}")
    
    print()
    
    # Test 4: Historical data (last 30 days)
    print(f"4️⃣ Test Historical Data ({test_symbol}, last 30 days)...")
    try:
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        response = requests.get(
            f"{base_url}/stock/{test_symbol}/historical",
            params={"start_date": start_date, "end_date": end_date}
        )
        
        if response.status_code == 200:
            print("✅ Historical data: OK")
            data = response.json()
            if data.get('success'):
                historical_data = data['data']
                daily_data = historical_data.get('daily_data', [])
                print(f"   Period: {historical_data.get('period', {}).get('start_date')} to {historical_data.get('period', {}).get('end_date')}")
                print(f"   Daily records: {len(daily_data)}")
                print(f"   Weekly records: {len(historical_data.get('weekly_data', []))}")
                print(f"   Monthly records: {len(historical_data.get('monthly_data', []))}")
            else:
                print(f"   Error in response: {data.get('error')}")
        else:
            print(f"❌ Historical data failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Historical data error: {str(e)}")
    
    print()
    
    # Test 5: Complete stock data (POST)
    print(f"5️⃣ Test Complete Stock Data via POST ({test_symbol})...")
    try:
        payload = {
            "symbol": test_symbol,
            "start_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "end_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        response = requests.post(
            f"{base_url}/stock/batch",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Complete stock data (POST): OK")
            data = response.json()
            if data.get('success'):
                stock_data = data['data']
                print(f"   Symbol: {stock_data.get('request_info', {}).get('symbol')}")
                print(f"   Data source: {stock_data.get('request_info', {}).get('data_source')}")
                
                # Check data completeness
                completeness = stock_data.get('ai_analysis_metadata', {}).get('data_completeness', {})
                print(f"   Data completeness:")
                for key, value in completeness.items():
                    status = "✅" if value else "❌"
                    print(f"     {status} {key}: {value}")
                
                # Analysis suggestions
                suggestions = stock_data.get('ai_analysis_metadata', {}).get('analysis_suggestions', [])
                print(f"   AI Analysis suggestions: {len(suggestions)} items")
                
            else:
                print(f"   Error in response: {data.get('error')}")
        else:
            print(f"❌ Complete stock data failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Complete stock data error: {str(e)}")
    
    print()
    print("🏁 Test hoàn thành!")
    print("=" * 50)
    print("💡 Để test thêm:")
    print(f"   - Truy cập {base_url}/docs để xem Swagger UI")
    print(f"   - Test với các mã cổ phiếu khác: VCB, FPT, HPG, etc.")
    print(f"   - Test với khoảng thời gian dài hơn")

if __name__ == "__main__":
    test_api()
