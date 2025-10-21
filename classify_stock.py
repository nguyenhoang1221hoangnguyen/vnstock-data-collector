#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple CLI for Stock Classification
Usage: python classify_stock.py <SYMBOL>
"""

import sys
from stock_classifier import StockClassifier

def main():
    if len(sys.argv) < 2:
        print("\n❌ Error: Thiếu mã cổ phiếu!")
        print("\nUsage:")
        print("  python classify_stock.py <SYMBOL>")
        print("\nExample:")
        print("  python classify_stock.py FPT")
        print("  python classify_stock.py VCB")
        sys.exit(1)
    
    symbol = sys.argv[1].upper()
    
    print(f"\n🔍 Classifying {symbol}...")
    print("⏳ Please wait (this may take 5-10 seconds)...\n")
    
    classifier = StockClassifier()
    result = classifier.classify_stock(symbol)
    
    if 'error' in result and result['error']:
        print(f"❌ Error: {result['error']}\n")
        sys.exit(1)
    
    # Print results
    print("=" * 70)
    print(f"📊 CLASSIFICATION RESULT: {result['symbol']}")
    print("=" * 70)
    
    # Overall Rating
    rating = result['overall_rating']
    print(f"\n⭐ OVERALL RATING: {rating['rating']} ({rating['score']}/10)")
    print(f"   {rating['recommendation']}")
    
    # Growth
    growth = result['classifications']['growth']
    print(f"\n📈 GROWTH POTENTIAL: {growth['category']} (Score: {growth['score']}/10)")
    print(f"   {growth['description']}")
    if 'roe' in growth:
        print(f"   ROE: {growth['roe']}%")
    if 'pe' in growth and growth['pe'] > 0:
        print(f"   P/E: {growth['pe']}")
    if 'npm' in growth:
        print(f"   NPM: {growth['npm']}%")
    
    # Risk
    risk = result['classifications']['risk']
    print(f"\n⚠️  RISK LEVEL: {risk['category']} (Score: {risk['risk_score']}/10)")
    print(f"   {risk['description']}")
    print(f"   Volatility: {risk['volatility']}%")
    if 'debt_equity' in risk:
        print(f"   D/E Ratio: {risk['debt_equity']}")
    
    # Market Cap
    market_cap = result['classifications']['market_cap']
    print(f"\n💰 MARKET CAP: {market_cap['category']}")
    print(f"   {market_cap['description']}")
    print(f"   {market_cap['market_cap_trillion']} trillion VND")
    
    # Momentum
    momentum = result['classifications']['momentum']
    print(f"\n📊 MOMENTUM: {momentum['category']} (Score: {momentum['momentum_score']}/10)")
    print(f"   {momentum['description']}")
    if 'bullish_signals' in momentum and momentum['bullish_signals']:
        print(f"   Bullish signals: {', '.join(momentum['bullish_signals'])}")
    if 'bearish_signals' in momentum and momentum['bearish_signals']:
        print(f"   Bearish signals: {', '.join(momentum['bearish_signals'])}")
    
    # Component Scores
    print(f"\n🔢 COMPONENT SCORES:")
    components = rating['component_scores']
    print(f"   Growth:        {components['growth']}/10")
    print(f"   Risk Adjusted: {components['risk_adjusted']}/10")
    print(f"   Momentum:      {components['momentum']}/10")
    
    # Formula
    print(f"\n📐 CALCULATION:")
    print(f"   Overall = (Growth × 0.4) + (Risk Adj × 0.3) + (Momentum × 0.3)")
    print(f"   {rating['score']} = ({components['growth']} × 0.4) + ({components['risk_adjusted']} × 0.3) + ({components['momentum']} × 0.3)")
    
    print("\n" + "=" * 70)
    print(f"✅ Classification completed for {symbol}")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()

