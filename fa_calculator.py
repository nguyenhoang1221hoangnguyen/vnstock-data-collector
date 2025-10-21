"""
FA (Fundamental Analysis) Calculator - VNStock Data Collector
Tính toán các chỉ số phân tích cơ bản cho cổ phiếu Việt Nam
"""

import pandas as pd
from datetime import datetime
from typing import Dict, Any, Optional
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_fa_ratios(symbol: str) -> Dict[str, Any]:
    """
    Tính toán các chỉ số phân tích cơ bản (FA) cho một mã cổ phiếu
    
    Args:
        symbol: Mã cổ phiếu (VD: VIC, VCB, FPT)
    
    Returns:
        Dictionary chứa các chỉ số FA:
        - P/E (Price to Earnings): Giá / Thu nhập mỗi cổ phiếu
        - ROE (Return on Equity): Lợi nhuận ròng / Vốn chủ sở hữu
        - Biên lợi nhuận ròng (Net Profit Margin): Lợi nhuận ròng / Doanh thu
        - D/E (Debt to Equity): Nợ phải trả / Vốn chủ sở hữu
        - EPS (Earnings Per Share): Thu nhập mỗi cổ phiếu
    """
    try:
        from vnstock import Vnstock
        
        logger.info(f"Bắt đầu tính toán FA ratios cho mã {symbol}")
        
        # Khởi tạo vnstock client
        stock = Vnstock().stock(symbol=symbol, source='VCI')
        
        # 1. Lấy giá thị trường hiện tại
        logger.info("Lấy giá thị trường...")
        current_price = None
        try:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - pd.Timedelta(days=7)).strftime("%Y-%m-%d")
            price_data = stock.quote.history(start=start_date, end=end_date)
            
            if not price_data.empty:
                # Giá đóng cửa gần nhất (đã ở đơn vị nghìn đồng)
                current_price = float(price_data.iloc[-1]['close'])
                logger.info(f"Giá hiện tại: {current_price} nghìn đồng")
        except Exception as e:
            logger.warning(f"Không lấy được giá thị trường: {str(e)}")
        
        # 2. Lấy Báo cáo Kết quả Kinh doanh (KQKD) - 4 quý gần nhất
        logger.info("Lấy Báo cáo KQKD (4 quý gần nhất)...")
        income_statement = pd.DataFrame()
        try:
            income_statement = stock.finance.income_statement(period='quarterly', lang='vi')
            if not income_statement.empty:
                # Lấy 4 quý gần nhất
                income_statement = income_statement.head(4)
                logger.info(f"Lấy được {len(income_statement)} quý KQKD")
        except Exception as e:
            logger.warning(f"Không lấy được KQKD: {str(e)}")
        
        # 3. Lấy Bảng Cân đối Kế toán (CĐKT) - quý gần nhất
        logger.info("Lấy Bảng CĐKT (quý gần nhất)...")
        balance_sheet = pd.DataFrame()
        try:
            balance_sheet = stock.finance.balance_sheet(period='quarterly', lang='vi')
            if not balance_sheet.empty:
                # Lấy quý gần nhất
                balance_sheet = balance_sheet.head(1)
                logger.info(f"Lấy được CĐKT quý gần nhất")
        except Exception as e:
            logger.warning(f"Không lấy được CĐKT: {str(e)}")
        
        # 4. Tính toán các chỉ số
        fa_ratios = {
            "symbol": symbol,
            "calculation_date": datetime.now().isoformat(),
            "current_price": current_price,
            "price_unit": "nghìn đồng",
            "ratios": {},
            "data_quality": {},
            "raw_data": {}
        }
        
        # === Tính toán EPS (Earnings Per Share) ===
        eps = None
        total_net_profit_4q = None
        if not income_statement.empty:
            try:
                # Lợi nhuận ròng 4 quý gần nhất
                net_profit_col = None
                for col in income_statement.columns:
                    if 'lợi nhuận sau thuế' in col.lower() or 'lãi ròng' in col.lower():
                        net_profit_col = col
                        break
                
                if net_profit_col:
                    # Tính tổng lợi nhuận 4 quý
                    total_net_profit_4q = income_statement[net_profit_col].sum()
                    
                    # Lấy số lượng cổ phiếu đang lưu hành
                    outstanding_shares = None
                    if not balance_sheet.empty:
                        for col in balance_sheet.columns:
                            if 'cổ phiếu phổ thông' in col.lower():
                                outstanding_shares = balance_sheet.iloc[0][col]
                                break
                    
                    if outstanding_shares and outstanding_shares > 0:
                        eps = (total_net_profit_4q / outstanding_shares) * 1000  # Chuyển về nghìn đồng
                        fa_ratios["ratios"]["EPS"] = round(eps, 2)
                        fa_ratios["data_quality"]["EPS"] = "good"
                        logger.info(f"EPS: {eps:.2f} nghìn đồng")
                    else:
                        logger.warning("Không tìm thấy số lượng cổ phiếu lưu hành")
            except Exception as e:
                logger.error(f"Lỗi khi tính EPS: {str(e)}")
                fa_ratios["data_quality"]["EPS"] = "error"
        
        # === Tính toán P/E (Price to Earnings) ===
        if current_price and eps and eps > 0:
            pe_ratio = current_price / eps
            fa_ratios["ratios"]["PE"] = round(pe_ratio, 2)
            fa_ratios["data_quality"]["PE"] = "good"
            logger.info(f"P/E: {pe_ratio:.2f}")
        else:
            fa_ratios["ratios"]["PE"] = None
            fa_ratios["data_quality"]["PE"] = "insufficient_data"
            logger.warning("Không đủ dữ liệu để tính P/E")
        
        # === Tính toán ROE (Return on Equity) ===
        if not income_statement.empty and not balance_sheet.empty:
            try:
                # Lợi nhuận ròng 4 quý (đã tính ở trên)
                if total_net_profit_4q is None:
                    net_profit_col = None
                    for col in income_statement.columns:
                        if 'lợi nhuận sau thuế' in col.lower() or 'lãi ròng' in col.lower():
                            net_profit_col = col
                            break
                    if net_profit_col:
                        total_net_profit_4q = income_statement[net_profit_col].sum()
                
                # Vốn chủ sở hữu quý gần nhất
                equity_col = None
                for col in balance_sheet.columns:
                    if 'vốn chủ sở hữu' in col.lower():
                        equity_col = col
                        break
                
                if total_net_profit_4q and equity_col:
                    equity = balance_sheet.iloc[0][equity_col]
                    if equity and equity > 0:
                        roe = (total_net_profit_4q / equity) * 100  # Phần trăm
                        fa_ratios["ratios"]["ROE"] = round(roe, 2)
                        fa_ratios["data_quality"]["ROE"] = "good"
                        logger.info(f"ROE: {roe:.2f}%")
                    else:
                        fa_ratios["data_quality"]["ROE"] = "zero_equity"
                else:
                    fa_ratios["data_quality"]["ROE"] = "missing_columns"
            except Exception as e:
                logger.error(f"Lỗi khi tính ROE: {str(e)}")
                fa_ratios["ratios"]["ROE"] = None
                fa_ratios["data_quality"]["ROE"] = "error"
        else:
            fa_ratios["ratios"]["ROE"] = None
            fa_ratios["data_quality"]["ROE"] = "no_data"
        
        # === Tính toán Biên lợi nhuận ròng (Net Profit Margin) ===
        if not income_statement.empty:
            try:
                # Lấy quý gần nhất
                latest_quarter = income_statement.iloc[0]
                
                # Lợi nhuận ròng
                net_profit_col = None
                for col in income_statement.columns:
                    if 'lợi nhuận sau thuế' in col.lower() or 'lãi ròng' in col.lower():
                        net_profit_col = col
                        break
                
                # Doanh thu
                revenue_col = None
                for col in income_statement.columns:
                    if 'doanh thu' in col.lower() and 'thuần' in col.lower():
                        revenue_col = col
                        break
                
                if net_profit_col and revenue_col:
                    net_profit = latest_quarter[net_profit_col]
                    revenue = latest_quarter[revenue_col]
                    
                    if revenue and revenue > 0:
                        npm = (net_profit / revenue) * 100  # Phần trăm
                        fa_ratios["ratios"]["NPM"] = round(npm, 2)
                        fa_ratios["data_quality"]["NPM"] = "good"
                        logger.info(f"Biên lợi nhuận ròng: {npm:.2f}%")
                    else:
                        fa_ratios["data_quality"]["NPM"] = "zero_revenue"
                else:
                    fa_ratios["data_quality"]["NPM"] = "missing_columns"
            except Exception as e:
                logger.error(f"Lỗi khi tính NPM: {str(e)}")
                fa_ratios["ratios"]["NPM"] = None
                fa_ratios["data_quality"]["NPM"] = "error"
        else:
            fa_ratios["ratios"]["NPM"] = None
            fa_ratios["data_quality"]["NPM"] = "no_data"
        
        # === Tính toán D/E (Debt to Equity) ===
        if not balance_sheet.empty:
            try:
                # Nợ phải trả
                debt_col = None
                for col in balance_sheet.columns:
                    if 'nợ phải trả' in col.lower():
                        debt_col = col
                        break
                
                # Vốn chủ sở hữu
                equity_col = None
                for col in balance_sheet.columns:
                    if 'vốn chủ sở hữu' in col.lower():
                        equity_col = col
                        break
                
                if debt_col and equity_col:
                    debt = balance_sheet.iloc[0][debt_col]
                    equity = balance_sheet.iloc[0][equity_col]
                    
                    if equity and equity > 0:
                        de_ratio = debt / equity
                        fa_ratios["ratios"]["DE"] = round(de_ratio, 2)
                        fa_ratios["data_quality"]["DE"] = "good"
                        logger.info(f"D/E: {de_ratio:.2f}")
                    else:
                        fa_ratios["data_quality"]["DE"] = "zero_equity"
                else:
                    fa_ratios["data_quality"]["DE"] = "missing_columns"
            except Exception as e:
                logger.error(f"Lỗi khi tính D/E: {str(e)}")
                fa_ratios["ratios"]["DE"] = None
                fa_ratios["data_quality"]["DE"] = "error"
        else:
            fa_ratios["ratios"]["DE"] = None
            fa_ratios["data_quality"]["DE"] = "no_data"
        
        # === Thêm raw data cho debugging ===
        fa_ratios["raw_data"]["income_statement_periods"] = len(income_statement) if not income_statement.empty else 0
        fa_ratios["raw_data"]["balance_sheet_periods"] = len(balance_sheet) if not balance_sheet.empty else 0
        fa_ratios["raw_data"]["has_price_data"] = current_price is not None
        
        # === Đánh giá tổng thể ===
        complete_ratios = sum(1 for k, v in fa_ratios["ratios"].items() if v is not None)
        total_ratios = len(fa_ratios["ratios"])
        fa_ratios["completeness"] = {
            "complete_ratios": complete_ratios,
            "total_ratios": total_ratios,
            "percentage": round((complete_ratios / total_ratios * 100) if total_ratios > 0 else 0, 2)
        }
        
        logger.info(f"Hoàn thành tính toán FA ratios cho {symbol}: {complete_ratios}/{total_ratios} chỉ số")
        return fa_ratios
        
    except Exception as e:
        logger.error(f"Lỗi khi tính toán FA ratios cho {symbol}: {str(e)}")
        return {
            "symbol": symbol,
            "calculation_date": datetime.now().isoformat(),
            "error": str(e),
            "ratios": {
                "PE": None,
                "ROE": None,
                "NPM": None,
                "DE": None,
                "EPS": None
            },
            "data_quality": {
                "PE": "error",
                "ROE": "error",
                "NPM": "error",
                "DE": "error",
                "EPS": "error"
            }
        }


