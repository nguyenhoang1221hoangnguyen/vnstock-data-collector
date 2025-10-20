#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VNStock Data Collector - Web Interface
Giao diện web đẹp mắt để tra cứu thông tin cổ phiếu
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import json
import logging
from typing import Optional, List, Dict, Any
import pandas as pd
from datetime import datetime, timedelta
import os

# Import data collector
from vnstock_data_collector_simple import VNStockDataCollector

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="VNStock Data Collector - Web Interface",
    description="Giao diện web tra cứu thông tin cổ phiếu Việt Nam",
    version="1.0.0"
)

# Initialize data collector
data_collector = VNStockDataCollector()

# Setup templates
templates = Jinja2Templates(directory="templates")

# Create templates directory if not exists
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Sample company data for autocomplete (you can expand this)
COMPANY_SYMBOLS = {
    "VIC": "Tập đoàn Vingroup",
    "VCB": "Ngân hàng TMCP Ngoại thương Việt Nam",
    "VHM": "Vinhomes",
    "HPG": "Tập đoàn Hòa Phát",
    "MSN": "Tập đoàn Masan",
    "VRE": "Vincom Retail",
    "GAS": "Tổng Công ty Khí Việt Nam",
    "PLX": "Tập đoàn Xăng dầu Việt Nam",
    "MWG": "Công ty Cổ phần Đầu tư Thế giới Di động",
    "FPT": "Tập đoàn FPT",
    "CTG": "Ngân hàng TMCP Công thương Việt Nam",
    "BID": "Ngân hàng TMCP Đầu tư và Phát triển Việt Nam",
    "TCB": "Ngân hàng TMCP Kỹ thương Việt Nam",
    "ACB": "Ngân hàng TMCP Á Châu",
    "VNM": "Công ty Cổ phần Sữa Việt Nam",
    "SAB": "Tổng Công ty Cổ phần Bia - Rượu - Nước giải khát Sài Gòn",
    "VJC": "Công ty Cổ phần Hàng không VietJet",
    "PNJ": "Công ty Cổ phần Vàng bạc Đá quý Phú Nhuận",
    "REE": "Công ty Cổ phần Refrigeration Electrical Engineering",
    "SSI": "Công ty Cổ phần Chứng khoán SSI"
}

def format_currency(value: float, currency: str = "VND") -> str:
    """Format currency with Vietnamese locale"""
    if pd.isna(value) or value is None:
        return "N/A"
    
    if currency == "VND":
        return f"{value:,.0f} VND"
    else:
        return f"{value:,.2f} {currency}"

def format_percentage(value: float) -> str:
    """Format percentage"""
    if pd.isna(value) or value is None:
        return "N/A"
    return f"{value:.2f}%"

def format_number(value: float) -> str:
    """Format large numbers"""
    if pd.isna(value) or value is None:
        return "N/A"
    
    if abs(value) >= 1e12:
        return f"{value/1e12:.2f}T"
    elif abs(value) >= 1e9:
        return f"{value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"{value/1e6:.2f}M"
    elif abs(value) >= 1e3:
        return f"{value/1e3:.2f}K"
    else:
        return f"{value:,.0f}"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with search interface"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "company_symbols": COMPANY_SYMBOLS
    })

@app.get("/api/search")
async def search_companies(query: str = ""):
    """API endpoint for company search autocomplete"""
    if not query:
        return {"suggestions": []}
    
    query = query.upper()
    suggestions = []
    
    for symbol, name in COMPANY_SYMBOLS.items():
        if query in symbol or query in name.upper():
            suggestions.append({
                "symbol": symbol,
                "name": name,
                "display": f"{symbol} - {name}"
            })
    
    return {"suggestions": suggestions[:10]}  # Limit to 10 suggestions

@app.post("/api/analyze")
async def analyze_stock(symbol: str = Form(...)):
    """Analyze stock data and return formatted results"""
    try:
        symbol = symbol.upper().strip()
        
        # Get comprehensive data
        logger.info(f"Analyzing stock: {symbol}")
        data = data_collector.get_complete_stock_data(symbol)
        
        if not data or data.get("error"):
            raise HTTPException(status_code=404, detail=f"Không tìm thấy dữ liệu cho mã cổ phiếu: {symbol}")
        
        # Format data for display
        formatted_data = format_stock_data(data)
        
        return JSONResponse(content=formatted_data)
        
    except Exception as e:
        logger.error(f"Error analyzing stock {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi khi phân tích cổ phiếu: {str(e)}")

