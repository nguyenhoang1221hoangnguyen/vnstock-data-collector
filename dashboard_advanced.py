"""
VNStock Dashboard Advanced - Trực quan hóa dữ liệu cổ phiếu nâng cao
Tính năng: Technical Indicators, Multi-stock Comparison, FA/TA Analysis, Watchlist, Alerts
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from vnstock import Vnstock
import logging
import json
import requests

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cấu hình trang
st.set_page_config(
    page_title="VNStock Advanced Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []
if 'price_alerts' not in st.session_state:
    st.session_state.price_alerts = []
if 'selected_stocks' not in st.session_state:
    st.session_state.selected_stocks = []

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
    .watchlist-item {
        background-color: #f0f2f6;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        margin: 0.2rem 0;
        display: inline-block;
    }
    .alert-badge {
        background-color: #ff4444;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
        font-size: 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)

# ============= Technical Indicators Functions =============

def calculate_ma(df, period):
    """Tính Moving Average"""
    return df['close'].rolling(window=period).mean()

def calculate_ema(df, period):
    """Tính Exponential Moving Average"""
    return df['close'].ewm(span=period, adjust=False).mean()

def calculate_rsi(df, period=14):
    """Tính Relative Strength Index"""
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(df, fast=12, slow=26, signal=9):
    """Tính MACD"""
    ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram

def calculate_bollinger_bands(df, period=20, std_dev=2):
    """Tính Bollinger Bands"""
    ma = df['close'].rolling(window=period).mean()
    std = df['close'].rolling(window=period).std()
    upper_band = ma + (std * std_dev)
    lower_band = ma - (std * std_dev)
    return upper_band, ma, lower_band

# ============= Data Functions =============

def format_currency(value):
    """Format số tiền theo định dạng VND"""
    try:
        if pd.isna(value):
            return "N/A"
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

@st.cache_data(ttl=300)
def get_stock_data(symbol, days=365):
    """Lấy dữ liệu cổ phiếu từ vnstock (cached 5 phút)"""
    try:
        stock = Vnstock().stock(symbol=symbol.upper(), source='VCI')
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        df = stock.quote.history(start=start_date, end=end_date)
        
        if df.empty:
            return None
        
        if 'time' in df.columns:
            df['time'] = pd.to_datetime(df['time'])
        
        return df
        
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu {symbol}: {str(e)}")
        return None

def get_fa_data(symbol):
    """Lấy dữ liệu FA từ API"""
    try:
        response = requests.get(f"http://localhost:8501/stock/{symbol}/fa", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"Lỗi khi lấy FA data: {str(e)}")
        return None

def get_ta_analysis(symbol):
    """Lấy phân tích TA từ API"""
    try:
        response = requests.get(f"http://localhost:8501/stock/{symbol}/ta/analyze", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        logger.error(f"Lỗi khi lấy TA analysis: {str(e)}")
        return None

# ============= Plotting Functions =============

def plot_advanced_chart(df, symbol, indicators):
    """Vẽ biểu đồ nâng cao với indicators"""
    
    # Tạo subplots
    rows = 1
    row_heights = [0.7]
    
    if 'RSI' in indicators:
        rows += 1
        row_heights.append(0.15)
    if 'MACD' in indicators:
        rows += 1
        row_heights.append(0.15)
    
    fig = make_subplots(
        rows=rows, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=row_heights,
        subplot_titles=['Price Chart'] + 
                       (['RSI'] if 'RSI' in indicators else []) +
                       (['MACD'] if 'MACD' in indicators else [])
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df['time'],
            open=df['open'] * 1000,
            high=df['high'] * 1000,
            low=df['low'] * 1000,
            close=df['close'] * 1000,
            name=symbol,
            increasing=dict(line=dict(color='#26a69a'), fillcolor='#26a69a'),
            decreasing=dict(line=dict(color='#ef5350'), fillcolor='#ef5350')
        ),
        row=1, col=1
    )
    
    # Moving Averages
    if 'MA20' in indicators:
        ma20 = calculate_ma(df, 20)
        fig.add_trace(
            go.Scatter(x=df['time'], y=ma20 * 1000, name='MA20',
                      line=dict(color='blue', width=1)),
            row=1, col=1
        )
    
    if 'MA50' in indicators:
        ma50 = calculate_ma(df, 50)
        fig.add_trace(
            go.Scatter(x=df['time'], y=ma50 * 1000, name='MA50',
                      line=dict(color='orange', width=1)),
            row=1, col=1
        )
    
    if 'MA200' in indicators:
        ma200 = calculate_ma(df, 200)
        fig.add_trace(
            go.Scatter(x=df['time'], y=ma200 * 1000, name='MA200',
                      line=dict(color='red', width=1)),
            row=1, col=1
        )
    
    if 'EMA12' in indicators:
        ema12 = calculate_ema(df, 12)
        fig.add_trace(
            go.Scatter(x=df['time'], y=ema12 * 1000, name='EMA12',
                      line=dict(color='purple', width=1, dash='dash')),
            row=1, col=1
        )
    
    # Bollinger Bands
    if 'BB' in indicators:
        upper, middle, lower = calculate_bollinger_bands(df)
        fig.add_trace(
            go.Scatter(x=df['time'], y=upper * 1000, name='BB Upper',
                      line=dict(color='gray', width=1, dash='dot'),
                      showlegend=True),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['time'], y=lower * 1000, name='BB Lower',
                      line=dict(color='gray', width=1, dash='dot'),
                      fill='tonexty', fillcolor='rgba(128,128,128,0.1)',
                      showlegend=True),
            row=1, col=1
        )
    
    current_row = 2
    
    # RSI
    if 'RSI' in indicators:
        rsi = calculate_rsi(df)
        fig.add_trace(
            go.Scatter(x=df['time'], y=rsi, name='RSI', line=dict(color='purple', width=2)),
            row=current_row, col=1
        )
        # RSI levels
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=current_row, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=current_row, col=1)
        fig.update_yaxes(title_text="RSI", row=current_row, col=1)
        current_row += 1
    
    # MACD
    if 'MACD' in indicators:
        macd, signal, histogram = calculate_macd(df)
        fig.add_trace(
            go.Scatter(x=df['time'], y=macd, name='MACD', line=dict(color='blue', width=1)),
            row=current_row, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['time'], y=signal, name='Signal', line=dict(color='red', width=1)),
            row=current_row, col=1
        )
        colors = ['green' if h > 0 else 'red' for h in histogram]
        fig.add_trace(
            go.Bar(x=df['time'], y=histogram, name='Histogram', marker_color=colors),
            row=current_row, col=1
        )
        fig.update_yaxes(title_text="MACD", row=current_row, col=1)
    
    # Update layout
    fig.update_layout(
        title=f'{symbol.upper()} - Technical Analysis',
        title_font=dict(size=24, color='#1f77b4'),
        xaxis_rangeslider_visible=False,
        template='plotly_white',
        height=600 + (200 * (rows - 1)),
        hovermode='x unified',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
    
    return fig

def plot_comparison_chart(data_dict):
    """Vẽ biểu đồ so sánh nhiều mã cổ phiếu"""
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    for idx, (symbol, df) in enumerate(data_dict.items()):
        if df is not None and not df.empty:
            # Normalize về 100 để so sánh
            normalized = (df['close'] / df['close'].iloc[0]) * 100
            
            fig.add_trace(
                go.Scatter(
                    x=df['time'],
                    y=normalized,
                    name=symbol,
                    line=dict(color=colors[idx % len(colors)], width=2)
                )
            )
    
    fig.update_layout(
        title='So sánh hiệu suất (Normalized to 100)',
        title_font=dict(size=20, color='#1f77b4'),
        xaxis_title='Thời gian',
        yaxis_title='Giá trị (base=100)',
        template='plotly_white',
        height=500,
        hovermode='x unified',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

# ============= Alert Functions =============

def check_price_alerts(symbol, current_price):
    """Kiểm tra và trigger alerts"""
    triggered_alerts = []
    
    for alert in st.session_state.price_alerts:
        if alert['symbol'] == symbol:
            if alert['condition'] == 'above' and current_price >= alert['price']:
                triggered_alerts.append(alert)
            elif alert['condition'] == 'below' and current_price <= alert['price']:
                triggered_alerts.append(alert)
    
    return triggered_alerts

# ============= Main Dashboard =============

def main():
    """Hàm chính của dashboard"""
    
    # Header
    st.title("📊 VNStock Advanced Dashboard")
    st.markdown("*Technical Indicators • Multi-Stock Comparison • FA/TA Analysis • Watchlist • Price Alerts*")
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Technical Chart",
        "📊 Multi-Stock Comparison", 
        "🧮 FA/TA Analysis",
        "⭐ Watchlist",
        "🔔 Price Alerts"
    ])
    
    # ========== TAB 1: Technical Chart ==========
    with tab1:
        col_left, col_right = st.columns([1, 3])
        
        with col_left:
            st.subheader("⚙️ Settings")
            
            symbol = st.text_input(
                "Mã cổ phiếu:",
                value="ACB",
                key="tech_symbol"
            ).upper()
            
            time_period = st.selectbox(
                "Khoảng thời gian:",
                options=[30, 90, 180, 365, 730],
                index=3,
                format_func=lambda x: f"{x} ngày" if x < 365 else f"{x//365} năm",
                key="tech_period"
            )
            
            st.markdown("**Technical Indicators:**")
            
            indicators = []
            col1, col2 = st.columns(2)
            
            with col1:
                if st.checkbox("MA20", value=True):
                    indicators.append("MA20")
                if st.checkbox("MA50", value=True):
                    indicators.append("MA50")
                if st.checkbox("MA200"):
                    indicators.append("MA200")
                if st.checkbox("EMA12"):
                    indicators.append("EMA12")
            
            with col2:
                if st.checkbox("RSI", value=True):
                    indicators.append("RSI")
                if st.checkbox("MACD", value=True):
                    indicators.append("MACD")
                if st.checkbox("Bollinger Bands"):
                    indicators.append("BB")
            
            load_btn = st.button("🔄 Load Chart", type="primary", use_container_width=True)
            
            # Add to watchlist button
            if st.button("⭐ Add to Watchlist", use_container_width=True):
                if symbol not in st.session_state.watchlist:
                    st.session_state.watchlist.append(symbol)
                    st.success(f"✅ Added {symbol} to watchlist")
                else:
                    st.info(f"ℹ️ {symbol} already in watchlist")
        
        with col_right:
            if load_btn or symbol:
                with st.spinner(f"⏳ Loading {symbol}..."):
                    df = get_stock_data(symbol, days=time_period)
                
                if df is not None and not df.empty:
                    # Metrics
                    current_price = df['close'].iloc[-1] * 1000
                    prev_price = df['close'].iloc[0] * 1000
                    price_change = current_price - prev_price
                    price_change_pct = (price_change / prev_price) * 100
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "Current Price",
                            f"{current_price:,.0f} VND",
                            f"{price_change:,.0f} ({price_change_pct:.2f}%)"
                        )
                    
                    with col2:
                        st.metric("High", f"{df['high'].max() * 1000:,.0f} VND")
                    
                    with col3:
                        st.metric("Low", f"{df['low'].min() * 1000:,.0f} VND")
                    
                    with col4:
                        st.metric("Avg Volume", format_volume(df['volume'].mean()))
                    
                    # Check alerts
                    triggered = check_price_alerts(symbol, current_price)
                    if triggered:
                        for alert in triggered:
                            st.warning(f"🔔 Alert! {symbol} is {alert['condition']} {alert['price']:,.0f} VND")
                    
                    # Chart
                    fig = plot_advanced_chart(df, symbol, indicators)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Quick Stats
                    with st.expander("📊 Quick Statistics"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if 'RSI' in indicators:
                                rsi_current = calculate_rsi(df).iloc[-1]
                                st.metric("RSI (14)", f"{rsi_current:.2f}")
                                if rsi_current > 70:
                                    st.warning("⚠️ Overbought")
                                elif rsi_current < 30:
                                    st.success("✅ Oversold")
                        
                        with col2:
                            if 'MACD' in indicators:
                                macd, signal, _ = calculate_macd(df)
                                macd_current = macd.iloc[-1]
                                signal_current = signal.iloc[-1]
                                st.metric("MACD", f"{macd_current:.2f}")
                                if macd_current > signal_current:
                                    st.success("✅ Bullish")
                                else:
                                    st.warning("⚠️ Bearish")
                else:
                    st.error(f"❌ Cannot load data for {symbol}")
    
    # ========== TAB 2: Multi-Stock Comparison ==========
    with tab2:
        st.subheader("📊 Compare Multiple Stocks")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            symbols_input = st.text_input(
                "Enter stock symbols (comma separated):",
                value="ACB,VCB,TCB",
                help="Example: ACB,VCB,TCB,MBB"
            )
        
        with col2:
            compare_period = st.selectbox(
                "Time period:",
                options=[30, 90, 180, 365],
                index=2,
                format_func=lambda x: f"{x} days",
                key="compare_period"
            )
        
        compare_btn = st.button("📈 Compare", type="primary", use_container_width=True)
        
        if compare_btn or symbols_input:
            symbols = [s.strip().upper() for s in symbols_input.split(',') if s.strip()]
            
            if len(symbols) > 6:
                st.warning("⚠️ Maximum 6 stocks for comparison")
                symbols = symbols[:6]
            
            with st.spinner("⏳ Loading data..."):
                data_dict = {}
                stats_dict = {}
                
                for symbol in symbols:
                    df = get_stock_data(symbol, days=compare_period)
                    if df is not None and not df.empty:
                        data_dict[symbol] = df
                        
                        # Calculate stats
                        start_price = df['close'].iloc[0]
                        end_price = df['close'].iloc[-1]
                        change_pct = ((end_price - start_price) / start_price) * 100
                        
                        stats_dict[symbol] = {
                            'start': start_price * 1000,
                            'end': end_price * 1000,
                            'change': change_pct,
                            'high': df['high'].max() * 1000,
                            'low': df['low'].min() * 1000,
                            'avg_volume': df['volume'].mean()
                        }
            
            if data_dict:
                # Comparison chart
                fig = plot_comparison_chart(data_dict)
                st.plotly_chart(fig, use_container_width=True)
                
                # Stats table
                st.subheader("📊 Performance Summary")
                
                cols = st.columns(len(stats_dict))
                for idx, (symbol, stats) in enumerate(stats_dict.items()):
                    with cols[idx]:
                        st.markdown(f"**{symbol}**")
                        st.metric(
                            "Change",
                            f"{stats['change']:.2f}%",
                            delta=f"{stats['change']:.2f}%"
                        )
                        st.write(f"High: {stats['high']:,.0f}")
                        st.write(f"Low: {stats['low']:,.0f}")
                        st.write(f"Vol: {format_volume(stats['avg_volume'])}")
            else:
                st.error("❌ No data available for selected stocks")
    
    # ========== TAB 3: FA/TA Analysis ==========
    with tab3:
        st.subheader("🧮 Fundamental & Technical Analysis")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            analysis_symbol = st.text_input(
                "Stock Symbol:",
                value="ACB",
                key="analysis_symbol"
            ).upper()
            
            analysis_type = st.radio(
                "Analysis Type:",
                options=["Fundamental (FA)", "Technical (TA)", "Both"],
                index=2
            )
            
            analyze_btn = st.button("🔍 Analyze", type="primary", use_container_width=True)
        
        with col2:
            if analyze_btn or analysis_symbol:
                with st.spinner(f"⏳ Analyzing {analysis_symbol}..."):
                    
                    if analysis_type in ["Fundamental (FA)", "Both"]:
                        st.markdown("### 📊 Fundamental Analysis")
                        fa_data = get_fa_data(analysis_symbol)
                        
                        if fa_data and fa_data.get('success'):
                            try:
                                ratios = fa_data.get('data', {}).get('ratios', {})
                                interpretation = fa_data.get('data', {}).get('interpretation', {})
                                
                                col1, col2, col3, col4 = st.columns(4)
                                
                                with col1:
                                    pe = ratios.get('PE')
                                    st.metric("P/E Ratio", f"{pe:.2f}" if pe else "N/A")
                                
                                with col2:
                                    roe = ratios.get('ROE')
                                    st.metric("ROE", f"{roe:.2f}%" if roe else "N/A")
                                
                                with col3:
                                    npm = ratios.get('net_profit_margin')
                                    st.metric("NPM", f"{npm:.2f}%" if npm else "N/A")
                                
                                with col4:
                                    de = ratios.get('DE')
                                    st.metric("D/E", f"{de:.2f}" if de else "N/A")
                                
                                if interpretation:
                                    st.markdown("**Interpretation:**")
                                    st.info(interpretation.get('summary', 'No interpretation available'))
                            except Exception as e:
                                st.error(f"❌ Error parsing FA data: {str(e)}")
                                logger.error(f"FA data parsing error: {str(e)}")
                        else:
                            st.warning("⚠️ FA data not available (API may be offline)")
                    
                    if analysis_type in ["Technical (TA)", "Both"]:
                        st.markdown("### 📈 Technical Analysis")
                        ta_data = get_ta_analysis(analysis_symbol)
                        
                        if ta_data and ta_data.get('success'):
                            try:
                                analysis = ta_data.get('data', {})
                                
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.markdown("**Trend Analysis:**")
                                    trend_found = False
                                    for signal in analysis.get('signals', []):
                                        if signal.get('type') == 'trend':
                                            st.write(f"• {signal.get('indicator', 'N/A')}: {signal.get('signal', 'N/A')}")
                                            trend_found = True
                                    if not trend_found:
                                        st.write("No trend signals available")
                                
                                with col2:
                                    st.markdown("**Momentum:**")
                                    momentum_found = False
                                    for signal in analysis.get('signals', []):
                                        if signal.get('type') == 'momentum':
                                            st.write(f"• {signal.get('indicator', 'N/A')}: {signal.get('signal', 'N/A')}")
                                            momentum_found = True
                                    if not momentum_found:
                                        st.write("No momentum signals available")
                                
                                st.markdown("**Overall Signal:**")
                                overall = analysis.get('overall_signal', 'Neutral')
                                if overall == 'Bullish':
                                    st.success(f"✅ {overall}")
                                elif overall == 'Bearish':
                                    st.error(f"⚠️ {overall}")
                                else:
                                    st.info(f"ℹ️ {overall}")
                            except Exception as e:
                                st.error(f"❌ Error parsing TA data: {str(e)}")
                                logger.error(f"TA data parsing error: {str(e)}")
                        else:
                            st.warning("⚠️ TA data not available (API may be offline)")
    
    # ========== TAB 4: Watchlist ==========
    with tab4:
        st.subheader("⭐ Your Watchlist")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            new_symbol = st.text_input("Add new stock:", key="watchlist_input")
        
        with col2:
            if st.button("➕ Add", use_container_width=True):
                if new_symbol and new_symbol.upper() not in st.session_state.watchlist:
                    st.session_state.watchlist.append(new_symbol.upper())
                    st.success(f"✅ Added {new_symbol.upper()}")
                    st.rerun()
        
        if st.session_state.watchlist:
            # Display watchlist with real-time prices
            watchlist_data = []
            
            for symbol in st.session_state.watchlist:
                df = get_stock_data(symbol, days=7)
                if df is not None and not df.empty:
                    current_price = df['close'].iloc[-1] * 1000
                    prev_price = df['close'].iloc[0] * 1000
                    change_pct = ((current_price - prev_price) / prev_price) * 100
                    
                    watchlist_data.append({
                        'Symbol': symbol,
                        'Price': f"{current_price:,.0f}",
                        'Change (%)': f"{change_pct:.2f}%",
                        'Volume': format_volume(df['volume'].iloc[-1])
                    })
            
            if watchlist_data:
                df_watchlist = pd.DataFrame(watchlist_data)
                st.dataframe(df_watchlist, use_container_width=True, hide_index=True)
                
                # Remove from watchlist
                st.markdown("**Remove from watchlist:**")
                cols = st.columns(len(st.session_state.watchlist))
                for idx, symbol in enumerate(st.session_state.watchlist):
                    with cols[idx]:
                        if st.button(f"❌ {symbol}", key=f"remove_{symbol}"):
                            st.session_state.watchlist.remove(symbol)
                            st.rerun()
        else:
            st.info("📝 Your watchlist is empty. Add some stocks to track!")
    
    # ========== TAB 5: Price Alerts ==========
    with tab5:
        st.subheader("🔔 Price Alerts")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            alert_symbol = st.text_input("Stock Symbol:", key="alert_symbol")
        
        with col2:
            alert_condition = st.selectbox("Condition:", ["above", "below"])
        
        with col3:
            alert_price = st.number_input("Price (VND):", min_value=0, step=1000, value=25000)
        
        with col4:
            st.write("")  # Spacer
            st.write("")
            if st.button("➕ Add Alert", use_container_width=True):
                if alert_symbol:
                    new_alert = {
                        'symbol': alert_symbol.upper(),
                        'condition': alert_condition,
                        'price': alert_price,
                        'created': datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    st.session_state.price_alerts.append(new_alert)
                    st.success(f"✅ Alert added: {alert_symbol.upper()} {alert_condition} {alert_price:,.0f} VND")
                    st.rerun()
        
        # Display alerts
        if st.session_state.price_alerts:
            st.markdown("### Active Alerts")
            
            for idx, alert in enumerate(st.session_state.price_alerts):
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"""
                    **{alert['symbol']}** - Alert when price goes **{alert['condition']} {alert['price']:,.0f} VND**
                    <br>*Created: {alert['created']}*
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("🗑️ Delete", key=f"del_alert_{idx}"):
                        st.session_state.price_alerts.pop(idx)
                        st.rerun()
                
                st.markdown("---")
        else:
            st.info("📝 No active alerts. Create one to get notified!")

if __name__ == "__main__":
    main()

