"""
Smart Notifications Module - VNStock
Multi-channel notifications: Telegram, Email, Discord
"""

import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class NotificationManager:
    """Quản lý thông báo đa kênh"""
    
    def __init__(self, config_file: str = 'notification_config.json'):
        """
        Initialize notification manager
        
        Args:
            config_file: Path to configuration file
        """
        self.config = self.load_config(config_file)
        self.enabled_channels = self.config.get('enabled_channels', [])
        logger.info(f"NotificationManager initialized. Channels: {self.enabled_channels}")
    
    def load_config(self, config_file: str) -> Dict:
        """Load configuration from file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            return config
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found. Using defaults.")
            return self.get_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            'enabled_channels': [],
            'telegram': {
                'bot_token': '',
                'chat_id': ''
            },
            'email': {
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'sender_email': '',
                'sender_password': '',
                'receiver_email': ''
            },
            'discord': {
                'webhook_url': ''
            }
        }
    
    def save_config(self, config_file: str = 'notification_config.json'):
        """Save configuration to file"""
        try:
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Config saved to {config_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            return False
    
    # ========== TELEGRAM NOTIFICATIONS ==========
    
    def send_telegram(self, message: str, parse_mode: str = 'HTML') -> bool:
        """
        Send notification via Telegram
        
        Args:
            message: Message to send (supports HTML)
            parse_mode: Parse mode ('HTML' or 'Markdown')
        
        Returns:
            True if successful, False otherwise
        """
        if 'telegram' not in self.enabled_channels:
            logger.debug("Telegram not enabled")
            return False
        
        try:
            telegram_config = self.config.get('telegram', {})
            bot_token = telegram_config.get('bot_token')
            chat_id = telegram_config.get('chat_id')
            
            if not bot_token or not chat_id:
                logger.warning("Telegram credentials not configured")
                return False
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                logger.info("Telegram notification sent successfully")
                return True
            else:
                logger.error(f"Telegram error: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending Telegram notification: {e}")
            return False
    
    # ========== EMAIL NOTIFICATIONS ==========
    
    def send_email(self, subject: str, body: str, html: bool = True) -> bool:
        """
        Send notification via Email
        
        Args:
            subject: Email subject
            body: Email body (text or HTML)
            html: Whether body is HTML
        
        Returns:
            True if successful, False otherwise
        """
        if 'email' not in self.enabled_channels:
            logger.debug("Email not enabled")
            return False
        
        try:
            email_config = self.config.get('email', {})
            smtp_server = email_config.get('smtp_server')
            smtp_port = email_config.get('smtp_port', 587)
            sender_email = email_config.get('sender_email')
            sender_password = email_config.get('sender_password')
            receiver_email = email_config.get('receiver_email')
            
            if not all([smtp_server, sender_email, sender_password, receiver_email]):
                logger.warning("Email credentials not configured")
                return False
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = receiver_email
            
            # Attach body
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            
            logger.info("Email notification sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email notification: {e}")
            return False
    
    # ========== DISCORD NOTIFICATIONS ==========
    
    def send_discord(self, message: str, username: str = 'VNStock Bot') -> bool:
        """
        Send notification via Discord webhook
        
        Args:
            message: Message to send
            username: Bot username
        
        Returns:
            True if successful, False otherwise
        """
        if 'discord' not in self.enabled_channels:
            logger.debug("Discord not enabled")
            return False
        
        try:
            discord_config = self.config.get('discord', {})
            webhook_url = discord_config.get('webhook_url')
            
            if not webhook_url:
                logger.warning("Discord webhook not configured")
                return False
            
            data = {
                'content': message,
                'username': username
            }
            
            response = requests.post(webhook_url, json=data, timeout=10)
            
            if response.status_code == 204:
                logger.info("Discord notification sent successfully")
                return True
            else:
                logger.error(f"Discord error: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending Discord notification: {e}")
            return False
    
    # ========== PRICE ALERT NOTIFICATIONS ==========
    
    def notify_price_alert(self, symbol: str, current_price: float, 
                          alert_price: float, condition: str) -> bool:
        """
        Send price alert notification to all enabled channels
        
        Args:
            symbol: Stock symbol
            current_price: Current stock price
            alert_price: Alert trigger price
            condition: 'above' or 'below'
        
        Returns:
            True if at least one channel succeeded
        """
        success = False
        
        # Format message
        emoji = "🚀" if condition == "above" else "📉"
        condition_text = "vượt" if condition == "above" else "xuống dưới"
        
        # Telegram message (HTML)
        telegram_msg = f"""
{emoji} <b>PRICE ALERT!</b>

