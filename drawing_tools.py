"""
Drawing Tools Module - VNStock
Interactive chart drawing tools: Lines, Fibonacci, Zones, Annotations
"""

import plotly.graph_objects as go
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ChartDrawing:
    """Class để quản lý các drawing tools trên chart"""
    
    def __init__(self):
        """Initialize drawing manager"""
        self.drawings = []
        self.drawing_count = 0
    
    def add_horizontal_line(self, y: float, color: str = '#FF0000', 
                           width: int = 2, dash: str = 'dash',
                           label: str = '') -> Dict:
        """
        Thêm đường ngang (horizontal line) cho support/resistance
        
        Args:
            y: Giá trị Y (price level)
            color: Màu sắc (hex code)
            width: Độ dày đường
            dash: Kiểu đường ('solid', 'dash', 'dot')
            label: Label cho đường
        
        Returns:
            Dict chứa drawing info
        """
        drawing = {
            'type': 'hline',
            'id': f'hline_{self.drawing_count}',
            'y': y,
            'color': color,
            'width': width,
            'dash': dash,
            'label': label or f'Level {y:,.0f}',
            'created': datetime.now().isoformat()
        }
        
        self.drawings.append(drawing)
        self.drawing_count += 1
        logger.info(f"Added horizontal line at {y}")
        
        return drawing
    
    def add_vertical_line(self, x: str, color: str = '#0000FF',
                         width: int = 2, dash: str = 'dash',
                         label: str = '') -> Dict:
        """
        Thêm đường dọc (vertical line) cho events/dates
        
        Args:
            x: Ngày/thời gian (datetime string)
            color: Màu sắc
            width: Độ dày
            dash: Kiểu đường
            label: Label
        
        Returns:
            Dict chứa drawing info
        """
        drawing = {
            'type': 'vline',
            'id': f'vline_{self.drawing_count}',
            'x': x,
            'color': color,
            'width': width,
            'dash': dash,
            'label': label or f'Event {x}',
            'created': datetime.now().isoformat()
        }
        
        self.drawings.append(drawing)
        self.drawing_count += 1
        logger.info(f"Added vertical line at {x}")
        
        return drawing
    
    def add_trend_line(self, x0: str, y0: float, x1: str, y1: float,
                      color: str = '#00FF00', width: int = 2,
                      extend: bool = False, label: str = '') -> Dict:
        """
        Thêm trend line (đường xu hướng)
        
        Args:
            x0, y0: Điểm đầu (date, price)
            x1, y1: Điểm cuối (date, price)
            color: Màu sắc
            width: Độ dày
            extend: Extend line beyond points
            label: Label
        
        Returns:
            Dict chứa drawing info
        """
        drawing = {
            'type': 'trendline',
            'id': f'trendline_{self.drawing_count}',
            'x0': x0,
            'y0': y0,
            'x1': x1,
            'y1': y1,
            'color': color,
            'width': width,
            'extend': extend,
            'label': label or 'Trend Line',
            'created': datetime.now().isoformat()
        }
        
        self.drawings.append(drawing)
        self.drawing_count += 1
        logger.info(f"Added trend line from ({x0}, {y0}) to ({x1}, {y1})")
        
        return drawing
    
    def add_fibonacci_retracement(self, x0: str, y0: float, x1: str, y1: float,
                                 levels: List[float] = None) -> Dict:
        """
        Thêm Fibonacci Retracement levels
        
        Args:
            x0, y0: Điểm swing low (date, price)
            x1, y1: Điểm swing high (date, price)
            levels: Custom Fibonacci levels (default: [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1])
        
        Returns:
            Dict chứa drawing info
        """
        if levels is None:
            levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
        
        # Calculate Fibonacci prices
        price_range = y1 - y0
        fib_prices = {}
        
        for level in levels:
            fib_price = y1 - (price_range * level)
            fib_prices[level] = fib_price
        
        drawing = {
            'type': 'fibonacci',
            'id': f'fibonacci_{self.drawing_count}',
            'x0': x0,
            'y0': y0,
            'x1': x1,
            'y1': y1,
            'levels': levels,
            'prices': fib_prices,
            'label': 'Fibonacci Retracement',
            'created': datetime.now().isoformat()
        }
        
        self.drawings.append(drawing)
        self.drawing_count += 1
        logger.info(f"Added Fibonacci retracement from {y0} to {y1}")
        
        return drawing
    
    def add_rectangle(self, x0: str, y0: float, x1: str, y1: float,
                     fillcolor: str = 'rgba(0,100,80,0.2)',
                     line_color: str = '#006450',
                     label: str = '') -> Dict:
        """
        Thêm rectangle zone (vùng hỗ trợ/kháng cự)
        
        Args:
            x0, y0: Góc trên trái
            x1, y1: Góc dưới phải
            fillcolor: Màu nền (rgba)
            line_color: Màu viền
            label: Label
        
        Returns:
            Dict chứa drawing info
        """
        drawing = {
            'type': 'rectangle',
            'id': f'rectangle_{self.drawing_count}',
            'x0': x0,
            'y0': y0,
            'x1': x1,
            'y1': y1,
            'fillcolor': fillcolor,
            'line_color': line_color,
            'label': label or 'Zone',
            'created': datetime.now().isoformat()
        }
        
        self.drawings.append(drawing)
        self.drawing_count += 1
        logger.info(f"Added rectangle from ({x0}, {y0}) to ({x1}, {y1})")
        
        return drawing
    
    def add_annotation(self, x: str, y: float, text: str,
                      arrow: bool = True, arrow_color: str = '#000000',
                      font_size: int = 12, font_color: str = '#000000',
                      bg_color: str = 'rgba(255,255,255,0.8)') -> Dict:
        """
        Thêm text annotation
        
        Args:
            x, y: Vị trí (date, price)
            text: Nội dung text
            arrow: Hiển thị arrow
            arrow_color: Màu arrow
            font_size: Kích thước font
            font_color: Màu chữ
            bg_color: Màu nền
        
        Returns:
            Dict chứa drawing info
        """
        drawing = {
            'type': 'annotation',
            'id': f'annotation_{self.drawing_count}',
            'x': x,
            'y': y,
            'text': text,
            'arrow': arrow,
            'arrow_color': arrow_color,
            'font_size': font_size,
            'font_color': font_color,
            'bg_color': bg_color,
            'created': datetime.now().isoformat()
        }
        
        self.drawings.append(drawing)
        self.drawing_count += 1
        logger.info(f"Added annotation at ({x}, {y}): {text}")
        
        return drawing
    
    def apply_to_figure(self, fig: go.Figure) -> go.Figure:
        """
        Apply tất cả drawings vào Plotly figure
        
        Args:
            fig: Plotly figure object
        
        Returns:
            Updated figure
        """
        shapes = []
        annotations = []
        
        for drawing in self.drawings:
            if drawing['type'] == 'hline':
                shapes.append({
                    'type': 'line',
                    'xref': 'paper',
                    'yref': 'y',
                    'x0': 0,
                    'y0': drawing['y'],
                    'x1': 1,
                    'y1': drawing['y'],
                    'line': {
                        'color': drawing['color'],
                        'width': drawing['width'],
                        'dash': drawing['dash']
                    }
                })
                
                # Add label
                annotations.append({
                    'xref': 'paper',
                    'yref': 'y',
                    'x': 1,
                    'y': drawing['y'],
                    'text': drawing['label'],
                    'showarrow': False,
                    'xanchor': 'left',
                    'bgcolor': 'rgba(255,255,255,0.8)',
                    'font': {'size': 10, 'color': drawing['color']}
                })
            
            elif drawing['type'] == 'vline':
                shapes.append({
                    'type': 'line',
                    'xref': 'x',
                    'yref': 'paper',
                    'x0': drawing['x'],
                    'y0': 0,
                    'x1': drawing['x'],
                    'y1': 1,
                    'line': {
                        'color': drawing['color'],
                        'width': drawing['width'],
                        'dash': drawing['dash']
                    }
                })
            
            elif drawing['type'] == 'trendline':
                shapes.append({
                    'type': 'line',
                    'xref': 'x',
                    'yref': 'y',
                    'x0': drawing['x0'],
                    'y0': drawing['y0'],
                    'x1': drawing['x1'],
                    'y1': drawing['y1'],
                    'line': {
                        'color': drawing['color'],
                        'width': drawing['width']
                    }
                })
            
            elif drawing['type'] == 'fibonacci':
                # Draw horizontal lines for each Fibonacci level
                for level, price in drawing['prices'].items():
                    color_alpha = 1 - level  # Fade color based on level
                    shapes.append({
                        'type': 'line',
                        'xref': 'paper',
                        'yref': 'y',
                        'x0': 0,
                        'y0': price,
                        'x1': 1,
                        'y1': price,
                        'line': {
                            'color': f'rgba(255,165,0,{color_alpha})',
                            'width': 1,
                            'dash': 'dot'
                        }
                    })
                    
                    # Add level labels
                    annotations.append({
                        'xref': 'paper',
                        'yref': 'y',
                        'x': 1,
                        'y': price,
                        'text': f'{level:.3f} ({price:,.0f})',
                        'showarrow': False,
                        'xanchor': 'left',
                        'bgcolor': 'rgba(255,255,255,0.8)',
                        'font': {'size': 9, 'color': 'orange'}
                    })
            
            elif drawing['type'] == 'rectangle':
                shapes.append({
                    'type': 'rect',
                    'xref': 'x',
                    'yref': 'y',
                    'x0': drawing['x0'],
                    'y0': drawing['y0'],
                    'x1': drawing['x1'],
                    'y1': drawing['y1'],
                    'fillcolor': drawing['fillcolor'],
                    'line': {'color': drawing['line_color'], 'width': 2}
                })
            
            elif drawing['type'] == 'annotation':
                annotations.append({
                    'x': drawing['x'],
                    'y': drawing['y'],
                    'text': drawing['text'],
                    'showarrow': drawing['arrow'],
                    'arrowhead': 2 if drawing['arrow'] else 0,
                    'arrowcolor': drawing['arrow_color'],
                    'bgcolor': drawing['bg_color'],
                    'font': {
                        'size': drawing['font_size'],
                        'color': drawing['font_color']
                    }
                })
        
        # Update figure
        fig.update_layout(
            shapes=shapes,
            annotations=annotations
        )
        
        logger.info(f"Applied {len(self.drawings)} drawings to figure")
        return fig
    
    def remove_drawing(self, drawing_id: str) -> bool:
        """Remove drawing by ID"""
        for i, drawing in enumerate(self.drawings):
            if drawing['id'] == drawing_id:
                removed = self.drawings.pop(i)
                logger.info(f"Removed drawing: {drawing_id}")
                return True
        
        logger.warning(f"Drawing not found: {drawing_id}")
        return False
    
    def clear_all(self):
        """Clear all drawings"""
        count = len(self.drawings)
        self.drawings = []
        logger.info(f"Cleared {count} drawings")
    
    def clear_by_type(self, drawing_type: str):
        """Clear drawings by type"""
        self.drawings = [d for d in self.drawings if d['type'] != drawing_type]
        logger.info(f"Cleared all {drawing_type} drawings")
    
    def to_json(self) -> str:
        """Export drawings to JSON string"""
        return json.dumps(self.drawings, indent=2)
    
    def from_json(self, json_str: str):
        """Import drawings from JSON string"""
        try:
            self.drawings = json.loads(json_str)
            self.drawing_count = len(self.drawings)
            logger.info(f"Loaded {self.drawing_count} drawings from JSON")
        except Exception as e:
            logger.error(f"Error loading drawings from JSON: {e}")
    
    def get_drawing_summary(self) -> Dict:
        """Get summary of all drawings"""
        summary = {
            'total': len(self.drawings),
            'by_type': {}
        }
        
        for drawing in self.drawings:
            dtype = drawing['type']
            summary['by_type'][dtype] = summary['by_type'].get(dtype, 0) + 1
        
        return summary


