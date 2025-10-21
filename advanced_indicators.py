"""
Advanced Technical Indicators - VNStock Enhancement
Các chỉ báo kỹ thuật nâng cao: Ichimoku, ADX, Stochastic, OBV, ATR, etc.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


# ============= TREND INDICATORS =============

def calculate_ichimoku(df: pd.DataFrame) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Tính toán Ichimoku Cloud
    
    Returns:
        Tuple (Tenkan-sen, Kijun-sen, Senkou Span A, Senkou Span B, Chikou Span)
    """
    # Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2
    high_9 = df['High'].rolling(window=9).max()
    low_9 = df['Low'].rolling(window=9).min()
    tenkan_sen = (high_9 + low_9) / 2
    
    # Kijun-sen (Base Line): (26-period high + 26-period low)/2
    high_26 = df['High'].rolling(window=26).max()
    low_26 = df['Low'].rolling(window=26).min()
    kijun_sen = (high_26 + low_26) / 2
    
    # Senkou Span A (Leading Span A): (Tenkan-sen + Kijun-sen)/2, plotted 26 periods ahead
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)
    
    # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2, plotted 26 periods ahead
    high_52 = df['High'].rolling(window=52).max()
    low_52 = df['Low'].rolling(window=52).min()
    senkou_span_b = ((high_52 + low_52) / 2).shift(26)
    
    # Chikou Span (Lagging Span): Close price plotted 26 periods in the past
    chikou_span = df['Close'].shift(-26)
    
    return tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span


