#!/usr/bin/env python3
"""
Test vnstock API mới
"""

try:
    from vnstock import Vnstock
    
    # Khởi tạo vnstock client
    stock = Vnstock().stock(symbol='VIC', source='VCI')
    
    print("🧪 Testing new vnstock API:")
    
    # Test quote data
    try:
        quote = stock.quote.history(start='2024-01-01', end='2024-01-10')
        print(f"✅ quote.history(): {len(quote)} records")
        print(f"   Columns: {list(quote.columns)}")
    except Exception as e:
        print(f"❌ quote.history(): {str(e)}")
    
    # Test company profile
    try:
        profile = stock.company.profile()
        print(f"✅ company.profile(): Data retrieved")
        print(f"   Columns: {list(profile.columns) if hasattr(profile, 'columns') else 'Not a DataFrame'}")
    except Exception as e:
        print(f"❌ company.profile(): {str(e)}")
    
    # Test financial data
    try:
        finance = stock.finance.balance_sheet(period='quarterly', lang='vi')
        print(f"✅ finance.balance_sheet(): {len(finance)} records")
    except Exception as e:
        print(f"❌ finance.balance_sheet(): {str(e)}")
    
    # Test listing
    try:
        from vnstock import Listing
        listing = Listing().companies()
        print(f"✅ Listing().companies(): {len(listing)} companies")
    except Exception as e:
        print(f"❌ Listing().companies(): {str(e)}")

except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
