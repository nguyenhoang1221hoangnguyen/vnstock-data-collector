#!/bin/bash
# Quick start script for Stock Classifier

cd "/Users/nguyenhoang/Desktop/2025/hoc-tap code/vscode/VNSTOCK 2"

echo "🎯 STOCK CLASSIFICATION SYSTEM"
echo "=============================="
echo ""
echo "Chọn chức năng:"
echo "1. Scan 20 stocks (nhanh - 2 phút)"
echo "2. Scan 50 stocks (vừa - 5 phút)"
echo "3. Scan 100 stocks (đầy đủ - 10 phút)"
echo "4. Quick test (5 stocks)"
echo "5. Classify 1 mã cụ thể"
echo ""
read -p "Nhập lựa chọn (1-5): " choice

# Activate virtual environment
source venv/bin/activate

case $choice in
    1)
        echo ""
        echo "🔍 Scanning 20 stocks from HOSE..."
        python stock_classifier.py 20
        ;;
    2)
        echo ""
        echo "🔍 Scanning 50 stocks from HOSE..."
        python stock_classifier.py 50
        ;;
    3)
        echo ""
        echo "🔍 Scanning 100 stocks from HOSE..."
        python stock_classifier.py 100
        ;;
    4)
        echo ""
        echo "🧪 Running quick test (5 stocks)..."
        python test_classifier_quick.py
        ;;
    5)
        echo ""
        read -p "Nhập mã cổ phiếu (VD: FPT): " symbol
        echo ""
        echo "🔍 Classifying $symbol..."
        python -c "
from stock_classifier import StockClassifier
import json

classifier = StockClassifier()
result = classifier.classify_stock('$symbol')

if 'error' not in result or result['error'] is None:
    print('\n' + '='*60)
    print(f\"📊 CLASSIFICATION RESULT: {result['symbol']}\")
    print('='*60)
    
    print(f\"\n⭐ Overall Rating: {result['overall_rating']['rating']} ({result['overall_rating']['score']})\")
    print(f\"   {result['overall_rating']['recommendation']}\")
    
    print(f\"\n📈 Growth: {result['classifications']['growth']['category']} (Score: {result['classifications']['growth']['score']})\")
    print(f\"   {result['classifications']['growth']['description']}\")
    
    print(f\"\n⚠️  Risk: {result['classifications']['risk']['category']} (Score: {result['classifications']['risk']['risk_score']})\")
    print(f\"   {result['classifications']['risk']['description']}\")
    print(f\"   Volatility: {result['classifications']['risk']['volatility']}%\")
    
    print(f\"\n💰 Market Cap: {result['classifications']['market_cap']['category']}\")
    print(f\"   {result['classifications']['market_cap']['description']}\")
    print(f\"   Value: {result['classifications']['market_cap']['market_cap_trillion']} trillion VND\")
    
    print(f\"\n📊 Momentum: {result['classifications']['momentum']['category']} (Score: {result['classifications']['momentum']['momentum_score']})\")
    print(f\"   {result['classifications']['momentum']['description']}\")
    
    print(f\"\n🔢 Component Scores:\")
    print(f\"   Growth: {result['overall_rating']['component_scores']['growth']}\")
    print(f\"   Risk Adjusted: {result['overall_rating']['component_scores']['risk_adjusted']}\")
    print(f\"   Momentum: {result['overall_rating']['component_scores']['momentum']}\")
    
    print('\n' + '='*60)
else:
    print(f\"❌ Error: {result['error']}\")
"
        ;;
    *)
        echo "❌ Lựa chọn không hợp lệ!"
        exit 1
        ;;
esac

echo ""
echo "✅ Hoàn tất!"

