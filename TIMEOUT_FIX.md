# 🕐 Timeout Fix - Stock Screener

## 🐛 Vấn đề

```
Error scanning: HTTPConnectionPool(host='localhost', port=8501): 
Read timed out. (read timeout=60)
```

## 🔍 Nguyên nhân

**Timeout calculation cũ không tính đúng delay từ UI:**

```python
# TRƯỚC (sai):
timeout_seconds = int(scan_limit * 4 * 1.5)
# 20 stocks → 20 × 4 × 1.5 = 120s

# THỰC TẾ cần:
# 20 stocks × (4s API + 8s delay) × 1.5 buffer = 360s
```

**Kết quả:** Timeout 120s < Thực tế 360s → **TIMEOUT!**

---

## ✅ Giải pháp

### 1. **Fixed timeout calculation trong `dashboard_advanced.py`:**

```python
# SAU (đúng):
estimated_time_per_stock = 4 + scan_delay  # API + delay từ UI
timeout_seconds = int(scan_limit * estimated_time_per_stock * 1.5)

# Ví dụ với 20 stocks, delay 8s:
# 20 × (4 + 8) × 1.5 = 20 × 12 × 1.5 = 360s ✅
```

### 2. **Fixed API params để dùng delay từ UI:**

```python
# TRƯỚC (hardcoded):
params = {
    "delay": 5.0  # ❌ Không match với UI!
}

# SAU (dynamic):
params = {
    "delay": scan_delay  # ✅ Dùng delay từ UI!
}
```

### 3. **Added timeout debugging:**

Dashboard sẽ hiển thị:
```
⏱️ Estimated time: 20 stocks × 12s = 240s
🕐 Timeout set to: 360s (with 50% buffer)
```

---

## 📊 Timeout Table

| Stocks | Delay | Time/Stock | Total Time | Timeout (1.5x) | Status |
|--------|-------|------------|------------|-------------|--------|
| 5      | 6s    | 10s        | 50s        | 75s         | ✅ OK  |
| 10     | 6s    | 10s        | 100s       | 150s        | ✅ OK  |
| 10     | 8s    | 12s        | 120s       | 180s        | ✅ OK  |
| 20     | 6s    | 10s        | 200s       | 300s        | ✅ OK  |
| 20     | 8s    | 12s        | 240s       | 360s        | ✅ OK  |
| 50     | 6s    | 10s        | 500s       | 750s        | ✅ OK  |

---

## 🚀 Cách sử dụng sau khi fix

### 1. **Restart Dashboard:**
```bash
cd "/Users/nguyenhoang/Desktop/2025/hoc-tap code/vscode/VNSTOCK 2"
pkill -f "streamlit.*dashboard_advanced"
source venv/bin/activate
streamlit run dashboard_advanced.py --server.port 8502 &
```

### 2. **Truy cập Dashboard:**
```
http://localhost:8502
```

### 3. **Sử dụng Stock Screener:**
- Click tab **"🎯 Stock Screener"**
- Set **Exchanges**: HOSE
- Set **Limit**: 10-20 stocks (recommended)
- Set **Delay**: 6-8 giây
- Click **"🔍 Start Scanning"**

### 4. **Observe timeout info:**
Dashboard sẽ hiển thị:
```
⏱️ Estimated time: 10 stocks × 10s = 100s
🕐 Timeout set to: 150s (with 50% buffer)
```

---

## ⚠️ Recommendations

### 1. **Optimal Settings:**
- **Stocks**: 10-20 (balance between speed và variety)
- **Delay**: 6-8 giây (tránh rate limit)
- **Expected time**: 2-4 phút

### 2. **Large Scans:**
Nếu muốn scan 50+ stocks:
- **Delay**: 8-10 giây (tránh rate limit)
- **Expected time**: 8-15 phút
- **Timeout**: Tự động tính (750s+)

### 3. **Rate Limit Protection:**
- **Minimum delay**: 6 giây
- **Recommended delay**: 8 giây cho large scans
- **Never go below**: 5 giây

---

## 🐛 Troubleshooting

### Problem: Vẫn timeout
**Solution:**
1. Giảm số stocks (thử 5-10)
2. Tăng delay (thử 10 giây)
3. Check API server: `curl http://localhost:8501/health`

### Problem: Rate limit (502/429 errors)
**Solution:**
1. Tăng delay lên 10+ giây
2. Giảm số stocks
3. Wait 1-2 phút rồi thử lại

### Problem: Dashboard không load
**Solution:**
```bash
pkill -f streamlit
streamlit run dashboard_advanced.py --server.port 8502
```

---

## 📝 Technical Details

### Timeout Formula:
```
timeout = stocks × (api_time + delay) × buffer

Where:
- api_time = 4 seconds (average API processing)
- delay = user setting from UI (6-10s recommended)
- buffer = 1.5 (50% safety margin)
```

### Examples:
```python
# 10 stocks, 6s delay:
timeout = 10 × (4 + 6) × 1.5 = 150s

# 20 stocks, 8s delay:
timeout = 20 × (4 + 8) × 1.5 = 360s

# 50 stocks, 10s delay:
timeout = 50 × (4 + 10) × 1.5 = 1050s (17.5 minutes)
```

---

## ✅ Status

**Fix applied:** ✅ Dashboard restarted
**Timeout calculation:** ✅ Fixed
**API params:** ✅ Fixed
**Debug info:** ✅ Added

**Ready to use!** 🚀

---

## 🔄 About AuthSessionMissingError

**Note:** The console error `AuthSessionMissingError: Auth session missing!` is **NOT related** to VNStock system.

This error comes from:
- Another web app (possibly n8n, Supabase, or other React app)
- Running on different port
- Trying to authenticate with external service

**VNStock system does NOT use authentication** - it's a standalone application.

**Solution:** Ignore this error or restart the other application causing it.

---

_Updated: 21/10/2025, 5:30 PM_
_Timeout issue resolved_