<b>Symbol:</b> {symbol}
<b>Condition:</b> Giá {condition_text} {alert_price:,.0f} VND
<b>Current Price:</b> {current_price:,.0f} VND
<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💡 <i>Check your VNStock dashboard for details!</i>
"""
        
        # Discord/Plain text message
        plain_msg = f"""
{emoji} **PRICE ALERT!**

**Symbol:** {symbol}
**Condition:** Giá {condition_text} {alert_price:,.0f} VND
**Current Price:** {current_price:,.0f} VND
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💡 Check your VNStock dashboard for details!
"""
        
        # Email HTML
        email_html = f"""
<html>
<body style="font-family: Arial, sans-serif; padding: 20px;">
    <h2 style="color: #1f77b4;">{emoji} VNStock Price Alert</h2>
    <div style="background-color: #f0f2f6; padding: 15px; border-radius: 5px;">
        <p><strong>Symbol:</strong> {symbol}</p>
        <p><strong>Condition:</strong> Giá {condition_text} {alert_price:,.0f} VND</p>
        <p><strong>Current Price:</strong> <span style="color: {'green' if condition == 'above' else 'red'}; font-size: 1.2em;">{current_price:,.0f} VND</span></p>
        <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    <p style="margin-top: 20px; color: #666;">💡 Check your VNStock dashboard for detailed analysis!</p>
</body>
</html>
"""
        
        # Send to all channels
        if self.send_telegram(telegram_msg):
            success = True
        
        if self.send_email(f"🔔 Price Alert: {symbol}", email_html):
            success = True
        
        if self.send_discord(plain_msg):
            success = True
        
        return success
    
    # ========== TRADE NOTIFICATIONS ==========
    
    def notify_trade_execution(self, symbol: str, action: str, quantity: float, 
                              price: float, total: float) -> bool:
        """
        Send trade execution notification
        
        Args:
            symbol: Stock symbol
            action: 'buy' or 'sell'
            quantity: Number of shares
            price: Execution price
            total: Total amount
        
        Returns:
            True if successful
        """
        emoji = "💰" if action == "buy" else "💸"
        action_text = "MUA" if action == "buy" else "BÁN"
        
        message = f"""
{emoji} <b>GIAO DỊCH THỰC HIỆN</b>

<b>Lệnh:</b> {action_text} {symbol}
<b>Số lượng:</b> {quantity:,.0f} cp
<b>Giá:</b> {price:,.0f} VND
<b>Tổng tiền:</b> {total:,.0f} VND
<b>Thời gian:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return self.send_telegram(message)
    
    # ========== TECHNICAL SIGNAL NOTIFICATIONS ==========
    
    def notify_technical_signal(self, symbol: str, signal_type: str, 
                               indicator: str, details: str) -> bool:
        """
        Send technical analysis signal notification
        
        Args:
            symbol: Stock symbol
            signal_type: 'bullish', 'bearish', or 'neutral'
            indicator: Indicator name
            details: Signal details
        
        Returns:
            True if successful
        """
        emoji_map = {
            'bullish': '📈',
            'bearish': '📉',
            'neutral': '➡️'
        }
        
        emoji = emoji_map.get(signal_type, '💡')
        
        message = f"""
{emoji} <b>TECHNICAL SIGNAL</b>

<b>Symbol:</b> {symbol}
<b>Indicator:</b> {indicator}
<b>Signal:</b> {signal_type.upper()}
<b>Details:</b> {details}
<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return self.send_telegram(message)
    
    # ========== PORTFOLIO NOTIFICATIONS ==========
    
    def notify_portfolio_summary(self, total_value: float, daily_pnl: float, 
                                daily_pnl_pct: float, top_gainers: List[Dict], 
                                top_losers: List[Dict]) -> bool:
        """
        Send daily portfolio summary
        
        Args:
            total_value: Total portfolio value
            daily_pnl: Daily P&L
            daily_pnl_pct: Daily P&L percentage
            top_gainers: List of top gaining stocks
            top_losers: List of top losing stocks
        
        Returns:
            True if successful
        """
        pnl_emoji = "📈" if daily_pnl >= 0 else "📉"
        
        gainers_text = "\n".join([f"  • {g['symbol']}: +{g['change']:.2f}%" for g in top_gainers[:3]])
        losers_text = "\n".join([f"  • {l['symbol']}: {l['change']:.2f}%" for l in top_losers[:3]])
        
        message = f"""
