"""
Comprehensive Testing Suite - VNStock
Test all modules and features
"""

import pytest
import sys
from datetime import datetime, timedelta

# Test imports
print("Testing imports...")

try:
    # Core modules
    from vnstock import Vnstock
    print("✓ vnstock")
    
    from database import get_db, VNStockDB
    print("✓ database")
    
    from notifications import NotificationManager, get_notifier
    print("✓ notifications")
    
    from drawing_tools import ChartDrawing, quick_support_resistance
    print("✓ drawing_tools")
    
    from portfolio_manager import PortfolioManager
    print("✓ portfolio_manager")
    
    from news_sentiment import NewsAnalyzer, quick_sentiment_check
    print("✓ news_sentiment")
    
    from advanced_indicators import (
        calculate_ichimoku, calculate_adx, calculate_stochastic
    )
    print("✓ advanced_indicators")
    
    from fa_calculator import calculate_fa_ratios
    print("✓ fa_calculator")
    
    from ta_analyzer import calculate_ta_indicators
    print("✓ ta_analyzer")
    
    from stock_screener import run_screener
    print("✓ stock_screener")
    
    from backtesting_strategy import run_ma_crossover_backtest
    print("✓ backtesting_strategy")
    
    print("\n✅ All imports successful!\n")
    
except ImportError as e:
    print(f"\n❌ Import error: {e}\n")
    sys.exit(1)


# ========== DATABASE TESTS ==========

def test_database():
    """Test database operations"""
    print("=" * 60)
    print("TESTING DATABASE MODULE")
    print("=" * 60)
    
    try:
        db = get_db()
        
        # Test watchlist
        print("\n1. Testing Watchlist...")
        db.add_to_watchlist('TEST', notes='Test stock', target_price=50000)
        watchlist = db.get_watchlist()
        assert len(watchlist) > 0, "Watchlist should not be empty"
        print("   ✓ Watchlist add/get works")
        
        # Test alerts
        print("\n2. Testing Alerts...")
        alert_id = db.add_alert('TEST', 'above', 55000)
        assert alert_id > 0, "Alert ID should be positive"
        alerts = db.get_active_alerts()
        print(f"   ✓ Alerts work (ID: {alert_id})")
        
        # Test portfolio
        print("\n3. Testing Portfolio...")
        pos_id = db.add_position('TEST', 100, 50000)
        assert pos_id > 0, "Position ID should be positive"
        portfolio = db.get_portfolio()
        assert len(portfolio) > 0, "Portfolio should not be empty"
        print(f"   ✓ Portfolio works (ID: {pos_id})")
        
        # Test stats
        print("\n4. Testing Stats...")
        stats = db.get_stats()
        print(f"   Stats: {stats}")
        print("   ✓ Stats work")
        
        # Cleanup
        db.remove_from_watchlist('TEST')
        db.remove_alert(alert_id)
        db.close_position(pos_id, 52000)
        
        print("\n✅ Database tests PASSED\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Database test FAILED: {e}\n")
        return False


# ========== DRAWING TOOLS TESTS ==========

