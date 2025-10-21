"""
VNStock Dashboard - Trực quan hóa dữ liệu cổ phiếu
Sử dụng Streamlit và Plotly để tạo giao diện web tương tác
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from vnstock import Vnstock
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cấu hình trang
st.set_page_config(
    page_title="VNStock Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #1f77b4;
        font-size: 3rem !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

def format_currency(value):
    """Format số tiền theo định dạng VND"""
    try:
        if pd.isna(value):
            return "N/A"
        # Chuyển từ nghìn đồng sang VND đầy đủ
        vnd_value = value * 1000
        return f"{vnd_value:,.0f} VND"
    except:
        return "N/A"

def format_volume(value):
    """Format khối lượng giao dịch"""
    try:
        if pd.isna(value):
            return "N/A"
        if value >= 1_000_000:
            return f"{value/1_000_000:.2f}M"
        elif value >= 1_000:
            return f"{value/1_000:.2f}K"
        return f"{value:,.0f}"
    except:
        return "N/A"

def get_stock_data(symbol, days=365):
    """
    Lấy dữ liệu cổ phiếu từ vnstock
    
    Args:
        symbol: Mã cổ phiếu
        days: Số ngày lịch sử (mặc định 365 - 1 năm)
    
    Returns:
        DataFrame chứa dữ liệu OHLCV
    """
    try:
        # Khởi tạo vnstock client
        stock = Vnstock().stock(symbol=symbol.upper(), source='VCI')
        
        # Tính toán khoảng thời gian
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        # Lấy dữ liệu lịch sử
        logger.info(f"Đang lấy dữ liệu {symbol} từ {start_date} đến {end_date}")
        df = stock.quote.history(start=start_date, end=end_date)
        
        if df.empty:
            st.error(f"Không có dữ liệu cho mã {symbol}")
            return None
        
        # Chuyển đổi cột time thành datetime nếu chưa
        if 'time' in df.columns:
            df['time'] = pd.to_datetime(df['time'])
        
        logger.info(f"Đã lấy được {len(df)} bản ghi dữ liệu")
        return df
        
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu {symbol}: {str(e)}")
        st.error(f"Lỗi: {str(e)}")
        return None

def plot_candlestick(df, symbol):
    """
    Vẽ biểu đồ nến bằng Plotly
    
    Args:
        df: DataFrame chứa dữ liệu OHLCV
        symbol: Mã cổ phiếu
    
    Returns:
        Plotly figure object
    """
    try:
        # Tạo biểu đồ nến
        fig = go.Figure(data=[go.Candlestick(
            x=df['time'],
            open=df['open'] * 1000,  # Chuyển từ nghìn đồng sang VND
            high=df['high'] * 1000,
            low=df['low'] * 1000,
            close=df['close'] * 1000,
            name=symbol,
            increasing=dict(
                line=dict(color='#26a69a', width=1),
                fillcolor='#26a69a'
            ),
            decreasing=dict(
                line=dict(color='#ef5350', width=1),
                fillcolor='#ef5350'
            )
        )])
        
        # Cập nhật layout
        fig.update_layout(
            title=f'Biểu đồ Nến - {symbol.upper()}',
            title_font=dict(size=24, color='#1f77b4', family='Arial Black'),
            xaxis_title='Thời gian',
            yaxis_title='Giá (VND)',
            xaxis_rangeslider_visible=False,
            template='plotly_white',
            height=600,
            hovermode='x unified',
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='#e0e0e0'
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='#e0e0e0',
                tickformat=',d'
            )
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Lỗi khi vẽ biểu đồ: {str(e)}")
        st.error(f"Lỗi khi vẽ biểu đồ: {str(e)}")
        return None

def plot_volume(df):
    """
    Vẽ biểu đồ khối lượng giao dịch
    
    Args:
        df: DataFrame chứa dữ liệu volume
    
    Returns:
        Plotly figure object
    """
    try:
        # Tạo màu sắc cho volume (xanh khi tăng, đỏ khi giảm)
        colors = ['#26a69a' if close >= open_price else '#ef5350' 
                  for close, open_price in zip(df['close'], df['open'])]
        
        fig = go.Figure(data=[go.Bar(
            x=df['time'],
            y=df['volume'],
            name='Khối lượng',
            marker_color=colors,
            opacity=0.7
        )])
        
        fig.update_layout(
            title='Khối lượng giao dịch',
            title_font=dict(size=18, color='#1f77b4'),
            xaxis_title='Thời gian',
            yaxis_title='Khối lượng',
            template='plotly_white',
            height=300,
            showlegend=False,
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='#e0e0e0'
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='#e0e0e0',
                tickformat=',d'
            )
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Lỗi khi vẽ biểu đồ volume: {str(e)}")
        return None

def calculate_statistics(df):
    """
    Tính toán các chỉ số thống kê
    
    Args:
        df: DataFrame chứa dữ liệu
    
    Returns:
        Dictionary chứa các chỉ số
    """
    try:
        stats = {
            'current_price': df['close'].iloc[-1] * 1000,
            'open_price': df['open'].iloc[-1] * 1000,
            'high_price': df['high'].max() * 1000,
            'low_price': df['low'].min() * 1000,
            'avg_volume': df['volume'].mean(),
            'total_volume': df['volume'].sum(),
            'price_change': (df['close'].iloc[-1] - df['close'].iloc[0]) * 1000,
            'price_change_percent': ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0] * 100),
            'volatility': df['close'].std() * 1000
        }
        return stats
    except Exception as e:
        logger.error(f"Lỗi khi tính toán thống kê: {str(e)}")
        return None

def main():
    """Hàm chính của dashboard"""
    
    # Header
    st.title("📊 VNStock Dashboard")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Cài đặt")
        
        # Input mã cổ phiếu
        symbol = st.text_input(
            "Nhập mã cổ phiếu:",
            value="ACB",
            help="Ví dụ: VIC, VNM, FPT, TCB, ACB"
        ).upper()
        
        # Chọn khoảng thời gian
        time_period = st.selectbox(
            "Khoảng thời gian:",
            options=[30, 90, 180, 365, 730, 1095],
            index=3,
            format_func=lambda x: f"{x} ngày ({x//365} năm)" if x >= 365 else f"{x} ngày"
        )
        
        # Nút tải dữ liệu
        load_data = st.button("🔄 Tải dữ liệu", type="primary", use_container_width=True)
        
        st.markdown("---")
        
        # Thông tin
        st.markdown("""
        ### 📖 Hướng dẫn
        1. Nhập mã cổ phiếu (VD: ACB, VIC)
        2. Chọn khoảng thời gian
        3. Nhấn "Tải dữ liệu"
        
        ### ℹ️ Thông tin
        - **Nguồn**: vnstock
        - **Đơn vị tiền tệ**: VND
        - **Cập nhật**: Real-time
        """)
    
    # Main content
    if load_data or symbol:
        with st.spinner(f"⏳ Đang tải dữ liệu {symbol}..."):
            df = get_stock_data(symbol, days=time_period)
        
        if df is not None and not df.empty:
            # Tính toán thống kê
            stats = calculate_statistics(df)
            
            if stats:
                # Hiển thị metrics
                st.subheader(f"📈 Thông tin {symbol}")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        label="Giá hiện tại",
                        value=f"{stats['current_price']:,.0f} VND",
                        delta=f"{stats['price_change']:,.0f} VND ({stats['price_change_percent']:.2f}%)"
                    )
                
                with col2:
                    st.metric(
                        label="Giá cao nhất",
                        value=f"{stats['high_price']:,.0f} VND"
                    )
                
                with col3:
                    st.metric(
                        label="Giá thấp nhất",
                        value=f"{stats['low_price']:,.0f} VND"
                    )
                
                with col4:
                    st.metric(
                        label="Khối lượng TB",
                        value=format_volume(stats['avg_volume'])
                    )
                
                st.markdown("---")
                
                # Biểu đồ nến
                st.subheader("🕯️ Biểu đồ nến")
                candlestick_fig = plot_candlestick(df, symbol)
                if candlestick_fig:
                    st.plotly_chart(candlestick_fig, use_container_width=True)
                
                # Biểu đồ khối lượng
                st.subheader("📊 Khối lượng giao dịch")
                volume_fig = plot_volume(df)
                if volume_fig:
                    st.plotly_chart(volume_fig, use_container_width=True)
                
                st.markdown("---")
                
                # Bảng dữ liệu
                with st.expander("📋 Xem dữ liệu chi tiết"):
                    # Format dữ liệu để hiển thị
                    display_df = df.copy()
                    display_df['open'] = display_df['open'] * 1000
                    display_df['high'] = display_df['high'] * 1000
                    display_df['low'] = display_df['low'] * 1000
                    display_df['close'] = display_df['close'] * 1000
                    
                    st.dataframe(
                        display_df[['time', 'open', 'high', 'low', 'close', 'volume']].tail(50),
                        use_container_width=True,
                        hide_index=True
                    )
                
                # Thống kê chi tiết
                with st.expander("📊 Thống kê chi tiết"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        **Thông tin giá:**
                        - Giá mở cửa: {stats['open_price']:,.0f} VND
                        - Giá đóng cửa: {stats['current_price']:,.0f} VND
                        - Biến động: ±{stats['volatility']:,.0f} VND
                        """)
                    
                    with col2:
                        st.markdown(f"""
                        **Thông tin khối lượng:**
                        - Tổng KL: {format_volume(stats['total_volume'])}
                        - KL trung bình: {format_volume(stats['avg_volume'])}
                        - Số phiên: {len(df)} ngày
                        """)
        else:
            st.warning(f"⚠️ Không tìm thấy dữ liệu cho mã {symbol}")
    else:
        # Hiển thị thông tin chào mừng
        st.info("👈 Vui lòng nhập mã cổ phiếu và nhấn 'Tải dữ liệu' để bắt đầu")
        
        # Hiển thị một số mã phổ biến
        st.subheader("🔥 Mã cổ phiếu phổ biến")
        
        popular_stocks = {
            "Ngân hàng": ["ACB", "TCB", "VCB", "MBB", "VPB"],
            "Bất động sản": ["VHM", "VIC", "NVL", "KDH", "DXG"],
            "Công nghệ": ["FPT", "CMG", "VGI"],
            "Hàng tiêu dùng": ["VNM", "MSN", "MWG", "PNJ"]
        }
        
        for sector, stocks in popular_stocks.items():
            with st.expander(f"📌 {sector}"):
                st.write(", ".join(stocks))

if __name__ == "__main__":
    main()

