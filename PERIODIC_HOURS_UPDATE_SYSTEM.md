# Periodic Hours Update System

## 🎯 Overview

The Periodic Hours Update System automatically keeps restaurant hours current by regularly checking and updating them according to Google Places data. This ensures that users always see accurate, up-to-date opening hours.

## 🔧 System Components

### 1. **Periodic Hours Updater** (`scripts/maintenance/periodic_hours_updater.py`)
- Main script that performs periodic hours updates
- Checks restaurants with old hours data (configurable age)
- Updates hours from Google Places API
- Handles quota management and error recovery
- Provides detailed reporting and logging

### 2. **Setup Script** (`scripts/maintenance/setup_periodic_updates.py`)
- Configures automatic scheduling (cron jobs, systemd timers)
- Creates manual schedule scripts
- Manages different scheduling options

### 3. **Scheduling Options**
- **Cron Jobs**: Traditional Unix/Linux scheduling
- **Systemd Timers**: Modern Linux service scheduling
- **Manual Scripts**: Custom scheduling solutions

## 🚀 Features

### **Smart Update Logic**
- Updates restaurants with hours older than specified days (default: 7 days)
- Prioritizes restaurants without hours over those with old hours
- Tracks when hours were last updated
- Detects if hours have actually changed

### **Additional Data Updates**
- Updates phone numbers from Google Places
- Updates website URLs from Google Places
- Updates ratings from Google Places
- Maintains data freshness across multiple fields

### **Quota Management**
- Tracks daily API usage
- Respects Google Places API limits
- Graceful handling of quota exhaustion
- Configurable rate limiting (200ms between requests)

### **Error Handling**
- Comprehensive error logging
- Graceful handling of missing restaurants
- API error recovery
- Database transaction safety

## 📊 Update Logic

### **Restaurant Selection Criteria**
```sql
-- Restaurants without hours
(hours_open IS NULL OR hours_open = '' OR hours_open = 'None')

-- OR restaurants with old hours
updated_at < NOW() - INTERVAL '7 days'
```

### **Priority Order**
1. **High Priority**: Restaurants without any hours data
2. **Medium Priority**: Restaurants with hours older than specified days
3. **Low Priority**: Restaurants with recent hours data

### **Update Frequency Options**
- **Daily**: Update restaurants with hours older than 7 days
- **Weekly**: Update restaurants with hours older than 7 days
- **Bi-weekly**: Update restaurants with hours older than 14 days
- **Monthly**: Update restaurants with hours older than 30 days

## 🔧 Usage

### **Command Line Options**
```bash
# Basic usage (update restaurants with hours older than 7 days)
python scripts/maintenance/periodic_hours_updater.py

# Custom days threshold
python scripts/maintenance/periodic_hours_updater.py --days 14

# Limit number of restaurants processed
python scripts/maintenance/periodic_hours_updater.py --limit 50

# Interactive mode
python scripts/maintenance/periodic_hours_updater.py --interactive
```

### **Interactive Mode Options**
1. **Update restaurants with old hours (default: 7 days)**
2. **Update restaurants with old hours (custom days)**
3. **Update all restaurants without hours**
4. **Update with limit**
5. **Check quota status**

## 📅 Scheduling Setup

### **Option 1: Cron Jobs (Linux/Mac)**
```bash
# Run setup script
python scripts/maintenance/setup_periodic_updates.py

# Choose option 1 (Create Cron Job)
# Select frequency: Daily, Weekly, Bi-weekly, or Monthly
```

**Example Cron Jobs:**
```bash
# Daily at 2 AM
0 2 * * * cd /path/to/jewgo && python scripts/maintenance/periodic_hours_updater.py --days 7 >> logs/periodic_hours_update.log 2>&1

# Weekly on Sunday at 3 AM
0 3 * * 0 cd /path/to/jewgo && python scripts/maintenance/periodic_hours_updater.py --days 7 >> logs/periodic_hours_update.log 2>&1

# Monthly on 1st at 5 AM
0 5 1 * * cd /path/to/jewgo && python scripts/maintenance/periodic_hours_updater.py --days 30 >> logs/periodic_hours_update.log 2>&1
```

### **Option 2: Systemd Timers (Linux)**
```bash
# Run setup script
python scripts/maintenance/setup_periodic_updates.py

# Choose option 2 (Create Systemd Service & Timer)
```

**Systemd Service File:**
```ini
[Unit]
Description=JewGo Periodic Hours Updater
After=network.target

[Service]
Type=oneshot
User=your_user
WorkingDirectory=/path/to/jewgo
Environment=GOOGLE_PLACES_API_KEY=your_api_key
ExecStart=/usr/bin/python3 scripts/maintenance/periodic_hours_updater.py --days 7
StandardOutput=append:/var/log/jewgo-hours-update.log
StandardError=append:/var/log/jewgo-hours-update.log

[Install]
WantedBy=multi-user.target
```

**Systemd Timer File:**
```ini
[Unit]
Description=Run JewGo Hours Update Weekly
Requires=jewgo-hours-update.service

[Timer]
OnCalendar=weekly
Persistent=true

[Install]
WantedBy=timers.target
```

### **Option 3: Manual Schedule Script**
```bash
# Run setup script
python scripts/maintenance/setup_periodic_updates.py

# Choose option 3 (Create Manual Schedule Script)
```

