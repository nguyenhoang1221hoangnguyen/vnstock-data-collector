"""
Backtesting Strategy - VNStock Data Collector
Kiểm thử chiến lược giao dịch với dữ liệu lịch sử
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_historical_data_for_backtest(symbol: str, period_days: int = 1095) -> pd.DataFrame:
    """
    Lấy dữ liệu OHLCV cho backtesting
    
    Args:
        symbol: Mã cổ phiếu
        period_days: Số ngày lấy dữ liệu (mặc định 1095 ngày = 3 năm)
    
    Returns:
        DataFrame với cột OHLCV phù hợp cho backtesting
    """
    try:
        from vnstock import Vnstock
        
        logger.info(f"Lấy dữ liệu OHLCV cho backtesting mã {symbol}")
        
        # Khởi tạo vnstock client
        stock = Vnstock().stock(symbol=symbol, source='VCI')
        
        # Tính toán khoảng thời gian
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=period_days)).strftime("%Y-%m-%d")
        
        logger.info(f"Lấy dữ liệu từ {start_date} đến {end_date}")
        
        # Lấy dữ liệu OHLCV
        df = stock.quote.history(start=start_date, end=end_date)
        
        if df.empty:
            logger.warning(f"Không có dữ liệu cho mã {symbol}")
            return pd.DataFrame()
        
        # Đổi tên cột và format theo yêu cầu của backtesting.py
        df = df.rename(columns={
            'time': 'Date',
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        })
        
        # Set Date làm index
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        
        # Chuyển đổi giá từ nghìn đồng sang VND đầy đủ
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = df[col] * 1000
        
        # Sắp xếp theo thời gian
        df.sort_index(inplace=True)
        
        logger.info(f"Lấy được {len(df)} ngày giao dịch")
        
        return df
        
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu cho {symbol}: {str(e)}")
        return pd.DataFrame()


def run_ma_crossover_backtest(
    symbol: str,
    initial_cash: float = 100_000_000,
    ma_fast: int = 20,
    ma_slow: int = 50,
    period_days: int = 1095,
    commission: float = 0.001
) -> Dict[str, Any]:
    """
    Chạy backtest cho chiến lược MA Crossover
    
    Args:
        symbol: Mã cổ phiếu
        initial_cash: Vốn ban đầu (VND)
        ma_fast: Chu kỳ MA nhanh (mặc định 20)
        ma_slow: Chu kỳ MA chậm (mặc định 50)
        period_days: Số ngày dữ liệu (mặc định 1095 = 3 năm)
        commission: Phí giao dịch % (mặc định 0.1%)
    
    Returns:
        Dictionary chứa kết quả backtest
    """
    try:
        from backtesting import Backtest, Strategy
        from backtesting.lib import crossover
        
        logger.info(f"Bắt đầu backtest cho mã {symbol}")
        logger.info(f"Chiến lược: MA({ma_fast}) crossover MA({ma_slow})")
        logger.info(f"Vốn ban đầu: {initial_cash:,.0f} VND")
        
        # Lấy dữ liệu
        df = get_historical_data_for_backtest(symbol, period_days)
        
        if df.empty:
            return {
                "success": False,
                "error": "Không có dữ liệu",
                "symbol": symbol
            }
        
        # Định nghĩa chiến lược MA Crossover
        class MACrossoverStrategy(Strategy):
            """
            Chiến lược Golden Cross / Death Cross
            - Mua khi MA nhanh cắt lên MA chậm (Golden Cross)
            - Bán khi MA nhanh cắt xuống MA chậm (Death Cross)
            """
            
            # Parameters
            n1 = ma_fast  # MA nhanh
            n2 = ma_slow  # MA chậm
            
            def init(self):
                # Tính toán MA
                close = self.data.Close
                self.ma_fast = self.I(lambda x: pd.Series(x).rolling(self.n1).mean(), close)
                self.ma_slow = self.I(lambda x: pd.Series(x).rolling(self.n2).mean(), close)
            
            def next(self):
                # Nếu chưa có vị thế
                if not self.position:
                    # Golden Cross: MA nhanh cắt lên MA chậm -> MUA
                    if crossover(self.ma_fast, self.ma_slow):
                        self.buy()
                
                # Nếu đang có vị thế
                else:
                    # Death Cross: MA nhanh cắt xuống MA chậm -> BÁN
                    if crossover(self.ma_slow, self.ma_fast):
                        self.position.close()
        
        # Khởi tạo Backtest
        bt = Backtest(
            df,
            MACrossoverStrategy,
            cash=initial_cash,
            commission=commission,
            exclusive_orders=True
        )
        
        # Chạy backtest
        logger.info("Chạy backtest...")
        stats = bt.run()
        
        # Thu thập kết quả
        result = {
            "success": True,
            "symbol": symbol,
            "strategy": f"MA({ma_fast}) Crossover MA({ma_slow})",
            "backtest_period": {
                "start_date": df.index[0].strftime("%Y-%m-%d"),
                "end_date": df.index[-1].strftime("%Y-%m-%d"),
                "total_days": len(df),
                "trading_days": len(df)
            },
            "initial_capital": initial_cash,
            "statistics": {
                "equity_final": float(stats['Equity Final [$]']),
                "equity_peak": float(stats['Equity Peak [$]']),
                "return_pct": float(stats['Return [%]']),
                "buy_hold_return_pct": float(stats['Buy & Hold Return [%]']),
                "max_drawdown_pct": float(stats['Max. Drawdown [%]']),
                "avg_drawdown_pct": float(stats.get('Avg. Drawdown [%]', 0)),
                "total_trades": int(stats['# Trades']),
                "win_rate_pct": float(stats['Win Rate [%]']),
                "best_trade_pct": float(stats.get('Best Trade [%]', 0)),
                "worst_trade_pct": float(stats.get('Worst Trade [%]', 0)),
                "avg_trade_pct": float(stats.get('Avg. Trade [%]', 0)),
                "profit_factor": float(stats.get('Profit Factor', 0)),
                "sharpe_ratio": float(stats.get('Sharpe Ratio', 0)),
                "sortino_ratio": float(stats.get('Sortino Ratio', 0)),
                "calmar_ratio": float(stats.get('Calmar Ratio', 0))
            },
            "performance": {
                "total_return": float(stats['Equity Final [$]'] - initial_cash),
                "total_return_pct": float(stats['Return [%]']),
                "vs_buy_hold": float(stats['Return [%]'] - stats['Buy & Hold Return [%]']),
                "annual_return_pct": float(stats['Return [%]']) / (period_days / 365),
                "max_drawdown": float(stats['Max. Drawdown [%]'])
            },
            "configuration": {
                "ma_fast": ma_fast,
                "ma_slow": ma_slow,
                "commission": commission * 100
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # Tạo interpretation
        interpretation = interpret_backtest_results(result)
        result["interpretation"] = interpretation
        
        logger.info(f"Hoàn thành backtest cho {symbol}")
        logger.info(f"Return: {result['statistics']['return_pct']:.2f}%")
        logger.info(f"Win Rate: {result['statistics']['win_rate_pct']:.2f}%")
        logger.info(f"Max Drawdown: {result['statistics']['max_drawdown_pct']:.2f}%")
        
        return result
        
    except ImportError:
        logger.error("Thiếu thư viện backtesting. Cài đặt: pip install backtesting")
        return {
            "success": False,
            "error": "Thiếu thư viện backtesting. Vui lòng cài đặt: pip install backtesting",
            "symbol": symbol
        }
    except Exception as e:
        logger.error(f"Lỗi khi chạy backtest cho {symbol}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "symbol": symbol
        }


def interpret_backtest_results(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Diễn giải kết quả backtest
    
    Args:
        result: Kết quả backtest từ run_ma_crossover_backtest()
    
    Returns:
        Dictionary chứa diễn giải
    """
    stats = result.get("statistics", {})
    
    interpretation = {
        "overall_rating": None,
        "profitability": {},
        "risk": {},
        "efficiency": {},
        "recommendation": ""
    }
    
    # Đánh giá lợi nhuận
    return_pct = stats.get("return_pct", 0)
    if return_pct > 50:
        interpretation["profitability"]["rating"] = "excellent"
        interpretation["profitability"]["message"] = f"Lợi nhuận xuất sắc: {return_pct:.2f}%"
    elif return_pct > 20:
        interpretation["profitability"]["rating"] = "good"
        interpretation["profitability"]["message"] = f"Lợi nhuận tốt: {return_pct:.2f}%"
    elif return_pct > 0:
        interpretation["profitability"]["rating"] = "moderate"
        interpretation["profitability"]["message"] = f"Lợi nhuận trung bình: {return_pct:.2f}%"
    else:
        interpretation["profitability"]["rating"] = "poor"
        interpretation["profitability"]["message"] = f"Thua lỗ: {return_pct:.2f}%"
    
    # Đánh giá rủi ro
    max_dd = abs(stats.get("max_drawdown_pct", 0))
    if max_dd < 10:
        interpretation["risk"]["rating"] = "low"
        interpretation["risk"]["message"] = f"Rủi ro thấp: Max DD {max_dd:.2f}%"
    elif max_dd < 20:
        interpretation["risk"]["rating"] = "moderate"
        interpretation["risk"]["message"] = f"Rủi ro trung bình: Max DD {max_dd:.2f}%"
    elif max_dd < 30:
        interpretation["risk"]["rating"] = "high"
        interpretation["risk"]["message"] = f"Rủi ro cao: Max DD {max_dd:.2f}%"
    else:
        interpretation["risk"]["rating"] = "very_high"
        interpretation["risk"]["message"] = f"Rủi ro rất cao: Max DD {max_dd:.2f}%"
    
    # Đánh giá hiệu quả
    win_rate = stats.get("win_rate_pct", 0)
    if win_rate > 60:
        interpretation["efficiency"]["rating"] = "excellent"
        interpretation["efficiency"]["message"] = f"Tỷ lệ thắng xuất sắc: {win_rate:.2f}%"
    elif win_rate > 50:
        interpretation["efficiency"]["rating"] = "good"
        interpretation["efficiency"]["message"] = f"Tỷ lệ thắng tốt: {win_rate:.2f}%"
    elif win_rate > 40:
        interpretation["efficiency"]["rating"] = "moderate"
        interpretation["efficiency"]["message"] = f"Tỷ lệ thắng trung bình: {win_rate:.2f}%"
    else:
        interpretation["efficiency"]["rating"] = "poor"
        interpretation["efficiency"]["message"] = f"Tỷ lệ thắng thấp: {win_rate:.2f}%"
    
    # So sánh với Buy & Hold
    vs_buy_hold = result.get("performance", {}).get("vs_buy_hold", 0)
    if vs_buy_hold > 0:
        interpretation["vs_buy_hold"] = f"Tốt hơn Buy & Hold: +{vs_buy_hold:.2f}%"
    else:
        interpretation["vs_buy_hold"] = f"Kém hơn Buy & Hold: {vs_buy_hold:.2f}%"
    
    # Đánh giá tổng thể
    ratings = [
        interpretation["profitability"]["rating"],
        interpretation["risk"]["rating"],
        interpretation["efficiency"]["rating"]
    ]
    
    if return_pct > 20 and max_dd < 20 and win_rate > 50:
        interpretation["overall_rating"] = "excellent"
        interpretation["recommendation"] = "Chiến lược rất tốt, có thể áp dụng thực tế"
    elif return_pct > 10 and max_dd < 30:
        interpretation["overall_rating"] = "good"
        interpretation["recommendation"] = "Chiến lược khá tốt, cần xem xét kỹ rủi ro"
    elif return_pct > 0:
        interpretation["overall_rating"] = "moderate"
        interpretation["recommendation"] = "Chiến lược cần cải thiện"
    else:
        interpretation["overall_rating"] = "poor"
        interpretation["recommendation"] = "Không nên áp dụng chiến lược này"
    
    return interpretation


