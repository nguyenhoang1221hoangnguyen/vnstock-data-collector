# -*- coding: utf-8 -*-
"""
Quick Test for Stock Classifier - Test với 5 mã
"""

from stock_classifier import StockClassifier
import time

def test_single_classification():
    """Test phân loại 1 mã"""
    print("\n🧪 TEST 1: Single Stock Classification")
    print("=" * 60)
    
    classifier = StockClassifier()
    symbol = 'VCB'
    
    print(f"\nClassifying {symbol}...")
    result = classifier.classify_stock(symbol)
    
    if 'error' in result and result['error']:
        print(f"❌ Error: {result['error']}")
        return
    
    print(f"\n✅ {symbol} Classification:")
    print(f"  Overall Rating: {result['overall_rating']['rating']}")
    print(f"  Overall Score: {result['overall_rating']['score']}")
    print(f"  Recommendation: {result['overall_rating']['recommendation']}")
    
    print(f"\n  📈 Growth: {result['classifications']['growth']['category']}")
    print(f"     {result['classifications']['growth']['description']}")
    
    print(f"\n  ⚠️  Risk: {result['classifications']['risk']['category']}")
    print(f"     {result['classifications']['risk']['description']}")
    
    print(f"\n  💰 Market Cap: {result['classifications']['market_cap']['category']}")
    print(f"     {result['classifications']['market_cap']['description']}")
    
    print(f"\n  📊 Momentum: {result['classifications']['momentum']['category']}")
    print(f"     {result['classifications']['momentum']['description']}")


def test_market_scan():
    """Test quét thị trường"""
    print("\n\n🧪 TEST 2: Market Scan (5 stocks)")
    print("=" * 60)
    
    classifier = StockClassifier()
    
    # Test với 5 mã
    test_symbols = ['VCB', 'TCB', 'FPT', 'VNM', 'HPG']
    
    results = []
    for i, symbol in enumerate(test_symbols, 1):
        print(f"\n[{i}/5] Testing {symbol}...", end=' ')
        
        result = classifier.classify_stock(symbol)
        
        if 'error' not in result or result['error'] is None:
            results.append(result)
            rating = result['overall_rating']['rating']
            score = result['overall_rating']['score']
            print(f"✅ {rating} ({score})")
        else:
            print(f"❌ Error")
        
        # Delay
        if i < len(test_symbols):
            time.sleep(3)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    if results:
        print(f"\nSuccessfully classified: {len(results)}/5")
        
        print("\n📈 Rankings:")
        sorted_results = sorted(results, key=lambda x: x['overall_rating']['score'], reverse=True)
        
        for i, r in enumerate(sorted_results, 1):
            symbol = r['symbol']
            rating = r['overall_rating']['rating']
            score = r['overall_rating']['score']
            growth = r['classifications']['growth']['category']
            risk = r['classifications']['risk']['category']
            
            print(f"  {i}. {symbol:6} - {rating:3} ({score:.2f}) - {growth} / {risk}")
    else:
        print("\n❌ No stocks classified successfully")


def test_filters():
    """Test filtering"""
    print("\n\n🧪 TEST 3: Filter Test")
    print("=" * 60)
    
    from stock_classifier import scan_market
    
    print("\nScanning 10 stocks from HOSE...")
    df = scan_market(exchanges=['HOSE'], limit=10)
    
    if df.empty:
        print("❌ No data to filter")
        return
    
    print(f"\n✅ Got {len(df)} stocks")
    
    # Test filters
    classifier = StockClassifier()
    
    print("\n🔍 Filter: High Growth")
    high_growth = classifier.get_stocks_by_filter(df, growth='high_growth')
    print(f"   Found: {len(high_growth)} stocks")
    if not high_growth.empty:
        print(f"   Symbols: {', '.join(high_growth['symbol'].tolist())}")
    
    print("\n🔍 Filter: Low Risk")
    low_risk = classifier.get_stocks_by_filter(df, risk='low_risk')
    print(f"   Found: {len(low_risk)} stocks")
    if not low_risk.empty:
        print(f"   Symbols: {', '.join(low_risk['symbol'].tolist())}")
    
    print("\n🔍 Filter: A+ Rating")
    a_plus = classifier.get_stocks_by_filter(df, rating='A+')
    print(f"   Found: {len(a_plus)} stocks")
    if not a_plus.empty:
        print(f"   Symbols: {', '.join(a_plus['symbol'].tolist())}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎯 STOCK CLASSIFIER - QUICK TEST")
    print("="*60)
    
    # Run tests
    test_single_classification()
    test_market_scan()
    # test_filters()  # Commented out to avoid too many API calls
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED")
    print("="*60 + "\n")