📊 <b>PORTFOLIO DAILY SUMMARY</b>

<b>Total Value:</b> {total_value:,.0f} VND
<b>Daily P&L:</b> {pnl_emoji} {daily_pnl:,.0f} VND ({daily_pnl_pct:+.2f}%)

<b>Top Gainers:</b>
{gainers_text}

<b>Top Losers:</b>
{losers_text}

<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return self.send_telegram(message)


# Singleton instance
_notifier_instance = None

def get_notifier() -> NotificationManager:
    """Get notification manager instance (singleton)"""
    global _notifier_instance
    if _notifier_instance is None:
        _notifier_instance = NotificationManager()
    return _notifier_instance


# ========== ALERT MONITORING BACKGROUND TASK ==========

def start_alert_monitor(check_interval: int = 60):
    """
    Start background task to monitor price alerts
    
    Args:
        check_interval: Check interval in seconds (default 60)
    """
    import threading
    import time
    from database import get_db
    
    def monitor_alerts():
        """Monitor function running in background"""
        logger.info(f"Alert monitor started (interval: {check_interval}s)")
        db = get_db()
        notifier = get_notifier()
        
        while True:
            try:
                # Get active alerts
                alerts = db.get_active_alerts()
                
                for alert in alerts:
                    # Get current price
                    from vnstock import Vnstock
                    stock = Vnstock().stock(symbol=alert['symbol'], source='VCI')
                    end_date = datetime.now().strftime("%Y-%m-%d")
                    start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                    
                    df = stock.quote.history(start=start_date, end=end_date)
                    
                    if not df.empty:
                        current_price = df['close'].iloc[-1] * 1000  # Convert to VND
                        
                        # Check if alert should trigger
                        should_trigger = False
                        if alert['condition'] == 'above' and current_price >= alert['price']:
                            should_trigger = True
                        elif alert['condition'] == 'below' and current_price <= alert['price']:
                            should_trigger = True
                        
                        if should_trigger and not alert['notification_sent']:
                            # Send notification
                            success = notifier.notify_price_alert(
                                alert['symbol'],
                                current_price,
                                alert['price'],
                                alert['condition']
                            )
                            
                            if success:
                                # Mark alert as triggered
                                db.trigger_alert(alert['id'])
                                db.mark_alert_notification_sent(alert['id'])
                                logger.info(f"Alert triggered and notified: {alert['symbol']}")
                
            except Exception as e:
                logger.error(f"Error in alert monitor: {e}")
            
            # Wait for next check
            time.sleep(check_interval)
    
    # Start monitor thread
    monitor_thread = threading.Thread(target=monitor_alerts, daemon=True)
    monitor_thread.start()
    logger.info("Alert monitor thread started")


if __name__ == "__main__":
    # Test notifications
    notifier = NotificationManager()
    
    # Enable Telegram for testing
    notifier.enabled_channels = ['telegram']
    notifier.config['telegram'] = {
        'bot_token': 'YOUR_BOT_TOKEN_HERE',
        'chat_id': 'YOUR_CHAT_ID_HERE'
    }
    
    # Test price alert
    notifier.notify_price_alert('ACB', 25100, 25000, 'above')

