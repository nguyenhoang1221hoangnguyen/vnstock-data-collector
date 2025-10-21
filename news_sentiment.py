"""
News & Sentiment Analysis Module - VNStock
Crawl news, analyze sentiment, detect trends
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
import re
from collections import Counter

logger = logging.getLogger(__name__)


class NewsAnalyzer:
    """Phân tích tin tức và sentiment"""
    
    def __init__(self):
        """Initialize news analyzer"""
        self.sources = {
            'cafef': 'https://cafef.vn',
            'vnexpress': 'https://vnexpress.net/kinh-doanh',
            'vietstock': 'https://vietstock.vn'
        }
        
        # Vietnamese sentiment keywords
        self.positive_keywords = [
            'tăng', 'tăng trưởng', 'lợi nhuận', 'khả quan', 'tích cực',
            'thành công', 'phát triển', 'mạnh mẽ', 'tốt', 'cao',
            'đột phá', 'vượt', 'kỷ lục', 'dương', 'lạc quan',
            'cải thiện', 'nâng cao', 'mở rộng', 'đầu tư', 'hợp tác'
        ]
        
        self.negative_keywords = [
            'giảm', 'sụt giảm', 'thua lỗ', 'khó khăn', 'tiêu cực',
            'thất bại', 'suy thoái', 'yếu', 'kém', 'thấp',
            'rủi ro', 'lo ngại', 'âm', 'bi quan', 'đình trệ',
            'giảm sút', 'tụt', 'rớt', 'nợ', 'phạt'
        ]
        
        logger.info("NewsAnalyzer initialized")
    
    # ========== NEWS CRAWLING ==========
    
    def get_stock_news(self, symbol: str, days: int = 7) -> List[Dict]:
        """
        Lấy tin tức về một mã cổ phiếu
        
        Args:
            symbol: Mã cổ phiếu
            days: Số ngày tin tức (default 7)
        
        Returns:
            List of news articles
        """
        try:
            all_news = []
            
            # Cafef news
            cafef_news = self._crawl_cafef(symbol, days)
            all_news.extend(cafef_news)
            
            # VnExpress news (generic business news)
            vnexpress_news = self._crawl_vnexpress(symbol, days)
            all_news.extend(vnexpress_news)
            
            # Sort by date
            all_news.sort(key=lambda x: x['published_date'], reverse=True)
            
            logger.info(f"Found {len(all_news)} news articles for {symbol}")
            return all_news
            
        except Exception as e:
            logger.error(f"Error getting news for {symbol}: {e}")
            return []
    
    def _crawl_cafef(self, symbol: str, days: int) -> List[Dict]:
        """Crawl news from Cafef"""
        try:
            # This is a simplified version - actual implementation needs proper API/crawling
            # For demo purposes, return mock data
            
            news = []
            base_date = datetime.now()
            
            # Mock news data
            mock_news = [
                {
                    'title': f'{symbol}: Lợi nhuận quý 3 tăng 25% so với cùng kỳ',
                    'summary': f'Kết quả kinh doanh của {symbol} trong quý 3 đạt mức tăng trưởng ấn tượng...',
                    'url': f'https://cafef.vn/{symbol.lower()}-loi-nhuan-tang',
                    'source': 'cafef',
                    'published_date': base_date - timedelta(days=1),
                    'category': 'financial_results'
                },
                {
                    'title': f'{symbol} triển khai dự án mở rộng nhà máy mới',
                    'summary': f'Công ty {symbol} vừa công bố kế hoạch đầu tư mở rộng sản xuất...',
                    'url': f'https://cafef.vn/{symbol.lower()}-mo-rong',
                    'source': 'cafef',
                    'published_date': base_date - timedelta(days=3),
                    'category': 'business_expansion'
                },
                {
                    'title': f'Cổ đông lớn của {symbol} đăng ký bán 5 triệu cổ phiếu',
                    'summary': f'Theo thông báo từ HOSE, cổ đông lớn của {symbol} dự kiến bán...',
                    'url': f'https://cafef.vn/{symbol.lower()-ban-co-phieu',
                    'source': 'cafef',
                    'published_date': base_date - timedelta(days=5),
                    'category': 'insider_trading'
                }
            ]
            
            # Filter by days
            cutoff_date = base_date - timedelta(days=days)
            news = [n for n in mock_news if n['published_date'] >= cutoff_date]
            
            return news
            
        except Exception as e:
            logger.error(f"Error crawling Cafef: {e}")
            return []
    
    def _crawl_vnexpress(self, symbol: str, days: int) -> List[Dict]:
        """Crawl news from VnExpress"""
        try:
            # Mock implementation
            news = []
            base_date = datetime.now()
            
            mock_news = [
                {
                    'title': 'Thị trường chứng khoán Việt Nam hấp dẫn nhà đầu tư ngoại',
                    'summary': 'Dòng vốn ngoại đang quay trở lại thị trường chứng khoán Việt Nam...',
                    'url': 'https://vnexpress.net/thi-truong-chung-khoan',
                    'source': 'vnexpress',
                    'published_date': base_date - timedelta(days=2),
                    'category': 'market_analysis'
                }
            ]
            
            cutoff_date = base_date - timedelta(days=days)
            news = [n for n in mock_news if n['published_date'] >= cutoff_date]
            
            return news
            
        except Exception as e:
            logger.error(f"Error crawling VnExpress: {e}")
            return []
    
    # ========== SENTIMENT ANALYSIS ==========
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Phân tích sentiment của một đoạn text
        
        Args:
            text: Text cần phân tích (tiếng Việt)
        
        Returns:
            Dict chứa sentiment analysis results
        """
        try:
            # Convert to lowercase for matching
            text_lower = text.lower()
            
            # Count positive and negative keywords
            positive_count = sum(1 for word in self.positive_keywords if word in text_lower)
            negative_count = sum(1 for word in self.negative_keywords if word in text_lower)
            
            # Calculate sentiment score (-1 to 1)
            total_count = positive_count + negative_count
            
            if total_count == 0:
                sentiment_score = 0
                sentiment_label = 'neutral'
            else:
                sentiment_score = (positive_count - negative_count) / total_count
                
                if sentiment_score > 0.3:
                    sentiment_label = 'positive'
                elif sentiment_score < -0.3:
                    sentiment_label = 'negative'
                else:
                    sentiment_label = 'neutral'
            
            # Find matched keywords
            matched_positive = [w for w in self.positive_keywords if w in text_lower]
            matched_negative = [w for w in self.negative_keywords if w in text_lower]
            
            return {
                'sentiment_score': sentiment_score,
                'sentiment_label': sentiment_label,
                'positive_count': positive_count,
                'negative_count': negative_count,
                'matched_positive': matched_positive,
                'matched_negative': matched_negative,
                'confidence': min(abs(sentiment_score) * 100, 100)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                'sentiment_score': 0,
                'sentiment_label': 'neutral',
                'error': str(e)
            }
    
    def analyze_news_sentiment(self, symbol: str, days: int = 7) -> Dict:
        """
        Phân tích sentiment tổng hợp từ tin tức
        
        Args:
            symbol: Mã cổ phiếu
            days: Số ngày tin tức
        
        Returns:
            Dict chứa aggregated sentiment analysis
        """
        try:
            # Get news
            news_list = self.get_stock_news(symbol, days)
            
            if not news_list:
                return {
                    'symbol': symbol,
                    'news_count': 0,
                    'overall_sentiment': 'neutral',
                    'sentiment_score': 0,
                    'sentiment_breakdown': {},
                    'trending_topics': []
                }
            
            # Analyze each article
            sentiments = []
            all_text = []
            
            for news in news_list:
                text = f"{news['title']} {news['summary']}"
                sentiment = self.analyze_sentiment(text)
                sentiment['article'] = news
                sentiments.append(sentiment)
                all_text.append(text)
            
            # Calculate overall sentiment
            avg_score = sum(s['sentiment_score'] for s in sentiments) / len(sentiments)
            
            if avg_score > 0.3:
                overall_sentiment = 'positive'
            elif avg_score < -0.3:
                overall_sentiment = 'negative'
            else:
                overall_sentiment = 'neutral'
            
            # Sentiment breakdown
            sentiment_breakdown = {
                'positive': len([s for s in sentiments if s['sentiment_label'] == 'positive']),
                'negative': len([s for s in sentiments if s['sentiment_label'] == 'negative']),
                'neutral': len([s for s in sentiments if s['sentiment_label'] == 'neutral'])
            }
            
            # Extract trending topics (most common keywords)
            all_keywords = []
            for s in sentiments:
                all_keywords.extend(s['matched_positive'])
                all_keywords.extend(s['matched_negative'])
            
            trending_topics = Counter(all_keywords).most_common(5)
            
            return {
                'symbol': symbol,
                'news_count': len(news_list),
                'overall_sentiment': overall_sentiment,
                'sentiment_score': avg_score,
                'sentiment_breakdown': sentiment_breakdown,
                'trending_topics': trending_topics,
                'articles': sentiments,
                'period_days': days
            }
            
        except Exception as e:
            logger.error(f"Error analyzing news sentiment: {e}")
            return {
                'error': str(e)
            }
    
    # ========== SOCIAL MENTIONS ==========
    
    def get_social_mentions(self, symbol: str, days: int = 7) -> Dict:
        """
        Lấy social media mentions (mock implementation)
        
        Args:
            symbol: Mã cổ phiếu
            days: Số ngày
        
        Returns:
            Dict chứa social mentions data
        """
        # This would integrate with Twitter/Facebook/Forums APIs
        # For now, return mock data
        
        try:
            import random
            
            base_date = datetime.now()
            mentions = []
            
            for i in range(days):
                date = base_date - timedelta(days=i)
                count = random.randint(10, 100)
                sentiment = random.choice(['positive', 'negative', 'neutral'])
                
                mentions.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'mention_count': count,
                    'sentiment': sentiment,
                    'engagement': random.randint(50, 500)
                })
            
            return {
                'symbol': symbol,
                'total_mentions': sum(m['mention_count'] for m in mentions),
                'daily_mentions': mentions,
                'avg_daily_mentions': sum(m['mention_count'] for m in mentions) / len(mentions),
                'trending_score': random.uniform(0, 100)
            }
            
        except Exception as e:
            logger.error(f"Error getting social mentions: {e}")
            return {
                'error': str(e)
            }
    
    # ========== ECONOMIC CALENDAR ==========
    
    def get_economic_events(self, days_ahead: int = 7) -> List[Dict]:
        """
        Lấy lịch sự kiện kinh tế (mock implementation)
        
        Args:
            days_ahead: Số ngày tới
        
        Returns:
            List of economic events
        """
        try:
            base_date = datetime.now()
            events = []
            
            # Mock events
            mock_events = [
                {
                    'date': base_date + timedelta(days=2),
                    'event': 'Công bố GDP Q3/2024',
                    'importance': 'high',
                    'impact': 'positive',
                    'description': 'Tổng cục Thống kê công bố số liệu GDP quý 3'
                },
                {
                    'date': base_date + timedelta(days=5),
                    'event': 'Họp NHNN về lãi suất',
                    'importance': 'high',
                    'impact': 'neutral',
                    'description': 'Ngân hàng Nhà nước họp xem xét chính sách lãi suất'
                },
                {
                    'date': base_date + timedelta(days=1),
                    'event': 'Số liệu CPI tháng 10',
                    'importance': 'medium',
                    'impact': 'neutral',
                    'description': 'Chỉ số giá tiêu dùng tháng 10'
                }
            ]
            
            # Filter by days_ahead
            cutoff_date = base_date + timedelta(days=days_ahead)
            events = [e for e in mock_events if e['date'] <= cutoff_date]
            
            # Sort by date
            events.sort(key=lambda x: x['date'])
            
            return events
            
        except Exception as e:
            logger.error(f"Error getting economic events: {e}")
            return []
    
    # ========== MARKET SENTIMENT ==========
    
    def get_market_sentiment(self) -> Dict:
        """
        Tính toán market sentiment tổng thể
        
        Returns:
            Dict chứa market sentiment metrics
        """
        try:
            # Mock implementation - would integrate with real market data
            import random
            
            sentiment_score = random.uniform(-1, 1)
            
            if sentiment_score > 0.3:
                sentiment_label = 'bullish'
            elif sentiment_score < -0.3:
                sentiment_label = 'bearish'
            else:
                sentiment_label = 'neutral'
            
            return {
                'sentiment_label': sentiment_label,
                'sentiment_score': sentiment_score,
                'fear_greed_index': random.uniform(0, 100),
                'market_breadth': {
                    'advancing': random.randint(100, 300),
                    'declining': random.randint(100, 300),
                    'unchanged': random.randint(50, 150)
                },
                'volume_trend': random.choice(['increasing', 'decreasing', 'stable']),
                'foreign_flow': random.uniform(-1000, 1000),  # Billion VND
                'updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting market sentiment: {e}")
            return {
                'error': str(e)
            }


# ========== HELPER FUNCTIONS ==========

def quick_sentiment_check(symbol: str) -> str:
    """
    Quick sentiment check for a symbol
    
    Args:
        symbol: Stock symbol
    
    Returns:
        Sentiment label (positive/negative/neutral)
    """
    analyzer = NewsAnalyzer()
    result = analyzer.analyze_news_sentiment(symbol, days=7)
    return result.get('overall_sentiment', 'neutral')


def get_sentiment_report(symbol: str, days: int = 7) -> Dict:
    """
    Get comprehensive sentiment report
    
    Args:
        symbol: Stock symbol
        days: Number of days
    
    Returns:
        Complete sentiment report
    """
    analyzer = NewsAnalyzer()
    
    news_sentiment = analyzer.analyze_news_sentiment(symbol, days)
    social_mentions = analyzer.get_social_mentions(symbol, days)
    market_sentiment = analyzer.get_market_sentiment()
    
    return {
        'symbol': symbol,
        'news_sentiment': news_sentiment,
        'social_mentions': social_mentions,
        'market_sentiment': market_sentiment,
        'generated_at': datetime.now().isoformat()
    }


if __name__ == "__main__":
    # Test news analyzer
    analyzer = NewsAnalyzer()
    
    # Test sentiment analysis
    test_text = "Lợi nhuận của công ty tăng mạnh, triển vọng tích cực trong quý tới"
    sentiment = analyzer.analyze_sentiment(test_text)
    print("Sentiment:", sentiment)
    
    # Test news sentiment
    news_sentiment = analyzer.analyze_news_sentiment('ACB', days=7)
    print("\nNews Sentiment:", news_sentiment)
    
    # Test market sentiment
    market_sentiment = analyzer.get_market_sentiment()
    print("\nMarket Sentiment:", market_sentiment)

