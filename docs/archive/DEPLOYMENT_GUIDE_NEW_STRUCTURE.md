# 🚀 Deployment Guide - New File Structure

## 📋 Overview

This guide provides instructions for deploying the JewGo application with the new organized file structure. The project is now split into separate backend and frontend directories for better deployment management.

## 🏗️ New Structure

```
jewgo-app/
├── backend/                    # Backend API (Render)
│   ├── app.py                 # Main Flask application
│   ├── database/              # Database management
│   ├── scrapers/              # Web scraping services
│   ├── config/                # Configuration files
│   ├── requirements.txt       # Python dependencies
│   ├── runtime.txt            # Python version
│   └── render.yaml            # Render deployment config
├── frontend/                  # Frontend (Vercel)
│   ├── app/                   # Next.js app directory
│   ├── components/            # React components
│   ├── package.json           # Node.js dependencies
│   ├── next.config.js         # Next.js configuration
│   └── vercel.json            # Vercel deployment config
└── docs/                      # Documentation
```

## 🔧 Backend Deployment (Render)

### 1. **Prepare Backend for Deployment**

The backend is configured to deploy to Render with the following files:

- `backend/app.py` - Main Flask application
- `backend/requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification (root directory)
- `render.yaml` - Render deployment configuration (root directory)

### 2. **Environment Variables**

Set the following environment variables in Render:

```bash
DATABASE_URL=postgresql://username:password@host:port/database
ENVIRONMENT=production
PYTHON_VERSION=3.11.9
```

### 3. **Deploy to Render**

1. **Connect Repository**:
   - Go to Render Dashboard
   - Click "New Web Service"
   - Connect your GitHub repository

2. **Configure Service**:
   - **Name**: `jewgo-backend`
   - **Environment**: `Python`
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && gunicorn --config config/gunicorn.conf.py app:app`
   - **Root Directory**: Leave as default (root of repository)

3. **Environment Variables**:
   - Add `DATABASE_URL` with your PostgreSQL connection string
   - Add `ENVIRONMENT=production`

4. **Deploy**:
   - Click "Create Web Service"
   - Render will automatically build and deploy

### 4. **Verify Backend Deployment**

Test the backend API:

```bash
# Health check
curl https://your-render-app.onrender.com/health

# Get restaurants
curl https://your-render-app.onrender.com/api/restaurants

# Get statistics
curl https://your-render-app.onrender.com/api/statistics
```

## 🎨 Frontend Deployment (Vercel)

### 1. **Prepare Frontend for Deployment**

The frontend is configured to deploy to Vercel with the following files:

- `frontend/package.json` - Node.js dependencies and scripts
- `frontend/next.config.js` - Next.js configuration
- `frontend/vercel.json` - Vercel deployment configuration

### 2. **Environment Variables**

Set the following environment variables in Vercel:

```bash
NEXT_PUBLIC_API_URL=https://your-render-app.onrender.com
```

### 3. **Deploy to Vercel**

1. **Connect Repository**:
   - Go to Vercel Dashboard
   - Click "New Project"
   - Import your GitHub repository

2. **Configure Project**:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

3. **Environment Variables**:
   - Add `NEXT_PUBLIC_API_URL` with your backend API URL

4. **Deploy**:
   - Click "Deploy"
   - Vercel will automatically build and deploy

### 4. **Verify Frontend Deployment**

Test the frontend application:

```bash
# Visit your Vercel URL
https://your-vercel-app.vercel.app

# Check API integration
# The frontend should be able to fetch data from your backend
```

## 🔄 Continuous Deployment

### Automatic Deployments

Both Render and Vercel support automatic deployments:

- **Render**: Automatically deploys when you push to the `main` branch
- **Vercel**: Automatically deploys when you push to the `main` branch

### Manual Deployments

To trigger manual deployments:

```bash
# Backend (Render)
git push origin main

# Frontend (Vercel)
git push origin main
```

## 🧪 Testing Deployments

### Backend Testing

```bash
# Health check
curl https://your-render-app.onrender.com/health

# Expected response:
{
  "status": "healthy",
  "database": "connected",
  "restaurants_count": 107,
  "version": "3.0"
}

# API endpoints
curl https://your-render-app.onrender.com/api/restaurants
curl https://your-render-app.onrender.com/api/statistics
curl https://your-render-app.onrender.com/api/kosher-types
```

### Frontend Testing

1. **Visit the application URL**
2. **Check that the frontend loads correctly**
3. **Verify API integration works**
4. **Test search and filtering functionality**

## 🔧 Troubleshooting

### Backend Issues

1. **Database Connection**:
   ```bash
   # Check DATABASE_URL environment variable
   # Verify PostgreSQL database is accessible
   ```

2. **Build Failures**:
   ```bash
   # Check requirements.txt is in backend/ directory
   # Verify Python version in runtime.txt
   ```

3. **Runtime Errors**:
   ```bash
   # Check Render logs for error messages
   # Verify all dependencies are installed
   ```

### Frontend Issues

1. **Build Failures**:
   ```bash
   # Check package.json is in frontend/ directory
   # Verify all dependencies are installed
   ```

2. **API Integration**:
   ```bash
   # Check NEXT_PUBLIC_API_URL environment variable
   # Verify backend is accessible from frontend
   ```

3. **Runtime Errors**:
   ```bash
   # Check Vercel logs for error messages
   # Verify environment variables are set correctly
   ```

## 📊 Monitoring

### Backend Monitoring

- **Render Dashboard**: Monitor application health and logs
- **Health Check Endpoint**: `/health` for automated monitoring
- **Database Monitoring**: Check connection status and performance

### Frontend Monitoring

- **Vercel Dashboard**: Monitor application performance and errors
- **Analytics**: Track user interactions and performance metrics
- **Error Tracking**: Monitor JavaScript errors and API failures

## 🔄 Updates and Maintenance

### Backend Updates

1. **Code Changes**:
   ```bash
   # Make changes in backend/ directory
   git add .
   git commit -m "Update backend functionality"
   git push origin main
   ```

2. **Dependency Updates**:
   ```bash
   # Update requirements.txt
   # Test locally first
   git push origin main
   ```

### Frontend Updates

1. **Code Changes**:
   ```bash
   # Make changes in frontend/ directory
   git add .
   git commit -m "Update frontend functionality"
   git push origin main
   ```

2. **Dependency Updates**:
   ```bash
   # Update package.json
   # Test locally first
   git push origin main
   ```

## 🎯 Best Practices

### Backend

- **Environment Variables**: Never commit sensitive data
- **Database Migrations**: Test migrations locally before deployment
- **Error Handling**: Implement proper error handling and logging
- **Security**: Use HTTPS and implement proper CORS settings

### Frontend

- **Environment Variables**: Use `NEXT_PUBLIC_` prefix for client-side variables
- **Performance**: Optimize images and implement proper caching
- **SEO**: Use proper meta tags and structured data
- **Accessibility**: Ensure WCAG compliance

## 📞 Support

For deployment issues:

1. **Check the logs** in Render/Vercel dashboards
2. **Verify environment variables** are set correctly
3. **Test locally** before deploying
4. **Check documentation** for specific error messages

---

The new file structure provides better separation of concerns and makes deployment more reliable and maintainable! 🚀 