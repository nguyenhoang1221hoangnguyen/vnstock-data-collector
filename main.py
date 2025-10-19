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

if __name__ == "__main__":
    # Chạy server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8501,
        reload=True,
        log_level="info"
    )
