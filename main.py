"""
FastAPI Server cho VNStock Data Collector
Được thiết kế để tích hợp với n8n workflow
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
from datetime import datetime
import logging

from vnstock_data_collector_simple import VNStockDataCollector
from fa_calculator import calculate_fa_ratios, get_fa_interpretation
from ta_analyzer import calculate_ta_indicators, plot_technical_chart, get_ta_analysis
from stock_screener import get_stock_list, screen_stock, run_screener
from backtesting_strategy import run_ma_crossover_backtest
from bluechip_detector import BlueChipDetector

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Khởi tạo FastAPI app
app = FastAPI(
    title="VNStock Data Collector API",
    description="API để thu thập dữ liệu cổ phiếu Việt Nam cho n8n workflow",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Cấu hình CORS cho n8n
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên giới hạn origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Khởi tạo data collector
collector = VNStockDataCollector()

# Pydantic models cho request/response
class StockRequest(BaseModel):
    symbol: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class StockResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str

@app.get("/")
async def root():
    """Endpoint gốc - thông tin API"""
    return {
        "message": "VNStock Data Collector API",
        "version": "1.0.0",
        "description": "API để thu thập dữ liệu cổ phiếu Việt Nam",
        "endpoints": {
            "/stock/{symbol}": "Lấy toàn bộ dữ liệu cổ phiếu",
            "/stock/{symbol}/overview": "Lấy thông tin tổng quan",
            "/stock/{symbol}/historical": "Lấy dữ liệu lịch sử",
            "/stock/{symbol}/financial": "Lấy dữ liệu tài chính",
            "/stock/{symbol}/market": "Lấy dữ liệu thị trường",
            "/stock/{symbol}/fa": "Phân tích cơ bản (FA) - Tính toán chỉ số",
            "/stock/{symbol}/fa/interpret": "Phân tích FA với diễn giải đầy đủ",
            "/stock/{symbol}/ta": "Phân tích kỹ thuật (TA) - Tính toán chỉ báo",
            "/stock/{symbol}/ta/analyze": "Phân tích TA với diễn giải tín hiệu",
            "/stock/{symbol}/ta/chart": "Vẽ biểu đồ kỹ thuật (candlestick + indicators)",
            "/screener/list": "Lấy danh sách cổ phiếu theo sàn",
            "/screener/screen": "Sàng lọc cổ phiếu theo tiêu chí FA + TA",
            "/screener/{symbol}": "Kiểm tra một mã cổ phiếu với tiêu chí",
            "/backtest/{symbol}": "Backtest chiến lược MA Crossover",
            "/health": "Kiểm tra trạng thái API"
        }
    }

@app.get("/health")
async def health_check():
    """Kiểm tra trạng thái API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "VNStock Data Collector"
    }

@app.get("/stock/{symbol}", response_model=StockResponse)
async def get_complete_stock_data(
    symbol: str,
    start_date: Optional[str] = Query(None, description="Ngày bắt đầu (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Ngày kết thúc (YYYY-MM-DD)")
):
    """
    Lấy toàn bộ dữ liệu của một mã cổ phiếu
    
    - **symbol**: Mã cổ phiếu (VD: VIC, VCB, FPT)
    - **start_date**: Ngày bắt đầu (tùy chọn, mặc định từ 2010-01-01)
    - **end_date**: Ngày kết thúc (tùy chọn, mặc định đến hiện tại)
    """
    try:
        logger.info(f"Nhận yêu cầu lấy dữ liệu cho mã: {symbol}")
        
        # Validate symbol
        if not symbol or len(symbol.strip()) == 0:
            raise HTTPException(status_code=400, detail="Mã cổ phiếu không được để trống")
        
        # Validate dates nếu có
        if start_date:
            try:
                datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(status_code=400, detail="Định dạng start_date không hợp lệ. Sử dụng YYYY-MM-DD")
        
        if end_date:
            try:
                datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(status_code=400, detail="Định dạng end_date không hợp lệ. Sử dụng YYYY-MM-DD")
        
        # Thu thập dữ liệu
        data = collector.get_complete_stock_data(symbol, start_date, end_date)
        
        return StockResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lỗi khi xử lý yêu cầu cho {symbol}: {str(e)}")
        return StockResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.get("/stock/{symbol}/overview", response_model=StockResponse)