def print_backtest_results(result: Dict[str, Any]):
    """
    In kết quả backtest ra console
    
    Args:
        result: Kết quả từ run_ma_crossover_backtest()
    """
    if not result.get("success"):
        print(f"\n❌ Lỗi: {result.get('error')}")
        return
    
    print("\n" + "="*80)
    print(f"📊 BACKTEST RESULTS - {result['symbol']}")
    print("="*80)
    
    print(f"\n📈 Chiến lược: {result['strategy']}")
    
    period = result.get("backtest_period", {})
    print(f"\n📅 Thời gian:")
    print(f"   Từ: {period.get('start_date')}")
    print(f"   Đến: {period.get('end_date')}")
    print(f"   Số ngày giao dịch: {period.get('trading_days')}")
    
    print(f"\n💰 Vốn ban đầu: {result['initial_capital']:,.0f} VND")
    
    stats = result.get("statistics", {})
    print(f"\n📊 Kết quả chính:")
    print(f"   ✅ Equity Final:       {stats.get('equity_final', 0):>15,.0f} VND")
    print(f"   📈 Total Return:       {stats.get('return_pct', 0):>14.2f} %")
    print(f"   🎯 Win Rate:           {stats.get('win_rate_pct', 0):>14.2f} %")
    print(f"   📉 Max Drawdown:       {stats.get('max_drawdown_pct', 0):>14.2f} %")
    print(f"   🔄 Total Trades:       {stats.get('total_trades', 0):>15}")
    
    print(f"\n📈 So sánh với Buy & Hold:")
    print(f"   Buy & Hold Return:     {stats.get('buy_hold_return_pct', 0):>14.2f} %")
    perf = result.get("performance", {})
    vs_bh = perf.get('vs_buy_hold', 0)
    symbol = "+" if vs_bh > 0 else ""
    print(f"   Vs Buy & Hold:         {symbol}{vs_bh:>13.2f} %")
    
    print(f"\n📊 Chi tiết thống kê:")
    print(f"   Equity Peak:           {stats.get('equity_peak', 0):>15,.0f} VND")
    print(f"   Best Trade:            {stats.get('best_trade_pct', 0):>14.2f} %")
    print(f"   Worst Trade:           {stats.get('worst_trade_pct', 0):>14.2f} %")
    print(f"   Avg Trade:             {stats.get('avg_trade_pct', 0):>14.2f} %")
    print(f"   Profit Factor:         {stats.get('profit_factor', 0):>15.2f}")
    print(f"   Sharpe Ratio:          {stats.get('sharpe_ratio', 0):>15.2f}")
    print(f"   Sortino Ratio:         {stats.get('sortino_ratio', 0):>15.2f}")
    
    config = result.get("configuration", {})
    print(f"\n⚙️  Cấu hình:")
    print(f"   MA Fast:               {config.get('ma_fast', 0):>15}")
    print(f"   MA Slow:               {config.get('ma_slow', 0):>15}")
    print(f"   Commission:            {config.get('commission', 0):>14.2f} %")
    
    # Diễn giải
    interp = result.get("interpretation", {})
    if interp:
        print(f"\n💡 Diễn giải:")
        print(f"   Đánh giá tổng thể:     {interp.get('overall_rating', 'N/A')}")
        print(f"   Lợi nhuận:             {interp.get('profitability', {}).get('message', 'N/A')}")
        print(f"   Rủi ro:                {interp.get('risk', {}).get('message', 'N/A')}")
        print(f"   Hiệu quả:              {interp.get('efficiency', {}).get('message', 'N/A')}")
        print(f"   So sánh:               {interp.get('vs_buy_hold', 'N/A')}")
        print(f"\n   💬 Khuyến nghị: {interp.get('recommendation', 'N/A')}")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    print("\n🚀 VNStock Backtesting System")
    print("="*80)
    
    # Cấu hình backtest
    SYMBOL = "TCB"  # Mã cổ phiếu
    INITIAL_CASH = 100_000_000  # 100 triệu VND
    MA_FAST = 20    # MA nhanh
    MA_SLOW = 50    # MA chậm
    PERIOD_DAYS = 1095  # 3 năm
    COMMISSION = 0.001  # 0.1%
    
    print(f"\n📋 Cấu hình:")
    print(f"   Mã cổ phiếu:           {SYMBOL}")
    print(f"   Vốn ban đầu:           {INITIAL_CASH:,.0f} VND")
    print(f"   Chiến lược:            MA({MA_FAST}) Crossover MA({MA_SLOW})")
    print(f"   Thời gian:             {PERIOD_DAYS} ngày (≈ {PERIOD_DAYS//365} năm)")
    print(f"   Phí giao dịch:         {COMMISSION*100}%")
    print()
    
    # Chạy backtest
    result = run_ma_crossover_backtest(
        symbol=SYMBOL,
        initial_cash=INITIAL_CASH,
        ma_fast=MA_FAST,
        ma_slow=MA_SLOW,
        period_days=PERIOD_DAYS,
        commission=COMMISSION
    )
    
    # In kết quả
    print_backtest_results(result)