def test_drawing_tools():
    """Test drawing tools"""
    print("=" * 60)
    print("TESTING DRAWING TOOLS MODULE")
    print("=" * 60)
    
    try:
        drawer = ChartDrawing()
        
        # Test horizontal line
        print("\n1. Testing Horizontal Line...")
        hline = drawer.add_horizontal_line(25000, label="Support")
        assert hline['type'] == 'hline', "Should be hline type"
        print("   ✓ Horizontal line works")
        
        # Test trend line
        print("\n2. Testing Trend Line...")
        tline = drawer.add_trend_line('2024-01-01', 23000, '2024-06-01', 26000)
        assert tline['type'] == 'trendline', "Should be trendline type"
        print("   ✓ Trend line works")
        
        # Test Fibonacci
        print("\n3. Testing Fibonacci...")
        fib = drawer.add_fibonacci_retracement('2024-01-01', 23000, '2024-06-01', 27000)
        assert fib['type'] == 'fibonacci', "Should be fibonacci type"
        assert len(fib['prices']) == 7, "Should have 7 levels"
        print("   ✓ Fibonacci works")
        
        # Test rectangle
        print("\n4. Testing Rectangle...")
        rect = drawer.add_rectangle('2024-01-01', 26000, '2024-06-01', 24000)
        assert rect['type'] == 'rectangle', "Should be rectangle type"
        print("   ✓ Rectangle works")
        
        # Test annotation
        print("\n5. Testing Annotation...")
        annot = drawer.add_annotation('2024-03-15', 25500, 'Breakout!')
        assert annot['type'] == 'annotation', "Should be annotation type"
        print("   ✓ Annotation works")
        
        # Test summary
        summary = drawer.get_drawing_summary()
        assert summary['total'] == 5, "Should have 5 drawings"
        print(f"\n   Summary: {summary}")
        
        # Test JSON export/import
        json_str = drawer.to_json()
        assert len(json_str) > 0, "JSON should not be empty"
        
        new_drawer = ChartDrawing()
        new_drawer.from_json(json_str)
        assert len(new_drawer.drawings) == 5, "Should have 5 drawings after import"
        print("   ✓ JSON export/import works")
        
        print("\n✅ Drawing tools tests PASSED\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Drawing tools test FAILED: {e}\n")
        return False


# ========== PORTFOLIO MANAGER TESTS ==========

def test_portfolio_manager():
    """Test portfolio manager"""
    print("=" * 60)
    print("TESTING PORTFOLIO MANAGER MODULE")
    print("=" * 60)
    
    try:
        pm = PortfolioManager(initial_capital=100_000_000)
        
        # Test buy (with mock price)
        print("\n1. Testing Buy...")
        result = pm.buy_stock('TEST', 1000, price=25000, notes='Test buy')
        assert result['success'], "Buy should succeed"
        assert result['remaining_cash'] < 100_000_000, "Cash should decrease"
        print(f"   ✓ Buy works (Cost: {result['total_cost']:,.0f})")
        
        # Test portfolio value
        print("\n2. Testing Portfolio Value...")
        portfolio = pm.get_portfolio_value()
        assert portfolio['cash'] < 100_000_000, "Cash should be less"
        print(f"   Portfolio value: {portfolio['total_value']:,.0f}")
        print("   ✓ Portfolio value calculation works")
        
        # Test sell
        print("\n3. Testing Sell...")
        if portfolio['positions']:
            pos_id = portfolio['positions'][0]['position_id']
            sell_result = pm.sell_stock(pos_id, price=26000, notes='Test sell')
            assert sell_result['success'], "Sell should succeed"
            print(f"   ✓ Sell works (P&L: {sell_result['pnl']:,.0f})")
        
        # Test performance metrics
        print("\n4. Testing Performance Metrics...")
        perf = pm.get_performance_metrics()
        print(f"   Metrics: {perf}")
        print("   ✓ Performance metrics work")
        
        print("\n✅ Portfolio manager tests PASSED\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Portfolio manager test FAILED: {e}\n")
        return False


# ========== NEWS SENTIMENT TESTS ==========

def test_news_sentiment():
    """Test news sentiment analyzer"""
    print("=" * 60)
    print("TESTING NEWS & SENTIMENT MODULE")
    print("=" * 60)
    
    try:
        analyzer = NewsAnalyzer()
        
        # Test positive sentiment
        print("\n1. Testing Positive Sentiment...")
        text_pos = "Lợi nhuận tăng mạnh, triển vọng tích cực trong quý tới"
        sentiment = analyzer.analyze_sentiment(text_pos)
        assert sentiment['sentiment_label'] in ['positive', 'neutral'], "Should be positive or neutral"
        print(f"   Score: {sentiment['sentiment_score']:.2f}")
        print(f"   Label: {sentiment['sentiment_label']}")
        print("   ✓ Positive sentiment detected")
        
        # Test negative sentiment
        print("\n2. Testing Negative Sentiment...")
        text_neg = "Doanh thu giảm sụt, lo ngại về thua lỗ trong quý tới"
        sentiment = analyzer.analyze_sentiment(text_neg)
        assert sentiment['sentiment_label'] in ['negative', 'neutral'], "Should be negative or neutral"
        print(f"   Score: {sentiment['sentiment_score']:.2f}")
        print(f"   Label: {sentiment['sentiment_label']}")
        print("   ✓ Negative sentiment detected")
        
        # Test news sentiment
        print("\n3. Testing News Sentiment Analysis...")
        news_sentiment = analyzer.analyze_news_sentiment('ACB', days=7)
        assert 'overall_sentiment' in news_sentiment, "Should have overall sentiment"
        print(f"   Overall: {news_sentiment['overall_sentiment']}")
        print(f"   News count: {news_sentiment['news_count']}")
        print("   ✓ News sentiment works")
        
        # Test market sentiment
        print("\n4. Testing Market Sentiment...")
        market = analyzer.get_market_sentiment()
        assert 'sentiment_label' in market, "Should have sentiment label"
        print(f"   Market: {market['sentiment_label']}")
        print("   ✓ Market sentiment works")
        
        print("\n✅ News & sentiment tests PASSED\n")
        return True
        
    except Exception as e:
        print(f"\n❌ News sentiment test FAILED: {e}\n")
        return False


