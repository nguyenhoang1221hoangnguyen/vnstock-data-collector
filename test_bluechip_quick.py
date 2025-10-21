# -*- coding: utf-8 -*-
"""
Quick test for Blue-chip Detector - Test với 5 mã
"""

from bluechip_detector import BlueChipDetector
import time

def test_quick():
    """Test nhanh với 5 mã"""
    detector = BlueChipDetector()
    
    # Test với 5 mã lớn
    test_symbols = ['VCB', 'TCB', 'FPT', 'VNM', 'HPG']
    
    print(f"\n🧪 Quick Test: Scanning {len(test_symbols)} stocks...")
    print("=" * 60)
    
    results = []
    
    for i, symbol in enumerate(test_symbols, 1):
        print(f"\n[{i}/{len(test_symbols)}] Testing {symbol}...")
        
        result = detector.check_bluechip_criteria(symbol)
        results.append(result)
        
        print(f"  Score: {result['score']}/{result['max_score']}")
        print(f"  Blue-chip: {'✅ YES' if result['is_bluechip'] else '❌ NO'}")
        
        details = result.get('details', {})
        if 'pe' in details:
            print(f"  P/E: {details['pe']}")
        if 'roe' in details:
            print(f"  ROE: {details['roe']}%")
        
        # Delay để tránh rate limit
        if i < len(test_symbols):
            print("  ⏳ Waiting 3 seconds...")
            time.sleep(3)
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    bluechips = [r for r in results if r['is_bluechip']]
    print(f"\nBlue-chips found: {len(bluechips)}/{len(test_symbols)}")
    
    for bc in bluechips:
        print(f"  ✅ {bc['symbol']} - Score: {bc['score']}/6")
    
    print("\n✅ Test completed!\n")
    
    return results


if __name__ == "__main__":
    test_quick()

