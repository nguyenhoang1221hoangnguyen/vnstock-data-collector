# -*- coding: utf-8 -*-
"""
Blue-chip Stock Detector - VNStock
Tự động phát hiện và theo dõi cổ phiếu blue-chip Việt Nam
"""

from vnstock import Vnstock
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict
import logging
from database import get_db

logger = logging.getLogger(__name__)


class BlueChipDetector:
    """Phát hiện cổ phiếu blue-chip"""
    
    def __init__(self):
        """Initialize detector"""
        self.db = get_db()
        
        # Tiêu chí blue-chip
        self.criteria = {
            'min_market_cap': 10_000_000_000_000,  # 10,000 tỷ VND
            'min_pe': 5,
            'max_pe': 20,
            'min_roe': 15,  # %
            'min_avg_volume': 500_000,  # cp/ngày
            'max_volatility': 30,  # %
        }
        
        # Danh sách VN30 (update định kỳ)
        self.vn30_list = [
            'ACB', 'BCM', 'BID', 'BVH', 'CTG', 'FPT', 'GAS', 'GVR',
            'HDB', 'HPG', 'KDH', 'MBB', 'MSN', 'MWG', 'NVL', 'PDR',
            'PLX', 'POW', 'SAB', 'SSI', 'STB', 'TCB', 'TPB', 'VCB',
            'VHM', 'VIB', 'VIC', 'VJC', 'VNM', 'VPB'
        ]
        
        logger.info("BlueChipDetector initialized")
    
    def get_all_hose_stocks(self) -> List[str]:
        """Lấy danh sách tất cả mã HOSE"""
        try:
            stock = Vnstock()
            # Lấy danh sách HOSE
            listing = stock.listing.all_symbols()
            hose_stocks = listing[listing['exchange'] == 'HOSE']['ticker'].tolist()
            logger.info(f"Found {len(hose_stocks)} HOSE stocks")
            return hose_stocks
        except Exception as e:
            logger.error(f"Error getting HOSE stocks: {e}")
            return self.vn30_list  # Fallback to VN30
    
    def calculate_market_cap(self, symbol: str) -> float:
        """Tính vốn hóa thị trường (ước tính)"""
        try:
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            
            # Get current price
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
            df = stock.quote.history(start=start_date, end=end_date)
            
            if df.empty:
                return 0
            
            current_price = df['close'].iloc[-1] * 1000  # VND
            
            # Get shares outstanding from balance sheet
            balance_sheet = stock.finance.balance_sheet(period='quarter', lang='en')
            
            if not balance_sheet.empty:
                # Estimate market cap from equity (rough estimate)
                equity = balance_sheet['totalStockholderEquity'].iloc[0] * 1_000_000_000  # Billion to VND
                
                # Assume P/B ratio of 2 for estimate
                estimated_market_cap = equity * 2
                return estimated_market_cap
            
            return 0
            
        except Exception as e:
            logger.debug(f"Error calculating market cap for {symbol}: {e}")
            return 0
    
    def calculate_volatility(self, symbol: str, days: int = 365) -> float:
        """Tính độ biến động giá (% change trong khoảng thời gian)"""
        try:
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            df = stock.quote.history(start=start_date, end=end_date)
            
            if df.empty or len(df) < 10:
                return 100  # High volatility if not enough data
            
            max_price = df['close'].max()
            min_price = df['close'].min()
            volatility = ((max_price - min_price) / min_price) * 100
            
            return volatility
            
        except Exception as e:
            logger.debug(f"Error calculating volatility for {symbol}: {e}")
            return 100
    
    def get_average_volume(self, symbol: str, days: int = 30) -> float:
        """Tính volume trung bình"""
        try:
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            df = stock.quote.history(start=start_date, end=end_date)
            
            if df.empty:
                return 0
            
            return df['volume'].mean()
            
        except Exception as e:
            logger.debug(f"Error getting volume for {symbol}: {e}")
            return 0
    
    def check_bluechip_criteria(self, symbol: str) -> Dict:
        """Kiểm tra tiêu chí blue-chip cho một mã"""
        try:
            from fa_calculator import calculate_fa_ratios
            
            result = {
                'symbol': symbol,
                'is_bluechip': False,
                'score': 0,
                'max_score': 6,
                'criteria_met': {},
                'details': {}
            }
            
            # 1. Check VN30
            is_vn30 = symbol in self.vn30_list
            result['criteria_met']['vn30'] = is_vn30
            result['details']['vn30'] = is_vn30
            if is_vn30:
                result['score'] += 1
            
            # 2. Check FA ratios
            fa_ratios = calculate_fa_ratios(symbol)
            
            if 'error' not in fa_ratios:
                ratios = fa_ratios.get('ratios', {})
                
                # P/E
                pe = ratios.get('pe_ratio', 0)
                if pe and pe > 0:
                    pe_ok = self.criteria['min_pe'] < pe < self.criteria['max_pe']
                    result['criteria_met']['pe'] = pe_ok
                    result['details']['pe'] = round(pe, 2)
                    if pe_ok:
                        result['score'] += 1
                
                # ROE
                roe = ratios.get('roe', 0)
                if roe:
                    roe_ok = roe > self.criteria['min_roe']
                    result['criteria_met']['roe'] = roe_ok
                    result['details']['roe'] = round(roe, 2)
                    if roe_ok:
                        result['score'] += 1
            
            # 3. Check Market Cap
            market_cap = self.calculate_market_cap(symbol)
            market_cap_ok = market_cap > self.criteria['min_market_cap']
            result['criteria_met']['market_cap'] = market_cap_ok
            result['details']['market_cap'] = market_cap
            if market_cap_ok:
                result['score'] += 1
            
            # 4. Check Volume
            avg_volume = self.get_average_volume(symbol)
            volume_ok = avg_volume > self.criteria['min_avg_volume']
            result['criteria_met']['volume'] = volume_ok
            result['details']['avg_volume'] = int(avg_volume)
            if volume_ok:
                result['score'] += 1
            
            # 5. Check Volatility
            volatility = self.calculate_volatility(symbol)
            volatility_ok = volatility < self.criteria['max_volatility']
            result['criteria_met']['volatility'] = volatility_ok
            result['details']['volatility'] = round(volatility, 2)
            if volatility_ok:
                result['score'] += 1
            
            # Determine if blue-chip (score >= 4/6)
            result['is_bluechip'] = result['score'] >= 4
            
            return result
            
        except Exception as e:
            logger.error(f"Error checking blue-chip for {symbol}: {e}")
            return {
                'symbol': symbol,
                'is_bluechip': False,
                'score': 0,
                'error': str(e)
            }
    
    def scan_bluechips(self, symbols: List[str] = None, min_score: int = 4) -> List[Dict]:
        """
        Quét tìm blue-chips từ danh sách
        
        Args:
            symbols: Danh sách mã cần quét (None = VN30)
            min_score: Điểm tối thiểu để được coi là blue-chip (default 4/6)
        
        Returns:
            List of blue-chip stocks with details
        """
        if symbols is None:
            symbols = self.vn30_list
        
        bluechips = []
        
        print(f"\n🔍 Scanning {len(symbols)} stocks for blue-chips...\n")
        
        for i, symbol in enumerate(symbols, 1):
            print(f"[{i}/{len(symbols)}] Checking {symbol}...", end=' ')
            
            result = self.check_bluechip_criteria(symbol)
            
            if result['is_bluechip'] and result.get('score', 0) >= min_score:
                bluechips.append(result)
                print(f"✅ BLUE-CHIP! (Score: {result['score']}/{result['max_score']})")
            else:
                print(f"❌ Not qualified (Score: {result.get('score', 0)}/{result.get('max_score', 6)})")
        
        # Sort by score
        bluechips.sort(key=lambda x: x['score'], reverse=True)
        
        print(f"\n✅ Found {len(bluechips)} blue-chip stocks!\n")
        
        return bluechips
    
    def auto_add_to_watchlist(self, bluechips: List[Dict]) -> int:
        """
        Tự động thêm blue-chips vào watchlist
        
        Args:
            bluechips: List of blue-chip results
        
        Returns:
            Number of stocks added
        """
        added = 0
        
        for bc in bluechips:
            symbol = bc['symbol']
            score = bc['score']
            
            # Create detailed notes
            details = bc.get('details', {})
            notes_parts = [
                f"Blue-chip (Score: {score}/{bc['max_score']})",
            ]
            
            if details.get('vn30'):
                notes_parts.append("VN30")
            
            if 'pe' in details:
                notes_parts.append(f"P/E: {details['pe']}")
            
            if 'roe' in details:
                notes_parts.append(f"ROE: {details['roe']}%")
            
            notes = " | ".join(notes_parts)
            
            # Add to database
            try:
                success = self.db.add_to_watchlist(
                    symbol=symbol,
                    notes=notes,
                    sector='Blue-chip'
                )
                
                if success:
                    added += 1
                    logger.info(f"Added {symbol} to watchlist")
            except Exception as e:
                # Stock might already exist
                logger.debug(f"Could not add {symbol}: {e}")
        
        return added
    
    def get_bluechip_report(self, bluechips: List[Dict]) -> str:
        """Generate text report"""
        report = "\n" + "=" * 70 + "\n"
        report += "📊 BLUE-CHIP STOCKS REPORT\n"
        report += "=" * 70 + "\n\n"
        
        report += f"Total Blue-chips Found: {len(bluechips)}\n"
        report += f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if not bluechips:
            report += "⚠️ No blue-chip stocks found matching criteria.\n"
            return report
        
        for i, bc in enumerate(bluechips, 1):
            report += f"{i}. {bc['symbol']} - Score: {bc['score']}/{bc['max_score']}\n"
            
            details = bc.get('details', {})
            criteria = bc.get('criteria_met', {})
            
            report += f"   ✓ VN30: {'Yes ✅' if details.get('vn30') else 'No'}\n"
            
            if 'pe' in details:
                status = '✅' if criteria.get('pe') else '❌'
                report += f"   {status} P/E: {details['pe']}\n"
            
            if 'roe' in details:
                status = '✅' if criteria.get('roe') else '❌'
                report += f"   {status} ROE: {details['roe']}%\n"
            
            if 'market_cap' in details:
                status = '✅' if criteria.get('market_cap') else '❌'
                market_cap_trillion = details['market_cap'] / 1_000_000_000_000
                report += f"   {status} Market Cap: {market_cap_trillion:.1f} trillion VND\n"
            
            if 'avg_volume' in details:
                status = '✅' if criteria.get('volume') else '❌'
                report += f"   {status} Avg Volume: {details['avg_volume']:,}\n"
            
            if 'volatility' in details:
                status = '✅' if criteria.get('volatility') else '❌'
                report += f"   {status} Volatility: {details['volatility']:.1f}%\n"
            
            report += "\n"
        
        report += "=" * 70 + "\n"
        
        return report


# ========== CLI COMMANDS ==========

def run_bluechip_scan(auto_add: bool = False):
    """Run blue-chip scan and optionally add to watchlist"""
    detector = BlueChipDetector()
    
    # Scan VN30 first
    print("\n🎯 Scanning VN30 for Blue-chips...")
    bluechips = detector.scan_bluechips()
    
    # Show report
    report = detector.get_bluechip_report(bluechips)
    print(report)
    
    # Add to watchlist
    if bluechips:
        if auto_add:
            answer = 'y'
        else:
            answer = input(f"\n📌 Add {len(bluechips)} blue-chips to watchlist? (y/n): ")
        
        if answer.lower() == 'y':
            added = detector.auto_add_to_watchlist(bluechips)
            print(f"✅ Added {added} stocks to watchlist!")
            print("\n💡 Tip: View watchlist in Advanced Dashboard or via API")
    else:
        print("⚠️ No blue-chips found matching criteria")
        print("\n💡 Tip: You can adjust criteria in bluechip_detector.py")


if __name__ == "__main__":
    import sys
    
    # Check for auto-add flag
    auto_add = '--auto' in sys.argv or '-a' in sys.argv
    
    run_bluechip_scan(auto_add=auto_add)