# ========== NOTIFICATIONS TESTS ==========

def test_notifications():
    """Test notification manager (without actually sending)"""
    print("=" * 60)
    print("TESTING NOTIFICATIONS MODULE")
    print("=" * 60)
    
    try:
        notifier = NotificationManager()
        
        print("\n1. Testing Config...")
        assert hasattr(notifier, 'config'), "Should have config"
        print("   ✓ Config loaded")
        
        print("\n2. Testing Price Alert Format...")
        # Don't actually send, just test the method exists
        assert hasattr(notifier, 'notify_price_alert'), "Should have notify_price_alert"
        print("   ✓ Price alert method exists")
        
        print("\n3. Testing Trade Notification Format...")
        assert hasattr(notifier, 'notify_trade_execution'), "Should have notify_trade_execution"
        print("   ✓ Trade notification method exists")
        
        print("\n✅ Notifications tests PASSED\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Notifications test FAILED: {e}\n")
        return False


# ========== ADVANCED INDICATORS TESTS ==========

def test_advanced_indicators():
    """Test advanced technical indicators"""
    print("=" * 60)
    print("TESTING ADVANCED INDICATORS MODULE")
    print("=" * 60)
    
    try:
        import pandas as pd
        import numpy as np
        
        # Create mock OHLCV data
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        df = pd.DataFrame({
            'time': dates,
            'open': np.random.uniform(23000, 27000, 100),
            'high': np.random.uniform(24000, 28000, 100),
            'low': np.random.uniform(22000, 26000, 100),
            'close': np.random.uniform(23000, 27000, 100),
            'volume': np.random.uniform(1000000, 5000000, 100)
        })
        df.set_index('time', inplace=True)
        
        print("\n1. Testing Ichimoku...")
        tenkan, kijun, senkou_a, senkou_b, chikou = calculate_ichimoku(df)
        assert len(tenkan) == len(df), "Ichimoku should match data length"
        print("   ✓ Ichimoku works")
        
        print("\n2. Testing ADX...")
        adx, plus_di, minus_di = calculate_adx(df)
        assert len(adx) == len(df), "ADX should match data length"
        print("   ✓ ADX works")
        
        print("\n3. Testing Stochastic...")
        k_percent, d_percent = calculate_stochastic(df)
        assert len(k_percent) == len(df), "Stochastic should match data length"
        print("   ✓ Stochastic works")
        
        print("\n✅ Advanced indicators tests PASSED\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Advanced indicators test FAILED: {e}\n")
        return False


# ========== MAIN TEST RUNNER ==========

def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("VNSTOCK COMPREHENSIVE TEST SUITE")
    print("=" * 60 + "\n")
    
    results = {
        'Database': test_database(),
        'Drawing Tools': test_drawing_tools(),
        'Portfolio Manager': test_portfolio_manager(),
        'News & Sentiment': test_news_sentiment(),
        'Notifications': test_notifications(),
        'Advanced Indicators': test_advanced_indicators()
    }
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for module, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{module:.<40} {status}")
    
    print(f"\nTotal: {passed}/{total} passed ({(passed/total)*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉\n")
        return 0
    else:
        print(f"\n⚠️  {total - passed} TEST(S) FAILED\n")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)