def calculate_adx(df: pd.DataFrame, period: int = 14) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Tính toán ADX (Average Directional Index)
    
    Args:
        df: DataFrame với columns High, Low, Close
        period: Chu kỳ (mặc định 14)
    
    Returns:
        Tuple (ADX, +DI, -DI)
    """
    # Calculate True Range
    high_low = df['High'] - df['Low']
    high_close = abs(df['High'] - df['Close'].shift())
    low_close = abs(df['Low'] - df['Close'].shift())
    
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    # Calculate Directional Movement
    up_move = df['High'] - df['High'].shift()
    down_move = df['Low'].shift() - df['Low']
    
    plus_dm = pd.Series(0, index=df.index)
    minus_dm = pd.Series(0, index=df.index)
    
    plus_dm[(up_move > down_move) & (up_move > 0)] = up_move
    minus_dm[(down_move > up_move) & (down_move > 0)] = down_move
    
    # Calculate Directional Indicators
    plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr)
    
    # Calculate ADX
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.rolling(window=period).mean()
    
    return adx, plus_di, minus_di


def calculate_supertrend(df: pd.DataFrame, period: int = 10, multiplier: float = 3) -> Tuple[pd.Series, pd.Series]:
    """
    Tính toán Supertrend Indicator
    
    Args:
        df: DataFrame với columns High, Low, Close
        period: Chu kỳ ATR (mặc định 10)
        multiplier: Multiplier cho ATR (mặc định 3)
    
    Returns:
        Tuple (Supertrend, Trend Direction: 1=uptrend, -1=downtrend)
    """
    # Calculate ATR
    atr = calculate_atr(df, period)
    
    # Calculate basic upper and lower bands
    hl_avg = (df['High'] + df['Low']) / 2
    upper_band = hl_avg + (multiplier * atr)
    lower_band = hl_avg - (multiplier * atr)
    
    # Initialize supertrend
    supertrend = pd.Series(index=df.index, dtype=float)
    direction = pd.Series(1, index=df.index)  # 1 = uptrend, -1 = downtrend
    
    for i in range(period, len(df)):
        if df['Close'].iloc[i] > upper_band.iloc[i-1]:
            direction.iloc[i] = 1
        elif df['Close'].iloc[i] < lower_band.iloc[i-1]:
            direction.iloc[i] = -1
        else:
            direction.iloc[i] = direction.iloc[i-1]
        
        if direction.iloc[i] == 1:
            supertrend.iloc[i] = lower_band.iloc[i]
        else:
            supertrend.iloc[i] = upper_band.iloc[i]
    
    return supertrend, direction


def calculate_parabolic_sar(df: pd.DataFrame, af_start: float = 0.02, af_max: float = 0.2) -> pd.Series:
    """
    Tính toán Parabolic SAR
    
    Args:
        df: DataFrame với columns High, Low, Close
        af_start: Acceleration Factor start (mặc định 0.02)
        af_max: Acceleration Factor maximum (mặc định 0.2)
    
    Returns:
        Series chứa giá trị SAR
    """
    sar = pd.Series(index=df.index, dtype=float)
    trend = pd.Series(1, index=df.index)  # 1 = uptrend, -1 = downtrend
    af = af_start
    ep = df['High'].iloc[0]  # Extreme Point
    
    sar.iloc[0] = df['Low'].iloc[0]
    
    for i in range(1, len(df)):
        if trend.iloc[i-1] == 1:  # Uptrend
            sar.iloc[i] = sar.iloc[i-1] + af * (ep - sar.iloc[i-1])
            
            if df['Low'].iloc[i] < sar.iloc[i]:
                trend.iloc[i] = -1
                sar.iloc[i] = ep
                ep = df['Low'].iloc[i]
                af = af_start
            else:
                trend.iloc[i] = 1
                if df['High'].iloc[i] > ep:
                    ep = df['High'].iloc[i]
                    af = min(af + af_start, af_max)
        else:  # Downtrend
            sar.iloc[i] = sar.iloc[i-1] - af * (sar.iloc[i-1] - ep)
            
            if df['High'].iloc[i] > sar.iloc[i]:
                trend.iloc[i] = 1
                sar.iloc[i] = ep
                ep = df['High'].iloc[i]
                af = af_start
            else:
                trend.iloc[i] = -1
                if df['Low'].iloc[i] < ep:
                    ep = df['Low'].iloc[i]
                    af = min(af + af_start, af_max)
    
    return sar


# ============= MOMENTUM INDICATORS =============

def calculate_stochastic(df: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> Tuple[pd.Series, pd.Series]:
    """
    Tính toán Stochastic Oscillator
    
    Args:
        df: DataFrame với columns High, Low, Close
        k_period: Chu kỳ %K (mặc định 14)
        d_period: Chu kỳ %D (mặc định 3)
    
    Returns:
        Tuple (%K, %D)
    """
    # Calculate %K
    low_min = df['Low'].rolling(window=k_period).min()
    high_max = df['High'].rolling(window=k_period).max()
    
    k_percent = 100 * ((df['Close'] - low_min) / (high_max - low_min))
    
    # Calculate %D (moving average of %K)
    d_percent = k_percent.rolling(window=d_period).mean()
    
    return k_percent, d_percent


def calculate_williams_r(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Tính toán Williams %R
    
    Args:
        df: DataFrame với columns High, Low, Close
        period: Chu kỳ (mặc định 14)
    
    Returns:
        Series chứa giá trị Williams %R
    """
    high_max = df['High'].rolling(window=period).max()
    low_min = df['Low'].rolling(window=period).min()
    
    williams_r = -100 * ((high_max - df['Close']) / (high_max - low_min))
    
    return williams_r


def calculate_cci(df: pd.DataFrame, period: int = 20) -> pd.Series:
    """
    Tính toán CCI (Commodity Channel Index)
    
    Args:
        df: DataFrame với columns High, Low, Close
        period: Chu kỳ (mặc định 20)
    
    Returns:
        Series chứa giá trị CCI
    """
    # Typical Price
    tp = (df['High'] + df['Low'] + df['Close']) / 3
    
    # Moving Average of Typical Price
    tp_ma = tp.rolling(window=period).mean()
    
    # Mean Deviation
    mad = tp.rolling(window=period).apply(lambda x: abs(x - x.mean()).mean())
    
    # CCI
    cci = (tp - tp_ma) / (0.015 * mad)
    
    return cci


# ============= VOLUME INDICATORS =============

