# 🚀 JewGo Backend Production Deployment Guide

## 📋 **Overview**

This guide covers deploying the JewGo Flask backend to production with PostgreSQL database support, enhanced security, and monitoring.

## 🏗️ **Architecture**

### **Recommended Stack:**
- **Backend:** Flask + Gunicorn
- **Database:** PostgreSQL (Neon, Supabase, Railway)
- **Hosting:** Render, Railway, or Fly.io
- **Monitoring:** Sentry (optional)

## 🔧 **Pre-Deployment Setup**

### **1. Database Setup**

#### **Option A: Neon (Recommended)**
```bash
# 1. Create account at neon.tech
# 2. Create new project
# 3. Get connection string
DATABASE_URL=postgresql://username:password@host.neon.tech:5432/database_name
```

#### **Option B: Supabase**
```bash
# 1. Create account at supabase.com
# 2. Create new project
# 3. Get connection string from Settings > Database
DATABASE_URL=postgresql://postgres:password@host.supabase.co:5432/postgres
```

#### **Option C: Railway**
```bash
# 1. Create account at railway.app
# 2. Create new project
# 3. Add PostgreSQL service
# 4. Get connection string from Variables tab
```

### **2. Environment Configuration**

Copy `env.production.example` to `.env.production` and configure:

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_SECRET_KEY=your-super-secret-production-key-here

# Database (use your actual PostgreSQL URL)
DATABASE_URL=postgresql://username:password@host:port/database_name

# CORS (add your frontend domain)
CORS_ORIGINS=https://jewgo.com,https://www.jewgo.com

# Google API Keys
GOOGLE_PLACES_API_KEY=your-google-places-api-key
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

## 🚀 **Deployment Options**

### **Option 1: Render (Recommended)**

#### **Setup:**
1. **Create Render Account:** [render.com](https://render.com)
2. **Connect GitHub Repository**
3. **Create New Web Service**

#### **Configuration:**
```yaml
# render.yaml
services:
  - type: web
    name: jewgo-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app_production:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: jewgo-db
          property: connectionString
      - key: FLASK_SECRET_KEY
        generateValue: true
      - key: CORS_ORIGINS
        value: https://jewgo.com,https://www.jewgo.com
      - key: GOOGLE_PLACES_API_KEY
        sync: false
      - key: GOOGLE_MAPS_API_KEY
        sync: false

databases:
  - name: jewgo-db
    databaseName: jewgo
    user: jewgo_user
```

#### **Environment Variables in Render Dashboard:**
- `FLASK_ENV`: `production`
- `DATABASE_URL`: (auto-generated from PostgreSQL service)
- `FLASK_SECRET_KEY`: (auto-generated)
- `CORS_ORIGINS`: `https://jewgo.com,https://www.jewgo.com`
- `GOOGLE_PLACES_API_KEY`: Your Google Places API key
- `GOOGLE_MAPS_API_KEY`: Your Google Maps API key

### **Option 2: Railway**

#### **Setup:**
1. **Create Railway Account:** [railway.app](https://railway.app)
2. **Connect GitHub Repository**
3. **Add PostgreSQL Service**
4. **Add Web Service**

#### **Configuration:**
```json
// railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app_production:app",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

### **Option 3: Fly.io**

#### **Setup:**
1. **Install Fly CLI:** `curl -L https://fly.io/install.sh | sh`
2. **Login:** `fly auth login`
3. **Create App:** `fly launch`

#### **Configuration:**
```toml
# fly.toml
app = "jewgo-api"
primary_region = "iad"

[build]

[env]
  FLASK_ENV = "production"
  PORT = "8081"

[http_service]
  internal_port = 8081
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[http_service.checks]]
  grace_period = "10s"
  interval = "30s"
  method = "GET"
  timeout = "5s"
  path = "/health"
```

## 🔒 **Security Configuration**

### **1. CORS Setup**
```python
# Ensure your frontend domain is in CORS_ORIGINS
CORS_ORIGINS=https://jewgo.com,https://www.jewgo.com,https://app.jewgo.com
```

### **2. Rate Limiting**
```python
# Configured in config.py
RATELIMIT_DEFAULT = "200 per day;50 per hour;10 per minute"
```

### **3. Environment Variables**
- ✅ **Never commit secrets to Git**
- ✅ **Use platform environment variables**
- ✅ **Rotate keys regularly**

## 📊 **Monitoring & Logging**

### **1. Structured Logging**
The app uses `structlog` for JSON-formatted logs:
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "info",
  "message": "Restaurant search completed",
  "query": "kosher",
  "results_count": 25
}
```

### **2. Health Checks**
```bash
# Test health endpoint
curl https://your-api-domain.com/health
```

### **3. Sentry Integration (Optional)**
```python
# Add to requirements.txt
sentry-sdk[flask]==1.32.0

# Add to app_production.py
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.1,
    environment=os.environ.get('FLASK_ENV', 'development')
)
```

## 🗄️ **Database Migration**

### **1. Initial Setup**
```bash
# Install Alembic
pip install alembic