# ========== PRESET DRAWING TEMPLATES ==========

class DrawingPresets:
    """Predefined drawing templates"""
    
    @staticmethod
    def support_resistance_levels(prices: List[float], color: str = '#FF0000') -> List[Dict]:
        """
        Create horizontal lines for support/resistance levels
        
        Args:
            prices: List of price levels
            color: Color for all lines
        
        Returns:
            List of drawing configs
        """
        drawings = []
        for price in prices:
            drawings.append({
                'type': 'hline',
                'y': price,
                'color': color,
                'width': 2,
                'dash': 'dash',
                'label': f'S/R {price:,.0f}'
            })
        return drawings
    
    @staticmethod
    def price_channel(high_line: Tuple[str, float, str, float],
                     low_line: Tuple[str, float, str, float]) -> List[Dict]:
        """
        Create price channel with upper and lower trend lines
        
        Args:
            high_line: (x0, y0, x1, y1) for upper line
            low_line: (x0, y0, x1, y1) for lower line
        
        Returns:
            List of drawing configs
        """
        return [
            {
                'type': 'trendline',
                'x0': high_line[0],
                'y0': high_line[1],
                'x1': high_line[2],
                'y1': high_line[3],
                'color': '#FF0000',
                'width': 2,
                'label': 'Upper Channel'
            },
            {
                'type': 'trendline',
                'x0': low_line[0],
                'y0': low_line[1],
                'x1': low_line[2],
                'y1': low_line[3],
                'color': '#00FF00',
                'width': 2,
                'label': 'Lower Channel'
            }
        ]
    
    @staticmethod
    def breakout_zone(x0: str, x1: str, resistance: float, 
                     support: float) -> Dict:
        """
        Create rectangle zone for breakout area
        
        Args:
            x0, x1: Start and end dates
            resistance: Upper price
            support: Lower price
        
        Returns:
            Rectangle drawing config
        """
        return {
            'type': 'rectangle',
            'x0': x0,
            'y0': resistance,
            'x1': x1,
            'y1': support,
            'fillcolor': 'rgba(255,0,0,0.1)',
            'line_color': '#FF0000',
            'label': 'Breakout Zone'
        }


