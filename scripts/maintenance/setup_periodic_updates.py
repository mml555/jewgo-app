#!/usr/bin/env python3
"""
Setup Periodic Hours Updates
============================

Configure automatic periodic updates for restaurant hours.
Sets up cron jobs and scheduling for keeping hours current.
"""

import os
import sys
import subprocess
from datetime import datetime, timedelta

def create_cron_job():
    """Create a cron job for periodic hours updates."""
    print("🔧 Setting up Cron Job for Periodic Hours Updates")
    print("=" * 60)
    
    # Get the current directory
    current_dir = os.getcwd()
    script_path = os.path.join(current_dir, "scripts/maintenance/periodic_hours_updater.py")
    
    # Check if script exists
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        return False
    
    print(f"✅ Found script: {script_path}")
    
    # Create different cron job options
    cron_options = {
        "1": {
            "name": "Daily Update",
            "schedule": "0 2 * * *",  # 2 AM daily
            "description": "Update restaurants with hours older than 7 days"
        },
        "2": {
            "name": "Weekly Update",
            "schedule": "0 3 * * 0",  # 3 AM every Sunday
            "description": "Update restaurants with hours older than 7 days"
        },
        "3": {
            "name": "Bi-weekly Update",
            "schedule": "0 4 1,15 * *",  # 4 AM on 1st and 15th of month
            "description": "Update restaurants with hours older than 14 days"
        },
        "4": {
            "name": "Monthly Update",
            "schedule": "0 5 1 * *",  # 5 AM on 1st of month
            "description": "Update restaurants with hours older than 30 days"
        }
    }
    
    print("\n📅 Available Cron Job Options:")
    for key, option in cron_options.items():
        print(f"   {key}. {option['name']}")
        print(f"      Schedule: {option['schedule']}")
        print(f"      Description: {option['description']}")
        print()
    
    choice = input("Select cron job option (1-4): ").strip()
    
    if choice not in cron_options:
        print("❌ Invalid choice")
        return False
    
    selected_option = cron_options[choice]
    
    # Create the cron command
    cron_command = f"{selected_option['schedule']} cd {current_dir} && python {script_path} --days 7 >> logs/periodic_hours_update.log 2>&1"
    
    print(f"\n📝 Cron Job Details:")
    print(f"   Name: {selected_option['name']}")
    print(f"   Schedule: {selected_option['schedule']}")
    print(f"   Command: {cron_command}")
    print(f"   Log File: logs/periodic_hours_update.log")
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(current_dir, "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        print(f"✅ Created logs directory: {logs_dir}")
    
    # Ask for confirmation
    confirm = input(f"\n🤔 Create this cron job? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Cron job creation cancelled")
        return False
    
    try:
        # Add the cron job
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        current_crontab = result.stdout
        
        # Check if cron job already exists
        if "periodic_hours_updater.py" in current_crontab:
            print("⚠️  Cron job already exists. Updating...")
            # Remove existing cron job
            lines = current_crontab.split('\n')
            lines = [line for line in lines if "periodic_hours_updater.py" not in line]
            new_crontab = '\n'.join(lines) + '\n' + cron_command + '\n'
        else:
            new_crontab = current_crontab + cron_command + '\n'
        
        # Write new crontab
        subprocess.run(['crontab', '-'], input=new_crontab, text=True, check=True)
        
        print("✅ Cron job created successfully!")
        print(f"📅 Schedule: {selected_option['schedule']}")
        print(f"📝 Log file: logs/periodic_hours_update.log")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating cron job: {e}")
        return False

def create_systemd_service():
    """Create a systemd service for periodic updates."""
    print("\n🔧 Setting up Systemd Service for Periodic Hours Updates")
    print("=" * 60)
    
    current_dir = os.getcwd()
    script_path = os.path.join(current_dir, "scripts/maintenance/periodic_hours_updater.py")
    
    service_content = f"""[Unit]
Description=JewGo Periodic Hours Updater
After=network.target

[Service]
Type=oneshot
User={os.getenv('USER', 'root')}
WorkingDirectory={current_dir}
Environment=GOOGLE_PLACES_API_KEY={os.getenv('GOOGLE_PLACES_API_KEY', '')}
ExecStart=/usr/bin/python3 {script_path} --days 7
StandardOutput=append:/var/log/jewgo-hours-update.log
StandardError=append:/var/log/jewgo-hours-update.log

[Install]
WantedBy=multi-user.target
"""
    
    timer_content = f"""[Unit]
Description=Run JewGo Hours Update Weekly
Requires=jewgo-hours-update.service

[Timer]
OnCalendar=weekly
Persistent=true

[Install]
WantedBy=timers.target
"""
    
    print("📝 Systemd Service Configuration:")
    print(service_content)
    print("\n📝 Systemd Timer Configuration:")
    print(timer_content)
    
    # Ask for confirmation
    confirm = input(f"\n🤔 Create systemd service and timer? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Systemd service creation cancelled")
        return False
    
    try:
        # Write service file
        service_file = "/etc/systemd/system/jewgo-hours-update.service"
        with open(service_file, 'w') as f:
            f.write(service_content)
        
        # Write timer file
        timer_file = "/etc/systemd/system/jewgo-hours-update.timer"
        with open(timer_file, 'w') as f:
            f.write(timer_content)
        
        # Reload systemd and enable timer
        subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
        subprocess.run(['sudo', 'systemctl', 'enable', 'jewgo-hours-update.timer'], check=True)
        subprocess.run(['sudo', 'systemctl', 'start', 'jewgo-hours-update.timer'], check=True)
        
        print("✅ Systemd service and timer created successfully!")
        print(f"📅 Service: jewgo-hours-update.service")
        print(f"⏰ Timer: jewgo-hours-update.timer")
        print(f"📝 Log file: /var/log/jewgo-hours-update.log")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating systemd service: {e}")
        return False

def create_manual_schedule():
    """Create a manual schedule script."""
    print("\n🔧 Creating Manual Schedule Script")
    print("=" * 60)
    
    current_dir = os.getcwd()
    script_path = os.path.join(current_dir, "scripts/maintenance/periodic_hours_updater.py")
    
    schedule_script = f"""#!/bin/bash
# JewGo Periodic Hours Update - Manual Schedule
# Run this script manually or add to your preferred scheduler

cd {current_dir}

# Set environment variables
export GOOGLE_PLACES_API_KEY="{os.getenv('GOOGLE_PLACES_API_KEY', '')}"

# Run the periodic updater
echo "$(date): Starting periodic hours update..." >> logs/periodic_hours_update.log
python3 {script_path} --days 7 >> logs/periodic_hours_update.log 2>&1
echo "$(date): Periodic hours update completed" >> logs/periodic_hours_update.log
"""
    
    schedule_file = os.path.join(current_dir, "scripts/maintenance/run_periodic_update.sh")
    
    with open(schedule_file, 'w') as f:
        f.write(schedule_script)
    
    # Make it executable
    os.chmod(schedule_file, 0o755)
    
    print(f"✅ Manual schedule script created: {schedule_file}")
    print(f"📝 Usage: {schedule_file}")
    print(f"📝 Log file: logs/periodic_hours_update.log")
    
    return True

def show_current_schedule():
    """Show current cron jobs and systemd timers."""
    print("\n📅 Current Schedule Status")
    print("=" * 40)
    
    # Check cron jobs
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        if result.stdout:
            print("📋 Cron Jobs:")
            for line in result.stdout.split('\n'):
                if line.strip() and "periodic_hours_updater.py" in line:
                    print(f"   {line}")
        else:
            print("📋 No cron jobs found")
    except subprocess.CalledProcessError:
        print("📋 No cron jobs found")
    
    # Check systemd timers (Linux only)
    try:
        result = subprocess.run(['systemctl', 'list-timers', 'jewgo-hours-update.timer'], 
                              capture_output=True, text=True)
        if result.stdout and "jewgo-hours-update.timer" in result.stdout:
            print("\n⏰ Systemd Timers:")
            print(result.stdout)
        else:
            print("\n⏰ No systemd timers found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n⏰ Systemd not available (likely macOS)")

def main():
    """Main function to set up periodic updates."""
    print("🚀 JewGo Periodic Hours Update Setup")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not api_key:
        print("❌ GOOGLE_PLACES_API_KEY environment variable not set")
        print("Please set your Google Places API key first:")
        print("export GOOGLE_PLACES_API_KEY='your_api_key_here'")
        return
    
    print(f"✅ API Key found (length: {len(api_key)})")
    
    # Show current schedule
    show_current_schedule()
    
    print("\n🔧 Setup Options:")
    print("1. Create Cron Job (Linux/Mac)")
    print("2. Create Systemd Service & Timer (Linux)")
    print("3. Create Manual Schedule Script")
    print("4. Test Periodic Updater")
    print("5. Exit")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == '1':
        create_cron_job()
    elif choice == '2':
        create_systemd_service()
    elif choice == '3':
        create_manual_schedule()
    elif choice == '4':
        print("\n🧪 Testing Periodic Updater...")
        subprocess.run(['python3', 'scripts/maintenance/periodic_hours_updater.py', '--limit', '3'])
    elif choice == '5':
        print("👋 Setup completed")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main() 