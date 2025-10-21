"""
TA (Technical Analysis) Analyzer - VNStock Data Collector
Phân tích kỹ thuật và vẽ biểu đồ cho cổ phiếu Việt Nam
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
import logging
import os

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_ta_indicators(symbol: str, period_days: int = 365) -> Dict[str, Any]:
    """
    Tính toán các chỉ báo kỹ thuật (TA) cho một mã cổ phiếu
    
    Args:
        symbol: Mã cổ phiếu (VD: FPT, VIC, VCB)
        period_days: Số ngày lấy dữ liệu (mặc định 365 ngày = 1 năm)
    
    Returns:
        Dictionary chứa:
        - Dữ liệu OHLCV
        - Các chỉ báo: MA(50), MA(200), RSI(14)
        - Metadata
    """
    try:
        from vnstock import Vnstock
        
        logger.info(f"Bắt đầu phân tích TA cho mã {symbol}")
        
        # Khởi tạo vnstock client
        stock = Vnstock().stock(symbol=symbol, source='VCI')
        
        # Tính toán khoảng thời gian
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=period_days)).strftime("%Y-%m-%d")
        
        logger.info(f"Lấy dữ liệu OHLCV từ {start_date} đến {end_date}")
        
        # Lấy dữ liệu OHLCV
        df = stock.quote.history(start=start_date, end=end_date)
        
        if df.empty:
            logger.warning(f"Không có dữ liệu cho mã {symbol}")
            return {
                "symbol": symbol,
                "error": "Không có dữ liệu",
                "data": None
            }
        
        # Đổi tên cột để phù hợp với mplfinance
        df = df.rename(columns={
            'time': 'Date',
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        })
        
        # Set Date làm index
        df.set_index('Date', inplace=True)
        df.index = pd.to_datetime(df.index)
        
        # Chuyển đổi giá từ nghìn đồng sang VND đầy đủ
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = df[col] * 1000
        
        logger.info(f"Lấy được {len(df)} ngày giao dịch")
        
        # === Tính toán các chỉ báo kỹ thuật ===
        
        # 1. Moving Averages (MA)
        logger.info("Tính toán Moving Averages...")
        df['MA50'] = df['Close'].rolling(window=50).mean()
        df['MA200'] = df['Close'].rolling(window=200).mean()
        
        # 2. RSI (Relative Strength Index)
        logger.info("Tính toán RSI(14)...")
        df['RSI'] = calculate_rsi(df['Close'], period=14)
        
        # 3. MACD (Moving Average Convergence Divergence)
        logger.info("Tính toán MACD...")
        df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = calculate_macd(df['Close'])
        
        # 4. Bollinger Bands
        logger.info("Tính toán Bollinger Bands...")
        df['BB_Upper'], df['BB_Middle'], df['BB_Lower'] = calculate_bollinger_bands(df['Close'])
        
        # 5. Volume MA
        df['Volume_MA'] = df['Volume'].rolling(window=20).mean()
        
        # Tạo kết quả
        result = {
            "symbol": symbol,
            "period": {
                "start_date": start_date,
                "end_date": end_date,
                "total_days": period_days,
                "trading_days": len(df)
            },
            "data": df,
            "indicators": {
                "MA50": {
                    "latest_value": float(df['MA50'].iloc[-1]) if not pd.isna(df['MA50'].iloc[-1]) else None,
                    "description": "Moving Average 50 ngày"
                },
                "MA200": {
                    "latest_value": float(df['MA200'].iloc[-1]) if not pd.isna(df['MA200'].iloc[-1]) else None,
                    "description": "Moving Average 200 ngày"
                },
                "RSI": {
                    "latest_value": float(df['RSI'].iloc[-1]) if not pd.isna(df['RSI'].iloc[-1]) else None,
                    "description": "Relative Strength Index (14 ngày)",
                    "signal": get_rsi_signal(df['RSI'].iloc[-1]) if not pd.isna(df['RSI'].iloc[-1]) else None
                },
                "MACD": {
                    "latest_value": float(df['MACD'].iloc[-1]) if not pd.isna(df['MACD'].iloc[-1]) else None,
                    "signal_value": float(df['MACD_Signal'].iloc[-1]) if not pd.isna(df['MACD_Signal'].iloc[-1]) else None,
                    "histogram": float(df['MACD_Hist'].iloc[-1]) if not pd.isna(df['MACD_Hist'].iloc[-1]) else None,
                    "description": "Moving Average Convergence Divergence"
                }
            },
            "current_price": float(df['Close'].iloc[-1]),
            "price_unit": "VND",
            "calculation_date": datetime.now().isoformat()
        }
        
        logger.info(f"Hoàn thành tính toán TA cho {symbol}")
        return result
        
    except Exception as e:
        logger.error(f"Lỗi khi tính toán TA cho {symbol}: {str(e)}")
        return {
            "symbol": symbol,
            "error": str(e),
            "data": None
        }


def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """
    Tính toán RSI (Relative Strength Index)
    
    Args:
        prices: Series giá đóng cửa
        period: Chu kỳ tính RSI (mặc định 14)
    
    Returns:
        Series chứa giá trị RSI
    """
    # Tính delta
    delta = prices.diff()
    
    # Tách gain và loss
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    # Tính RS và RSI
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Tính toán MACD (Moving Average Convergence Divergence)
    
    Args:
        prices: Series giá đóng cửa
        fast: Chu kỳ EMA nhanh (mặc định 12)
        slow: Chu kỳ EMA chậm (mặc định 26)
        signal: Chu kỳ Signal line (mặc định 9)
    
    Returns:
        Tuple (MACD line, Signal line, Histogram)
    """
    # Tính EMA
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    
    # MACD line
    macd_line = ema_fast - ema_slow
    
    # Signal line
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    
    # Histogram
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram


