"""
VNStock Data Collector - Web Interface
Giao diện web đẹp mắt để tra cứu thông tin cổ phiếu
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import time

# Cấu hình trang
st.set_page_config(
    page_title="VNStock Data Collector",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .success-metric {
        border-left-color: #28a745;
    }
    
    .warning-metric {
        border-left-color: #ffc107;
    }
    
    .danger-metric {
        border-left-color: #dc3545;
    }
    
    .info-metric {
        border-left-color: #17a2b8;
    }
    
    .search-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .company-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-left: 20px;
        padding-right: 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Danh sách mã cổ phiếu phổ biến
POPULAR_STOCKS = {
    "VIC": "Vingroup",
    "VCB": "Vietcombank", 
    "VHM": "Vinhomes",
    "HPG": "Hoa Phat Group",
    "MSN": "Masan Group",
    "VRE": "Vincom Retail",
    "GAS": "PetroVietnam Gas",
    "VNM": "Vinamilk",
    "BID": "BIDV",
    "CTG": "VietinBank",
    "FPT": "FPT Corporation",
    "MWG": "Mobile World",
    "PLX": "Petrolimex",
    "POW": "PetroVietnam Power",
    "SSI": "SSI Securities",
    "TCB": "Techcombank",
    "VGC": "Viglacera",
    "VJC": "VietJet Air",
    "VND": "VNDirect Securities",
    "VPB": "VPBank"
}

def format_currency(value, unit="VND"):
    """Format số tiền với đơn vị VND"""
    if pd.isna(value) or value is None:
        return "N/A"
    
    try:
        if abs(value) >= 1e12:  # Nghìn tỷ
            return f"{value/1e12:.2f} nghìn tỷ {unit}"
        elif abs(value) >= 1e9:  # Tỷ
            return f"{value/1e9:.2f} tỷ {unit}"
        elif abs(value) >= 1e6:  # Triệu
            return f"{value/1e6:.2f} triệu {unit}"
        elif abs(value) >= 1e3:  # Nghìn
            return f"{value/1e3:.2f} nghìn {unit}"
        else:
            return f"{value:,.0f} {unit}"
    except:
        return "N/A"

def format_percentage(value):
    """Format phần trăm"""
    if pd.isna(value) or value is None:
        return "N/A"
    try:
        return f"{value:.2f}%"
    except:
        return "N/A"

def search_stocks(query):
    """Tìm kiếm mã cổ phiếu"""
    if not query:
        return []
    
    query = query.upper()
    results = []
    
    # Tìm kiếm theo mã
    for code, name in POPULAR_STOCKS.items():
        if query in code or query in name.upper():
            results.append({"code": code, "name": name})
    
    return results[:10]  # Giới hạn 10 kết quả

def get_stock_data(symbol):
    """Lấy dữ liệu cổ phiếu từ API"""
    try:
        url = "http://localhost:8501/api/v1/stock/batch"
        payload = {"symbol": symbol}
        
        with st.spinner(f"Đang tải dữ liệu cho {symbol}..."):
            response = requests.post(url, json=payload, timeout=30)
            
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Lỗi API: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Không thể kết nối đến API. Vui lòng đảm bảo server đang chạy tại http://localhost:8501")
        return None
    except Exception as e:
        st.error(f"Lỗi: {str(e)}")
        return None

def create_price_chart(historical_data):
    """Tạo biểu đồ giá cổ phiếu"""
    if not historical_data or 'data' not in historical_data:
        return None
    
    df = pd.DataFrame(historical_data['data'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    fig = go.Figure()
    
    # Biểu đồ nến
    fig.add_trace(go.Candlestick(
        x=df['date'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name="Giá cổ phiếu"
    ))
    
    # Đường trung bình 20 ngày
    df['ma20'] = df['close'].rolling(window=20).mean()
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['ma20'],
        mode='lines',
        name='MA20',
        line=dict(color='orange', width=2)
    ))
    
    fig.update_layout(
        title="Biểu đồ giá cổ phiếu",
        xaxis_title="Ngày",
        yaxis_title="Giá (VND)",
        template="plotly_white",
        height=500
    )
    
    return fig

def create_volume_chart(historical_data):
    """Tạo biểu đồ khối lượng giao dịch"""
    if not historical_data or 'data' not in historical_data:
        return None
    
    df = pd.DataFrame(historical_data['data'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['date'],
        y=df['volume'],
        name="Khối lượng",
        marker_color='lightblue'
    ))
    
    fig.update_layout(
        title="Khối lượng giao dịch",
        xaxis_title="Ngày",
        yaxis_title="Khối lượng",
        template="plotly_white",
        height=400
    )
    
    return fig

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 VNStock Data Collector</h1>
        <p>Tra cứu thông tin cổ phiếu Việt Nam - Dữ liệu toàn diện và chính xác</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔍 Tìm kiếm cổ phiếu")
        
        # Tìm kiếm
        search_query = st.text_input(
            "Nhập mã cổ phiếu hoặc tên công ty:",
            placeholder="VD: VIC, Vingroup, VCB..."
        )
        
        # Gợi ý
        if search_query:
            suggestions = search_stocks(search_query)
            if suggestions:
                st.markdown("**💡 Gợi ý:**")
                for suggestion in suggestions:
                    if st.button(f"{suggestion['code']} - {suggestion['name']}", key=f"suggest_{suggestion['code']}"):
                        st.session_state.selected_symbol = suggestion['code']
                        st.rerun()
        
        # Danh sách cổ phiếu phổ biến
        st.markdown("### 📈 Cổ phiếu phổ biến")
        for code, name in list(POPULAR_STOCKS.items())[:10]:
            if st.button(f"{code} - {name}", key=f"popular_{code}"):
                st.session_state.selected_symbol = code
                st.rerun()
        
        # Thông tin API
        st.markdown("### ℹ️ Thông tin")
        st.info("""
        **API Status:** 
        - Endpoint: http://localhost:8501
        - Dữ liệu: 15+ năm lịch sử
        - Cập nhật: Real-time
        """)
    
    # Main content
    if 'selected_symbol' in st.session_state:
        symbol = st.session_state.selected_symbol
    else:
        symbol = None
    
    if not symbol:
        st.markdown("""
        <div class="search-container">
            <h2>🎯 Chọn cổ phiếu để bắt đầu</h2>
            <p>Nhập mã cổ phiếu hoặc tên công ty vào ô tìm kiếm bên trái, hoặc chọn từ danh sách cổ phiếu phổ biến.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Hiển thị danh sách cổ phiếu
        st.markdown("### 📊 Danh sách cổ phiếu phổ biến")
        cols = st.columns(4)
        for i, (code, name) in enumerate(POPULAR_STOCKS.items()):
            with cols[i % 4]:
                if st.button(f"**{code}**\n{name}", key=f"list_{code}"):
                    st.session_state.selected_symbol = code
                    st.rerun()
        return
    
    # Lấy dữ liệu
    data = get_stock_data(symbol)
    
    if not data:
        st.error("Không thể tải dữ liệu. Vui lòng thử lại.")
        return
    
    # Hiển thị thông tin công ty
    if 'overview' in data and data['overview']:
        overview = data['overview']
        st.markdown(f"""
        <div class="company-info">
            <h2>🏢 {overview.get('company_name', symbol)}</h2>
            <p><strong>Mã cổ phiếu:</strong> {symbol}</p>
            <p><strong>Ngành:</strong> {overview.get('industry', 'N/A')}</p>
            <p><strong>Sàn giao dịch:</strong> {overview.get('exchange', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs cho các loại dữ liệu
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Tổng quan", 
        "📈 Biểu đồ giá", 
        "💰 Tài chính", 
        "📋 Báo cáo", 
        "📊 Phân tích"
    ])
    
    with tab1:
        st.markdown("### 📊 Thông tin tổng quan")
        
        # Thông tin giá hiện tại
        if 'overview' in data and data['overview']:
            overview = data['overview']
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                current_price = overview.get('current_price', 0)
                change = overview.get('change', 0)
                change_percent = overview.get('change_percent', 0)
                
                st.metric(
                    "Giá hiện tại",
                    format_currency(current_price),
                    f"{change:+.0f} ({change_percent:+.2f}%)"
                )
            
            with col2:
                st.metric(
                    "Vốn hóa thị trường",
                    format_currency(overview.get('market_cap', 0))
                )
            
            with col3:
                st.metric(
                    "Khối lượng giao dịch",
                    format_currency(overview.get('volume', 0))
                )
            
            with col4:
                st.metric(
                    "P/E Ratio",
                    f"{overview.get('pe_ratio', 0):.2f}"
                )
        
        # Thông tin tài chính cơ bản
        if 'financial_data' in data and data['financial_data']:
            st.markdown("### 💰 Chỉ số tài chính")
            
            financial = data['financial_data']
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Doanh thu",
                    format_currency(financial.get('revenue', 0))
                )
            
            with col2:
                st.metric(
                    "Lợi nhuận",
                    format_currency(financial.get('net_income', 0))
                )
            
            with col3:
                st.metric(
                    "Tổng tài sản",
                    format_currency(financial.get('total_assets', 0))
                )
            
            with col4:
                st.metric(
                    "Tổng nợ",
                    format_currency(financial.get('total_debt', 0))
                )
    
    with tab2:
        st.markdown("### 📈 Biểu đồ giá cổ phiếu")
        
        if 'historical_data' in data and data['historical_data']:
            # Biểu đồ giá
            price_chart = create_price_chart(data['historical_data'])
            if price_chart:
                st.plotly_chart(price_chart, use_container_width=True)
            
            # Biểu đồ khối lượng
            volume_chart = create_volume_chart(data['historical_data'])
            if volume_chart:
                st.plotly_chart(volume_chart, use_container_width=True)
        else:
            st.warning("Không có dữ liệu biểu đồ")
    
    with tab3:
        st.markdown("### 💰 Dữ liệu tài chính chi tiết")
        
        if 'financial_data' in data and data['financial_data']:
            financial = data['financial_data']
            
            # Bảng cân đối kế toán
            if 'balance_sheet' in financial:
                st.markdown("#### 📋 Bảng cân đối kế toán")
                balance_df = pd.DataFrame(financial['balance_sheet'])
                st.dataframe(balance_df, use_container_width=True)
            
            # Báo cáo kết quả kinh doanh
            if 'income_statement' in financial:
                st.markdown("#### 📊 Báo cáo kết quả kinh doanh")
                income_df = pd.DataFrame(financial['income_statement'])
                st.dataframe(income_df, use_container_width=True)
            
            # Báo cáo lưu chuyển tiền tệ
            if 'cash_flow' in financial:
                st.markdown("#### 💸 Báo cáo lưu chuyển tiền tệ")
                cashflow_df = pd.DataFrame(financial['cash_flow'])
                st.dataframe(cashflow_df, use_container_width=True)
        else:
            st.warning("Không có dữ liệu tài chính")
    
    with tab4:
        st.markdown("### 📋 Dữ liệu lịch sử")
        
        if 'historical_data' in data and data['historical_data']:
            hist_data = data['historical_data']
            
            if 'data' in hist_data:
                df = pd.DataFrame(hist_data['data'])
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date', ascending=False)
                
                # Hiển thị 100 bản ghi gần nhất
                st.dataframe(df.head(100), use_container_width=True)
            else:
                st.warning("Không có dữ liệu lịch sử")
        else:
            st.warning("Không có dữ liệu lịch sử")
    
    with tab5:
        st.markdown("### 📊 Phân tích và đánh giá")
        
        # Thông tin metadata
        if 'metadata' in data:
            metadata = data['metadata']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📈 Thống kê dữ liệu")
                st.info(f"""
                - **Số bản ghi lịch sử:** {metadata.get('total_records', 0):,}
                - **Khoảng thời gian:** {metadata.get('date_range', 'N/A')}
                - **Thời gian cập nhật:** {metadata.get('last_updated', 'N/A')}
                - **Nguồn dữ liệu:** {metadata.get('data_source', 'N/A')}
                """)
            
            with col2:
                st.markdown("#### ⚡ Hiệu suất API")
                st.info(f"""
                - **Thời gian xử lý:** {metadata.get('processing_time', 0):.2f}s
                - **Trạng thái:** {metadata.get('status', 'N/A')}
                - **Phiên bản API:** {metadata.get('api_version', 'N/A')}
                """)
        
        # Gợi ý phân tích
        st.markdown("#### 🤖 Gợi ý phân tích AI")
        st.success("""
        **Dữ liệu đã sẵn sàng cho phân tích AI:**
        - ✅ Dữ liệu lịch sử đầy đủ (15+ năm)
        - ✅ Báo cáo tài chính chi tiết
        - ✅ Cấu trúc JSON chuẩn hóa
        - ✅ Metadata đầy đủ
        - ✅ Định dạng thân thiện với AI
        """)

if __name__ == "__main__":
    main()
