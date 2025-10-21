# 📊 VNStock Dashboard - Hướng dẫn sử dụng

Dashboard trực quan hóa dữ liệu cổ phiếu Việt Nam với giao diện web tương tác.

## 🎯 Tính năng

### 1. Biểu đồ nến (Candlestick Chart)
- **Hiển thị**: Giá OHLC (Open-High-Low-Close)
- **Tương tác**: Zoom, Pan, Hover để xem chi tiết
- **Màu sắc**: 
  - 🟢 Xanh: Phiên tăng giá
  - 🔴 Đỏ: Phiên giảm giá

### 2. Biểu đồ khối lượng
- **Hiển thị**: Khối lượng giao dịch theo thời gian
- **Màu sắc**: Tương ứng với xu hướng giá

### 3. Metrics & Statistics
- Giá hiện tại & biến động
- Giá cao/thấp nhất trong kỳ
- Khối lượng giao dịch trung bình
- Volatility (độ biến động)

### 4. Dữ liệu chi tiết
- Bảng dữ liệu OHLCV đầy đủ
- Export được (qua giao diện Streamlit)
- Có thể xem 50 phiên gần nhất

## 🚀 Khởi chạy Dashboard

### Phương pháp 1: Sử dụng script (Khuyến nghị)
```bash
# Activate virtual environment
source venv/bin/activate

# Chạy dashboard
python start_dashboard.py
```

### Phương pháp 2: Chạy trực tiếp
```bash
# Activate virtual environment
source venv/bin/activate

# Chạy streamlit
streamlit run dashboard.py --server.port=8502 --server.address=0.0.0.0
```

### Phương pháp 3: Background mode
```bash
# Chạy dashboard ở background
nohup python start_dashboard.py > dashboard.log 2>&1 &

# Kiểm tra log
tail -f dashboard.log

# Dừng dashboard
pkill -f "streamlit run dashboard.py"
```

## 🌐 Truy cập Dashboard

### Local
```
http://localhost:8502
```

### Từ máy khác trong mạng LAN
```
http://192.168.1.4:8502
```
*Thay `192.168.1.4` bằng IP thực của máy chủ*

## 📖 Hướng dẫn sử dụng

### Bước 1: Nhập mã cổ phiếu
- Gõ mã cổ phiếu vào ô "Nhập mã cổ phiếu"
- Ví dụ: `ACB`, `VIC`, `FPT`, `TCB`

### Bước 2: Chọn khoảng thời gian
- 30 ngày
- 90 ngày (3 tháng)
- 180 ngày (6 tháng)
- **365 ngày (1 năm)** - Mặc định
- 730 ngày (2 năm)
- 1095 ngày (3 năm)

### Bước 3: Tải dữ liệu
- Nhấn nút **"🔄 Tải dữ liệu"**
- Đợi hệ thống tải dữ liệu (3-5 giây)

### Bước 4: Phân tích
- Xem biểu đồ nến để phân tích xu hướng
- Kiểm tra khối lượng giao dịch
- Xem các metrics quan trọng
- Mở rộng để xem dữ liệu chi tiết

## 💡 Tips & Tricks

### 1. Tương tác với biểu đồ
- **Zoom**: Click và kéo trên biểu đồ
- **Pan**: Giữ Shift + Click và kéo
- **Reset**: Double-click trên biểu đồ
- **Hover**: Di chuột để xem chi tiết từng điểm

### 2. So sánh nhiều mã
- Mở nhiều tab trình duyệt
- Nhập các mã khác nhau
- Đặt cửa sổ cạnh nhau để so sánh

### 3. Xuất dữ liệu
- Mở phần "Xem dữ liệu chi tiết"
- Click vào icon ⋮ ở góc phải bảng
- Chọn "Download as CSV"

### 4. Tùy chỉnh giao diện
- Sử dụng **Settings** (⚙️) ở góc trên bên phải
- Chọn **Theme**: Light/Dark mode
- Điều chỉnh độ rộng: Wide mode

## 🎨 Các mã cổ phiếu phổ biến

