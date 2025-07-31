# 🔧 Deployment Troubleshooting Guide

## 🚨 Common Deployment Issues and Solutions

### Backend Deployment (Render)

#### Issue: "Could not open requirements file: No such file or directory: 'requirements.txt'"

**Problem**: Render is looking for `requirements.txt` in the root directory, but it's in the `backend/` directory.

**Solution**: ✅ **FIXED**
- `render.yaml` is now in the root directory
- `runtime.txt` is now in the root directory
- Build command: `cd backend && pip install -r requirements.txt`

**Current Configuration**:
```yaml
# render.yaml (root directory)
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
```

#### Issue: Python Version Mismatch

**Problem**: Render is using a different Python version than expected.

**Solution**: ✅ **FIXED**
- `runtime.txt` specifies `python-3.11.9`
- `render.yaml` sets `PYTHON_VERSION: 3.11.9`

#### Issue: Database Connection Failed

**Problem**: Backend can't connect to the database.

**Solution**:
1. Check `DATABASE_URL` environment variable in Render
2. Verify database is accessible from Render's servers
3. Check database credentials and permissions

**Debug Steps**:
```bash
# Check health endpoint
curl https://your-render-app.onrender.com/health

# Expected response:
{
  "status": "healthy",
  "database": "connected",
  "restaurants_count": 107,
  "version": "3.0"
}
```

#### Issue: Import Errors

**Problem**: Python can't find modules.

**Solution**:
1. Verify all dependencies in `backend/requirements.txt`
2. Check import paths in `backend/app.py`
3. Ensure virtual environment is properly set up

### Frontend Deployment (Vercel)

#### Issue: Build Failures

**Problem**: Vercel build fails during npm install or build.

**Solution**:
1. Check `frontend/package.json` for correct dependencies
2. Verify Node.js version in `frontend/.nvmrc`
3. Check for TypeScript compilation errors

**Debug Steps**:
```bash
# Test build locally
cd frontend
npm install
npm run build
```

#### Issue: API Integration Failures

**Problem**: Frontend can't connect to backend API.

**Solution**:
1. Set `NEXT_PUBLIC_API_URL` environment variable in Vercel
2. Verify backend is deployed and accessible
3. Check CORS configuration in backend

**Debug Steps**:
```bash
# Test API endpoint
curl https://your-render-app.onrender.com/api/restaurants

# Check frontend environment variable
echo $NEXT_PUBLIC_API_URL
```

## 🔍 Debugging Commands

### Backend Debugging

```bash
# Check Render logs
# Go to Render Dashboard > Your Service > Logs

# Test health endpoint
curl https://your-render-app.onrender.com/health

# Test API endpoints
curl https://your-render-app.onrender.com/api/restaurants
curl https://your-render-app.onrender.com/api/statistics

# Check database connection
curl https://your-render-app.onrender.com/api/kosher-types
```

### Frontend Debugging

```bash
# Test local build
cd frontend
npm install
npm run build
npm start

# Check environment variables
echo $NEXT_PUBLIC_API_URL

# Test API integration
curl $NEXT_PUBLIC_API_URL/health
```

## 📋 Deployment Checklist

### Before Deploying Backend (Render)

- [ ] `render.yaml` is in root directory
- [ ] `runtime.txt` is in root directory
- [ ] `backend/requirements.txt` exists and is up to date
- [ ] `backend/app.py` exists and is functional
- [ ] `DATABASE_URL` environment variable is set in Render
- [ ] Database is accessible from Render

### Before Deploying Frontend (Vercel)

- [ ] `frontend/package.json` is up to date
- [ ] `frontend/vercel.json` is configured
- [ ] `NEXT_PUBLIC_API_URL` environment variable is set in Vercel
- [ ] Backend is deployed and accessible
- [ ] All TypeScript compilation passes

### After Deployment

- [ ] Backend health check passes
- [ ] Frontend loads without errors
- [ ] API integration works
- [ ] Search functionality works
- [ ] Kosher filtering works

## 🚨 Emergency Rollback

### If Backend Deployment Fails

1. **Check Render logs** for specific error messages
2. **Verify environment variables** are set correctly
3. **Test locally** to ensure code works
4. **Redeploy** with fixes

### If Frontend Deployment Fails

1. **Check Vercel logs** for build errors
2. **Test build locally** with `npm run build`
3. **Verify environment variables** are set
4. **Redeploy** with fixes

## 📞 Support Resources

### Render Documentation
- [Render Python Deployment](https://render.com/docs/deploy-python-app)
- [Render Environment Variables](https://render.com/docs/environment-variables)
- [Render Troubleshooting](https://render.com/docs/troubleshooting-deploys)

### Vercel Documentation
- [Vercel Next.js Deployment](https://vercel.com/docs/deployments)
- [Vercel Environment Variables](https://vercel.com/docs/environment-variables)
- [Vercel Troubleshooting](https://vercel.com/docs/troubleshooting)

### Project Documentation
- `docs/DEPLOYMENT_GUIDE_NEW_STRUCTURE.md` - Complete deployment guide
- `docs/DEVELOPMENT_GUIDE.md` - Development setup guide
- `FINAL_VERIFICATION_SUMMARY.md` - Project verification summary

## 🎯 Quick Fixes

### Most Common Issues

1. **Missing requirements.txt**: Ensure `backend/requirements.txt` exists
2. **Wrong Python version**: Check `runtime.txt` and `render.yaml`
3. **Database connection**: Verify `DATABASE_URL` environment variable
4. **API integration**: Check `NEXT_PUBLIC_API_URL` environment variable
5. **Build failures**: Test locally before deploying

### File Structure Verification

```bash
# Root directory should have:
render.yaml
runtime.txt
backend/
frontend/
docs/

# Backend directory should have:
backend/requirements.txt
backend/app.py
backend/config/gunicorn.conf.py

# Frontend directory should have:
frontend/package.json
frontend/vercel.json
frontend/next.config.js
```

---

**Remember**: Always test locally before deploying, and check the logs for specific error messages! 🔧 