def format_stock_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format stock data for web display"""
    request_info = data.get("request_info", {})
    overview = data.get("overview", {})
    historical_data = data.get("historical_data", {})
    financial_data = data.get("financial_data", {})
    market_data = data.get("market_data", {})
    ai_metadata = data.get("ai_analysis_metadata", {})
    
    formatted = {
        "symbol": request_info.get("symbol", ""),
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "overview": {},
        "current_price": {},
        "historical_summary": {},
        "financial_highlights": {},
        "technical_indicators": {},
        "company_info": {},
        "market_data": {}
    }
    
    # Format overview data - extract from current_price_info
    if "current_price_info" in overview and overview["current_price_info"]:
        current_info = overview["current_price_info"]
        if isinstance(current_info, list) and len(current_info) > 0:
            latest = current_info[-1]  # Get latest record
            formatted["overview"] = {
                "company_name": f"Công ty {request_info.get('symbol', 'N/A')}",
                "sector": "N/A",
                "industry": "N/A", 
                "market_cap": "N/A",
                "shares_outstanding": "N/A",
                "listing_date": "N/A"
            }
            
            # Format current price data from historical data
            formatted["current_price"] = {
                "price": format_currency(latest.get("close", 0)),
                "change": format_currency(latest.get("change", 0)),
                "change_percent": format_percentage(latest.get("change_percent", 0)),
                "volume": format_number(latest.get("volume", 0)),
                "high": format_currency(latest.get("high", 0)),
                "low": format_currency(latest.get("low", 0)),
                "open": format_currency(latest.get("open", 0)),
                "previous_close": format_currency(latest.get("close", 0))
            }
    
    # Format historical summary
    if "daily_data" in historical_data and historical_data["daily_data"]:
        daily_data = historical_data["daily_data"]
        if daily_data:
            prices = [day.get("close", 0) for day in daily_data if day.get("close")]
            volumes = [day.get("volume", 0) for day in daily_data if day.get("volume")]
            
            formatted["historical_summary"] = {
                "period": f"{historical_data.get('period', {}).get('start_date', 'N/A')} - {historical_data.get('period', {}).get('end_date', 'N/A')}",
                "total_records": format_number(len(daily_data)),
                "avg_volume": format_number(sum(volumes) / len(volumes) if volumes else 0),
                "max_price": format_currency(max(prices) if prices else 0),
                "min_price": format_currency(min(prices) if prices else 0),
                "volatility": format_percentage(ai_metadata.get("key_metrics_summary", {}).get("price_change_percent", 0))
            }
    
    # Format financial highlights - basic info from financial_data
    if "balance_sheet" in financial_data:
        formatted["financial_highlights"] = {
            "revenue": "N/A",
            "net_income": "N/A", 
            "total_assets": "N/A",
            "total_liabilities": "N/A",
            "equity": "N/A",
            "debt_to_equity": "N/A",
            "roe": "N/A",
            "roa": "N/A",
            "pe_ratio": "N/A",
            "pb_ratio": "N/A"
        }
    
    # Add key metrics from AI metadata
    key_metrics = ai_metadata.get("key_metrics_summary", {})
    if key_metrics:
        formatted["technical_indicators"] = {
            "latest_price": format_currency(key_metrics.get("latest_price", 0)),
            "latest_volume": format_number(key_metrics.get("latest_volume", 0)),
            "price_change_period": format_currency(key_metrics.get("price_change_period", 0)),
            "price_change_percent": format_percentage(key_metrics.get("price_change_percent", 0)),
            "max_price": format_currency(key_metrics.get("max_price", 0)),
            "min_price": format_currency(key_metrics.get("min_price", 0))
        }
    
    return formatted

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    print("🚀 Đang khởi chạy VNStock Web Interface...")
    print("📊 Giao diện web sẽ chạy tại: http://localhost:8502")
    print("🔍 API Documentation: http://localhost:8502/docs")
    print("=" * 50)
    
    uvicorn.run(
        "web_interface:app",
        host="0.0.0.0",
        port=8502,
        reload=True,
        log_level="info"
    )
