#!/bin/bash
"""
Setup API Monitoring Cron Job
============================

This script sets up a cron job to monitor the JewGo API endpoints every 15 minutes.
It will send alerts if any endpoints are failing.

Usage: ./setup_monitoring.sh
"""

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
MONITOR_SCRIPT="$SCRIPT_DIR/api_health_monitor.py"
LOG_DIR="$PROJECT_ROOT/logs"
CRON_LOG="$LOG_DIR/cron.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up JewGo API monitoring...${NC}"

# Check if script exists
if [ ! -f "$MONITOR_SCRIPT" ]; then
    echo -e "${RED}Error: Monitor script not found at $MONITOR_SCRIPT${NC}"
    exit 1
fi

# Create logs directory
mkdir -p "$LOG_DIR"

# Make the monitor script executable
chmod +x "$MONITOR_SCRIPT"

# Create the cron job entry
CRON_JOB="*/15 * * * * cd $PROJECT_ROOT && source backend/venv_py311/bin/activate && python $MONITOR_SCRIPT >> $CRON_LOG 2>&1"

echo -e "${YELLOW}Creating cron job entry:${NC}"
echo "$CRON_JOB"
echo ""

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "$MONITOR_SCRIPT"; then
    echo -e "${YELLOW}Cron job already exists. Updating...${NC}"
    # Remove existing entry
    crontab -l 2>/dev/null | grep -v "$MONITOR_SCRIPT" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Cron job installed successfully!${NC}"
    echo ""
    echo -e "${YELLOW}Monitoring will run every 15 minutes.${NC}"
    echo -e "${YELLOW}Logs will be saved to: $CRON_LOG${NC}"
    echo ""
    echo -e "${GREEN}To view current cron jobs:${NC}"
    echo "crontab -l"
    echo ""
    echo -e "${GREEN}To remove the monitoring cron job:${NC}"
    echo "crontab -l | grep -v '$MONITOR_SCRIPT' | crontab -"
    echo ""
    echo -e "${GREEN}To test the monitoring script manually:${NC}"
    echo "cd $PROJECT_ROOT && source backend/venv_py311/bin/activate && python $MONITOR_SCRIPT"
else
    echo -e "${RED}❌ Failed to install cron job${NC}"
    exit 1
fi 