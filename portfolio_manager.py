"""
Portfolio Manager - VNStock
Portfolio tracking, paper trading, P&L calculation, performance metrics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from database import get_db
from vnstock import Vnstock

logger = logging.getLogger(__name__)


class PortfolioManager:
    """Quản lý portfolio và paper trading"""
    
    def __init__(self, initial_capital: float = 100_000_000):
        """
        Initialize portfolio manager
        
        Args:
            initial_capital: Vốn ban đầu (VND)
        """
        self.db = get_db()
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.commission_rate = 0.0015  # 0.15% commission
        logger.info(f"Portfolio initialized with {initial_capital:,.0f} VND")
    
    # ========== POSITION MANAGEMENT ==========
    
    def buy_stock(self, symbol: str, quantity: int, price: float = None,
                  notes: str = '') -> Dict:
        """
        Mua cổ phiếu (paper trading)
        
        Args:
            symbol: Mã cổ phiếu
            quantity: Số lượng
            price: Giá mua (None = current price)
            notes: Ghi chú
        
        Returns:
            Dict chứa thông tin giao dịch
        """
        try:
            # Get current price if not provided
            if price is None:
                price = self._get_current_price(symbol)
            
            # Calculate costs
            stock_value = quantity * price
            commission = stock_value * self.commission_rate
            total_cost = stock_value + commission
            
            # Check if have enough cash
            if total_cost > self.cash:
                logger.warning(f"Insufficient cash: {self.cash:,.0f} < {total_cost:,.0f}")
                return {
                    'success': False,
                    'error': 'Insufficient cash',
                    'required': total_cost,
                    'available': self.cash
                }
            
            # Execute buy
            buy_date = datetime.now().isoformat()
            position_id = self.db.add_position(
                symbol=symbol,
                quantity=quantity,
                buy_price=price,
                buy_date=buy_date,
                notes=notes
            )
            
            # Update cash
            self.cash -= total_cost
            
            # Save transaction
            self.db.add_transaction(
                symbol=symbol,
                transaction_type='buy',
                quantity=quantity,
                price=price,
                transaction_date=buy_date,
                fees=commission,
                notes=notes
            )
            
            logger.info(f"BUY: {symbol} x{quantity} @ {price:,.0f} = {total_cost:,.0f}")
            
            return {
                'success': True,
                'position_id': position_id,
                'symbol': symbol,
                'quantity': quantity,
                'buy_price': price,
                'stock_value': stock_value,
                'commission': commission,
                'total_cost': total_cost,
                'remaining_cash': self.cash
            }
            
        except Exception as e:
            logger.error(f"Error buying stock: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def sell_stock(self, position_id: int, quantity: int = None, 
                   price: float = None, notes: str = '') -> Dict:
        """
        Bán cổ phiếu
        
        Args:
            position_id: ID của position
            quantity: Số lượng bán (None = bán hết)
            price: Giá bán (None = current price)
            notes: Ghi chú
        
        Returns:
            Dict chứa thông tin giao dịch
        """
        try:
            # Get position
            positions = self.db.get_portfolio(status='open')
            position = None
            for p in positions:
                if p['id'] == position_id:
                    position = p
                    break
            
            if not position:
                return {
                    'success': False,
                    'error': 'Position not found'
                }
            
            # Determine sell quantity
            sell_quantity = quantity if quantity else position['quantity']
            
            if sell_quantity > position['quantity']:
                return {
                    'success': False,
                    'error': 'Sell quantity exceeds position'
                }
            
            # Get current price if not provided
            if price is None:
                price = self._get_current_price(position['symbol'])
            
            # Calculate proceeds
            stock_value = sell_quantity * price
            commission = stock_value * self.commission_rate
            net_proceeds = stock_value - commission
            
            # Calculate P&L
            cost_basis = sell_quantity * position['buy_price']
            pnl = net_proceeds - cost_basis
            pnl_pct = (pnl / cost_basis) * 100
            
            # Execute sell
            sell_date = datetime.now().isoformat()
            
            if sell_quantity == position['quantity']:
                # Close entire position
                self.db.close_position(position_id, price, sell_date)
            else:
                # Partial sell - update quantity (not implemented in DB yet)
                logger.warning("Partial sell not fully implemented")
            
            # Update cash
            self.cash += net_proceeds
            
            # Save transaction
            self.db.add_transaction(
                symbol=position['symbol'],
                transaction_type='sell',
                quantity=sell_quantity,
                price=price,
                transaction_date=sell_date,
                fees=commission,
                notes=notes
            )
            
            logger.info(f"SELL: {position['symbol']} x{sell_quantity} @ {price:,.0f} = {net_proceeds:,.0f} (P&L: {pnl:,.0f})")
            
            return {
                'success': True,
                'symbol': position['symbol'],
                'quantity': sell_quantity,
                'sell_price': price,
                'stock_value': stock_value,
                'commission': commission,
                'net_proceeds': net_proceeds,
                'cost_basis': cost_basis,
                'pnl': pnl,
                'pnl_pct': pnl_pct,
                'remaining_cash': self.cash
            }
            
        except Exception as e:
            logger.error(f"Error selling stock: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    # ========== PORTFOLIO ANALYSIS ==========
    
    def get_portfolio_value(self) -> Dict:
        """
        Tính toán tổng giá trị portfolio hiện tại
        
        Returns:
            Dict chứa portfolio metrics
        """
        try:
            positions = self.db.get_portfolio(status='open')
            
            if not positions:
                return {
                    'cash': self.cash,
                    'stock_value': 0,
                    'total_value': self.cash,
                    'initial_capital': self.initial_capital,
                    'total_pnl': self.cash - self.initial_capital,
                    'total_pnl_pct': ((self.cash - self.initial_capital) / self.initial_capital) * 100,
                    'positions': []
                }
            
            # Calculate each position's current value
            position_details = []
            total_stock_value = 0
            
            for pos in positions:
                current_price = self._get_current_price(pos['symbol'])
                current_value = pos['quantity'] * current_price
                cost_basis = pos['quantity'] * pos['buy_price']
                pnl = current_value - cost_basis
                pnl_pct = (pnl / cost_basis) * 100
                
                position_details.append({
                    'position_id': pos['id'],
                    'symbol': pos['symbol'],
                    'quantity': pos['quantity'],
                    'buy_price': pos['buy_price'],
                    'current_price': current_price,
                    'cost_basis': cost_basis,
                    'current_value': current_value,
                    'pnl': pnl,
                    'pnl_pct': pnl_pct,
                    'buy_date': pos['buy_date']
                })
                
                total_stock_value += current_value
            
            total_value = self.cash + total_stock_value
            total_pnl = total_value - self.initial_capital
            total_pnl_pct = (total_pnl / self.initial_capital) * 100
            
            return {
                'cash': self.cash,
                'stock_value': total_stock_value,
                'total_value': total_value,
                'initial_capital': self.initial_capital,
                'total_pnl': total_pnl,
                'total_pnl_pct': total_pnl_pct,
                'positions': position_details,
                'position_count': len(positions),
                'cash_pct': (self.cash / total_value) * 100,
                'stock_pct': (total_stock_value / total_value) * 100
            }
            
        except Exception as e:
            logger.error(f"Error calculating portfolio value: {e}")
            return {
                'error': str(e)
            }
    
    def get_performance_metrics(self) -> Dict:
        """
        Tính toán các chỉ số hiệu suất
        
        Returns:
            Dict chứa performance metrics
        """
        try:
            # Get all transactions
            transactions = self.db.get_transactions(limit=1000)
            
            if not transactions:
                return {
                    'total_trades': 0,
                    'win_rate': 0,
                    'avg_pnl': 0,
                    'best_trade': None,
                    'worst_trade': None
                }
            
            # Analyze trades
            buy_trades = [t for t in transactions if t['transaction_type'] == 'buy']
            sell_trades = [t for t in transactions if t['transaction_type'] == 'sell']
            
            # Calculate P&L for each completed trade
            completed_trades = []
            
            for sell in sell_trades:
                # Find matching buy
                matching_buys = [b for b in buy_trades 
                               if b['symbol'] == sell['symbol'] 
                               and b['transaction_date'] < sell['transaction_date']]
                
                if matching_buys:
                    buy = matching_buys[-1]  # Most recent buy
                    
                    pnl = (sell['price'] - buy['price']) * sell['quantity']
                    pnl_pct = ((sell['price'] - buy['price']) / buy['price']) * 100
                    
                    completed_trades.append({
                        'symbol': sell['symbol'],
                        'buy_date': buy['transaction_date'],
                        'sell_date': sell['transaction_date'],
                        'buy_price': buy['price'],
                        'sell_price': sell['price'],
                        'quantity': sell['quantity'],
                        'pnl': pnl,
                        'pnl_pct': pnl_pct
                    })
            
            if not completed_trades:
                return {
                    'total_trades': 0,
                    'win_rate': 0,
                    'avg_pnl': 0,
                    'best_trade': None,
                    'worst_trade': None
                }
            
            # Calculate metrics
            winning_trades = [t for t in completed_trades if t['pnl'] > 0]
            losing_trades = [t for t in completed_trades if t['pnl'] < 0]
            
            total_trades = len(completed_trades)
            win_rate = (len(winning_trades) / total_trades) * 100 if total_trades > 0 else 0
            
            avg_pnl = np.mean([t['pnl'] for t in completed_trades])
            avg_pnl_pct = np.mean([t['pnl_pct'] for t in completed_trades])
            
            best_trade = max(completed_trades, key=lambda x: x['pnl'])
            worst_trade = min(completed_trades, key=lambda x: x['pnl'])
            
            avg_win = np.mean([t['pnl'] for t in winning_trades]) if winning_trades else 0
            avg_loss = np.mean([t['pnl'] for t in losing_trades]) if losing_trades else 0
            
            return {
                'total_trades': total_trades,
                'winning_trades': len(winning_trades),
                'losing_trades': len(losing_trades),
                'win_rate': win_rate,
                'avg_pnl': avg_pnl,
                'avg_pnl_pct': avg_pnl_pct,
                'avg_win': avg_win,
                'avg_loss': avg_loss,
                'profit_factor': abs(avg_win / avg_loss) if avg_loss != 0 else float('inf'),
                'best_trade': best_trade,
                'worst_trade': worst_trade,
                'completed_trades': completed_trades
            }
            
        except Exception as e:
            logger.error(f"Error calculating performance metrics: {e}")
            return {
                'error': str(e)
            }
    
    def get_portfolio_history(self, days: int = 30) -> pd.DataFrame:
        """
        Lấy lịch sử giá trị portfolio
        
        Args:
            days: Số ngày lịch sử
        
        Returns:
            DataFrame với portfolio value theo ngày
        """
        try:
            # Get all transactions
            transactions = self.db.get_transactions(limit=1000)
            
            if not transactions:
                return pd.DataFrame()
            
            # Create date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            
            # Calculate portfolio value for each date
            portfolio_history = []
            
            for date in date_range:
                # Simulate portfolio state at this date
                cash = self.initial_capital
                positions = {}
                
                for trans in transactions:
                    trans_date = datetime.fromisoformat(trans['transaction_date'])
                    
                    if trans_date.date() <= date.date():
                        if trans['transaction_type'] == 'buy':
                            cash -= trans['total_amount']
                            if trans['symbol'] not in positions:
                                positions[trans['symbol']] = {
                                    'quantity': 0,
                                    'avg_price': 0
                                }
                            
                            # Update average price
                            old_qty = positions[trans['symbol']]['quantity']
                            old_avg = positions[trans['symbol']]['avg_price']
                            new_qty = trans['quantity']
                            new_price = trans['price']
                            
                            total_qty = old_qty + new_qty
                            avg_price = ((old_qty * old_avg) + (new_qty * new_price)) / total_qty if total_qty > 0 else 0
                            
                            positions[trans['symbol']]['quantity'] = total_qty
                            positions[trans['symbol']]['avg_price'] = avg_price
                        
                        elif trans['transaction_type'] == 'sell':
                            cash += (trans['total_amount'] - trans['fees'])
                            if trans['symbol'] in positions:
                                positions[trans['symbol']]['quantity'] -= trans['quantity']
                                
                                if positions[trans['symbol']]['quantity'] <= 0:
                                    del positions[trans['symbol']]
                
                # Calculate stock value at this date
                stock_value = 0
                for symbol, pos_data in positions.items():
                    # Get historical price for this date
                    hist_price = self._get_historical_price(symbol, date)
                    if hist_price:
                        stock_value += pos_data['quantity'] * hist_price
                
                total_value = cash + stock_value
                
                portfolio_history.append({
                    'date': date,
                    'cash': cash,
                    'stock_value': stock_value,
                    'total_value': total_value,
                    'pnl': total_value - self.initial_capital,
                    'pnl_pct': ((total_value - self.initial_capital) / self.initial_capital) * 100
                })
            
            df = pd.DataFrame(portfolio_history)
            return df
            
        except Exception as e:
            logger.error(f"Error getting portfolio history: {e}")
            return pd.DataFrame()
    
    # ========== HELPER FUNCTIONS ==========
    
    def _get_current_price(self, symbol: str) -> float:
        """Get current price for a symbol"""
        try:
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
            
            df = stock.quote.history(start=start_date, end=end_date)
            
            if not df.empty:
                current_price = df['close'].iloc[-1] * 1000  # Convert to VND
                return current_price
            else:
                logger.warning(f"No price data for {symbol}")
                return 0
                
        except Exception as e:
            logger.error(f"Error getting current price for {symbol}: {e}")
            return 0
    
    def _get_historical_price(self, symbol: str, date: datetime) -> Optional[float]:
        """Get historical price for a symbol on a specific date"""
        try:
            stock = Vnstock().stock(symbol=symbol, source='VCI')
            date_str = date.strftime("%Y-%m-%d")
            start_date = (date - timedelta(days=7)).strftime("%Y-%m-%d")
            
            df = stock.quote.history(start=start_date, end=date_str)
            
            if not df.empty:
                # Get closest date
                return df['close'].iloc[-1] * 1000  # Convert to VND
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error getting historical price for {symbol}: {e}")
            return None
    
    def reset_portfolio(self, confirm: bool = False):
        """
        Reset portfolio to initial state (USE WITH CAUTION!)
        
        Args:
            confirm: Must be True to execute
        """
        if not confirm:
            logger.warning("Reset requires confirmation")
            return False
        
        try:
            self.cash = self.initial_capital
            # Note: Database positions are not deleted, just marked as closed
            logger.warning(f"Portfolio reset to {self.initial_capital:,.0f} VND")
            return True
        except Exception as e:
            logger.error(f"Error resetting portfolio: {e}")
            return False


# ========== PORTFOLIO ANALYSIS FUNCTIONS ==========

def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.05) -> float:
    """
    Calculate Sharpe Ratio
    
    Args:
        returns: Series of returns
        risk_free_rate: Annual risk-free rate (default 5%)
    
    Returns:
        Sharpe ratio
    """
    excess_returns = returns - (risk_free_rate / 252)  # Daily risk-free rate
    return np.sqrt(252) * (excess_returns.mean() / excess_returns.std())


def calculate_max_drawdown(portfolio_values: pd.Series) -> Dict:
    """
    Calculate Maximum Drawdown
    
    Args:
        portfolio_values: Series of portfolio values
    
    Returns:
        Dict with max drawdown info
    """
    cumulative = portfolio_values
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    
    max_drawdown = drawdown.min()
    max_drawdown_idx = drawdown.idxmin()
    
    return {
        'max_drawdown': max_drawdown,
        'max_drawdown_pct': max_drawdown * 100,
        'max_drawdown_date': max_drawdown_idx,
        'drawdown_series': drawdown
    }


if __name__ == "__main__":
    # Test portfolio manager
    pm = PortfolioManager(initial_capital=100_000_000)
    
    # Test buy
    result = pm.buy_stock('ACB', 1000, price=25000)
    print("Buy result:", result)
    
    # Get portfolio value
    portfolio = pm.get_portfolio_value()
    print("\nPortfolio:", portfolio)
    
    # Get performance
    performance = pm.get_performance_metrics()
    print("\nPerformance:", performance)

