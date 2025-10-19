#!/usr/bin/env python3
"""
Script kiểm tra API của vnstock
"""

try:
    import vnstock
    print("✅ vnstock imported successfully")
    print(f"📦 vnstock version: {vnstock.__version__ if hasattr(vnstock, '__version__') else 'unknown'}")
    print()
    
    # Liệt kê các hàm có sẵn
    print("🔍 Available functions in vnstock:")
    functions = [attr for attr in dir(vnstock) if not attr.startswith('_')]
    for func in sorted(functions):
        print(f"  - {func}")
    print()
    
    # Test một số hàm cơ bản
    print("🧪 Testing basic functions:")
    
    # Test listing
    try:
        listing = vnstock.listing_companies()
        print(f"✅ listing_companies(): {len(listing)} companies found")
    except Exception as e:
        print(f"❌ listing_companies(): {str(e)}")
    
    # Test stock data
    try:
        from datetime import datetime, timedelta
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        data = vnstock.stock_historical_data("VIC", start_date, end_date)
        print(f"✅ stock_historical_data(): {len(data)} records found")
    except Exception as e:
        print(f"❌ stock_historical_data(): {str(e)}")
    
    # Test company info
    try:
        info = vnstock.company_profile("VIC")
        print(f"✅ company_profile(): Data retrieved")
    except Exception as e:
        print(f"❌ company_profile(): {str(e)}")
        
    # Test financial data
    try:
        financial = vnstock.financial_report("VIC", "BalanceSheet", "Quarterly")
        print(f"✅ financial_report(): {len(financial)} records found")
    except Exception as e:
        print(f"❌ financial_report(): {str(e)}")

except ImportError as e:
    print(f"❌ Cannot import vnstock: {str(e)}")
except Exception as e:
    print(f"❌ Error: {str(e)}")