# Initialize migrations
alembic init migrations

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Run migration
alembic upgrade head
```

### **2. Data Migration from SQLite**
```python
# migration_script.py
from database_manager import DatabaseManager as OldDB
from database_manager_v2 import EnhancedDatabaseManager as NewDB

def migrate_data():
    old_db = OldDB()
    new_db = EnhancedDatabaseManager()
    
    if old_db.connect() and new_db.connect():
        restaurants = old_db.search_restaurants(limit=1000)
        
        for restaurant in restaurants:
            new_db.add_restaurant(restaurant)
        
        print(f"Migrated {len(restaurants)} restaurants")
```

## 🧪 **Testing**

### **1. Local Testing**
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment
export FLASK_ENV=production
export DATABASE_URL=your_postgresql_url

# Run tests
pytest tests/

# Test API locally
python app_production.py
```

### **2. API Testing**
```bash
# Test endpoints
curl https://your-api-domain.com/
curl https://your-api-domain.com/api/restaurants
curl https://your-api-domain.com/health
```

## 📈 **Performance Optimization**

### **1. Database Indexing**
```sql
-- Add indexes for better performance
CREATE INDEX idx_restaurants_status ON restaurants(status);
CREATE INDEX idx_restaurants_location ON restaurants(latitude, longitude);
CREATE INDEX idx_restaurants_category ON restaurants(listing_type);
CREATE INDEX idx_restaurants_agency ON restaurants(certifying_agency);
```

### **2. Connection Pooling**
```python
# Configured in database_manager_v2.py
engine = create_engine(
    database_url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

### **3. Caching (Optional)**
```python
# Add Redis caching
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379'})
cache.init_app(app)

@app.route('/api/statistics')
@cache.cached(timeout=300)  # Cache for 5 minutes
def api_statistics():
    # ... existing code
```

## 🔄 **CI/CD Pipeline**

### **GitHub Actions Example**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
      
      - name: Run tests
        run: pytest tests/
      
      - name: Deploy to Render
        env:
          RENDER_TOKEN: ${{ secrets.RENDER_TOKEN }}
        run: |
          curl -X POST "https://api.render.com/v1/services/$SERVICE_ID/deploys" \
            -H "Authorization: Bearer $RENDER_TOKEN" \
            -H "Content-Type: application/json"
```

## 🚨 **Troubleshooting**

### **Common Issues:**

1. **Database Connection Failed**
   - Check `DATABASE_URL` format
   - Verify database credentials
   - Check network connectivity

2. **CORS Errors**
   - Verify `CORS_ORIGINS` includes your frontend domain
   - Check for trailing slashes in URLs

3. **Rate Limiting**
   - Monitor rate limit headers in responses
   - Adjust limits in `config.py` if needed

4. **Memory Issues**
   - Monitor memory usage in platform dashboard
   - Adjust worker count in `gunicorn.conf.py`

### **Logs & Debugging:**
```bash
# View application logs
# Render: Dashboard > Logs
# Railway: Dashboard > Deployments > Logs
# Fly.io: fly logs

# Test database connection
python -c "
from database_manager_v2 import EnhancedDatabaseManager
db = EnhancedDatabaseManager()
print('Connected:', db.connect())
"
```

## 📞 **Support**

For deployment issues:
1. Check platform-specific documentation
2. Review application logs
3. Test endpoints with curl/Postman
4. Verify environment variables

---

**🎉 Your JewGo backend is now production-ready with PostgreSQL, enhanced security, and monitoring!** 