async def get_stock_overview(symbol: str):
    """Lấy thông tin tổng quan về cổ phiếu"""
    try:
        if not symbol or len(symbol.strip()) == 0:
            raise HTTPException(status_code=400, detail="Mã cổ phiếu không được để trống")
        
        data = collector.get_stock_overview(symbol)
        
        return StockResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lỗi khi lấy thông tin tổng quan cho {symbol}: {str(e)}")
        return StockResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.get("/stock/{symbol}/historical", response_model=StockResponse)
async def get_historical_data(
    symbol: str,
    start_date: Optional[str] = Query(None, description="Ngày bắt đầu (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Ngày kết thúc (YYYY-MM-DD)")
):
    """Lấy dữ liệu lịch sử giá cổ phiếu"""
    try:
        if not symbol or len(symbol.strip()) == 0:
            raise HTTPException(status_code=400, detail="Mã cổ phiếu không được để trống")
        
        data = collector.get_historical_data(symbol, start_date, end_date)
        
        return StockResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu lịch sử cho {symbol}: {str(e)}")
        return StockResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.get("/stock/{symbol}/financial", response_model=StockResponse)
async def get_financial_data(symbol: str):
    """Lấy dữ liệu tài chính của công ty"""
    try:
        if not symbol or len(symbol.strip()) == 0:
            raise HTTPException(status_code=400, detail="Mã cổ phiếu không được để trống")
        
        data = collector.get_financial_data(symbol)
        
        return StockResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu tài chính cho {symbol}: {str(e)}")
        return StockResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.get("/stock/{symbol}/market", response_model=StockResponse)
async def get_market_data(symbol: str):
    """Lấy dữ liệu thị trường và giao dịch"""
    try:
        if not symbol or len(symbol.strip()) == 0:
            raise HTTPException(status_code=400, detail="Mã cổ phiếu không được để trống")
        
        data = collector.get_market_data(symbol)
        
        return StockResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu thị trường cho {symbol}: {str(e)}")
        return StockResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.post("/stock/batch", response_model=StockResponse)
async def get_batch_stock_data(request: StockRequest):
    """
    Lấy dữ liệu cổ phiếu qua POST request (phù hợp cho n8n)
    """
    try:
        data = collector.get_complete_stock_data(
            request.symbol, 
            request.start_date, 
            request.end_date
        )
        
        return StockResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Lỗi khi xử lý batch request: {str(e)}")
        return StockResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.get("/stock/{symbol}/fa", response_model=StockResponse)
async def get_fa_ratios(symbol: str):
    """
    Phân tích cơ bản (FA) - Tính toán các chỉ số tài chính
    
    - **symbol**: Mã cổ phiếu (VD: VIC, VCB, FPT)
    
    Trả về các chỉ số:
    - P/E (Price to Earnings): Giá / Thu nhập
    - ROE (Return on Equity): Lợi nhuận ròng / Vốn chủ sở hữu
    - NPM (Net Profit Margin): Biên lợi nhuận ròng
    - D/E (Debt to Equity): Nợ / Vốn chủ sở hữu
    - EPS (Earnings Per Share): Thu nhập mỗi cổ phiếu
    """
    try:
        if not symbol or len(symbol.strip()) == 0:
            raise HTTPException(status_code=400, detail="Mã cổ phiếu không được để trống")
        
        logger.info(f"Tính toán FA ratios cho mã: {symbol}")
        data = calculate_fa_ratios(symbol)
        
        return StockResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lỗi khi tính FA ratios cho {symbol}: {str(e)}")
        return StockResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.get("/stock/{symbol}/fa/interpret", response_model=StockResponse)
