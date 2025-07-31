# Monitoring & Health Checks

## Overview

This guide covers comprehensive monitoring setup, health checks, and system status monitoring for the JewGo application.

## 🏥 Health Check System

### Health Check Endpoints

#### Backend Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "restaurants_count": 107,
  "version": "3.0",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "environment": "production",
  "uptime": "running",
  "memory_usage": "normal"
}
```

#### Frontend Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "3.0",
  "build_time": "2024-01-15T10:30:00.000Z",
  "environment": "production"
}
```

### Health Check Scripts

#### Automated Health Monitoring
```bash
# Test all health endpoints
curl https://jewgo.onrender.com/health
curl https://jewgo-app.vercel.app/health

# Run comprehensive health check
python monitoring/health_checks/health-check.js
```

#### Health Check Results
- **Frontend (Vercel)**: ✅ Healthy (1.5s response time)
- **Backend API**: ✅ Healthy (3.7s response time)
- **Database**: ✅ Connected (107 restaurants)
- **Overall System**: ✅ 80% healthy (4/5 services operational)

## 📊 Performance Monitoring

### Response Time Metrics
| Service | Average Response | Status |
|---------|------------------|--------|
| Frontend Load | 1.5s | ✅ Good |
| API Response | 3.7s | ⚠️ Acceptable |
| Database Query | <1s | ✅ Excellent |
| Build Time | ~30s | ✅ Good |

### System Capabilities
- ✅ Restaurant search and filtering
- ✅ Map integration (Google Maps)
- ✅ User authentication system
- ✅ Responsive mobile design
- ✅ Database connectivity
- ✅ CORS configuration

## 🚀 Monitoring Setup

### UptimeRobot Configuration
- **Health Check**: Every 5 minutes
- **Ping**: Every 1 minute
- **Restaurants API**: Every 5 minutes
- **Frontend**: Every 5 minutes

### Alert Settings
- **Down Alert**: ✅ Enabled
- **Response Time Alert**: >10 seconds
- **Error Rate Alert**: >5% errors

### Monitoring Endpoints
```bash
# Health check
curl https://jewgo.onrender.com/health

# Ping endpoint
curl https://jewgo.onrender.com/ping

# API test
curl https://jewgo.onrender.com/api/restaurants?limit=1
```

## 🔧 Setup Instructions

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

## 📈 Performance Optimization

### Recommendations
1. **API Response Optimization**: Consider caching for faster responses
2. **Database Indexing**: Optimize query performance
3. **CDN Integration**: Improve static asset delivery
4. **Error Monitoring**: Implement Sentry for error tracking

### Monitoring Tools
- **UptimeRobot**: Free uptime monitoring
- **Cronitor**: Advanced monitoring with metrics
- **Sentry**: Error tracking and performance monitoring
- **Google Analytics**: User behavior tracking

## 🚨 Troubleshooting

### Common Issues
1. **Health Page Missing**: 404 error on `/health` (not critical)
2. **Slow Response Times**: Backend responses 2-4 seconds
3. **Database Connection**: Verify connection strings
4. **CORS Issues**: Check frontend-backend communication

### Emergency Procedures
1. **Service Down**: Check health endpoints
2. **Database Issues**: Verify connection and restart if needed
3. **Performance Issues**: Review logs and optimize queries
4. **Deployment Issues**: Rollback to previous version

## 📋 Health Check Checklist

### Daily Monitoring
- [ ] All health endpoints responding
- [ ] Response times within acceptable range
- [ ] No critical errors in logs
- [ ] Database connectivity confirmed

### Weekly Monitoring
- [ ] Performance metrics review
- [ ] Error rate analysis
- [ ] System resource usage
- [ ] Backup verification

### Monthly Monitoring
- [ ] Security audit
- [ ] Performance optimization
- [ ] Monitoring configuration review
- [ ] Documentation updates

---

*For detailed setup instructions, see the deployment documentation.* 