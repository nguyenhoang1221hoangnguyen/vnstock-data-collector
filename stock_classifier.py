# -*- coding: utf-8 -*-
"""
Stock Classification System - VNStock
Phân loại toàn bộ cổ phiếu thị trường theo nhiều tiêu chí
"""

from vnstock import Vnstock
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
import time
from database import get_db
from fa_calculator import calculate_fa_ratios
from ta_analyzer import calculate_ta_indicators

logger = logging.getLogger(__name__)


class StockClassifier:
    """Phân loại cổ phiếu toàn thị trường"""
    
    def __init__(self):
        self.db = get_db()
        self.stock = Vnstock()
        
        # Classification thresholds
        self.thresholds = {
            'growth': {
                'high_growth': {'roe': 20, 'revenue_growth': 30, 'pe_max': 25},
                'growth': {'roe': 15, 'revenue_growth': 15, 'pe_max': 20},
                'stable': {'roe': 10, 'revenue_growth': 5, 'pe_max': 15},
                'value': {'pe_max': 10, 'pb_max': 1.5, 'de_max': 1},
            },
            'risk': {
                'low': {'volatility_max': 20, 'de_max': 1, 'roe_min': 15},
                'medium': {'volatility_max': 40, 'de_max': 2, 'roe_min': 5},
                'high': {'volatility_max': 60, 'de_max': 3},
            },
            'market_cap': {
                'mega': 100_000_000_000_000,    # 100,000 tỷ
                'large': 10_000_000_000_000,    # 10,000 tỷ
                'mid': 1_000_000_000_000,       # 1,000 tỷ
            }
        }
        
        logger.info("StockClassifier initialized")
    
    def get_all_stocks(self, exchanges: List[str] = ['HOSE', 'HNX']) -> List[str]:
        """Lấy tất cả mã cổ phiếu"""
        try:
            # Static list of major HOSE stocks (top 100 by market cap)
            hose_stocks = [
                'VCB', 'VHM', 'VIC', 'VNM', 'HPG', 'TCB', 'MSN', 'MBB', 'FPT', 'VPB',
                'VRE', 'CTG', 'BID', 'GAS', 'PLX', 'POW', 'SSI', 'MWG', 'SAB', 'HDB',
                'STB', 'VJC', 'ACB', 'GVR', 'TPB', 'PDR', 'REE', 'VCG', 'NVL', 'DGC',
                'BCM', 'KDH', 'VHC', 'VCI', 'HCM', 'DIG', 'VGC', 'CTD', 'VIB', 'PNJ',
                'DCM', 'DXG', 'GMD', 'HT1', 'KBC', 'MBB', 'NT2', 'PVD', 'SBT', 'VPI',
                'BVH', 'CII', 'DPM', 'FCN', 'HAG', 'HNG', 'HSG', 'ITA', 'KDC', 'LGC',
                'NLG', 'PC1', 'PPC', 'PVT', 'SCS', 'SHB', 'SSB', 'VCS', 'VGS', 'VHG',
                'DHG', 'DPR', 'DRC', 'DVP', 'EIB', 'EVF', 'GEG', 'GMD', 'HCM', 'HDC',
                'HHS', 'HQC', 'HT1', 'IDC', 'IJC', 'KBC', 'KDC', 'KDH', 'LCG', 'LDG',
                'LPB', 'MBB', 'MSB', 'NAF', 'NBB', 'NHA', 'NT2', 'NVT', 'OCB', 'PDN'
            ]
            
            hnx_stocks = [
                'PVS', 'CEO', 'SHS', 'PVI', 'HUT', 'VCG', 'PVX', 'DBC', 'TNG', 'PLC',
                'NRC', 'VIG', 'BAB', 'NDN', 'PVB', 'DXP', 'TIG', 'VGP', 'PVG', 'HHC',
                'DTD', 'VCS', 'SLS', 'VC3', 'PVE', 'L14', 'LIG', 'DTT', 'DQC', 'AMC'
            ]
            
            stocks = []
            if 'HOSE' in exchanges:
                stocks.extend(hose_stocks)
            if 'HNX' in exchanges:
                stocks.extend(hnx_stocks)
            
            # Remove duplicates and return
            stocks = list(set(stocks))
            logger.info(f"Found {len(stocks)} stocks on {exchanges}")
            return stocks
            
        except Exception as e:
            logger.error(f"Error getting stock list: {e}")
            return []
    
    def calculate_volatility(self, symbol: str, days: int = 365) -> float:
        """Tính độ biến động giá"""
        try:
            stock_obj = self.stock.stock(symbol=symbol, source='VCI')
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            df = stock_obj.quote.history(start=start_date, end=end_date)
            
            if df.empty or len(df) < 10:
                return 100
            
            # Standard deviation of daily returns
            returns = df['close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252) * 100  # Annualized
            
            return round(volatility, 2)
            
        except Exception as e:
            logger.debug(f"Error calculating volatility for {symbol}: {e}")
            return 50  # Default medium volatility
    
    def estimate_market_cap(self, symbol: str, fa_data: Dict) -> float:
        """Ước tính vốn hóa thị trường"""
        try:
            ratios = fa_data.get('ratios', {})
            
            # Get current price
            stock_obj = self.stock.stock(symbol=symbol, source='VCI')
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
            df = stock_obj.quote.history(start=start_date, end=end_date)
            
            if df.empty:
                return 0
            
            current_price = df['close'].iloc[-1] * 1000  # VND
            
            # Estimate from balance sheet
            stock_obj = self.stock.stock(symbol=symbol, source='VCI')
            balance_sheet = stock_obj.finance.balance_sheet(period='quarter', lang='en')
            
            if not balance_sheet.empty:
                equity = balance_sheet['totalStockholderEquity'].iloc[0] * 1_000_000_000
                # Assume P/B ratio of 2 for estimate
                market_cap = equity * 2
                return market_cap
            
            return 0
            
        except Exception as e:
            logger.debug(f"Error estimating market cap for {symbol}: {e}")
            return 0
    
    def classify_growth_potential(self, fa_data: Dict) -> Dict:
        """Phân loại tiềm năng tăng trưởng"""
        logger.info(f"classify_growth_potential - INPUT fa_data keys: {list(fa_data.keys())}")
        logger.info(f"classify_growth_potential - INPUT fa_data: {fa_data}")
        ratios = fa_data.get('ratios', {})
        logger.info(f"classify_growth_potential - ratios extracted: {ratios}")
        logger.debug(f"classify_growth_potential - ratios keys: {list(ratios.keys())}")
        logger.debug(f"classify_growth_potential - ratios values: {ratios}")
        
        # FA API returns uppercase keys: ROE, PE, NPM, DE
        roe = ratios.get('ROE') or ratios.get('roe', 0)
        pe = ratios.get('PE') or ratios.get('pe_ratio', 0) or ratios.get('pe', 0)
        npm = ratios.get('NPM') or ratios.get('net_profit_margin', 0) or ratios.get('npm', 0)
        logger.info(f"classify_growth_potential - Parsed: ROE={roe}, PE={pe}, NPM={npm}")
        
        # Scoring logic
        if roe > 20 and (pe == 0 or (pe > 0 and pe < 25)) and npm > 15:
            category = 'high_growth'
            score = 9
            description = '🚀 Tăng trưởng mạnh, triển vọng tốt'
        elif roe > 15 and (pe == 0 or (pe > 0 and pe < 20)):
            category = 'growth'
            score = 7
            description = '📈 Tăng trưởng ổn định'
        elif roe > 10 and (pe == 0 or (pe > 0 and pe < 15)):
            category = 'stable'
            score = 6
            description = '➡️ Ổn định, cổ tức tốt'
        elif pe > 0 and pe < 10:
            category = 'value'
            score = 5
            description = '📊 Giá rẻ, tiềm năng đảo chiều'
        elif roe < 0:
            category = 'distressed'
            score = 1
            description = '⚠️ Khó khăn, rủi ro cao'
        else:
            category = 'neutral'
            score = 4
            description = '➖ Trung lập'
        
        return {
            'category': category,
            'score': score,
            'description': description,
            'roe': round(roe, 2) if roe else 0,
            'pe': round(pe, 2) if pe else 0,
            'npm': round(npm, 2) if npm else 0
        }
    
    def classify_risk_level(self, fa_data: Dict, volatility: float) -> Dict:
        """Phân loại mức độ rủi ro"""
        ratios = fa_data.get('ratios', {})
        
        # FA API returns uppercase keys: ROE, PE, NPM, DE
        roe = ratios.get('ROE') or ratios.get('roe', 0)
        de = ratios.get('DE') or ratios.get('de_ratio', 0) or ratios.get('de', 0)
        logger.info(f"classify_risk_level - Parsed: ROE={roe}, DE={de}, Volatility={volatility}")
        
        # Risk scoring
        if volatility < 20 and de < 1 and roe > 15:
            category = 'low_risk'
            risk_score = 2
            description = '🟢 Rủi ro thấp, an toàn'
        elif volatility < 40 and de < 2 and roe > 5:
            category = 'medium_risk'
            risk_score = 5
            description = '🟡 Rủi ro trung bình'
        elif volatility < 60 and de < 3:
            category = 'high_risk'
            risk_score = 8
            description = '🟠 Rủi ro cao'
        else:
            category = 'very_high_risk'
            risk_score = 10
            description = '🔴 Rủi ro rất cao'
        
        return {
            'category': category,
            'risk_score': risk_score,
            'description': description,
            'volatility': volatility,
            'debt_equity': round(de, 2) if de else 0
        }
    
    def classify_market_cap(self, market_cap: float) -> Dict:
        """Phân loại theo vốn hóa"""
        if market_cap > self.thresholds['market_cap']['mega']:
            category = 'mega_cap'
            tier = 1
            description = '🏢 Mega Cap - Siêu lớn'
        elif market_cap > self.thresholds['market_cap']['large']:
            category = 'large_cap'
            tier = 2
            description = '🏪 Large Cap - Blue-chip'
        elif market_cap > self.thresholds['market_cap']['mid']:
            category = 'mid_cap'
            tier = 3
            description = '🏠 Mid Cap - Tăng trưởng ổn'
        else:
            category = 'small_cap'
            tier = 4
            description = '🏘️ Small Cap - Tiềm năng cao'
        
        market_cap_trillion = market_cap / 1_000_000_000_000
        
        return {
            'category': category,
            'tier': tier,
            'description': description,
            'market_cap': market_cap,
            'market_cap_trillion': round(market_cap_trillion, 2)
        }
    
    def classify_momentum(self, ta_data: Dict) -> Dict:
        """Phân loại xu hướng kỹ thuật"""
        if not ta_data or 'error' in ta_data:
            return {
                'category': 'unknown',
                'momentum_score': 5,
                'description': '❓ Không đủ dữ liệu',
                'signals': {}
            }
        
        signals = ta_data.get('signals', {})
        
        # Count bullish/bearish signals
        bullish_signals = []
        bearish_signals = []
        
        for key, value in signals.items():
            if isinstance(value, str):
                if 'bullish' in value.lower() or 'buy' in value.lower():
                    bullish_signals.append(key)
                elif 'bearish' in value.lower() or 'sell' in value.lower():
                    bearish_signals.append(key)
        
        bullish_count = len(bullish_signals)
        bearish_count = len(bearish_signals)
        
        # Classify momentum
        if bullish_count >= 3:
            category = 'strong_uptrend'
            momentum_score = 9
            description = '🔥 Xu hướng tăng mạnh'
        elif bullish_count >= 2:
            category = 'uptrend'
            momentum_score = 7
            description = '📈 Xu hướng tăng'
        elif bearish_count >= 3:
            category = 'strong_downtrend'
            momentum_score = 1
            description = '💥 Xu hướng giảm mạnh'
        elif bearish_count >= 2:
            category = 'downtrend'
            momentum_score = 3
            description = '📉 Xu hướng giảm'
        else:
            category = 'sideways'
            momentum_score = 5
            description = '➡️ Đi ngang'
        
        return {
            'category': category,
            'momentum_score': momentum_score,
            'description': description,
            'bullish_signals': bullish_signals,
            'bearish_signals': bearish_signals,
            'signal_count': {'bullish': bullish_count, 'bearish': bearish_count}
        }
    
    def classify_stock(self, symbol: str, use_cache: bool = True) -> Dict:
        """Phân loại toàn diện 1 mã cổ phiếu"""
        try:
            logger.info(f"Classifying {symbol}...")
            
            result = {
                'symbol': symbol,
                'timestamp': datetime.now().isoformat(),
                'classifications': {},
                'error': None
            }
            
            # Get FA data
            fa_data = calculate_fa_ratios(symbol)
            logger.info(f"FA data for {symbol}: FULL fa_data={fa_data}")
            logger.info(f"FA data for {symbol}: ratios={fa_data.get('ratios')}")
            
            if 'error' in fa_data:
                result['error'] = fa_data['error']
                return result
            
            # Get TA data
            try:
                ta_data = calculate_ta_indicators(symbol, period_days=365)
            except Exception as e:
                logger.warning(f"Could not get TA data for {symbol}: {e}")
                ta_data = {}
            
            # Calculate additional metrics
            volatility = self.calculate_volatility(symbol)
            market_cap = self.estimate_market_cap(symbol, fa_data)
            
            # Classify
            result['classifications']['growth'] = self.classify_growth_potential(fa_data)
            result['classifications']['risk'] = self.classify_risk_level(fa_data, volatility)
            result['classifications']['market_cap'] = self.classify_market_cap(market_cap)
            result['classifications']['momentum'] = self.classify_momentum(ta_data)
            
            # Overall rating
            result['overall_rating'] = self._calculate_overall_rating(result['classifications'])
            
            logger.info(f"Classified {symbol}: {result['overall_rating']['rating']}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error classifying {symbol}: {e}")
            return {
                'symbol': symbol,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _calculate_overall_rating(self, classifications: Dict) -> Dict:
        """Tính điểm tổng thể"""
        growth_score = classifications['growth']['score']
        risk_score = 10 - classifications['risk']['risk_score']  # Invert (lower risk = higher score)
        momentum_score = classifications['momentum']['momentum_score']
        
        # Weighted average
        weights = {'growth': 0.4, 'risk': 0.3, 'momentum': 0.3}
        total_score = (
            growth_score * weights['growth'] +
            risk_score * weights['risk'] +
            momentum_score * weights['momentum']
        )
        
        # Rating
        if total_score >= 8:
            rating = 'A+'
            recommendation = '🌟 Strong Buy - Mua mạnh'
        elif total_score >= 7:
            rating = 'A'
            recommendation = '✅ Buy - Mua'
        elif total_score >= 6:
            rating = 'B'
            recommendation = '👀 Hold/Accumulate - Giữ/Tích lũy'
        elif total_score >= 5:
            rating = 'C'
            recommendation = '⏸️ Hold - Giữ'
        elif total_score >= 4:
            rating = 'D'
            recommendation = '⚠️ Watch - Theo dõi'
        else:
            rating = 'F'
            recommendation = '🚫 Avoid - Tránh'
        
        return {
            'score': round(total_score, 2),
            'rating': rating,
            'recommendation': recommendation,
            'component_scores': {
                'growth': growth_score,
                'risk_adjusted': round(risk_score, 2),
                'momentum': momentum_score
            }
        }
    
    def scan_and_classify_market(self, 
                                 exchanges: List[str] = ['HOSE'],
                                 limit: Optional[int] = None,
                                 delay: float = 3.0) -> pd.DataFrame:
        """Quét và phân loại toàn bộ thị trường"""
        stocks = self.get_all_stocks(exchanges=exchanges)
        
        if limit:
            stocks = stocks[:limit]
        
        results = []
        errors = []
        
        logger.info(f"Scanning {len(stocks)} stocks from {exchanges}")
        
        for i, symbol in enumerate(stocks, 1):
            logger.info(f"[{i}/{len(stocks)}] Processing {symbol}...")
            
            try:
                classification = self.classify_stock(symbol)
                
                if 'error' not in classification or classification['error'] is None:
                    results.append(classification)
                    rating = classification['overall_rating']['rating']
                    logger.info(f"  ✅ {symbol}: {rating}")
                else:
                    errors.append(symbol)
                    logger.warning(f"  ❌ {symbol}: Has error field")
                
            except Exception as e:
                errors.append(symbol)
                logger.error(f"  ❌ {symbol}: {str(e)[:50]}")
            
            # Rate limit protection
            if i < len(stocks):
                time.sleep(delay)
        
        logger.info(f"Scan complete: {len(results)} classified, {len(errors)} errors")
        
        if errors:
            logger.warning(f"Failed symbols: {', '.join(errors[:10])}" + ("..." if len(errors) > 10 else ""))
        
        # Convert to DataFrame
        df = self._results_to_dataframe(results)
        
        return df
    
    def _results_to_dataframe(self, results: List[Dict]) -> pd.DataFrame:
        """Convert results to DataFrame"""
        data = []
        
        for r in results:
            if 'error' in r and r['error']:
                continue
            
            try:
                row = {
                    'symbol': r['symbol'],
                    'growth_category': r['classifications']['growth']['category'],
                    'growth_score': r['classifications']['growth']['score'],
                    'growth_desc': r['classifications']['growth']['description'],
                    'risk_category': r['classifications']['risk']['category'],
                    'risk_score': r['classifications']['risk']['risk_score'],
                    'risk_desc': r['classifications']['risk']['description'],
                    'volatility': r['classifications']['risk']['volatility'],
                    'market_cap_category': r['classifications']['market_cap']['category'],
                    'market_cap_trillion': r['classifications']['market_cap']['market_cap_trillion'],
                    'momentum_category': r['classifications']['momentum']['category'],
                    'momentum_score': r['classifications']['momentum']['momentum_score'],
                    'momentum_desc': r['classifications']['momentum']['description'],
                    'overall_rating': r['overall_rating']['rating'],
                    'overall_score': r['overall_rating']['score'],
                    'recommendation': r['overall_rating']['recommendation'],
                    'timestamp': r['timestamp']
                }
                
                data.append(row)
            except Exception as e:
                logger.error(f"Error converting result to dataframe: {e}")
                continue
        
        return pd.DataFrame(data)
    
    def get_stocks_by_filter(self, df: pd.DataFrame, 
                            growth: str = None,
                            risk: str = None,
                            rating: str = None,
                            min_score: float = None) -> pd.DataFrame:
        """Lọc cổ phiếu theo tiêu chí"""
        filtered = df.copy()
        
        if growth:
            filtered = filtered[filtered['growth_category'] == growth]
        
        if risk:
            filtered = filtered[filtered['risk_category'] == risk]
        
        if rating:
            filtered = filtered[filtered['overall_rating'] == rating]
        
        if min_score:
            filtered = filtered[filtered['overall_score'] >= min_score]
        
        return filtered.sort_values('overall_score', ascending=False)


# ========== QUICK FUNCTIONS ==========

def scan_market(exchanges: List[str] = ['HOSE'], limit: int = 50):
    """Quick scan market"""
    classifier = StockClassifier()
    df = classifier.scan_and_classify_market(exchanges=exchanges, limit=limit, delay=3.0)
    
    if df.empty:
        print("\n⚠️ No stocks classified successfully")
        return df
    
    # Print summary
    print("\n" + "="*70)
    print("📊 MARKET CLASSIFICATION SUMMARY")
    print("="*70)
    
    print("\n🚀 By Growth Potential:")
    print(df['growth_category'].value_counts())
    
    print("\n⚠️ By Risk Level:")
    print(df['risk_category'].value_counts())
    
    print("\n💰 By Market Cap:")
    print(df['market_cap_category'].value_counts())
    
    print("\n⭐ By Rating:")
    print(df['overall_rating'].value_counts())
    
    print("\n📈 Top 10 Recommendations:")
    top = df.nlargest(10, 'overall_score')[
        ['symbol', 'overall_rating', 'overall_score', 'growth_category', 'risk_category']
    ]
    print(top.to_string(index=False))
    
    return df


if __name__ == "__main__":
    import sys
    
    # Parse arguments
    limit = 20  # Default
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except:
            pass
    
    print(f"\n🎯 Stock Classification System")
    print(f"Scanning {limit} stocks from HOSE...\n")
    
    # Scan
    df = scan_market(exchanges=['HOSE'], limit=limit)
    
    if not df.empty:
        # Save to CSV
        filename = f'stock_classification_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n✅ Saved to {filename}")
        
        # Show sample
        print("\n📊 Sample Results:")
        print(df.head(5)[['symbol', 'overall_rating', 'overall_score', 'recommendation']].to_string(index=False))

