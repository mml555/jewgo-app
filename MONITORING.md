# API Monitoring Setup Guide

This guide explains how to set up comprehensive monitoring for the JewGo API using UptimeRobot and Cronitor to detect and alert on API downtime.

## 🎯 Overview

The monitoring system includes:
- **Health Check Endpoint**: `/health` - Comprehensive API health status
- **Ping Endpoint**: `/ping` - Simple uptime monitoring
- **UptimeRobot**: Free uptime monitoring service
- **Cronitor**: Advanced monitoring with detailed metrics

## 🔧 Enhanced Health Check Endpoint

### `/health` Endpoint
Returns comprehensive health status including:
- Database connectivity
- Database query testing
- API version and environment
- Monitoring readiness status

**Response Example:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "version": "1.0.0",
  "environment": "production",
  "database": {
    "status": "connected",
    "test_passed": true,
    "type": "PostgreSQL"
  },
  "uptime": "running",
  "memory_usage": "normal",
  "monitoring": {
    "uptimerobot": "ready",
    "cronitor": "ready"
  }
}
```

### `/ping` Endpoint
Simple endpoint for basic uptime monitoring:
```json
{
  "pong": true,
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

## 🚀 Quick Setup

### 1. Test Your Endpoints
```bash
# Test health check
curl https://jewgo.onrender.com/health

# Test ping
curl https://jewgo.onrender.com/ping

# Test restaurants endpoint
curl https://jewgo.onrender.com/api/restaurants?limit=1
```

### 2. Automated Setup
```bash
# Install dependencies
pip install requests

# Test endpoints
python monitoring/setup_monitoring.py --test

# Set up UptimeRobot (requires API key)
export UPTIMEROBOT_API_KEY=your_api_key
python monitoring/setup_monitoring.py --uptimerobot

# Set up Cronitor (requires API key)
export CRONITOR_API_KEY=your_api_key
python monitoring/setup_monitoring.py --cronitor
```

## 📊 UptimeRobot Setup

### Free Account Setup
1. **Create Account**: Go to [uptimerobot.com](https://uptimerobot.com)
2. **Get API Key**: Account Settings → API
3. **Set Environment Variable**:
   ```bash
   export UPTIMEROBOT_API_KEY=your_api_key
   ```

### Monitor Configuration
- **Health Check**: Every 5 minutes
- **Ping**: Every 1 minute
- **Restaurants API**: Every 5 minutes
- **Frontend**: Every 5 minutes

### Alert Settings
- **Down Alert**: ✅ Enabled
- **Up Alert**: ✅ Enabled
- **Retry Alert**: ❌ Disabled
- **Maintenance Windows**: Sunday 2:00-4:00 AM

## 📈 Cronitor Setup

### Account Setup
1. **Create Account**: Go to [cronitor.io](https://cronitor.io)
2. **Get API Key**: Account Settings → API
3. **Set Environment Variable**:
   ```bash
   export CRONITOR_API_KEY=your_api_key
   ```

### Advanced Features
- **Response Time Monitoring**: Alert if > 5 seconds
- **Error Rate Monitoring**: Alert if > 5%
- **Grace Period**: 5 minutes before alerting
- **Grouping**: Monitors grouped by service

### Notification Channels
- **Email**: admin@jewgo.com, alerts@jewgo.com
- **Slack**: #jewgo-alerts channel
- **Webhooks**: Custom integrations

## 🔍 Manual Monitor Creation

If automated setup fails, create these monitors manually:

### 1. JewGo API Health Check
- **URL**: `https://jewgo.onrender.com/health`
- **Expected Status**: 200
- **Expected Response**: `{"status": "healthy"}`
- **Interval**: 5 minutes
- **Timeout**: 30 seconds

### 2. JewGo API Ping
- **URL**: `https://jewgo.onrender.com/ping`
- **Expected Status**: 200
- **Expected Response**: `{"pong": true}`
- **Interval**: 1 minute
- **Timeout**: 10 seconds

### 3. JewGo API Restaurants
- **URL**: `https://jewgo.onrender.com/api/restaurants?limit=1`
- **Expected Status**: 200
- **Expected Response**: `{"success": true}`
- **Interval**: 5 minutes
- **Timeout**: 30 seconds

### 4. JewGo Frontend
- **URL**: `https://jewgo.com`
- **Expected Status**: 200
- **Interval**: 5 minutes
- **Timeout**: 30 seconds

## 🚨 Alert Configuration

### Email Alerts
- **Primary**: admin@jewgo.com
- **Secondary**: alerts@jewgo.com
- **Format**: Include monitor name, URL, and status

### Slack Integration
- **Channel**: #jewgo-alerts
- **Webhook**: Configure in Slack app settings
- **Format**: Rich notifications with status and links

### Escalation Policy
1. **Immediate**: Email to admin@jewgo.com
2. **5 minutes**: Slack notification
3. **15 minutes**: Email to alerts@jewgo.com
4. **30 minutes**: Escalate to on-call team

## 📊 Monitoring Dashboard

### Key Metrics to Track
- **Uptime Percentage**: Target > 99.9%
- **Response Time**: Target < 2 seconds
- **Error Rate**: Target < 0.1%
- **Database Health**: Always connected
- **API Endpoints**: All responding

### Dashboard Setup
1. **UptimeRobot Dashboard**: Built-in dashboard
2. **Cronitor Dashboard**: Advanced metrics and graphs
3. **Custom Dashboard**: Integrate with Grafana/Prometheus

## 🔧 Maintenance Windows

### Scheduled Maintenance
- **Day**: Sunday
- **Time**: 2:00 AM - 4:00 AM EST
- **Duration**: 2 hours
- **Notifications**: Disabled during maintenance

### Emergency Maintenance
- **Process**: Manual pause of monitors
- **Notification**: Email to admin@jewgo.com
- **Resume**: Manual restart of monitors

## 🛠️ Troubleshooting

### Common Issues

#### Health Check Failing
```bash
# Check database connection
curl https://jewgo.onrender.com/health | jq '.database'

# Check API logs
# Look for database connection errors
```

#### Monitor Not Responding
```bash
# Test endpoint directly
curl -v https://jewgo.onrender.com/health

# Check response time
time curl https://jewgo.onrender.com/health
```

#### False Positives
- **Adjust timeout**: Increase from 30s to 60s
- **Add retries**: Configure 2-3 retries
- **Check maintenance windows**: Ensure not during maintenance

### Debug Commands
```bash
# Test all endpoints
python monitoring/setup_monitoring.py --test

# Check monitor status
curl https://api.uptimerobot.com/v2/getMonitors

# View recent alerts
# Check email and Slack for recent notifications
```

## 📈 Performance Optimization

### Response Time Optimization
- **Database Queries**: Optimize health check queries
- **Caching**: Implement response caching
- **CDN**: Use CDN for static assets

### Monitoring Optimization
- **Reduce Frequency**: Increase intervals for stable endpoints
- **Smart Alerts**: Use conditional alerting
- **Batch Monitoring**: Group related endpoints

## 🔐 Security Considerations

### API Security
- **Rate Limiting**: Health endpoints have higher limits
- **Authentication**: Consider API keys for sensitive endpoints
- **HTTPS**: All endpoints use HTTPS

### Monitoring Security
- **API Keys**: Store securely, rotate regularly
- **Webhooks**: Use signed webhooks for Slack
- **Access Control**: Limit dashboard access

## 📞 Support

### Getting Help
- **UptimeRobot Support**: [support.uptimerobot.com](https://support.uptimerobot.com)
- **Cronitor Support**: [cronitor.io/support](https://cronitor.io/support)
- **Internal Support**: admin@jewgo.com

### Documentation
- **UptimeRobot API**: [uptimerobot.com/api](https://uptimerobot.com/api)
- **Cronitor API**: [cronitor.io/docs/api](https://cronitor.io/docs/api)
- **This Guide**: Update as needed

---

**Last Updated**: January 2024
**Version**: 1.0.0 