# ========== HELPER FUNCTIONS ==========

def create_drawing_manager() -> ChartDrawing:
    """Factory function to create new drawing manager"""
    return ChartDrawing()


def quick_support_resistance(fig: go.Figure, levels: List[float]) -> go.Figure:
    """
    Quick function to add support/resistance levels to existing figure
    
    Args:
        fig: Plotly figure
        levels: List of price levels
    
    Returns:
        Updated figure
    """
    drawer = ChartDrawing()
    for level in levels:
        drawer.add_horizontal_line(level, label=f'S/R {level:,.0f}')
    
    return drawer.apply_to_figure(fig)


def quick_fibonacci(fig: go.Figure, swing_low: Tuple[str, float],
                   swing_high: Tuple[str, float]) -> go.Figure:
    """
    Quick function to add Fibonacci retracement
    
    Args:
        fig: Plotly figure
        swing_low: (date, price) for swing low
        swing_high: (date, price) for swing high
    
    Returns:
        Updated figure
    """
    drawer = ChartDrawing()
    drawer.add_fibonacci_retracement(
        swing_low[0], swing_low[1],
        swing_high[0], swing_high[1]
    )
    
    return drawer.apply_to_figure(fig)


if __name__ == "__main__":
    # Test drawing tools
    drawer = ChartDrawing()
    
    # Add some drawings
    drawer.add_horizontal_line(25000, color='#FF0000', label='Resistance')
    drawer.add_horizontal_line(24000, color='#00FF00', label='Support')
    drawer.add_trend_line('2024-01-01', 23000, '2024-06-01', 26000, color='#0000FF')
    drawer.add_fibonacci_retracement('2024-01-01', 23000, '2024-06-01', 27000)
    drawer.add_annotation('2024-03-15', 25500, 'Breakout!', arrow=True)
    
    # Print summary
    print(drawer.get_drawing_summary())
    
    # Export to JSON
    json_str = drawer.to_json()
    print("Exported drawings:")
    print(json_str)