def get_fa_interpretation(fa_ratios: Dict[str, Any]) -> Dict[str, Any]:
    """
    Diễn giải các chỉ số FA theo chuẩn phân tích cổ phiếu Việt Nam
    
    Args:
        fa_ratios: Dictionary chứa các chỉ số FA từ calculate_fa_ratios()
    
    Returns:
        Dictionary chứa diễn giải và đánh giá các chỉ số
    """
    ratios = fa_ratios.get("ratios", {})
    
    interpretation = {
        "symbol": fa_ratios.get("symbol"),
        "analysis_date": datetime.now().isoformat(),
        "interpretations": {},
        "overall_rating": None,
        "investment_considerations": []
    }
    
    # === Diễn giải P/E ===
    pe = ratios.get("PE")
    if pe:
        if pe < 10:
            interpretation["interpretations"]["PE"] = {
                "value": pe,
                "rating": "low",
                "meaning": "Cổ phiếu có thể bị định giá thấp hoặc doanh nghiệp gặp khó khăn",
                "investment_note": "Cần xem xét kỹ nguyên nhân P/E thấp"
            }
        elif pe <= 15:
            interpretation["interpretations"]["PE"] = {
                "value": pe,
                "rating": "reasonable",
                "meaning": "Định giá hợp lý cho thị trường Việt Nam",
                "investment_note": "Mức định giá tốt, phù hợp đầu tư dài hạn"
            }
        elif pe <= 25:
            interpretation["interpretations"]["PE"] = {
                "value": pe,
                "rating": "moderate",
                "meaning": "Định giá cao, kỳ vọng tăng trưởng tốt",
                "investment_note": "Cần đánh giá triển vọng tăng trưởng"
            }
        else:
            interpretation["interpretations"]["PE"] = {
                "value": pe,
                "rating": "high",
                "meaning": "Định giá rất cao, có thể bị thổi phồng",
                "investment_note": "Rủi ro cao, cần thận trọng"
            }
    
    # === Diễn giải ROE ===
    roe = ratios.get("ROE")
    if roe:
        if roe < 10:
            interpretation["interpretations"]["ROE"] = {
                "value": roe,
                "rating": "low",
                "meaning": "Hiệu quả sử dụng vốn thấp",
                "investment_note": "Doanh nghiệp sinh lời kém"
            }
        elif roe <= 15:
            interpretation["interpretations"]["ROE"] = {
                "value": roe,
                "rating": "moderate",
                "meaning": "Hiệu quả sử dụng vốn ở mức trung bình",
                "investment_note": "Mức sinh lời chấp nhận được"
            }
        elif roe <= 25:
            interpretation["interpretations"]["ROE"] = {
                "value": roe,
                "rating": "good",
                "meaning": "Hiệu quả sử dụng vốn tốt",
                "investment_note": "Doanh nghiệp sinh lời tốt"
            }
        else:
            interpretation["interpretations"]["ROE"] = {
                "value": roe,
                "rating": "excellent",
                "meaning": "Hiệu quả sử dụng vốn xuất sắc",
                "investment_note": "Doanh nghiệp rất hiệu quả"
            }
    
    # === Diễn giải NPM (Net Profit Margin) ===
    npm = ratios.get("NPM")
    if npm:
        if npm < 5:
            interpretation["interpretations"]["NPM"] = {
                "value": npm,
                "rating": "low",
                "meaning": "Biên lợi nhuận thấp",
                "investment_note": "Doanh nghiệp kiểm soát chi phí kém"
            }
        elif npm <= 10:
            interpretation["interpretations"]["NPM"] = {
                "value": npm,
                "rating": "moderate",
                "meaning": "Biên lợi nhuận trung bình",
                "investment_note": "Mức lợi nhuận ổn định"
            }
        elif npm <= 20:
            interpretation["interpretations"]["NPM"] = {
                "value": npm,
                "rating": "good",
                "meaning": "Biên lợi nhuận tốt",
                "investment_note": "Kiểm soát chi phí hiệu quả"
            }
        else:
            interpretation["interpretations"]["NPM"] = {
                "value": npm,
                "rating": "excellent",
                "meaning": "Biên lợi nhuận rất cao",
                "investment_note": "Lợi thế cạnh tranh mạnh"
            }
    
    # === Diễn giải D/E ===
    de = ratios.get("DE")
    if de:
        if de < 0.5:
            interpretation["interpretations"]["DE"] = {
                "value": de,
                "rating": "conservative",
                "meaning": "Tỷ lệ nợ rất thấp, tài chính an toàn",
                "investment_note": "Doanh nghiệp có thể tận dụng đòn bẩy tốt hơn"
            }
        elif de <= 1.0:
            interpretation["interpretations"]["DE"] = {
                "value": de,
                "rating": "moderate",
                "meaning": "Tỷ lệ nợ hợp lý",
                "investment_note": "Cân đối tốt giữa nợ và vốn"
            }
        elif de <= 2.0:
            interpretation["interpretations"]["DE"] = {
                "value": de,
                "rating": "high",
                "meaning": "Tỷ lệ nợ cao",
                "investment_note": "Cần theo dõi khả năng trả nợ"
            }
        else:
            interpretation["interpretations"]["DE"] = {
                "value": de,
                "rating": "very_high",
                "meaning": "Tỷ lệ nợ rất cao, rủi ro tài chính",
                "investment_note": "Rủi ro cao, cần thận trọng"
            }
    
    # === Đánh giá tổng thể ===
    ratings = [interp.get("rating") for interp in interpretation["interpretations"].values()]
    excellent_count = ratings.count("excellent")
    good_count = ratings.count("good")
    moderate_count = ratings.count("moderate")
    low_count = ratings.count("low")
    high_risk_count = ratings.count("high") + ratings.count("very_high")
    
    if excellent_count >= 2 or (excellent_count >= 1 and good_count >= 2):
        interpretation["overall_rating"] = "excellent"
        interpretation["investment_considerations"].append("Doanh nghiệp có chất lượng tốt, phù hợp đầu tư dài hạn")
    elif good_count >= 2:
        interpretation["overall_rating"] = "good"
        interpretation["investment_considerations"].append("Doanh nghiệp ổn định, có thể cân nhắc đầu tư")
    elif moderate_count >= 3:
        interpretation["overall_rating"] = "moderate"
        interpretation["investment_considerations"].append("Doanh nghiệp ở mức trung bình, cần phân tích thêm")
    else:
        interpretation["overall_rating"] = "caution"
        interpretation["investment_considerations"].append("Cần thận trọng, đánh giá kỹ trước khi đầu tư")
    
    return interpretation