def calculate_bollinger_bands(prices: pd.Series, period: int = 20, std_dev: int = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Tính toán Bollinger Bands
    
    Args:
        prices: Series giá đóng cửa
        period: Chu kỳ (mặc định 20)
        std_dev: Số độ lệch chuẩn (mặc định 2)
    
    Returns:
        Tuple (Upper band, Middle band, Lower band)
    """
    # Middle band (SMA)
    middle_band = prices.rolling(window=period).mean()
    
    # Standard deviation
    std = prices.rolling(window=period).std()
    
    # Upper và Lower bands
    upper_band = middle_band + (std * std_dev)
    lower_band = middle_band - (std * std_dev)
    
    return upper_band, middle_band, lower_band


def get_rsi_signal(rsi_value: float) -> str:
    """
    Diễn giải tín hiệu RSI
    
    Args:
        rsi_value: Giá trị RSI
    
    Returns:
        Tín hiệu: oversold, neutral, overbought
    """
    if rsi_value < 30:
        return "oversold"  # Quá bán
    elif rsi_value > 70:
        return "overbought"  # Quá mua
    else:
        return "neutral"  # Trung tính


def plot_technical_chart(symbol: str, period_days: int = 365, save_path: str = "charts") -> Dict[str, Any]:
    """
    Vẽ biểu đồ kỹ thuật với candlestick và các chỉ báo
    
    Args:
        symbol: Mã cổ phiếu
        period_days: Số ngày lấy dữ liệu
        save_path: Thư mục lưu biểu đồ
    
    Returns:
        Dictionary chứa thông tin biểu đồ và đường dẫn file
    """
    try:
        import mplfinance as mpf
        
        logger.info(f"Bắt đầu vẽ biểu đồ cho mã {symbol}")
        
        # Tính toán các chỉ báo
        ta_result = calculate_ta_indicators(symbol, period_days)
        
        if ta_result.get("error") or ta_result.get("data") is None:
            return {
                "success": False,
                "error": ta_result.get("error", "Không có dữ liệu")
            }
        
        df = ta_result["data"]
        
        # Tạo thư mục lưu biểu đồ
        os.makedirs(save_path, exist_ok=True)
        
        # Tạo các addplot cho MA, RSI, MACD
        apds = []
        
        # MA50 và MA200
        apds.append(mpf.make_addplot(df['MA50'], color='blue', width=1.5, label='MA50'))
        apds.append(mpf.make_addplot(df['MA200'], color='red', width=1.5, label='MA200'))
        
        # Bollinger Bands
        apds.append(mpf.make_addplot(df['BB_Upper'], color='gray', width=0.7, linestyle='--', label='BB Upper'))
        apds.append(mpf.make_addplot(df['BB_Lower'], color='gray', width=0.7, linestyle='--', label='BB Lower'))
        
        # RSI (panel riêng)
        apds.append(mpf.make_addplot(df['RSI'], panel=2, color='purple', ylabel='RSI', label='RSI(14)'))
        
        # Thêm đường RSI 30 và 70
        apds.append(mpf.make_addplot([30]*len(df), panel=2, color='green', linestyle='--', width=0.7))
        apds.append(mpf.make_addplot([70]*len(df), panel=2, color='red', linestyle='--', width=0.7))
        
        # MACD (panel riêng)
        apds.append(mpf.make_addplot(df['MACD'], panel=3, color='blue', ylabel='MACD', label='MACD'))
        apds.append(mpf.make_addplot(df['MACD_Signal'], panel=3, color='red', label='Signal'))
        apds.append(mpf.make_addplot(df['MACD_Hist'], panel=3, type='bar', color='gray', alpha=0.5, label='Histogram'))
        
        # Cấu hình style
        mc = mpf.make_marketcolors(
            up='green', down='red',
            edge='inherit',
            wick='inherit',
            volume='in'
        )
        
        s = mpf.make_mpf_style(
            marketcolors=mc,
            gridstyle='-',
            y_on_right=False
        )
        
        # Tạo tên file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{symbol}_TA_{timestamp}.png"
        filepath = os.path.join(save_path, filename)
        
        # Vẽ biểu đồ
        logger.info(f"Vẽ biểu đồ và lưu tại {filepath}")
        
        mpf.plot(
            df,
            type='candle',
            style=s,
            title=f'{symbol} - Technical Analysis',
            ylabel='Price (VND)',
            ylabel_lower='Volume',
            volume=True,
            addplot=apds,
            figsize=(16, 12),
            panel_ratios=(3, 1, 1, 1),
            savefig=filepath,
            tight_layout=True
        )
        
        logger.info(f"Hoàn thành vẽ biểu đồ cho {symbol}")
        
        return {
            "success": True,
            "symbol": symbol,
            "filepath": filepath,
            "filename": filename,
            "indicators": ta_result["indicators"],
            "period": ta_result["period"],
            "current_price": ta_result["current_price"],
            "chart_info": {
                "candlestick": "Japanese Candlestick Chart",
                "indicators": [
                    "MA(50) - Moving Average 50 days",
                    "MA(200) - Moving Average 200 days",
                    "Bollinger Bands (20, 2)",
                    "RSI(14) - Relative Strength Index",
                    "MACD(12, 26, 9) - Moving Average Convergence Divergence"
                ],
                "panels": [
                    "Panel 1: Candlestick + MA + Bollinger Bands",
                    "Panel 2: RSI",
                    "Panel 3: MACD",
                    "Panel 4: Volume"
                ]
            }
        }
        
    except ImportError as e:
        logger.error("Thiếu thư viện mplfinance. Cài đặt: pip install mplfinance")
        return {
            "success": False,
            "error": "Thiếu thư viện mplfinance. Vui lòng cài đặt: pip install mplfinance"
        }
    except Exception as e:
        logger.error(f"Lỗi khi vẽ biểu đồ cho {symbol}: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def get_ta_analysis(symbol: str, period_days: int = 365) -> Dict[str, Any]:
    """
    Phân tích kỹ thuật toàn diện với diễn giải
    
    Args:
        symbol: Mã cổ phiếu
        period_days: Số ngày lấy dữ liệu
    
    Returns:
        Dictionary chứa phân tích và diễn giải
    """
    try:
        logger.info(f"Phân tích TA toàn diện cho mã {symbol}")
        
        # Tính toán các chỉ báo
        ta_result = calculate_ta_indicators(symbol, period_days)
        
        if ta_result.get("error"):
            return ta_result
        
        df = ta_result["data"]
        indicators = ta_result["indicators"]
        
        # Diễn giải các chỉ báo
        analysis = {
            "symbol": symbol,
            "analysis_date": datetime.now().isoformat(),
            "current_price": ta_result["current_price"],
            "period": ta_result["period"],
            "indicators_analysis": {},
            "signals": [],
            "overall_trend": None
        }
        
        # === Phân tích MA ===
        ma50 = indicators["MA50"]["latest_value"]
        ma200 = indicators["MA200"]["latest_value"]
        current_price = ta_result["current_price"]
        
        if ma50 and ma200:
            analysis["indicators_analysis"]["Moving_Averages"] = {
                "MA50": ma50,
                "MA200": ma200,
                "price_vs_MA50": "above" if current_price > ma50 else "below",
                "price_vs_MA200": "above" if current_price > ma200 else "below",
                "golden_cross": ma50 > ma200,
                "interpretation": ""
            }
            
            if ma50 > ma200:
                analysis["indicators_analysis"]["Moving_Averages"]["interpretation"] = "Golden Cross - Xu hướng tăng dài hạn"
                analysis["signals"].append("BULLISH: Golden Cross detected")
            else:
                analysis["indicators_analysis"]["Moving_Averages"]["interpretation"] = "Death Cross - Xu hướng giảm dài hạn"
                analysis["signals"].append("BEARISH: Death Cross detected")
        
        # === Phân tích RSI ===
        rsi = indicators["RSI"]["latest_value"]
        rsi_signal = indicators["RSI"]["signal"]
        
        if rsi:
            analysis["indicators_analysis"]["RSI"] = {
                "value": rsi,
                "signal": rsi_signal,
                "interpretation": ""
            }
            
            if rsi_signal == "oversold":
                analysis["indicators_analysis"]["RSI"]["interpretation"] = "Quá bán - Có thể sắp tăng"
                analysis["signals"].append("BULLISH: RSI Oversold")
            elif rsi_signal == "overbought":
                analysis["indicators_analysis"]["RSI"]["interpretation"] = "Quá mua - Có thể sắp giảm"
                analysis["signals"].append("BEARISH: RSI Overbought")
            else:
                analysis["indicators_analysis"]["RSI"]["interpretation"] = "Trung tính"
        
        # === Phân tích MACD ===
        macd = indicators["MACD"]["latest_value"]
        macd_signal = indicators["MACD"]["signal_value"]
        macd_hist = indicators["MACD"]["histogram"]
        
        if macd and macd_signal and macd_hist:
            analysis["indicators_analysis"]["MACD"] = {
                "macd": macd,
                "signal": macd_signal,
                "histogram": macd_hist,
                "bullish": macd > macd_signal,
                "interpretation": ""
            }
            
            if macd > macd_signal and macd_hist > 0:
                analysis["indicators_analysis"]["MACD"]["interpretation"] = "Tín hiệu tăng - MACD trên Signal"
                analysis["signals"].append("BULLISH: MACD above Signal")
            elif macd < macd_signal and macd_hist < 0:
                analysis["indicators_analysis"]["MACD"]["interpretation"] = "Tín hiệu giảm - MACD dưới Signal"
                analysis["signals"].append("BEARISH: MACD below Signal")
        
        # === Đánh giá xu hướng tổng thể ===
        bullish_signals = len([s for s in analysis["signals"] if "BULLISH" in s])
        bearish_signals = len([s for s in analysis["signals"] if "BEARISH" in s])
        
        if bullish_signals > bearish_signals:
            analysis["overall_trend"] = "BULLISH"
            analysis["trend_interpretation"] = "Xu hướng tăng - Nhiều tín hiệu mua"
        elif bearish_signals > bullish_signals:
            analysis["overall_trend"] = "BEARISH"
            analysis["trend_interpretation"] = "Xu hướng giảm - Nhiều tín hiệu bán"
        else:
            analysis["overall_trend"] = "NEUTRAL"
            analysis["trend_interpretation"] = "Trung tính - Tín hiệu không rõ ràng"
        
        logger.info(f"Hoàn thành phân tích TA cho {symbol}")
        return analysis
        
    except Exception as e:
        logger.error(f"Lỗi khi phân tích TA cho {symbol}: {str(e)}")
        return {
            "symbol": symbol,
            "error": str(e)
        }


if __name__ == "__main__":
    # Test với mã FPT
    symbol = "FPT"
    
    print(f"\n{'='*70}")
    print(f"PHÂN TÍCH KỸ THUẬT (TA) - {symbol}")
    print('='*70)
    
    # 1. Tính toán các chỉ báo
    print("\n📊 1. Tính toán các chỉ báo TA...")
    ta_result = calculate_ta_indicators(symbol, period_days=365)
    
    if not ta_result.get("error"):
        print(f"✅ Lấy được {ta_result['period']['trading_days']} ngày giao dịch")
        print(f"   Giá hiện tại: {ta_result['current_price']:,.0f} VND")
        print(f"\n   Các chỉ báo:")
        for name, indicator in ta_result['indicators'].items():
            if indicator.get('latest_value'):
                print(f"   - {name}: {indicator['latest_value']:.2f}")
                if indicator.get('signal'):
                    print(f"     Signal: {indicator['signal']}")
    
    # 2. Phân tích TA với diễn giải
    print("\n💡 2. Phân tích TA với diễn giải...")
    analysis = get_ta_analysis(symbol, period_days=365)
    
    if not analysis.get("error"):
        print(f"   Xu hướng tổng thể: {analysis['overall_trend']}")
        print(f"   Diễn giải: {analysis['trend_interpretation']}")
        print(f"\n   Tín hiệu:")
        for signal in analysis['signals']:
            print(f"   - {signal}")
    
    # 3. Vẽ biểu đồ
    print("\n📈 3. Vẽ biểu đồ kỹ thuật...")
    chart_result = plot_technical_chart(symbol, period_days=365)
    
    if chart_result.get("success"):
        print(f"✅ Biểu đồ đã được lưu tại: {chart_result['filepath']}")
        print(f"   Các chỉ báo trên biểu đồ:")
        for indicator in chart_result['chart_info']['indicators']:
            print(f"   - {indicator}")
    else:
        print(f"❌ Lỗi: {chart_result.get('error')}")

