#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Background Scanner - VNStock Classification System
Tự động scan toàn bộ thị trường mỗi đêm và lưu vào cache
"""

import schedule
import time
from datetime import datetime
from stock_classifier import StockClassifier
from database import get_db
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs_background_scanner.txt'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def daily_full_scan():
    """
    Scan toàn bộ thị trường mỗi đêm
    Chạy lúc 2:00 AM để tránh traffic cao
    """
    start_time = datetime.now()
    logger.info("=" * 80)
    logger.info("🌙 Starting nightly full market scan...")
    logger.info("=" * 80)
    
    try:
        classifier = StockClassifier()
        db = get_db()
        
        # Scan all exchanges
        logger.info("📊 Scanning HOSE and HNX markets...")
        
        results = classifier.scan_and_classify_market(
            exchanges=['HOSE', 'HNX'],
            limit=500,  # Scan all stocks
            delay=10.0,  # Safe delay to avoid rate limits
            use_cache=False,  # Force fresh scan
            save_cache=True  # Auto-save to cache
        )
        
        # Summary statistics
        successful = len([r for r in results if not r.get('error')])
        failed = len([r for r in results if r.get('error')])
        
        # Rating distribution
        ratings = {}
        for stock in results:
            if not stock.get('error'):
                rating = stock.get('overall_rating', {}).get('rating', 'Unknown')
                ratings[rating] = ratings.get(rating, 0) + 1
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info("=" * 80)
        logger.info("✅ Nightly scan complete!")
        logger.info(f"⏱️  Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
        logger.info(f"📈 Total stocks: {len(results)}")
        logger.info(f"✅ Successful: {successful}")
        logger.info(f"❌ Failed: {failed}")
        logger.info(f"📊 Rating distribution: {ratings}")
        logger.info("=" * 80)
        
        # Get cache stats
        cache_stats = db.get_cache_stats()
        logger.info(f"💾 Cache stats: {cache_stats}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error during nightly scan: {e}")
        logger.exception("Full traceback:")
        return False


def incremental_scan():
    """
    Scan incremental - chỉ update stocks cũ > 24h
    Chạy mỗi 4 tiếng
    """
    logger.info("🔄 Starting incremental scan...")
    
    try:
        db = get_db()
        classifier = StockClassifier()
        
        # Get outdated stocks
        outdated = db.get_outdated_classifications(max_age_hours=24, limit=50)
        
        if not outdated:
            logger.info("✅ No outdated stocks found. Cache is fresh!")
            return True
        
        logger.info(f"🔄 Found {len(outdated)} outdated stocks. Refreshing...")
        
        updated = 0
        for stock in outdated:
            try:
                symbol = stock['symbol']
                logger.info(f"Refreshing {symbol} (last scan: {stock['age_hours']:.1f}h ago)")
                
                # Classify and auto-save to cache
                result = classifier.classify_stock(symbol, use_cache=False, save_cache=True)
                
                if not result.get('error'):
                    updated += 1
                
                time.sleep(8)  # Rate limit safe
                
            except Exception as e:
                logger.error(f"Error refreshing {symbol}: {e}")
        
        logger.info(f"✅ Incremental scan complete: {updated}/{len(outdated)} updated")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error during incremental scan: {e}")
        return False


def main():
    """Main scheduler loop"""
    logger.info("🚀 VNStock Background Scanner started")
    logger.info(f"⏰ Current time: {datetime.now()}")
    
    # Schedule tasks
    # Daily full scan at 2:00 AM
    schedule.every().day.at("02:00").do(daily_full_scan)
    logger.info("📅 Scheduled: Daily full scan at 02:00 AM")
    
    # Incremental scan every 4 hours
    schedule.every(4).hours.do(incremental_scan)
    logger.info("📅 Scheduled: Incremental scan every 4 hours")
    
    # Run once at startup (optional - comment out if not needed)
    # logger.info("🔄 Running initial scan...")
    # incremental_scan()
    
    logger.info("✅ Scheduler running. Press Ctrl+C to stop.")
    logger.info("=" * 80)
    
    # Main loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        logger.info("\n\n⏹️  Scheduler stopped by user")
    except Exception as e:
        logger.error(f"❌ Scheduler error: {e}")
        logger.exception("Full traceback:")


if __name__ == "__main__":
    main()

