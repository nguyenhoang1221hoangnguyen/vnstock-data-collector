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
        data = data_collector.get_comprehensive_data(symbol)
        
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
    formatted = {
        "symbol": data.get("symbol", ""),
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "overview": {},
        "current_price": {},
        "historical_summary": {},
        "financial_highlights": {},
        "technical_indicators": {},
        "company_info": {},
        "market_data": {}
    }
    
    # Format overview data
    if "overview" in data:
        overview = data["overview"]
        formatted["overview"] = {
            "company_name": overview.get("company_name", "N/A"),
            "sector": overview.get("sector", "N/A"),
            "industry": overview.get("industry", "N/A"),
            "market_cap": format_currency(overview.get("market_cap", 0)),
            "shares_outstanding": format_number(overview.get("shares_outstanding", 0)),
            "listing_date": overview.get("listing_date", "N/A")
        }
    
    # Format current price data
    if "current_price" in data:
        current = data["current_price"]
        formatted["current_price"] = {
            "price": format_currency(current.get("price", 0)),
            "change": format_currency(current.get("change", 0)),
            "change_percent": format_percentage(current.get("change_percent", 0)),
            "volume": format_number(current.get("volume", 0)),
            "high": format_currency(current.get("high", 0)),
            "low": format_currency(current.get("low", 0)),
            "open": format_currency(current.get("open", 0)),
            "previous_close": format_currency(current.get("previous_close", 0))
        }
    
    # Format financial highlights
    if "financial_highlights" in data:
        financial = data["financial_highlights"]
        formatted["financial_highlights"] = {
            "revenue": format_currency(financial.get("revenue", 0)),
            "net_income": format_currency(financial.get("net_income", 0)),
            "total_assets": format_currency(financial.get("total_assets", 0)),
            "total_liabilities": format_currency(financial.get("total_liabilities", 0)),
            "equity": format_currency(financial.get("equity", 0)),
            "debt_to_equity": format_percentage(financial.get("debt_to_equity", 0)),
            "roe": format_percentage(financial.get("roe", 0)),
            "roa": format_percentage(financial.get("roa", 0)),
            "pe_ratio": f"{financial.get('pe_ratio', 0):.2f}",
            "pb_ratio": f"{financial.get('pb_ratio', 0):.2f}"
        }
    
    # Format historical summary
    if "historical_summary" in data:
        historical = data["historical_summary"]
        formatted["historical_summary"] = {
            "period": historical.get("period", "N/A"),
            "total_records": format_number(historical.get("total_records", 0)),
            "avg_volume": format_number(historical.get("avg_volume", 0)),
            "max_price": format_currency(historical.get("max_price", 0)),
            "min_price": format_currency(historical.get("min_price", 0)),
            "volatility": format_percentage(historical.get("volatility", 0))
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
