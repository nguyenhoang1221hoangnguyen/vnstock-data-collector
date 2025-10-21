"""
Stock Screener - VNStock Data Collector
Sàng lọc cổ phiếu theo các tiêu chí FA và TA
"""

import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
import time

from fa_calculator import calculate_fa_ratios
from ta_analyzer import calculate_ta_indicators

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_stock_list(exchange: str = "HOSE") -> List[str]:
    """
    Lấy danh sách tất cả cổ phiếu trên sàn
    
    Args:
        exchange: Sàn giao dịch (HOSE, HNX, UPCOM)
    
    Returns:
        List các mã cổ phiếu
    """
    try:
        logger.info(f"Lấy danh sách cổ phiếu sàn {exchange}...")
        
        # Static list of major stocks (same as stock_classifier.py)
        hose_stocks = [
            'VCB', 'VHM', 'VIC', 'VNM', 'HPG', 'TCB', 'MSN', 'MBB', 'FPT', 'VPB',
            'VRE', 'CTG', 'BID', 'GAS', 'PLX', 'POW', 'SSI', 'MWG', 'SAB', 'HDB',
            'STB', 'VJC', 'ACB', 'GVR', 'TPB', 'PDR', 'REE', 'VCG', 'NVL', 'DGC',
            'BCM', 'KDH', 'VHC', 'VCI', 'HCM', 'DIG', 'VGC', 'CTD', 'VIB', 'PNJ',
            'DCM', 'DXG', 'GMD', 'HT1', 'KBC', 'NT2', 'PVD', 'SBT', 'VPI',
            'BVH', 'CII', 'DPM', 'FCN', 'HAG', 'HNG', 'HSG', 'ITA', 'KDC', 'LGC',
            'NLG', 'PC1', 'PPC', 'PVT', 'SCS', 'SHB', 'SSB', 'VCS', 'VGS', 'VHG',
            'DHG', 'DPR', 'DRC', 'DVP', 'EIB', 'EVF', 'GEG', 'HDC',
            'HHS', 'HQC', 'IDC', 'IJC', 'LCG', 'LDG',
            'LPB', 'MSB', 'NAF', 'NBB', 'NHA', 'NVT', 'OCB', 'PDN'
        ]
        
        hnx_stocks = [
            'PVS', 'CEO', 'SHS', 'PVI', 'HUT', 'VCG', 'PVX', 'DBC', 'TNG', 'PLC',
            'NRC', 'VIG', 'BAB', 'NDN', 'PVB', 'DXP', 'TIG', 'VGP', 'PVG', 'HHC',
            'DTD', 'VCS', 'SLS', 'VC3', 'PVE', 'L14', 'LIG', 'DTT', 'DQC', 'AMC'
        ]
        
        upcom_stocks = [
            'KSB', 'HTP', 'BII', 'VTO', 'AAV', 'DLD', 'NHH', 'SVC', 'MCO', 'VNR'
        ]
        
        # Return based on exchange
        if exchange.upper() == "HOSE":
            stocks = hose_stocks
        elif exchange.upper() == "HNX":
            stocks = hnx_stocks
        elif exchange.upper() == "UPCOM":
            stocks = upcom_stocks
        else:
            stocks = []
        
        logger.info(f"Lấy được {len(stocks)} mã cổ phiếu sàn {exchange}")
        return stocks
            
    except Exception as e:
        logger.error(f"Lỗi khi lấy danh sách cổ phiếu: {str(e)}")
        return []


