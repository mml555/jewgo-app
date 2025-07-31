#!/bin/bash
# JewGo Periodic Hours Update - Manual Schedule
# Run this script manually or add to your preferred scheduler

cd "/Users/mendell/jewgo app"

# Set environment variables
export GOOGLE_PLACES_API_KEY="AIzaSyA12xiUBIe9EJmuP8pEmWgj_Fsv0FkUiqA"

# Create logs directory if it doesn't exist
mkdir -p logs

# Run the periodic updater
echo "$(date): Starting periodic hours update..." >> logs/periodic_hours_update.log
python3 scripts/maintenance/periodic_hours_updater.py --days 7 >> logs/periodic_hours_update.log 2>&1
echo "$(date): Periodic hours update completed" >> logs/periodic_hours_update.log
