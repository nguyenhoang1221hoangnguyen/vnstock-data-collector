"""
Database Module - VNStock Persistent Storage
SQLite database cho Watchlist, Alerts, Chart Layouts, Portfolio
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)


class VNStockDB:
    """Database manager cho VNStock application"""
    
    def __init__(self, db_path: str = 'vnstock.db'):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self.create_tables()
        logger.info(f"Database initialized: {db_path}")
    
    def create_tables(self):
        """Create all required tables"""
        cursor = self.conn.cursor()
        
        # Watchlist table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL UNIQUE,
                added_date TEXT NOT NULL,
                notes TEXT,
                sector TEXT,
                target_price REAL,
                stop_loss REAL
            )
        ''')
        
        # Price Alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                condition TEXT NOT NULL CHECK(condition IN ('above', 'below')),
                price REAL NOT NULL,
                created_date TEXT NOT NULL,
                triggered INTEGER DEFAULT 0,
                triggered_date TEXT,
                notification_sent INTEGER DEFAULT 0,
                active INTEGER DEFAULT 1
            )
        ''')
        
        # Chart Layouts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chart_layouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                symbol TEXT,
                indicators TEXT,
                drawings TEXT,
                timeframe TEXT,
                saved_date TEXT NOT NULL,
                is_default INTEGER DEFAULT 0
            )
        ''')
        
        # Portfolio table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                quantity REAL NOT NULL,
                buy_price REAL NOT NULL,
                buy_date TEXT NOT NULL,
                notes TEXT,
                status TEXT DEFAULT 'open' CHECK(status IN ('open', 'closed'))
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                transaction_type TEXT NOT NULL CHECK(transaction_type IN ('buy', 'sell')),
                quantity REAL NOT NULL,
                price REAL NOT NULL,
                total_amount REAL NOT NULL,
                fees REAL DEFAULT 0,
                transaction_date TEXT NOT NULL,
                notes TEXT
            )
        ''')
        
        # User Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_date TEXT
            )
        ''')
        
        self.conn.commit()
        logger.info("All tables created successfully")
    
    # ========== WATCHLIST OPERATIONS ==========
    
    def add_to_watchlist(self, symbol: str, notes: str = '', sector: str = '', 
                        target_price: float = None, stop_loss: float = None) -> bool:
        """Add stock to watchlist"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO watchlist (symbol, added_date, notes, sector, target_price, stop_loss)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (symbol.upper(), datetime.now().isoformat(), notes, sector, target_price, stop_loss))
            self.conn.commit()
            logger.info(f"Added {symbol} to watchlist")
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"{symbol} already in watchlist")
            return False
        except Exception as e:
            logger.error(f"Error adding to watchlist: {e}")
            return False
    
    def remove_from_watchlist(self, symbol: str) -> bool:
        """Remove stock from watchlist"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM watchlist WHERE symbol = ?', (symbol.upper(),))
            self.conn.commit()
            logger.info(f"Removed {symbol} from watchlist")
            return True
        except Exception as e:
            logger.error(f"Error removing from watchlist: {e}")
            return False
    
    def get_watchlist(self) -> List[Dict]:
        """Get all stocks in watchlist"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM watchlist ORDER BY added_date DESC')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def update_watchlist_item(self, symbol: str, **kwargs) -> bool:
        """Update watchlist item"""
        try:
            allowed_fields = ['notes', 'sector', 'target_price', 'stop_loss']
            updates = []
            values = []
            
            for field, value in kwargs.items():
                if field in allowed_fields:
                    updates.append(f"{field} = ?")
                    values.append(value)
            
            if not updates:
                return False
            
            values.append(symbol.upper())
            query = f"UPDATE watchlist SET {', '.join(updates)} WHERE symbol = ?"
            
            cursor = self.conn.cursor()
            cursor.execute(query, values)
            self.conn.commit()
            logger.info(f"Updated watchlist item: {symbol}")
            return True
        except Exception as e:
            logger.error(f"Error updating watchlist: {e}")
            return False
    
    # ========== ALERTS OPERATIONS ==========
    
    def add_alert(self, symbol: str, condition: str, price: float) -> int:
        """Add price alert"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO alerts (symbol, condition, price, created_date)
                VALUES (?, ?, ?, ?)
            ''', (symbol.upper(), condition, price, datetime.now().isoformat()))
            self.conn.commit()
            alert_id = cursor.lastrowid
            logger.info(f"Added alert for {symbol} {condition} {price}")
            return alert_id
        except Exception as e:
            logger.error(f"Error adding alert: {e}")
            return -1
    
    def remove_alert(self, alert_id: int) -> bool:
        """Remove alert by ID"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM alerts WHERE id = ?', (alert_id,))
            self.conn.commit()
            logger.info(f"Removed alert ID: {alert_id}")
            return True
        except Exception as e:
            logger.error(f"Error removing alert: {e}")
            return False
    
    def get_active_alerts(self) -> List[Dict]:
        """Get all active alerts"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM alerts 
            WHERE active = 1 AND triggered = 0
            ORDER BY created_date DESC
        ''')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def get_all_alerts(self) -> List[Dict]:
        """Get all alerts (including triggered)"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM alerts ORDER BY created_date DESC')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def trigger_alert(self, alert_id: int) -> bool:
        """Mark alert as triggered"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE alerts 
                SET triggered = 1, triggered_date = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), alert_id))
            self.conn.commit()
            logger.info(f"Triggered alert ID: {alert_id}")
            return True
        except Exception as e:
            logger.error(f"Error triggering alert: {e}")
            return False
    
    def mark_alert_notification_sent(self, alert_id: int) -> bool:
        """Mark alert notification as sent"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE alerts 
                SET notification_sent = 1
                WHERE id = ?
            ''', (alert_id,))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error marking notification: {e}")
            return False
    
    # ========== CHART LAYOUTS OPERATIONS ==========
    
    def save_chart_layout(self, name: str, symbol: str, indicators: dict, 
                         drawings: dict = None, timeframe: str = '365', 
                         is_default: bool = False) -> int:
        """Save chart layout"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO chart_layouts 
                (name, symbol, indicators, drawings, timeframe, saved_date, is_default)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                name,
                symbol.upper() if symbol else None,
                json.dumps(indicators),
                json.dumps(drawings) if drawings else None,
                timeframe,
                datetime.now().isoformat(),
                1 if is_default else 0
            ))
            self.conn.commit()
            layout_id = cursor.lastrowid
            logger.info(f"Saved chart layout: {name}")
            return layout_id
        except Exception as e:
            logger.error(f"Error saving chart layout: {e}")
            return -1
    
    def get_chart_layouts(self, symbol: str = None) -> List[Dict]:
        """Get chart layouts"""
        cursor = self.conn.cursor()
        if symbol:
            cursor.execute('''
                SELECT * FROM chart_layouts 
                WHERE symbol = ? OR symbol IS NULL
                ORDER BY is_default DESC, saved_date DESC
            ''', (symbol.upper(),))
        else:
            cursor.execute('''
                SELECT * FROM chart_layouts 
                ORDER BY is_default DESC, saved_date DESC
            ''')
        
        rows = cursor.fetchall()
        layouts = []
        for row in rows:
            layout = dict(row)
            layout['indicators'] = json.loads(layout['indicators']) if layout['indicators'] else {}
            layout['drawings'] = json.loads(layout['drawings']) if layout['drawings'] else {}
            layouts.append(layout)
        
        return layouts
    
    def delete_chart_layout(self, layout_id: int) -> bool:
        """Delete chart layout"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM chart_layouts WHERE id = ?', (layout_id,))
            self.conn.commit()
            logger.info(f"Deleted chart layout ID: {layout_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting chart layout: {e}")
            return False
    
    # ========== PORTFOLIO OPERATIONS ==========
    
    def add_position(self, symbol: str, quantity: float, buy_price: float, 
                    buy_date: str = None, notes: str = '') -> int:
        """Add position to portfolio"""
        try:
            if buy_date is None:
                buy_date = datetime.now().isoformat()
            
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO portfolio (symbol, quantity, buy_price, buy_date, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (symbol.upper(), quantity, buy_price, buy_date, notes))
            self.conn.commit()
            
            # Record buy transaction
            self.add_transaction(symbol, 'buy', quantity, buy_price, buy_date)
            
            position_id = cursor.lastrowid
            logger.info(f"Added position: {symbol} x{quantity} @ {buy_price}")
            return position_id
        except Exception as e:
            logger.error(f"Error adding position: {e}")
            return -1
    
    def close_position(self, position_id: int, sell_price: float, 
                      sell_date: str = None) -> bool:
        """Close position"""
        try:
            if sell_date is None:
                sell_date = datetime.now().isoformat()
            
            cursor = self.conn.cursor()
            
            # Get position details
            cursor.execute('SELECT * FROM portfolio WHERE id = ?', (position_id,))
            position = cursor.execute('SELECT * FROM portfolio WHERE id = ?', (position_id,)).fetchone()
            
            if not position:
                logger.warning(f"Position {position_id} not found")
                return False
            
            # Update position status
            cursor.execute('''
                UPDATE portfolio 
                SET status = 'closed'
                WHERE id = ?
            ''', (position_id,))
            
            # Record sell transaction
            self.add_transaction(
                position['symbol'], 
                'sell', 
                position['quantity'], 
                sell_price, 
                sell_date
            )
            
            self.conn.commit()
            logger.info(f"Closed position ID: {position_id}")
            return True
        except Exception as e:
            logger.error(f"Error closing position: {e}")
            return False
    
    def get_portfolio(self, status: str = 'open') -> List[Dict]:
        """Get portfolio positions"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM portfolio 
            WHERE status = ?
            ORDER BY buy_date DESC
        ''', (status,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    # ========== TRANSACTIONS OPERATIONS ==========
    
    def add_transaction(self, symbol: str, transaction_type: str, quantity: float, 
                       price: float, transaction_date: str = None, 
                       fees: float = 0, notes: str = '') -> int:
        """Record transaction"""
        try:
            if transaction_date is None:
                transaction_date = datetime.now().isoformat()
            
            total_amount = quantity * price + fees
            
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO transactions 
                (symbol, transaction_type, quantity, price, total_amount, fees, transaction_date, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (symbol.upper(), transaction_type, quantity, price, total_amount, 
                  fees, transaction_date, notes))
            self.conn.commit()
            
            transaction_id = cursor.lastrowid
            logger.info(f"Recorded transaction: {transaction_type} {symbol} x{quantity}")
            return transaction_id
        except Exception as e:
            logger.error(f"Error adding transaction: {e}")
            return -1
    
    def get_transactions(self, symbol: str = None, limit: int = 100) -> List[Dict]:
        """Get transaction history"""
        cursor = self.conn.cursor()
        if symbol:
            cursor.execute('''
                SELECT * FROM transactions 
                WHERE symbol = ?
                ORDER BY transaction_date DESC
                LIMIT ?
            ''', (symbol.upper(), limit))
        else:
            cursor.execute('''
                SELECT * FROM transactions 
                ORDER BY transaction_date DESC
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    # ========== SETTINGS OPERATIONS ==========
    
    def save_setting(self, key: str, value: Any) -> bool:
        """Save user setting"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO settings (key, value, updated_date)
                VALUES (?, ?, ?)
            ''', (key, str(value), datetime.now().isoformat()))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error saving setting: {e}")
            return False
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get user setting"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        row = cursor.fetchone()
        return row['value'] if row else default
    
    # ========== UTILITY FUNCTIONS ==========
    
    def close(self):
        """Close database connection"""
        self.conn.close()
        logger.info("Database connection closed")
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        cursor = self.conn.cursor()
        
        stats = {
            'watchlist_count': cursor.execute('SELECT COUNT(*) FROM watchlist').fetchone()[0],
            'active_alerts_count': cursor.execute('SELECT COUNT(*) FROM alerts WHERE active = 1 AND triggered = 0').fetchone()[0],
            'chart_layouts_count': cursor.execute('SELECT COUNT(*) FROM chart_layouts').fetchone()[0],
            'open_positions_count': cursor.execute('SELECT COUNT(*) FROM portfolio WHERE status = "open"').fetchone()[0],
            'total_transactions': cursor.execute('SELECT COUNT(*) FROM transactions').fetchone()[0],
        }
        
        return stats
    
    def clear_all_data(self, confirm: bool = False):
        """Clear all data (USE WITH CAUTION!)"""
        if not confirm:
            logger.warning("Clear all data requires confirmation")
            return False
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM watchlist')
            cursor.execute('DELETE FROM alerts')
            cursor.execute('DELETE FROM chart_layouts')
            cursor.execute('DELETE FROM portfolio')
            cursor.execute('DELETE FROM transactions')
            cursor.execute('DELETE FROM settings')
            self.conn.commit()
            logger.warning("All data cleared!")
            return True
        except Exception as e:
            logger.error(f"Error clearing data: {e}")
            return False


# Singleton instance
_db_instance = None

def get_db() -> VNStockDB:
    """Get database instance (singleton)"""
    global _db_instance
    if _db_instance is None:
        _db_instance = VNStockDB()
    return _db_instance

