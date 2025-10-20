"""
VNStock Data Collector - Phiên bản đơn giản hóa
Được thiết kế để tích hợp với n8n workflow
Đảm bảo đơn vị tiền tệ VND và không làm tròn để tránh sai số
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
from decimal import Decimal

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VNStockDataCollector:
    """
    Class chính để thu thập toàn bộ dữ liệu cổ phiếu từ vnstock
    """
    
    def __init__(self):
        """Khởi tạo collector"""
        self.start_date = "2010-01-01"  # Ngày bắt đầu mặc định
        self.end_date = datetime.now().strftime("%Y-%m-%d")  # Ngày hiện tại
        
    def _format_currency_value(self, value: Any) -> Any:
        """
        Format giá trị tiền tệ để đảm bảo chính xác
        - Giữ nguyên giá trị gốc (không làm tròn)
        - Đảm bảo đơn vị VND
        - Xử lý các trường hợp đặc biệt
        """
        if value is None:
            return None
        
        # Nếu là số
        if isinstance(value, (int, float)):
            # Nếu là float nhưng có thể chuyển thành int (không có phần thập phân)
            if isinstance(value, float) and value.is_integer():
                return int(value)
            # Giữ nguyên số thực
            return value
        
        # Nếu là string số
        if isinstance(value, str):
            try:
                # Thử chuyển thành float trước
                float_val = float(value)
                if float_val.is_integer():
                    return int(float_val)
                return float_val
            except (ValueError, TypeError):
                return value
        
        # Các trường hợp khác giữ nguyên
        return value
    
    def _format_dataframe_currency(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Format toàn bộ DataFrame để đảm bảo tiền tệ chính xác
        """
        if df.empty:
            return df
        
        # Tạo bản copy để không ảnh hưởng đến dữ liệu gốc
        formatted_df = df.copy()
        
        # Các cột có thể chứa giá trị tiền tệ
        currency_columns = [
            'open', 'high', 'low', 'close', 'volume',
            'adj_close', 'adjusted_close', 'value', 'amount'
        ]
        
        # Format các cột tiền tệ
        for col in formatted_df.columns:
            if any(currency_keyword in col.lower() for currency_keyword in 
                   ['price', 'value', 'amount', 'volume', 'đồng', 'vnd', 'open', 'high', 'low', 'close']):
                formatted_df[col] = formatted_df[col].apply(self._format_currency_value)
        
        return formatted_df
        
    def get_stock_overview(self, symbol: str) -> Dict[str, Any]:
        """
        Lấy thông tin tổng quan về cổ phiếu
        """
        try:
            from vnstock import Vnstock
            
            # Khởi tạo vnstock client
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            
            # Lấy dữ liệu giá gần nhất (7 ngày)
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            
            current_data = stock.quote.history(start=start_date, end=end_date)
            
            # Format dữ liệu tiền tệ để đảm bảo chính xác
            formatted_data = self._format_dataframe_currency(current_data)
            
            overview_data = {
                "symbol": symbol,
                "current_price_info": formatted_data.to_dict('records') if not formatted_data.empty else {},
                "data_collection_time": datetime.now().isoformat(),
                "currency_unit": "VND",
                "note": "Basic stock data from vnstock - Currency values preserved without rounding"
            }
            
            return overview_data
            
        except Exception as e:
            logger.error(f"Lỗi khi lấy thông tin tổng quan cho {symbol}: {str(e)}")
            return {"error": str(e), "symbol": symbol}
    
    def get_historical_data(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Lấy dữ liệu lịch sử giá cổ phiếu
        """
        try:
            from vnstock import Vnstock
            
            # Khởi tạo vnstock client
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            
            start = start_date or self.start_date
            end = end_date or self.end_date
            
            # Không giới hạn khoảng thời gian - lấy toàn bộ dữ liệu theo yêu cầu
            start_dt = datetime.strptime(start, "%Y-%m-%d")
            end_dt = datetime.strptime(end, "%Y-%m-%d")
            
            # Ghi log khoảng thời gian yêu cầu
            logger.info(f"Lấy dữ liệu từ {start} đến {end} ({(end_dt - start_dt).days} ngày)")
            
            # Lấy dữ liệu theo ngày
            daily_data = stock.quote.history(start=start, end=end)
            
            # Format dữ liệu tiền tệ để đảm bảo chính xác
            formatted_daily_data = self._format_dataframe_currency(daily_data)
            
            historical_data = {
                "symbol": symbol,
                "period": {
                    "start_date": start,
                    "end_date": end
                },
                "daily_data": formatted_daily_data.to_dict('records') if not formatted_daily_data.empty else [],
                "total_trading_days": len(formatted_daily_data) if not formatted_daily_data.empty else 0,
                "currency_unit": "VND",
                "note": "Historical price data from vnstock - Currency values preserved without rounding"
            }
            
            return historical_data
            
        except Exception as e:
            logger.error(f"Lỗi khi lấy dữ liệu lịch sử cho {symbol}: {str(e)}")
            return {"error": str(e), "symbol": symbol}
    
    def get_financial_data(self, symbol: str) -> Dict[str, Any]:
        """
        Lấy dữ liệu tài chính của công ty
        """
        try:
            from vnstock import Vnstock
            
            # Khởi tạo vnstock client
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            
            # Thử lấy báo cáo tài chính
            balance_sheet = pd.DataFrame()
            try:
                balance_sheet = stock.finance.balance_sheet(period='quarterly', lang='vi')
            except:
                pass
            
            # Format dữ liệu tài chính để đảm bảo chính xác
            formatted_balance_sheet = self._format_dataframe_currency(balance_sheet)
            
            financial_data = {
                "symbol": symbol,
                "balance_sheet": formatted_balance_sheet.to_dict('records') if not formatted_balance_sheet.empty else [],
                "last_updated": datetime.now().isoformat(),
                "currency_unit": "VND",
                "note": "Financial data from vnstock - Currency values preserved without rounding"
            }
            
            return financial_data
            
        except Exception as e:
            logger.error(f"Lỗi khi lấy dữ liệu tài chính cho {symbol}: {str(e)}")
            return {"error": str(e), "symbol": symbol}
    
    def get_market_data(self, symbol: str) -> Dict[str, Any]:
        """
        Lấy dữ liệu thị trường và giao dịch
        """
        try:
            market_data = {
                "symbol": symbol,
                "data_timestamp": datetime.now().isoformat(),
                "note": "Market data placeholder - implement as needed"
            }
            
            return market_data
            
        except Exception as e:
            logger.error(f"Lỗi khi lấy dữ liệu thị trường cho {symbol}: {str(e)}")
            return {"error": str(e), "symbol": symbol}
    
    def get_complete_stock_data(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Lấy toàn bộ dữ liệu của một mã cổ phiếu
        """
        logger.info(f"Bắt đầu thu thập dữ liệu cho mã cổ phiếu: {symbol}")
        
        # Chuẩn hóa mã cổ phiếu
        symbol = symbol.upper().strip()
        
        complete_data = {
            "request_info": {
                "symbol": symbol,
                "start_date": start_date or self.start_date,
                "end_date": end_date or self.end_date,
                "collection_timestamp": datetime.now().isoformat(),
                "data_source": "vnstock"
            }
        }
        
        # Thu thập từng loại dữ liệu
        logger.info("Thu thập thông tin tổng quan...")
        complete_data["overview"] = self.get_stock_overview(symbol)
        
        logger.info("Thu thập dữ liệu lịch sử...")
        complete_data["historical_data"] = self.get_historical_data(symbol, start_date, end_date)
        
        logger.info("Thu thập dữ liệu tài chính...")
        complete_data["financial_data"] = self.get_financial_data(symbol)
        
        logger.info("Thu thập dữ liệu thị trường...")
        complete_data["market_data"] = self.get_market_data(symbol)
        
        # Thêm metadata cho AI analysis
        complete_data["ai_analysis_metadata"] = {
            "data_completeness": self._check_data_completeness(complete_data),
            "analysis_suggestions": self._generate_analysis_suggestions(complete_data),
            "key_metrics_summary": self._extract_key_metrics(complete_data),
            "currency_info": {
                "unit": "VND",
                "description": "Vietnamese Dong",
                "precision": "No rounding applied - original values preserved",
                "note": "All monetary values are in VND without any rounding to prevent calculation errors"
            }
        }
        
        logger.info(f"Hoàn thành thu thập dữ liệu cho {symbol}")
        return complete_data
    
    def _check_data_completeness(self, data: Dict[str, Any]) -> Dict[str, bool]:
        """Kiểm tra tính đầy đủ của dữ liệu"""
        completeness = {
            "has_overview": "error" not in data.get("overview", {}),
            "has_historical_data": len(data.get("historical_data", {}).get("daily_data", [])) > 0,
            "has_financial_data": "error" not in data.get("financial_data", {}),
            "has_market_data": "error" not in data.get("market_data", {})
        }
        completeness["overall_complete"] = all(completeness.values())
        return completeness
    
    def _generate_analysis_suggestions(self, data: Dict[str, Any]) -> List[str]:
        """Tạo gợi ý phân tích cho AI"""
        suggestions = [
            "Phân tích xu hướng giá trong thời gian được yêu cầu",
            "Đánh giá biến động giá và khối lượng giao dịch",
            "So sánh hiệu suất với thị trường chung",
            "Phân tích các mức hỗ trợ và kháng cự",
            "Đánh giá tình hình tài chính (nếu có dữ liệu)"
        ]
        
        return suggestions
    
    def _extract_key_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Trích xuất các chỉ số quan trọng"""
        metrics = {}
        
        # Dữ liệu lịch sử
        historical = data.get("historical_data", {}).get("daily_data", [])
        if historical:
            metrics["total_trading_days"] = len(historical)
            latest_data = historical[-1] if historical else {}
            metrics["latest_price"] = latest_data.get("close", 0)
            metrics["latest_volume"] = latest_data.get("volume", 0)
            
            # Tính toán một số chỉ số cơ bản
            prices = [day.get("close", 0) for day in historical if day.get("close")]
            if len(prices) > 1:
                metrics["price_change_period"] = prices[-1] - prices[0]
                metrics["price_change_percent"] = ((prices[-1] - prices[0]) / prices[0] * 100) if prices[0] > 0 else 0
                metrics["max_price"] = max(prices)
                metrics["min_price"] = min(prices)
        
        return metrics