def screen_stock(
    symbol: str,
    pe_max: float = 15,
    roe_min: float = 18,
    price_vs_ma50: str = "above"
) -> Dict[str, Any]:
    """
    Sàng lọc một mã cổ phiếu theo các tiêu chí FA và TA
    
    Args:
        symbol: Mã cổ phiếu
        pe_max: P/E tối đa (mặc định 15)
        roe_min: ROE tối thiểu % (mặc định 18)
        price_vs_ma50: Giá so với MA50 ("above" hoặc "below")
    
    Returns:
        Dictionary chứa thông tin sàng lọc
    """
    try:
        logger.info(f"Sàng lọc mã {symbol}...")
        
        result = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "passed": False,
            "fa_data": {},
            "ta_data": {},
            "criteria_check": {},
            "error": None
        }
        
        # 1. Lấy dữ liệu FA
        logger.debug(f"Lấy FA data cho {symbol}")
        fa_result = calculate_fa_ratios(symbol)
        
        if fa_result.get("error"):
            result["error"] = f"FA Error: {fa_result['error']}"
            return result
        
        # Lấy các chỉ số FA
        pe_ratio = fa_result.get("ratios", {}).get("PE")
        roe = fa_result.get("ratios", {}).get("ROE")
        
        result["fa_data"] = {
            "PE": pe_ratio,
            "ROE": roe,
            "EPS": fa_result.get("ratios", {}).get("EPS"),
            "NPM": fa_result.get("ratios", {}).get("NPM"),
            "DE": fa_result.get("ratios", {}).get("DE")
        }
        
        # 2. Lấy dữ liệu TA
        logger.debug(f"Lấy TA data cho {symbol}")
        ta_result = calculate_ta_indicators(symbol, period_days=90)  # 90 ngày để nhanh hơn
        
        if ta_result.get("error"):
            result["error"] = f"TA Error: {ta_result['error']}"
            return result
        
        # Lấy giá hiện tại và MA50
        current_price = ta_result.get("current_price")
        ma50 = ta_result.get("indicators", {}).get("MA50", {}).get("latest_value")
        
        result["ta_data"] = {
            "current_price": current_price,
            "MA50": ma50,
            "MA200": ta_result.get("indicators", {}).get("MA200", {}).get("latest_value"),
            "RSI": ta_result.get("indicators", {}).get("RSI", {}).get("latest_value")
        }
        
        # 3. Kiểm tra các tiêu chí
        criteria_passed = []
        criteria_failed = []
        
        # Tiêu chí 1: P/E < pe_max
        if pe_ratio is not None:
            if pe_ratio < pe_max:
                criteria_passed.append(f"PE < {pe_max}")
                result["criteria_check"]["PE"] = {"value": pe_ratio, "passed": True, "criteria": f"< {pe_max}"}
            else:
                criteria_failed.append(f"PE >= {pe_max}")
                result["criteria_check"]["PE"] = {"value": pe_ratio, "passed": False, "criteria": f"< {pe_max}"}
        else:
            criteria_failed.append("PE data missing")
            result["criteria_check"]["PE"] = {"value": None, "passed": False, "criteria": f"< {pe_max}"}
        
        # Tiêu chí 2: ROE > roe_min
        if roe is not None:
            if roe > roe_min:
                criteria_passed.append(f"ROE > {roe_min}%")
                result["criteria_check"]["ROE"] = {"value": roe, "passed": True, "criteria": f"> {roe_min}%"}
            else:
                criteria_failed.append(f"ROE <= {roe_min}%")
                result["criteria_check"]["ROE"] = {"value": roe, "passed": False, "criteria": f"> {roe_min}%"}
        else:
            criteria_failed.append("ROE data missing")
            result["criteria_check"]["ROE"] = {"value": None, "passed": False, "criteria": f"> {roe_min}%"}
        
        # Tiêu chí 3: Giá > MA50
        if current_price is not None and ma50 is not None:
            price_above_ma50 = current_price > ma50
            if (price_vs_ma50 == "above" and price_above_ma50) or (price_vs_ma50 == "below" and not price_above_ma50):
                criteria_passed.append(f"Price {price_vs_ma50} MA50")
                result["criteria_check"]["Price_vs_MA50"] = {
                    "current_price": current_price,
                    "MA50": ma50,
                    "passed": True,
                    "criteria": f"Price {price_vs_ma50} MA50"
                }
            else:
                criteria_failed.append(f"Price not {price_vs_ma50} MA50")
                result["criteria_check"]["Price_vs_MA50"] = {
                    "current_price": current_price,
                    "MA50": ma50,
                    "passed": False,
                    "criteria": f"Price {price_vs_ma50} MA50"
                }
        else:
            criteria_failed.append("Price or MA50 data missing")
            result["criteria_check"]["Price_vs_MA50"] = {
                "current_price": current_price,
                "MA50": ma50,
                "passed": False,
                "criteria": f"Price {price_vs_ma50} MA50"
            }
        
        # Kiểm tra tất cả tiêu chí
        all_criteria_passed = len(criteria_passed) == 3 and len(criteria_failed) == 0
        
        result["passed"] = all_criteria_passed
        result["criteria_passed"] = criteria_passed
        result["criteria_failed"] = criteria_failed
        result["summary"] = f"{len(criteria_passed)}/3 criteria passed"
        
        if all_criteria_passed:
            logger.info(f"✅ {symbol} - PASSED all criteria")
        else:
            logger.info(f"❌ {symbol} - FAILED: {', '.join(criteria_failed)}")
        
        return result
        
    except Exception as e:
        logger.error(f"Lỗi khi sàng lọc {symbol}: {str(e)}")
        return {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "passed": False,
            "error": str(e)
        }


