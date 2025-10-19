"""
VNStock Data Collector - Module thu thập dữ liệu cổ phiếu từ vnstock
Được thiết kế để tích hợp với n8n workflow
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
from vnstock import Vnstock, Listing

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
        
    def get_stock_overview(self, symbol: str) -> Dict[str, Any]:
        """
        Lấy thông tin tổng quan về cổ phiếu
        
        Args:
            symbol: Mã cổ phiếu (VD: VIC, VCB, FPT)
            
        Returns:
            Dict chứa thông tin tổng quan
        """
        try:
            # Khởi tạo vnstock client
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            
            # Thông tin giao dịch hiện tại (lấy 1 ngày gần nhất)
            current_data = stock.quote.history(start=self.end_date, end=self.end_date)
            
            # Thông tin cơ bản công ty (thử các phương thức khác nhau)
            company_info = {}
            try:
                # Thử lấy thông tin cơ bản
                info = stock.company.overview()
                company_info = info.to_dict('records')[0] if not info.empty else {}
            except:
                try:
                    # Thử phương thức khác
                    info = stock.company.profile()
                    company_info = info.to_dict('records')[0] if not info.empty else {}
                except:
                    company_info = {"note": "Company info not available"}
            
            overview_data = {
                "symbol": symbol,
                "company_info": company_info,
                "current_price_info": current_data.to_dict('records')[0] if not current_data.empty else {},
                "data_collection_time": datetime.now().isoformat()
            }
            
            return overview_data
            
        except Exception as e:
            logger.error(f"Lỗi khi lấy thông tin tổng quan cho {symbol}: {str(e)}")
            return {"error": str(e), "symbol": symbol}
    
    def get_historical_data(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Lấy dữ liệu lịch sử giá cổ phiếu
        
        Args:
            symbol: Mã cổ phiếu
            start_date: Ngày bắt đầu (YYYY-MM-DD)
            end_date: Ngày kết thúc (YYYY-MM-DD)
            
        Returns:
            Dict chứa dữ liệu lịch sử
        """
        try:
            # Khởi tạo vnstock client
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            
            start = start_date or self.start_date
            end = end_date or self.end_date
            
            # Lấy dữ liệu theo ngày
            daily_data = stock.quote.history(start=start, end=end)
            
            # Lấy dữ liệu theo tuần và tháng (sử dụng resample nếu cần)
            weekly_data = pd.DataFrame()
            monthly_data = pd.DataFrame()
            
            if not daily_data.empty:
                # Resample để tạo dữ liệu tuần và tháng
                daily_data_indexed = daily_data.set_index('time')
                daily_data_indexed.index = pd.to_datetime(daily_data_indexed.index)
                
                # Dữ liệu theo tuần
                weekly_data = daily_data_indexed.resample('W').agg({
                    'open': 'first',
                    'high': 'max',
                    'low': 'min',
                    'close': 'last',
                    'volume': 'sum'
                }).reset_index()
                
                # Dữ liệu theo tháng
                monthly_data = daily_data_indexed.resample('M').agg({
                    'open': 'first',
                    'high': 'max',
                    'low': 'min',
                    'close': 'last',
                    'volume': 'sum'
                }).reset_index()
            
            historical_data = {
                "symbol": symbol,
                "period": {
                    "start_date": start,
                    "end_date": end
                },
                "daily_data": daily_data.to_dict('records') if not daily_data.empty else [],
                "weekly_data": weekly_data.to_dict('records') if not weekly_data.empty else [],
                "monthly_data": monthly_data.to_dict('records') if not monthly_data.empty else [],
                "total_trading_days": len(daily_data) if not daily_data.empty else 0
            }
            
            return historical_data
            
        except Exception as e:
            logger.error(f"Lỗi khi lấy dữ liệu lịch sử cho {symbol}: {str(e)}")
            return {"error": str(e), "symbol": symbol}
    
    def get_financial_data(self, symbol: str) -> Dict[str, Any]:
        """
        Lấy dữ liệu tài chính của công ty
        
        Args:
            symbol: Mã cổ phiếu
            
        Returns:
            Dict chứa dữ liệu tài chính
        """
        try:
            # Khởi tạo vnstock client
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            
            # Báo cáo tài chính
            balance_sheet = stock.finance.balance_sheet(period='quarterly', lang='vi')
            income_statement = stock.finance.income_statement(period='quarterly', lang='vi')
            cash_flow = stock.finance.cash_flow(period='quarterly', lang='vi')
            
            # Chỉ số tài chính
            ratios = stock.finance.ratio(period='quarterly', lang='vi')
            
            financial_data = {
                "symbol": symbol,
                "balance_sheet": balance_sheet.to_dict('records') if not balance_sheet.empty else [],
                "income_statement": income_statement.to_dict('records') if not income_statement.empty else [],
                "cash_flow": cash_flow.to_dict('records') if not cash_flow.empty else [],
                "financial_ratios": ratios.to_dict('records') if not ratios.empty else [],
                "last_updated": datetime.now().isoformat()
            }
            
            return financial_data
            
        except Exception as e:
            logger.error(f"Lỗi khi lấy dữ liệu tài chính cho {symbol}: {str(e)}")
            return {"error": str(e), "symbol": symbol}
    
    def get_market_data(self, symbol: str) -> Dict[str, Any]:
        """
        Lấy dữ liệu thị trường và giao dịch
        
        Args:
            symbol: Mã cổ phiếu
            
        Returns:
            Dict chứa dữ liệu thị trường
        """
        try:
            # Khởi tạo vnstock client
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            
            # Dữ liệu giao dịch trong ngày (nếu có)
            large_transactions = pd.DataFrame()
            try:
                large_transactions = stock.quote.intraday()
            except:
                large_transactions = pd.DataFrame({"note": ["Intraday data not available"]})
            
            # Thông tin cổ đông
            shareholders = pd.DataFrame()
            try:
                shareholders = stock.company.shareholders()
            except:
                shareholders = pd.DataFrame({"note": ["Shareholders data not available"]})
            
            # Sự kiện doanh nghiệp
            events = pd.DataFrame()
            try:
                events = stock.company.events()
            except:
                events = pd.DataFrame({"note": ["Events data not available"]})
            
            market_data = {
                "symbol": symbol,
                "large_transactions": large_transactions.to_dict('records') if not large_transactions.empty else [],
                "shareholders": shareholders.to_dict('records') if not shareholders.empty else [],
                "company_events": events.to_dict('records') if not events.empty else [],
                "data_timestamp": datetime.now().isoformat()
            }
            
            return market_data
            
        except Exception as e:
            logger.error(f"Lỗi khi lấy dữ liệu thị trường cho {symbol}: {str(e)}")
            return {"error": str(e), "symbol": symbol}
    
    def get_complete_stock_data(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Lấy toàn bộ dữ liệu của một mã cổ phiếu
        
        Args:
            symbol: Mã cổ phiếu
            start_date: Ngày bắt đầu (YYYY-MM-DD)
            end_date: Ngày kết thúc (YYYY-MM-DD)
            
        Returns:
            Dict chứa toàn bộ dữ liệu cổ phiếu
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
            "key_metrics_summary": self._extract_key_metrics(complete_data)
        }
        
        logger.info(f"Hoàn thành thu thập dữ liệu cho {symbol}")
        return complete_data
    
    def _check_data_completeness(self, data: Dict[str, Any]) -> Dict[str, bool]:
        """Kiểm tra tính đầy đủ của dữ liệu"""
        completeness = {
            "has_overview": "error" not in data.get("overview", {}),
            "has_historical_data": len(data.get("historical_data", {}).get("daily_data", [])) > 0,
            "has_financial_data": len(data.get("financial_data", {}).get("balance_sheet", [])) > 0,
            "has_market_data": "error" not in data.get("market_data", {})
        }
        completeness["overall_complete"] = all(completeness.values())
        return completeness
    
    def _generate_analysis_suggestions(self, data: Dict[str, Any]) -> List[str]:
        """Tạo gợi ý phân tích cho AI"""
        suggestions = [
            "Phân tích xu hướng giá trong 1 năm qua",
            "So sánh hiệu suất với VN-Index",
            "Đánh giá tình hình tài chính qua các quý",
            "Phân tích khối lượng giao dịch và thanh khoản",
            "Xem xét các sự kiện doanh nghiệp ảnh hưởng đến giá"
        ]
        
        # Thêm gợi ý dựa trên dữ liệu có sẵn
        if data.get("financial_data", {}).get("financial_ratios"):
            suggestions.append("Phân tích các chỉ số tài chính P/E, ROE, ROA")
        
        if data.get("market_data", {}).get("shareholders"):
            suggestions.append("Phân tích cơ cấu cổ đông và sự thay đổi")
            
        return suggestions
    
    def _extract_key_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Trích xuất các chỉ số quan trọng"""
        metrics = {}
        
        # Giá hiện tại
        current_price = data.get("overview", {}).get("current_price_info", {})
        if current_price:
            metrics["current_price"] = current_price.get("close", 0)
            metrics["price_change"] = current_price.get("change", 0)
            metrics["volume"] = current_price.get("volume", 0)
        
        # Dữ liệu lịch sử
        historical = data.get("historical_data", {}).get("daily_data", [])
        if historical:
            metrics["total_trading_days"] = len(historical)
            metrics["price_range_52w"] = {
                "high": max([day.get("high", 0) for day in historical[-252:]] or [0]),
                "low": min([day.get("low", 0) for day in historical[-252:]] or [0])
            }
        
        return metrics