def calculate_obv(df: pd.DataFrame) -> pd.Series:
    """
    Tính toán OBV (On-Balance Volume)
    
    Args:
        df: DataFrame với columns Close, Volume
    
    Returns:
        Series chứa giá trị OBV
    """
    obv = pd.Series(index=df.index, dtype=float)
    obv.iloc[0] = df['Volume'].iloc[0]
    
    for i in range(1, len(df)):
        if df['Close'].iloc[i] > df['Close'].iloc[i-1]:
            obv.iloc[i] = obv.iloc[i-1] + df['Volume'].iloc[i]
        elif df['Close'].iloc[i] < df['Close'].iloc[i-1]:
            obv.iloc[i] = obv.iloc[i-1] - df['Volume'].iloc[i]
        else:
            obv.iloc[i] = obv.iloc[i-1]
    
    return obv


def calculate_vwap(df: pd.DataFrame) -> pd.Series:
    """
    Tính toán VWAP (Volume Weighted Average Price)
    
    Args:
        df: DataFrame với columns High, Low, Close, Volume
    
    Returns:
        Series chứa giá trị VWAP
    """
    # Typical Price
    tp = (df['High'] + df['Low'] + df['Close']) / 3
    
    # VWAP = Cumulative(TP * Volume) / Cumulative(Volume)
    vwap = (tp * df['Volume']).cumsum() / df['Volume'].cumsum()
    
    return vwap


def calculate_ad_line(df: pd.DataFrame) -> pd.Series:
    """
    Tính toán Accumulation/Distribution Line
    
    Args:
        df: DataFrame với columns High, Low, Close, Volume
    
    Returns:
        Series chứa giá trị A/D Line
    """
    # Money Flow Multiplier
    mfm = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
    
    # Money Flow Volume
    mfv = mfm * df['Volume']
    
    # A/D Line (cumulative sum)
    ad_line = mfv.cumsum()
    
    return ad_line


# ============= VOLATILITY INDICATORS =============

def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Tính toán ATR (Average True Range)
    
    Args:
        df: DataFrame với columns High, Low, Close
        period: Chu kỳ (mặc định 14)
    
    Returns:
        Series chứa giá trị ATR
    """
    high_low = df['High'] - df['Low']
    high_close = abs(df['High'] - df['Close'].shift())
    low_close = abs(df['Low'] - df['Close'].shift())
    
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    return atr


def calculate_keltner_channels(df: pd.DataFrame, ema_period: int = 20, atr_period: int = 10, multiplier: float = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Tính toán Keltner Channels
    
    Args:
        df: DataFrame với columns High, Low, Close
        ema_period: Chu kỳ EMA (mặc định 20)
        atr_period: Chu kỳ ATR (mặc định 10)
        multiplier: Multiplier cho ATR (mặc định 2)
    
    Returns:
        Tuple (Upper Band, Middle Line, Lower Band)
    """
    # Middle Line (EMA)
    middle = df['Close'].ewm(span=ema_period, adjust=False).mean()
    
    # ATR
    atr = calculate_atr(df, atr_period)
    
    # Upper and Lower Bands
    upper = middle + (multiplier * atr)
    lower = middle - (multiplier * atr)
    
    return upper, middle, lower