if __name__ == "__main__":
    # Test với một số mã cổ phiếu
    test_symbols = ["VIC", "VCB", "FPT"]
    
    for symbol in test_symbols:
        print(f"\n{'='*60}")
        print(f"Phân tích FA cho mã {symbol}")
        print('='*60)
        
        # Tính toán FA ratios
        fa_ratios = calculate_fa_ratios(symbol)
        
        # Hiển thị kết quả
        print(f"\n📊 Các chỉ số FA:")
        print(f"   Mã: {fa_ratios['symbol']}")
        print(f"   Giá hiện tại: {fa_ratios.get('current_price')} {fa_ratios.get('price_unit', '')}")
        print(f"\n   Chỉ số:")
        for ratio_name, ratio_value in fa_ratios['ratios'].items():
            print(f"   - {ratio_name}: {ratio_value}")
        
        print(f"\n   Chất lượng dữ liệu:")
        for ratio_name, quality in fa_ratios['data_quality'].items():
            print(f"   - {ratio_name}: {quality}")
        
        print(f"\n   Độ hoàn thiện: {fa_ratios['completeness']['complete_ratios']}/{fa_ratios['completeness']['total_ratios']} ({fa_ratios['completeness']['percentage']}%)")
        
        # Diễn giải
        interpretation = get_fa_interpretation(fa_ratios)
        print(f"\n💡 Diễn giải:")
        print(f"   Đánh giá tổng thể: {interpretation['overall_rating']}")
        for ratio_name, interp in interpretation['interpretations'].items():
            print(f"\n   {ratio_name}:")
            print(f"   - Giá trị: {interp['value']}")
            print(f"   - Đánh giá: {interp['rating']}")
            print(f"   - Ý nghĩa: {interp['meaning']}")
            print(f"   - Lưu ý: {interp['investment_note']}")