async def get_fa_interpretation_endpoint(symbol: str):
    """
    Phân tích FA với diễn giải đầy đủ
    
    - **symbol**: Mã cổ phiếu (VD: VIC, VCB, FPT)
    
    Trả về:
    - Các chỉ số FA
    - Diễn giải từng chỉ số
    - Đánh giá tổng thể
    - Khuyến nghị đầu tư
    """
    try:
        if not symbol or len(symbol.strip()) == 0:
            raise HTTPException(status_code=400, detail="Mã cổ phiếu không được để trống")
        
        logger.info(f"Phân tích FA đầy đủ cho mã: {symbol}")
        
        # Tính toán FA ratios
        fa_ratios = calculate_fa_ratios(symbol)
        
        # Diễn giải
        interpretation = get_fa_interpretation(fa_ratios)
        
        # Kết hợp kết quả
        result = {
            "fa_ratios": fa_ratios,
            "interpretation": interpretation
        }
        
        return StockResponse(
            success=True,
            data=result,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lỗi khi phân tích FA cho {symbol}: {str(e)}")
        return StockResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.get("/stock/{symbol}/ta", response_model=StockResponse)
async def get_ta_indicators(
    symbol: str,
    period_days: Optional[int] = Query(365, description="Số ngày lấy dữ liệu (mặc định 365)")
):
    """
    Phân tích kỹ thuật (TA) - Tính toán các chỉ báo
    
    - **symbol**: Mã cổ phiếu (VD: FPT, VIC, VCB)
    - **period_days**: Số ngày lấy dữ liệu (mặc định 365 ngày)
    
    Trả về các chỉ báo:
    - MA(50), MA(200): Moving Averages
    - RSI(14): Relative Strength Index
    - MACD(12, 26, 9): Moving Average Convergence Divergence
    - Bollinger Bands (20, 2)
    """
    try:
        if not symbol or len(symbol.strip()) == 0:
            raise HTTPException(status_code=400, detail="Mã cổ phiếu không được để trống")
        
        logger.info(f"Tính toán TA indicators cho mã: {symbol}")
        ta_result = calculate_ta_indicators(symbol, period_days)
        
        if ta_result.get("error"):
            return StockResponse(
                success=False,
                error=ta_result["error"],
                timestamp=datetime.now().isoformat()
            )
        
        # Loại bỏ DataFrame khỏi response (quá lớn)
        response_data = {
            "symbol": ta_result["symbol"],
            "period": ta_result["period"],
            "current_price": ta_result["current_price"],
            "price_unit": ta_result["price_unit"],
            "indicators": ta_result["indicators"],
            "calculation_date": ta_result["calculation_date"]
        }
        
        return StockResponse(
            success=True,
            data=response_data,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lỗi khi tính TA indicators cho {symbol}: {str(e)}")
        return StockResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.get("/stock/{symbol}/ta/analyze", response_model=StockResponse)
async def get_ta_analysis_endpoint(
    symbol: str,
    period_days: Optional[int] = Query(365, description="Số ngày lấy dữ liệu (mặc định 365)")
):
    """
    Phân tích TA với diễn giải tín hiệu
    
    - **symbol**: Mã cổ phiếu (VD: FPT, VIC, VCB)
    - **period_days**: Số ngày lấy dữ liệu (mặc định 365 ngày)
    
    Trả về:
    - Các chỉ báo TA
    - Diễn giải từng chỉ báo
    - Tín hiệu mua/bán
    - Xu hướng tổng thể (BULLISH/BEARISH/NEUTRAL)
    """
    try:
        if not symbol or len(symbol.strip()) == 0:
            raise HTTPException(status_code=400, detail="Mã cổ phiếu không được để trống")
        
        logger.info(f"Phân tích TA đầy đủ cho mã: {symbol}")
        analysis = get_ta_analysis(symbol, period_days)
        
        if analysis.get("error"):
            return StockResponse(
                success=False,
                error=analysis["error"],
                timestamp=datetime.now().isoformat()
            )
        
        return StockResponse(
            success=True,
            data=analysis,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lỗi khi phân tích TA cho {symbol}: {str(e)}")
        return StockResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.get("/stock/{symbol}/ta/chart")
async def generate_ta_chart(
    symbol: str,
    period_days: Optional[int] = Query(365, description="Số ngày lấy dữ liệu (mặc định 365)")
):
    """
    Vẽ biểu đồ kỹ thuật (candlestick + indicators)
    
    - **symbol**: Mã cổ phiếu (VD: FPT, VIC, VCB)
    - **period_days**: Số ngày lấy dữ liệu (mặc định 365 ngày)
    
    Trả về:
    - Thông tin biểu đồ đã tạo
    - Đường dẫn file biểu đồ
    - Các chỉ báo trên biểu đồ
    """
    try:
        if not symbol or len(symbol.strip()) == 0:
            raise HTTPException(status_code=400, detail="Mã cổ phiếu không được để trống")
        
        logger.info(f"Vẽ biểu đồ TA cho mã: {symbol}")
        chart_result = plot_technical_chart(symbol, period_days)
        
        if not chart_result.get("success"):
            return StockResponse(
                success=False,
                error=chart_result.get("error", "Không thể tạo biểu đồ"),
                timestamp=datetime.now().isoformat()
            )
        
        return StockResponse(
            success=True,
            data=chart_result,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lỗi khi vẽ biểu đồ TA cho {symbol}: {str(e)}")
        return StockResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.get("/screener/list")
async def get_stock_list_endpoint(
    exchange: Optional[str] = Query("HOSE", description="Sàn giao dịch (HOSE, HNX, UPCOM)")
):
    """
    Lấy danh sách tất cả cổ phiếu trên sàn
    
    - **exchange**: Sàn giao dịch (HOSE, HNX, UPCOM)
    
    Trả về:
    - Danh sách mã cổ phiếu
    - Tổng số mã
    """
    try:
        logger.info(f"Lấy danh sách cổ phiếu sàn {exchange}")
        stock_list = get_stock_list(exchange)
        
        return StockResponse(
            success=True,
            data={
                "exchange": exchange,
                "total_stocks": len(stock_list),
                "stocks": stock_list
            },
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Lỗi khi lấy danh sách cổ phiếu: {str(e)}")
        return StockResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.get("/screener/{symbol}")
async def screen_single_stock(
    symbol: str,
    pe_max: Optional[float] = Query(15, description="P/E tối đa"),
    roe_min: Optional[float] = Query(18, description="ROE tối thiểu %"),
    price_vs_ma50: Optional[str] = Query("above", description="Giá so với MA50 (above/below)")
):
    """
    Kiểm tra một mã cổ phiếu với các tiêu chí sàng lọc
    
    - **symbol**: Mã cổ phiếu
    - **pe_max**: P/E tối đa (mặc định 15)
    - **roe_min**: ROE tối thiểu % (mặc định 18)
    - **price_vs_ma50**: Giá so với MA50 (above/below)
    
    Trả về:
    - Thông tin FA, TA
    - Kết quả kiểm tra từng tiêu chí
    - Kết quả tổng thể (passed/failed)
    """
    try:
        if not symbol or len(symbol.strip()) == 0:
            raise HTTPException(status_code=400, detail="Mã cổ phiếu không được để trống")
        
        logger.info(f"Sàng lọc mã {symbol}")
        result = screen_stock(symbol, pe_max, roe_min, price_vs_ma50)
        
        return StockResponse(
            success=True,
            data=result,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lỗi khi sàng lọc {symbol}: {str(e)}")
        return StockResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.get("/screener/screen")
async def run_stock_screener(
    exchange: Optional[str] = Query("HOSE", description="Sàn giao dịch"),
    limit: Optional[int] = Query(20, description="Số lượng mã test"),
    pe_max: Optional[float] = Query(15, description="P/E tối đa"),
    roe_min: Optional[float] = Query(18, description="ROE tối thiểu %"),
    price_vs_ma50: Optional[str] = Query("above", description="Giá so với MA50"),
    delay: Optional[float] = Query(1.0, description="Delay giữa các request (giây)")
):
    """
    Sàng lọc nhiều cổ phiếu theo tiêu chí FA + TA
    
    - **exchange**: Sàn giao dịch (HOSE, HNX, UPCOM)
    - **limit**: Số lượng mã test (mặc định 20)
    - **pe_max**: P/E tối đa (mặc định 15)
    - **roe_min**: ROE tối thiểu % (mặc định 18)
    - **price_vs_ma50**: Giá so với MA50 (above/below)
    - **delay**: Delay giữa các request (giây)
    
    Trả về:
    - Tổng số mã đã sàng lọc
    - Số mã đạt tiêu chí
    - Danh sách mã đạt tiêu chí
    - Chi tiết từng mã
    """
    try:
        logger.info(f"Chạy stock screener cho sàn {exchange}")
        
        results = run_screener(
            exchange=exchange,
            limit=limit,
            pe_max=pe_max,
            roe_min=roe_min,
            price_vs_ma50=price_vs_ma50,
            delay=delay
        )
        
        if not results.get("success"):
            return StockResponse(
                success=False,
                error=results.get("error", "Unknown error"),
                timestamp=datetime.now().isoformat()
            )
        
        return StockResponse(
            success=True,
            data=results,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Lỗi khi chạy screener: {str(e)}")
        return StockResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.get("/backtest/{symbol}")
async def backtest_ma_crossover(
    symbol: str,
    initial_cash: Optional[float] = Query(100_000_000, description="Vốn ban đầu (VND)"),
    ma_fast: Optional[int] = Query(20, description="MA nhanh"),
    ma_slow: Optional[int] = Query(50, description="MA chậm"),
    period_days: Optional[int] = Query(1095, description="Số ngày dữ liệu (3 năm)"),
    commission: Optional[float] = Query(0.001, description="Phí giao dịch (0.1%)")
):
    """
    Backtest chiến lược MA Crossover
    
    - **symbol**: Mã cổ phiếu (VD: TCB, VCB, FPT)
    - **initial_cash**: Vốn ban đầu VND (mặc định 100 triệu)
    - **ma_fast**: MA nhanh (mặc định 20)
    - **ma_slow**: MA chậm (mặc định 50)
    - **period_days**: Số ngày dữ liệu (mặc định 1095 = 3 năm)
    - **commission**: Phí giao dịch (mặc định 0.001 = 0.1%)
    
    Chiến lược:
    - Mua khi MA nhanh cắt lên MA chậm (Golden Cross)
    - Bán khi MA nhanh cắt xuống MA chậm (Death Cross)
    
    Trả về:
    - Kết quả backtest chi tiết
    - Thống kê (Equity, Return, Win Rate, Drawdown)
    - Diễn giải và khuyến nghị
    """
    try:
        if not symbol or len(symbol.strip()) == 0:
            raise HTTPException(status_code=400, detail="Mã cổ phiếu không được để trống")
        
        logger.info(f"Chạy backtest cho mã {symbol}")
        
        result = run_ma_crossover_backtest(
            symbol=symbol,
            initial_cash=initial_cash,
            ma_fast=ma_fast,
            ma_slow=ma_slow,
            period_days=period_days,
            commission=commission
        )
        
        if not result.get("success"):
            return StockResponse(
                success=False,
                error=result.get("error", "Unknown error"),
                timestamp=datetime.now().isoformat()
            )
        
        return StockResponse(
            success=True,
            data=result,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Lỗi khi chạy backtest cho {symbol}: {str(e)}")
        return StockResponse(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )


# ========== BLUE-CHIP DETECTOR ENDPOINTS ==========

@app.get("/bluechip/scan")
async def scan_bluechips(
    symbols: Optional[str] = Query(None, description="Comma-separated list of symbols (default: VN30)"),
    min_score: int = Query(4, description="Minimum score to be considered blue-chip (1-6)")
):
    """
    Scan for blue-chip stocks
    
    Args:
        symbols: Comma-separated symbols (e.g. "ACB,VCB,TCB") or None for VN30
        min_score: Minimum score (1-6) to qualify as blue-chip
    
    Returns:
        List of blue-chip stocks with detailed analysis
    """
    try:
        detector = BlueChipDetector()
        
        # Parse symbols
        symbol_list = None
        if symbols:
            symbol_list = [s.strip().upper() for s in symbols.split(',')]
        
        # Scan
        bluechips = detector.scan_bluechips(symbols=symbol_list, min_score=min_score)
        
        return {
            "success": True,
            "total": len(bluechips),
            "bluechips": bluechips,
            "scan_date": datetime.now().isoformat(),
            "criteria": detector.criteria
        }
    except Exception as e:
        logger.error(f"Error scanning blue-chips: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@app.post("/bluechip/add-to-watchlist")
async def add_bluechips_to_watchlist(
    symbols: Optional[str] = Query(None, description="Comma-separated symbols or None for VN30"),
    min_score: int = Query(4, description="Minimum score to add to watchlist")
):
    """
    Scan for blue-chips and auto-add to watchlist
    
    Args:
        symbols: Comma-separated symbols or None for VN30
        min_score: Minimum score to qualify
    
    Returns:
        Number of stocks added to watchlist
    """
    try:
        detector = BlueChipDetector()
        
        # Parse symbols
        symbol_list = None
        if symbols:
            symbol_list = [s.strip().upper() for s in symbols.split(',')]
        
        # Scan and add
        bluechips = detector.scan_bluechips(symbols=symbol_list, min_score=min_score)
        added = detector.auto_add_to_watchlist(bluechips)
        
        return {
            "success": True,
            "scanned": len(bluechips),
            "added": added,
            "symbols": [bc['symbol'] for bc in bluechips],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error adding blue-chips to watchlist: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@app.get("/bluechip/report")
async def get_bluechip_report(
    symbols: Optional[str] = Query(None, description="Comma-separated symbols or None for VN30"),
    min_score: int = Query(4, description="Minimum score")
):
    """
    Get detailed blue-chip report
    
    Returns:
        Formatted text report of blue-chip stocks
    """
    try:
        detector = BlueChipDetector()
        
        # Parse symbols
        symbol_list = None
        if symbols:
            symbol_list = [s.strip().upper() for s in symbols.split(',')]
        
        # Scan
        bluechips = detector.scan_bluechips(symbols=symbol_list, min_score=min_score)
        report = detector.get_bluechip_report(bluechips)
        
        return {
            "success": True,
            "report": report,
            "bluechips": bluechips,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


if __name__ == "__main__":
    # Chạy server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8501,
        reload=True,
        log_level="info"
    )