def calculate_donchian_channels(df: pd.DataFrame, period: int = 20) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Tính toán Donchian Channels
    
    Args:
        df: DataFrame với columns High, Low
        period: Chu kỳ (mặc định 20)
    
    Returns:
        Tuple (Upper Band, Middle Line, Lower Band)
    """
    upper = df['High'].rolling(window=period).max()
    lower = df['Low'].rolling(window=period).min()
    middle = (upper + lower) / 2
    
    return upper, middle, lower


# ============= SIGNAL DETECTION =============

def get_indicator_signals(df: pd.DataFrame, indicators: dict) -> dict:
    """
    Phát hiện tín hiệu từ các indicators
    
    Args:
        df: DataFrame với dữ liệu và indicators
        indicators: Dictionary chứa các indicator đã tính
    
    Returns:
        Dictionary chứa các signals
    """
    signals = {
        'trend': [],
        'momentum': [],
        'volume': [],
        'overall': 'NEUTRAL'
    }
    
    bullish_count = 0
    bearish_count = 0
    
    # ADX Signal
    if 'ADX' in indicators:
        adx = indicators['ADX'].iloc[-1]
        plus_di = indicators['+DI'].iloc[-1]
        minus_di = indicators['-DI'].iloc[-1]
        
        if adx > 25:  # Strong trend
            if plus_di > minus_di:
                signals['trend'].append('ADX: Strong Uptrend')
                bullish_count += 1
            else:
                signals['trend'].append('ADX: Strong Downtrend')
                bearish_count += 1
    
    # Stochastic Signal
    if 'Stochastic_K' in indicators:
        k = indicators['Stochastic_K'].iloc[-1]
        if k < 20:
            signals['momentum'].append('Stochastic: Oversold')
            bullish_count += 1
        elif k > 80:
            signals['momentum'].append('Stochastic: Overbought')
            bearish_count += 1
    
    # OBV Signal
    if 'OBV' in indicators:
        obv = indicators['OBV']
        obv_ma = obv.rolling(window=20).mean()
        if obv.iloc[-1] > obv_ma.iloc[-1]:
            signals['volume'].append('OBV: Accumulation')
            bullish_count += 1
        else:
            signals['volume'].append('OBV: Distribution')
            bearish_count += 1
    
    # Overall Signal
    if bullish_count > bearish_count + 1:
        signals['overall'] = 'BULLISH'
    elif bearish_count > bullish_count + 1:
        signals['overall'] = 'BEARISH'
    else:
        signals['overall'] = 'NEUTRAL'
    
    return signals


# ============= HELPER FUNCTIONS =============

def get_signal_interpretation(indicator_name: str, value: float, context: dict = None) -> dict:
    """
    Giải thích tín hiệu của indicator
    
    Args:
        indicator_name: Tên indicator
        value: Giá trị hiện tại
        context: Thông tin context (optional)
    
    Returns:
        Dictionary chứa signal và interpretation
    """
    interpretation = {
        'indicator': indicator_name,
        'value': value,
        'signal': 'NEUTRAL',
        'interpretation': ''
    }
    
    if indicator_name == 'ADX':
        if value < 20:
            interpretation['signal'] = 'WEAK_TREND'
            interpretation['interpretation'] = 'Xu hướng yếu, thị trường sideway'
        elif value < 40:
            interpretation['signal'] = 'STRONG_TREND'
            interpretation['interpretation'] = 'Xu hướng mạnh, có thể trade theo trend'
        else:
            interpretation['signal'] = 'VERY_STRONG_TREND'
            interpretation['interpretation'] = 'Xu hướng rất mạnh, nhưng có thể đảo chiều'
    
    elif indicator_name == 'Stochastic':
        if value < 20:
            interpretation['signal'] = 'OVERSOLD'
            interpretation['interpretation'] = 'Quá bán, có thể tăng trở lại'
        elif value > 80:
            interpretation['signal'] = 'OVERBOUGHT'
            interpretation['interpretation'] = 'Quá mua, có thể giảm'
        else:
            interpretation['signal'] = 'NEUTRAL'
            interpretation['interpretation'] = 'Vùng trung tính'
    
    elif indicator_name == 'Williams_R':
        if value < -80:
            interpretation['signal'] = 'OVERSOLD'
            interpretation['interpretation'] = 'Quá bán, tín hiệu mua'
        elif value > -20:
            interpretation['signal'] = 'OVERBOUGHT'
            interpretation['interpretation'] = 'Quá mua, tín hiệu bán'
    
    elif indicator_name == 'CCI':
        if value < -100:
            interpretation['signal'] = 'OVERSOLD'
            interpretation['interpretation'] = 'Quá bán, cơ hội mua'
        elif value > 100:
            interpretation['signal'] = 'OVERBOUGHT'
            interpretation['interpretation'] = 'Quá mua, cơ hội bán'
    
    return interpretation

