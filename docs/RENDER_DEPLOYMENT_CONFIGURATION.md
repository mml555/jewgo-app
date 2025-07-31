# 🚀 Render Deployment Configuration Guide

## 📋 Overview

This guide explains the different ways to configure Render deployment for the JewGo backend application.

## 🔧 Configuration Options

### Option 1: Using render.yaml (Recommended)

**File**: `render.yaml` (root directory)

```yaml
services:
  - type: web
    name: jewgo-backend
    env: python
    plan: free
    buildCommand: |
      cd backend
      pip install -r requirements.txt
    startCommand: |
      cd backend
      gunicorn --config config/gunicorn.conf.py app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.9
      - key: DATABASE_URL
        sync: false
      - key: ENVIRONMENT
        value: production
    healthCheckPath: /health
    autoDeploy: true
```

**Advantages**:
- ✅ Version controlled configuration
- ✅ Automatic deployment setup
- ✅ Clear build and start commands
- ✅ Environment variables defined

### Option 2: Using Procfile (Fallback)

**File**: `Procfile` (root directory)

```
web: cd backend && gunicorn --config config/gunicorn.conf.py app:app
```

**Advantages**:
- ✅ Simple and reliable
- ✅ Works with any Python web framework
- ✅ Render automatically detects and uses it

### Option 3: Manual Configuration in Render Dashboard

**Steps**:
1. Go to Render Dashboard
2. Create new Web Service
3. Connect GitHub repository
4. Configure manually:
   - **Environment**: Python
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && gunicorn --config config/gunicorn.conf.py app:app`
   - **Environment Variables**: Set `DATABASE_URL` and `ENVIRONMENT`

## 📁 Required Files

### Root Directory Files
```
jewgo-app/
├── render.yaml              # Render configuration (Option 1)
├── Procfile                 # Process file (Option 2)
├── requirements.txt         # Python dependencies
├── runtime.txt              # Python version
└── backend/                 # Backend application
    ├── app.py               # Flask application
    ├── requirements.txt     # Backend-specific dependencies
    └── config/
        └── gunicorn.conf.py # Gunicorn configuration
```

### Backend Directory Files
```
backend/
├── app.py                   # Main Flask application
├── requirements.txt         # Backend dependencies
├── config/
│   └── gunicorn.conf.py     # Gunicorn server config
└── database/
    └── database_manager_v3.py
```

## 🔍 Troubleshooting

### Issue: "Could not open requirements file"

**Problem**: Render can't find requirements.txt

**Solutions**:
1. **Option 1**: Use `render.yaml` with custom build command
2. **Option 2**: Place `requirements.txt` in root directory
3. **Option 3**: Configure build command manually in dashboard

### Issue: Service not starting

**Problem**: Application fails to start

**Solutions**:
1. Check start command in `render.yaml` or `Procfile`
2. Verify `backend/app.py` exists and is functional
3. Check environment variables are set correctly

### Issue: Import errors

**Problem**: Python can't find modules

**Solutions**:
1. Ensure all dependencies in `requirements.txt`
2. Check import paths in `backend/app.py`
3. Verify Python version compatibility

## 🎯 Recommended Setup

### For New Deployments

1. **Use `render.yaml`** (Option 1):
   - Provides complete configuration
   - Version controlled
   - Automatic setup

2. **Set Environment Variables**:
   ```bash
   DATABASE_URL=postgresql://username:password@host:port/database
   ENVIRONMENT=production
   ```

3. **Verify Configuration**:
   - Check `render.yaml` syntax
   - Ensure all files exist
   - Test locally before deploying

### For Existing Deployments

1. **Check Current Configuration**:
   - Go to Render Dashboard
   - Review service settings
   - Update if needed

2. **Update Configuration**:
   - Use `render.yaml` for new deployments
   - Keep `Procfile` as fallback
   - Ensure `requirements.txt` in root

## 📊 Deployment Verification

### Health Check
```bash
curl https://your-app.onrender.com/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "database": "connected",
  "restaurants_count": 107,
  "version": "3.0"
}
```

### API Endpoints
```bash
# Get all restaurants
curl https://your-app.onrender.com/api/restaurants

# Get statistics
curl https://your-app.onrender.com/api/statistics

# Get kosher types
curl https://your-app.onrender.com/api/kosher-types
```

## 🔄 Deployment Process

### Automatic Deployment (with render.yaml)
1. Push changes to GitHub
2. Render automatically detects `render.yaml`
3. Uses specified build and start commands
4. Deploys with configured settings

### Manual Deployment
1. Push changes to GitHub
2. Go to Render Dashboard
3. Trigger manual deployment
4. Monitor build logs

## 📝 Best Practices

### Configuration
- ✅ Use `render.yaml` for new deployments
- ✅ Keep `Procfile` as fallback
- ✅ Version control all configuration
- ✅ Test locally before deploying

### Environment Variables
- ✅ Never commit sensitive data
- ✅ Use Render's environment variable system
- ✅ Set `DATABASE_URL` securely
- ✅ Use `ENVIRONMENT=production`

### Monitoring
- ✅ Check health endpoint regularly
- ✅ Monitor build logs for errors
- ✅ Set up alerts for failures
- ✅ Track application performance

## 🚨 Emergency Procedures

### If Deployment Fails
1. Check Render logs for specific errors
2. Verify all required files exist
3. Test configuration locally
4. Update configuration and redeploy

### If Service is Down
1. Check health endpoint
2. Verify database connection
3. Check environment variables
4. Restart service if needed

---

**Current Status**: ✅ All configuration files in place and ready for deployment! 🚀 