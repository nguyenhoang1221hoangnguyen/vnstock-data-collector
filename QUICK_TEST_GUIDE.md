# 🧪 Quick Test Guide - Stock Screener & Classification

Hướng dẫn nhanh để test hệ thống Stock Screener sau khi fix bug.

---

## ✅ 1. Test Single Stock Classification (API)

### Test FPT (Full FA data)
```bash
curl -s "http://localhost:8501/classify/stock/FPT" | python3 -m json.tool
```

**Expected Output:**
```json
{
  "success": true,
  "data": {
    "symbol": "FPT",
    "classifications": {
      "growth": {
        "category": "growth",
        "score": 7,
        "roe": 21.61,     ← Should NOT be 0!
        "pe": 0.16,        ← Should NOT be 0!
        "npm": 13.58       ← Should NOT be 0!
      },
      "risk": {
        "category": "medium_risk",
        "debt_equity": 1.04  ← Should NOT be 0!
      },
      "overall_rating": {
        "rating": "C",        ← Should NOT be "F"!
        "score": 5.8
      }
    }
  }
}
```

### Test HPG (Manufacturing stock)
```bash
curl -s "http://localhost:8501/classify/stock/HPG" | python3 -m json.tool | grep -A10 "growth"
```

**Expected:**
- ROE ≈ 10-11%
- Rating: C or D

### Test TCB (Banking, high debt)
```bash
curl -s "http://localhost:8501/classify/stock/TCB" | python3 -m json.tool | grep -A10 "growth"
```

**Expected:**
- ROE ≈ 13%
- D/E ≈ 5.4 (very high!)
- Rating: F (correct because of high debt!)

---

## ✅ 2. Test Market Scan (API)

### Scan 5 stocks với delay 6s
```bash
curl -s "http://localhost:8501/classify/market?exchanges=HOSE&limit=5&delay=6.0" | python3 -m json.tool | head -60
```

**Expected Output:**
```json
{
  "success": true,
  "summary": {
    "total_stocks": 5,
    "by_rating": {
      "B": X,    ← Should have variety
      "C": Y,
      "D": Z
    },
    "avg_score": 5.0-6.0   ← Realistic average
  }
}
```

**Check Points:**
- ✅ `success: true`
- ✅ `total_stocks: 5`
- ✅ Ratings should be B/C/D (NOT all "F"!)
- ✅ Each stock should have roe/pe/npm values (NOT all 0!)

---

## ✅ 3. Test via Dashboard (Browser)

### 1. Start Services
```bash
cd "/Users/nguyenhoang/Desktop/2025/hoc-tap code/vscode/VNSTOCK 2"
./manage_system.sh
# → Choose: 1. Start All Services
```

### 2. Open Dashboard
```
http://localhost:8502
```

### 3. Go to Stock Screener Tab
- Click **"🎯 Stock Screener"** tab

### 4. Configure Scan
- Exchange: **HOSE**
- Limit: **5** stocks
- Delay: **6** seconds

### 5. Start Scan
- Click **"🔍 Start Scanning"**

### 6. Verify Results
**Should SEE:**
- ✅ Stocks appearing one by one
- ✅ Different ratings (A, B, C, D) - NOT all "F"!
- ✅ ROE/PE values displayed - NOT all 0!
- ✅ Progress bar showing "X/5 stocks scanned"
- ✅ Summary charts showing distribution

**Should NOT SEE:**
- ❌ All stocks with Rating "F"
- ❌ All ROE/PE/NPM = 0
- ❌ Error: "No stocks classified successfully"

---

## ✅ 4. Test Python Script Directly

