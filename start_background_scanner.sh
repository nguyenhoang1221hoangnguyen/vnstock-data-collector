#!/bin/bash
# Start Background Scanner for VNStock Classification System

echo "=============================================="
echo "🚀 VNStock Background Scanner"
echo "=============================================="
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if already running
if pgrep -f "background_scanner.py" > /dev/null; then
    echo "⚠️  Background scanner is already running!"
    echo ""
    echo "To stop it, run: pkill -f background_scanner.py"
    echo "To view logs: tail -f logs_background_scanner.txt"
    exit 1
fi

# Create logs directory if not exists
mkdir -p logs

# Start background scanner
echo "🌙 Starting background scanner..."
echo ""
echo "📅 Schedule:"
echo "   - Full scan: Daily at 2:00 AM"
echo "   - Incremental scan: Every 4 hours"
echo ""
echo "📝 Logs: logs_background_scanner.txt"
echo ""

nohup python3 background_scanner.py > logs_background_scanner.txt 2>&1 &
SCANNER_PID=$!

echo "✅ Background scanner started (PID: $SCANNER_PID)"
echo ""
echo "Commands:"
echo "  - View logs:  tail -f logs_background_scanner.txt"
echo "  - Stop:       pkill -f background_scanner.py"
echo "  - Status:     ps aux | grep background_scanner"
echo ""
echo "=============================================="