### Ngân hàng
`ACB`, `TCB`, `VCB`, `MBB`, `VPB`

### Bất động sản
`VHM`, `VIC`, `NVL`, `KDH`, `DXG`

### Công nghệ
`FPT`, `CMG`, `VGI`

### Hàng tiêu dùng
`VNM`, `MSN`, `MWG`, `PNJ`

## 🔧 Cấu hình nâng cao

### Thay đổi Port
Mặc định: `8502`

```python
# Trong start_dashboard.py
"--server.port=8502"  # Thay đổi port tại đây
```

### Thay đổi địa chỉ binding
Mặc định: `0.0.0.0` (cho phép truy cập từ xa)

```python
# Trong start_dashboard.py
"--server.address=0.0.0.0"  # Thay đổi địa chỉ tại đây
```

### Tùy chỉnh nguồn dữ liệu
```python
# Trong dashboard.py, function get_stock_data()
stock = Vnstock().stock(symbol=symbol.upper(), source='VCI')
# Thay đổi source: 'VCI', 'TCBS', 'VND', v.v.
```

## 📊 Ví dụ Use Cases

### 1. Phân tích xu hướng dài hạn
- Chọn khoảng thời gian 2-3 năm
- Xem biểu đồ nến
- Xác định các mức hỗ trợ/kháng cự

### 2. Trading ngắn hạn
- Chọn khoảng thời gian 30-90 ngày
- Theo dõi khối lượng giao dịch
- Xem biến động giá hàng ngày

### 3. So sánh cổ phiếu cùng ngành
- Mở nhiều tab cho các mã khác nhau
- Đặt cùng khoảng thời gian
- So sánh hiệu suất và khối lượng

### 4. Báo cáo & Presentation
- Screenshot các biểu đồ
- Export dữ liệu CSV
- Sử dụng trong PowerPoint/Excel

## 🐛 Troubleshooting

### Dashboard không khởi chạy
```bash
# Kiểm tra port đã được sử dụng chưa
lsof -i :8502

# Nếu đã được sử dụng, kill process
kill -9 <PID>
```

### Lỗi "Module not found"
```bash
# Cài đặt lại dependencies
pip install -r requirements.txt
```

### Không lấy được dữ liệu
- Kiểm tra kết nối Internet
- Kiểm tra mã cổ phiếu có đúng không
- Thử lại sau vài phút (có thể API đang bận)

### Dashboard chạy chậm
- Giảm khoảng thời gian xuống
- Đóng các tab không dùng
- Restart dashboard

## 🔒 Security Notes

### Chạy trong mạng LAN
- Dashboard mặc định bind `0.0.0.0` (cho phép truy cập từ mọi IP)
- **Khuyến nghị**: Chỉ sử dụng trong mạng tin cậy
- **Production**: Nên dùng reverse proxy (nginx) + authentication

### Giới hạn truy cập
Nếu muốn chỉ cho phép localhost:
```python
"--server.address=localhost"  # Chỉ localhost có thể truy cập
```

## 📈 Tích hợp với n8n

Dashboard có thể hoạt động song song với API server:
- **API**: Port 8501 (cho n8n và automation)
- **Dashboard**: Port 8502 (cho human visualization)

Cả hai có thể chạy đồng thời:
```bash
# Terminal 1: Chạy API
python start_server.py &

# Terminal 2: Chạy Dashboard
python start_dashboard.py &
```

## 🎯 Roadmap

### Upcoming Features
- [ ] Thêm các chỉ báo kỹ thuật (MA, RSI, MACD)
- [ ] So sánh nhiều mã trên cùng 1 biểu đồ
- [ ] Lưu watchlist yêu thích
- [ ] Alert khi giá đạt ngưỡng
- [ ] Dark mode mặc định
- [ ] Mobile responsive design

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra logs: `dashboard.log`
2. Xem lại hướng dẫn này
3. Kiểm tra API vnstock có hoạt động không
4. Restart dashboard

## 📝 License

MIT License - Sử dụng tự do cho mục đích cá nhân và thương mại.