Create `test_quick.py`:
```python
#!/usr/bin/env python3
from stock_classifier import StockClassifier

classifier = StockClassifier()

# Test 3 stocks
for symbol in ['FPT', 'HPG', 'TCB']:
    print(f"\n{'='*60}")
    print(f"Testing {symbol}:")
    print('='*60)
    
    result = classifier.classify_stock(symbol)
    
    growth = result['classifications']['growth']
    rating = result['overall_rating']
    
    print(f"ROE: {growth['roe']}%")
    print(f"PE: {growth['pe']}")
    print(f"NPM: {growth.get('npm', 'N/A')}%")
    print(f"Category: {growth['category']}")
    print(f"Rating: {rating['rating']} (Score: {rating['score']})")
    print(f"Recommendation: {rating['recommendation']}")
```

Run:
```bash
python3 test_quick.py
```

**Expected:**
- FPT: ROE ≈ 21%, Rating C
- HPG: ROE ≈ 11%, Rating C
- TCB: ROE ≈ 13%, Rating F (high D/E!)

---

## ✅ 5. Check Logs

### API Logs
```bash
tail -100 logs_api.txt | grep -E "(ROE|classify_growth)"
```

**Should see:**
```
INFO:fa_calculator:ROE: 21.61%
INFO:stock_classifier:classify_growth_potential - Parsed: ROE=21.61, PE=0.16, NPM=13.58
```

**Should NOT see:**
```
INFO:stock_classifier:classify_growth_potential - Parsed: ROE=0, PE=0, NPM=0
```

---

## ❌ Troubleshooting

### Problem: Still getting all ROE=0, PE=0

**Solution:**
```bash
# 1. Kill ALL Python processes
killall -9 python3

# 2. Clear cache
cd "/Users/nguyenhoang/Desktop/2025/hoc-tap code/vscode/VNSTOCK 2"
find . -name "__pycache__" -type d -exec rm -rf {} +

# 3. Restart API
source venv/bin/activate
python3 main.py > logs_api.txt 2>&1 &

# 4. Wait 8 seconds
sleep 8

# 5. Test again
curl -s "http://localhost:8501/classify/stock/FPT" | python3 -m json.tool | grep -A10 "growth"
```

### Problem: Port 8501 already in use

**Solution:**
```bash
lsof -ti:8501 | xargs kill -9
sleep 3
python3 main.py > logs_api.txt 2>&1 &
```

### Problem: Dashboard shows timeout

**Solution:**
- Reduce number of stocks to scan (try 5 instead of 10)
- Increase delay to 8 seconds
- Dashboard automatically increases timeout based on stock count

---

## 📊 Success Criteria

Hệ thống hoạt động đúng khi:

✅ **FA Data:**
- ROE, PE, NPM, D/E values **NOT all zero**
- Values match actual financial data

✅ **Classification:**
- Different stocks get **different ratings** (A/B/C/D/F)
- High ROE stocks (>20%) → "growth" or "high_growth"
- Low ROE stocks (<10%) → "value" or "neutral"

✅ **Market Scan:**
- `success: true`
- `total_stocks` matches `limit`
- Average score: **4.5 - 6.0** (realistic range)
- Rating distribution: **mix of B/C/D** (not all F!)

✅ **API Performance:**
- Single stock: 3-4 seconds
- 5 stocks scan: ~30 seconds (with 6s delay)
- No errors or crashes

---

## 🎯 Final Verification Commands

Run all these in sequence:

```bash
# Test 1: API Health
curl -s http://localhost:8501/health

# Test 2: Single stock (FPT)
curl -s "http://localhost:8501/classify/stock/FPT" | python3 -m json.tool | grep -E "(roe|pe|npm|rating)"

# Test 3: Market scan (3 stocks)
curl -s "http://localhost:8501/classify/market?exchanges=HOSE&limit=3&delay=6.0" | python3 -m json.tool | grep -E "(total_stocks|avg_score|by_rating)" -A5

# Test 4: Filter high-quality stocks
curl -s "http://localhost:8501/classify/filter?min_growth_score=7&max_risk_score=6" | python3 -m json.tool | head -40
```

**All tests should pass without errors!** ✅

---

Need help? Check `BUGFIX_COMPLETE.md` for detailed explanation.