**Generated Script:**
```bash
#!/bin/bash
# JewGo Periodic Hours Update - Manual Schedule

cd /path/to/jewgo
export GOOGLE_PLACES_API_KEY="your_api_key"

echo "$(date): Starting periodic hours update..." >> logs/periodic_hours_update.log
python3 scripts/maintenance/periodic_hours_updater.py --days 7 >> logs/periodic_hours_update.log 2>&1
echo "$(date): Periodic hours update completed" >> logs/periodic_hours_update.log
```

## 📊 Monitoring & Logging

### **Log Files**
- **Cron/Manual**: `logs/periodic_hours_update.log`
- **Systemd**: `/var/log/jewgo-hours-update.log`

### **Log Format**
```json
{
  "event": "Processing periodic update for: Restaurant Name",
  "logger": "__main__",
  "level": "info",
  "timestamp": "2025-07-31T14:00:00.000000Z",
  "id": 123,
  "existing_hours": true,
  "last_updated": "2025-07-24T10:30:00.000000Z"
}
```

### **Monitoring Commands**
```bash
# Check cron jobs
crontab -l

# Check systemd timers
systemctl list-timers jewgo-hours-update.timer

# View recent logs
tail -f logs/periodic_hours_update.log

# Check systemd logs
journalctl -u jewgo-hours-update.service
```

## 📈 Results & Reporting

### **Update Results Structure**
```python
{
    'total_processed': 50,
    'updated': 35,
    'not_found': 10,
    'no_hours': 3,
    'errors': 2,
    'skipped': 0,
    'quota_exceeded': False,
    'daily_requests': 100,
    'results': [
        {
            'restaurant_id': 123,
            'restaurant_name': 'Restaurant Name',
            'status': 'updated',
            'reason': 'hours_updated_successfully',
            'hours_updated': True,
            'hours_changed': True,
            'old_hours': 'Mon 9:00 AM – 5:00 PM',
            'new_hours': 'Mon 8:00 AM – 6:00 PM',
            'additional_data_updated': True
        }
    ]
}
```

### **Status Types**
- **updated**: Hours successfully updated
- **not_found**: Restaurant not found in Google Places
- **no_hours**: No hours available in Google Places
- **error**: Error occurred during processing
- **skipped**: Restaurant skipped (missing data, quota limit)

## 🔧 Configuration

### **Environment Variables**
```bash
GOOGLE_PLACES_API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:pass@host:port/db
```

### **Default Settings**
- **Days threshold**: 7 days
- **Rate limiting**: 200ms between requests
- **Daily quota limit**: 100,000 requests
- **Logging**: JSON format with timestamps

### **Customization**
```python
# Modify in periodic_hours_updater.py
self.max_daily_requests = 100000  # Adjust quota limit
self.min_request_interval = 0.2   # Adjust rate limiting
```

## 🎯 Benefits

### **For Users**
- **Always Current**: Hours data stays up-to-date
- **Accurate Information**: Real-time data from Google Places
- **Better Planning**: Reliable opening hours for planning

### **For System**
- **Automated Maintenance**: No manual intervention required
- **Data Freshness**: Regular updates ensure accuracy
- **Scalable**: Handles any number of restaurants
- **Cost Effective**: Efficient API usage with quota management

### **For Business**
- **Improved UX**: Better user experience with accurate hours
- **Reduced Support**: Fewer complaints about incorrect hours
- **Competitive Advantage**: Most current restaurant information

## 🚨 Troubleshooting

### **Common Issues**

1. **Quota Exceeded**
   ```bash
   # Check current usage
   python scripts/maintenance/periodic_hours_updater.py --interactive
   # Choose option 5 (Check quota status)
   ```

2. **API Key Issues**
   ```bash
   # Test API key
   python scripts/maintenance/test_api_key_status.py
   ```

3. **Database Connection Issues**
   ```bash
   # Check database connection
   python scripts/maintenance/check_hours_status.py
   ```

4. **Scheduling Issues**
   ```bash
   # Check cron jobs
   crontab -l
   
   # Check systemd timers
   systemctl list-timers
   ```

### **Log Analysis**
```bash
# Check for errors
grep "error" logs/periodic_hours_update.log

# Check update statistics
grep "updated" logs/periodic_hours_update.log | wc -l

# Check quota usage
grep "daily_requests" logs/periodic_hours_update.log | tail -1
```

## 🔄 Maintenance

### **Regular Tasks**
1. **Monitor Logs**: Check for errors and quota usage
2. **Review Results**: Analyze update success rates
3. **Adjust Frequency**: Modify update frequency based on needs
4. **Update API Key**: Renew API key when needed

### **Performance Optimization**
1. **Adjust Days Threshold**: Balance freshness vs. API usage
2. **Batch Processing**: Process restaurants in optimal batches
3. **Caching**: Implement caching for frequently accessed data
4. **Parallel Processing**: Consider parallel updates for large datasets

## 📋 Best Practices

### **Scheduling**
- Run during low-traffic hours (2-5 AM)
- Use appropriate frequency for your data needs
- Monitor and adjust based on results

### **Monitoring**
- Set up log monitoring and alerts
- Track API usage and costs
- Monitor update success rates

### **Maintenance**
- Regular log rotation
- Database backup before major updates
- API key rotation and security

---

## 🎉 Conclusion

The Periodic Hours Update System provides a robust, automated solution for keeping restaurant hours current. With flexible scheduling options, comprehensive monitoring, and intelligent update logic, it ensures that users always have access to accurate, up-to-date opening hours information.

**The system is production-ready and will significantly improve the JewGo application's data quality and user experience!** 