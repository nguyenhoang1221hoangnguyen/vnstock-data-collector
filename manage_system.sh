#!/bin/bash
# VNStock System Management Script
# Quản lý toàn bộ hệ thống VNStock

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║          VNStock System Manager                        ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

check_status() {
    echo -e "${YELLOW}📊 Checking system status...${NC}"
    echo ""
    
    # Check API
    if curl -s http://localhost:8501/health > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅ FastAPI Server:${NC} Running (Port 8501)"
    else
        echo -e "   ${RED}❌ FastAPI Server:${NC} Not running"
    fi
    
    # Check Dashboard
    if curl -s http://localhost:8503 > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅ Dashboard:${NC} Running (Port 8503)"
    else
        echo -e "   ${RED}❌ Dashboard:${NC} Not running"
    fi
    
    echo ""
}

start_api() {
    echo -e "${YELLOW}🚀 Starting FastAPI Server...${NC}"
    
    # Activate venv and start
    source venv/bin/activate
    nohup python main.py > logs_api.txt 2>&1 &
    echo $! > api_pid.txt
    
    sleep 3
    
    if curl -s http://localhost:8501/health > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅ FastAPI started (PID: $(cat api_pid.txt))${NC}"
        echo -e "   ${GREEN}📡 API URL: http://localhost:8501${NC}"
        echo -e "   ${GREEN}📖 Docs: http://localhost:8501/docs${NC}"
    else
        echo -e "   ${RED}❌ Failed to start FastAPI${NC}"
        echo -e "   ${YELLOW}Check logs_api.txt for details${NC}"
    fi
    echo ""
}

start_dashboard() {
    echo -e "${YELLOW}🚀 Starting Advanced Dashboard...${NC}"
    
    # Activate venv and start
    source venv/bin/activate
    nohup streamlit run dashboard_advanced.py --server.port 8503 > logs_dashboard.txt 2>&1 &
    echo $! > dashboard_pid.txt
    
    sleep 5
    
    if curl -s http://localhost:8503 > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅ Dashboard started (PID: $(cat dashboard_pid.txt))${NC}"
        echo -e "   ${GREEN}🌐 URL: http://localhost:8503${NC}"
    else
        echo -e "   ${RED}❌ Failed to start Dashboard${NC}"
        echo -e "   ${YELLOW}Check logs_dashboard.txt for details${NC}"
    fi
    echo ""
}

stop_all() {
    echo -e "${YELLOW}🛑 Stopping all services...${NC}"
    
    # Stop by PID files
    if [ -f api_pid.txt ]; then
        kill -9 $(cat api_pid.txt) 2>/dev/null
        rm api_pid.txt
        echo -e "   ${GREEN}✅ Stopped FastAPI${NC}"
    fi
    
    if [ -f dashboard_pid.txt ]; then
        kill -9 $(cat dashboard_pid.txt) 2>/dev/null
        rm dashboard_pid.txt
        echo -e "   ${GREEN}✅ Stopped Dashboard${NC}"
    fi
    
    # Kill any remaining processes
    pkill -f "python main.py" 2>/dev/null
    pkill -f "streamlit run dashboard_advanced.py" 2>/dev/null
    
    echo -e "   ${GREEN}✅ All services stopped${NC}"
    echo ""
}

start_all() {
    echo -e "${GREEN}🚀 Starting all services...${NC}"
    echo ""
    
    start_api
    start_dashboard
    
    echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✅ System Started Successfully!                      ║${NC}"
    echo -e "${GREEN}╠════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GREEN}║  📡 FastAPI:    http://localhost:8501                 ║${NC}"
    echo -e "${GREEN}║  📖 API Docs:   http://localhost:8501/docs            ║${NC}"
    echo -e "${GREEN}║  🌐 Dashboard:  http://localhost:8503                 ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

restart_all() {
    echo -e "${YELLOW}🔄 Restarting system...${NC}"
    echo ""
    
    stop_all
    sleep 2
    start_all
}

view_logs() {
    echo -e "${YELLOW}📋 Choose log to view:${NC}"
    echo "   1) API logs"
    echo "   2) Dashboard logs"
    echo "   3) Both"
    echo ""
    read -p "Enter choice [1-3]: " choice
    
    case $choice in
        1)
            echo -e "${YELLOW}📄 API Logs (last 50 lines):${NC}"
            tail -50 logs_api.txt 2>/dev/null || echo "No logs yet"
            ;;
        2)
            echo -e "${YELLOW}📄 Dashboard Logs (last 50 lines):${NC}"
            tail -50 logs_dashboard.txt 2>/dev/null || echo "No logs yet"
            ;;
        3)
            echo -e "${YELLOW}📄 API Logs:${NC}"
            tail -30 logs_api.txt 2>/dev/null || echo "No logs yet"
            echo ""
            echo -e "${YELLOW}📄 Dashboard Logs:${NC}"
            tail -30 logs_dashboard.txt 2>/dev/null || echo "No logs yet"
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            ;;
    esac
    echo ""
}

test_api() {
    echo -e "${YELLOW}🧪 Testing API endpoints...${NC}"
    echo ""
    
    # Test health
    echo -e "${BLUE}1. Health Check:${NC}"
    curl -s http://localhost:8501/health | python -m json.tool | head -5
    echo ""
    
    # Test single stock
    echo -e "${BLUE}2. Single Stock Classification (VCB):${NC}"
    curl -s "http://localhost:8501/classify/stock/VCB" | python -m json.tool | head -20
    echo ""
    
    # Test stock list
    echo -e "${BLUE}3. Stock List:${NC}"
    curl -s "http://localhost:8501/screener/list?exchange=HOSE" | python -m json.tool | head -10
    echo ""
    
    echo -e "${GREEN}✅ API tests complete${NC}"
    echo ""
}

# Main menu
show_menu() {
    print_header
    check_status
    
    echo -e "${BLUE}Choose an option:${NC}"
    echo ""
    echo "   1) 🚀 Start All Services"
    echo "   2) 🛑 Stop All Services"
    echo "   3) 🔄 Restart All Services"
    echo "   4) 📊 Check Status"
    echo "   5) 📋 View Logs"
    echo "   6) 🧪 Test API"
    echo "   7) 🚪 Exit"
    echo ""
    read -p "Enter choice [1-7]: " choice
    
    case $choice in
        1) start_all ;;
        2) stop_all ;;
        3) restart_all ;;
        4) check_status ;;
        5) view_logs ;;
        6) test_api ;;
        7) 
            echo -e "${GREEN}👋 Goodbye!${NC}"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Invalid choice${NC}"
            echo ""
            ;;
    esac
    
    # Loop back to menu
    read -p "Press Enter to continue..."
    show_menu
}

# Run menu
show_menu