def run_screener(
    exchange: str = "HOSE",
    limit: int = 20,
    pe_max: float = 15,
    roe_min: float = 18,
    price_vs_ma50: str = "above",
    delay: float = 1.0
) -> Dict[str, Any]:
    """
    Chạy stock screener cho nhiều mã cổ phiếu
    
    Args:
        exchange: Sàn giao dịch (HOSE, HNX, UPCOM)
        limit: Số lượng mã cần test (mặc định 20)
        pe_max: P/E tối đa (mặc định 15)
        roe_min: ROE tối thiểu % (mặc định 18)
        price_vs_ma50: Giá so với MA50 ("above" hoặc "below")
        delay: Thời gian delay giữa các request (giây)
    
    Returns:
        Dictionary chứa kết quả sàng lọc
    """
    try:
        logger.info(f"Bắt đầu Stock Screener cho sàn {exchange}")
        logger.info(f"Tiêu chí: PE < {pe_max}, ROE > {roe_min}%, Price {price_vs_ma50} MA50")
        
        # Lấy danh sách cổ phiếu
        stock_list = get_stock_list(exchange)
        
        if not stock_list:
            return {
                "success": False,
                "error": "Không lấy được danh sách cổ phiếu",
                "results": []
            }
        
        # Giới hạn số lượng để test
        test_symbols = stock_list[:limit]
        logger.info(f"Sàng lọc {len(test_symbols)} mã cổ phiếu...")
        
        # Sàng lọc từng mã
        results = []
        passed_stocks = []
        
        for idx, symbol in enumerate(test_symbols, 1):
            logger.info(f"[{idx}/{len(test_symbols)}] Sàng lọc {symbol}...")
            
            result = screen_stock(symbol, pe_max, roe_min, price_vs_ma50)
            results.append(result)
            
            if result.get("passed"):
                passed_stocks.append(result)
            
            # Delay để tránh quá tải API
            if idx < len(test_symbols):
                time.sleep(delay)
        
        # Tổng hợp kết quả
        summary = {
            "success": True,
            "screener_info": {
                "exchange": exchange,
                "total_screened": len(test_symbols),
                "total_passed": len(passed_stocks),
                "pass_rate": round((len(passed_stocks) / len(test_symbols) * 100), 2) if test_symbols else 0,
                "criteria": {
                    "pe_max": pe_max,
                    "roe_min": roe_min,
                    "price_vs_ma50": price_vs_ma50
                }
            },
            "passed_stocks": passed_stocks,
            "all_results": results,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Hoàn thành sàng lọc: {len(passed_stocks)}/{len(test_symbols)} mã đạt tiêu chí")
        
        return summary
        
    except Exception as e:
        logger.error(f"Lỗi khi chạy screener: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "results": []
        }


def print_screener_results(results: Dict[str, Any]):
    """
    In kết quả sàng lọc ra console
    
    Args:
        results: Kết quả từ run_screener()
    """
    print("\n" + "="*80)
    print("📊 STOCK SCREENER RESULTS")
    print("="*80)
    
    if not results.get("success"):
        print(f"❌ Lỗi: {results.get('error')}")
        return
    
    info = results.get("screener_info", {})
    print(f"\n📈 Sàn: {info.get('exchange')}")
    print(f"🔍 Đã sàng lọc: {info.get('total_screened')} mã")
    print(f"✅ Đạt tiêu chí: {info.get('total_passed')} mã ({info.get('pass_rate')}%)")
    
    criteria = info.get("criteria", {})
    print(f"\n📋 Tiêu chí sàng lọc:")
    print(f"   - P/E < {criteria.get('pe_max')}")
    print(f"   - ROE > {criteria.get('roe_min')}%")
    print(f"   - Giá hiện tại {criteria.get('price_vs_ma50')} MA50")
    
    passed_stocks = results.get("passed_stocks", [])
    
    if passed_stocks:
        print(f"\n✅ Các mã đạt tiêu chí:")
        print("-"*80)
        print(f"{'Mã':<8} {'Giá':<12} {'P/E':<8} {'ROE':<8} {'MA50':<12} {'vs MA50':<10}")
        print("-"*80)
        
        for stock in passed_stocks:
            symbol = stock.get("symbol", "N/A")
            fa = stock.get("fa_data", {})
            ta = stock.get("ta_data", {})
            
            price = ta.get("current_price", 0)
            pe = fa.get("PE", 0)
            roe = fa.get("ROE", 0)
            ma50 = ta.get("MA50", 0)
            
            price_diff = ((price - ma50) / ma50 * 100) if ma50 else 0
            
            print(f"{symbol:<8} {price:>10,.0f}đ {pe:>6.2f} {roe:>6.1f}% {ma50:>10,.0f}đ {price_diff:>+7.1f}%")
        
        print("-"*80)
    else:
        print(f"\n❌ Không có mã nào đạt tiêu chí")
    
    # Hiển thị một số mã không đạt (để tham khảo)
    all_results = results.get("all_results", [])
    failed_stocks = [r for r in all_results if not r.get("passed")]
    
    if failed_stocks:
        print(f"\n📋 Một số mã không đạt tiêu chí (top 5):")
        print("-"*80)
        print(f"{'Mã':<8} {'Giá':<12} {'P/E':<8} {'ROE':<8} {'Lý do':<40}")
        print("-"*80)
        
        for stock in failed_stocks[:5]:
            symbol = stock.get("symbol", "N/A")
            fa = stock.get("fa_data", {})
            ta = stock.get("ta_data", {})
            failed = stock.get("criteria_failed", [])
            
            price = ta.get("current_price") or 0
            pe = fa.get("PE")
            roe = fa.get("ROE")
            
            pe_str = f"{pe:.2f}" if pe else "N/A"
            roe_str = f"{roe:.1f}%" if roe else "N/A"
            reason = ", ".join(failed[:2]) if failed else "N/A"
            
            print(f"{symbol:<8} {price:>10,.0f}đ {pe_str:>6} {roe_str:>6} {reason:<40}")
        
        print("-"*80)
    
    print("\n" + "="*80)


if __name__ == "__main__":
    print("\n🚀 VNStock Stock Screener")
    print("="*80)
    
    # Cấu hình screener
    EXCHANGE = "HOSE"  # Sàn HOSE
    LIMIT = 20         # Test với 20 mã đầu tiên
    PE_MAX = 15        # P/E < 15
    ROE_MIN = 18       # ROE > 18%
    PRICE_VS_MA50 = "above"  # Giá > MA50
    DELAY = 1.0        # Delay 1 giây giữa các request
    
    print(f"📋 Cấu hình:")
    print(f"   - Sàn: {EXCHANGE}")
    print(f"   - Số lượng: {LIMIT} mã")
    print(f"   - Tiêu chí: PE < {PE_MAX}, ROE > {ROE_MIN}%, Giá {PRICE_VS_MA50} MA50")
    print(f"   - Delay: {DELAY}s")
    print()
    
    # Chạy screener
    results = run_screener(
        exchange=EXCHANGE,
        limit=LIMIT,
        pe_max=PE_MAX,
        roe_min=ROE_MIN,
        price_vs_ma50=PRICE_VS_MA50,
        delay=DELAY
    )
    
    # In kết quả
    print_screener_results(results)
    
    # Lưu kết quả ra file CSV
    if results.get("success") and results.get("passed_stocks"):
        try:
            passed_stocks = results["passed_stocks"]
            df_data = []
            
            for stock in passed_stocks:
                df_data.append({
                    "Symbol": stock["symbol"],
                    "Price": stock["ta_data"]["current_price"],
                    "PE": stock["fa_data"]["PE"],
                    "ROE": stock["fa_data"]["ROE"],
                    "MA50": stock["ta_data"]["MA50"],
                    "RSI": stock["ta_data"].get("RSI"),
                    "Timestamp": stock["timestamp"]
                })
            
            df = pd.DataFrame(df_data)
            filename = f"screener_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False)
            print(f"\n💾 Kết quả đã được lưu tại: {filename}")
            
        except Exception as e:
            print(f"\n❌ Lỗi khi lưu file: {str(e)}")

