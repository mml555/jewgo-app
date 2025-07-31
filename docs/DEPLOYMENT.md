# 🚀 Deployment Guide - JewGo App

This guide will help you deploy the JewGo app to GitHub and Cloudflare Pages.

## 📋 Prerequisites

- GitHub account
- Cloudflare account
- Google Cloud Platform account (for API keys)

## 🔧 Step 1: GitHub Repository Setup

### 1.1 Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon → "New repository"
3. Fill in details:
   - **Repository name**: `jewgo-app`
   - **Description**: `Kosher restaurant discovery app with Next.js frontend and Flask backend`
   - **Visibility**: Public or Private
   - **Don't** initialize with README (we already have one)
4. Click "Create repository"

### 1.2 Push Code to GitHub

```bash
# In your project directory
git remote add origin https://github.com/YOUR_USERNAME/jewgo-app.git
git push -u origin main
```

## 🌐 Step 2: Cloudflare Pages Setup

### 2.1 Connect Repository

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Navigate to **Pages** → **Create a project**
3. Choose **Connect to Git**
4. Select your GitHub account and `jewgo-app` repository
5. Click **Begin setup**

### 2.2 Configure Build Settings

**Project name**: `jewgo-app` (or your preferred name)

**Build settings**:
- **Framework preset**: `Next.js`
- **Build command**: `npm run build`
- **Build output directory**: `out`
- **Root directory**: `jewgo-frontend`

### 2.3 Environment Variables

Add these environment variables in Cloudflare Pages:

```
NODE_ENV=production
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
NEXT_PUBLIC_BACKEND_URL=https://your-backend-url.com
```

### 2.4 Deploy

Click **Save and Deploy**. Cloudflare will build and deploy your app.

## 🔧 Step 3: Backend Deployment

### Option A: Railway (Recommended)

1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub account
3. Create new project → **Deploy from GitHub repo**
4. Select your `jewgo-app` repository
5. Set root directory to `/` (not `/jewgo-frontend`)
6. Add environment variables:
   ```
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key
   GOOGLE_PLACES_API_KEY=your_google_places_api_key
   FLASK_ENV=production
   ```
7. Deploy

### Option B: Render

1. Go to [Render.com](https://render.com)
2. Connect GitHub and select your repository
3. Create new **Web Service**
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Root Directory**: `/` (not `/jewgo-frontend`)
5. Add environment variables
6. Deploy

### Option C: Heroku

1. Install Heroku CLI
2. Create `Procfile` in root:
   ```
   web: python app.py
   ```
3. Deploy:
   ```bash
   heroku create jewgo-backend
   git push heroku main
   ```

## 🔑 Step 4: Google API Setup

### 4.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project or select existing
3. Enable APIs:
   - Maps JavaScript API
   - Places API
   - Geocoding API

### 4.2 Create API Keys

1. Go to **Credentials** → **Create Credentials** → **API Key**
2. Create separate keys for frontend and backend
3. Set restrictions:
   - **Frontend key**: HTTP referrers (your domain)
   - **Backend key**: IP addresses (your server IP)

### 4.3 Update Configuration

Update `jewgo-frontend/next.config.js`:
```javascript
destination: process.env.NODE_ENV === 'production' 
  ? 'https://your-backend-url.com/api/:path*'  // Your actual backend URL
  : 'http://127.0.0.1:8081/api/:path*',
```

## 🔄 Step 5: Update Frontend Configuration

### 5.1 Update API Endpoints

In `jewgo-frontend/next.config.js`, replace `your-backend-url.com` with your actual backend URL.

### 5.2 Commit and Push Changes

```bash
git add .
git commit -m "Update configuration for production deployment"
git push origin main
```

Cloudflare Pages will automatically rebuild and deploy.

## 🌍 Step 6: Custom Domain (Optional)

### 6.1 Add Custom Domain

1. In Cloudflare Pages, go to **Custom domains**
2. Click **Set up a custom domain**
3. Enter your domain (e.g., `jewgo.com`)
4. Follow DNS configuration instructions

### 6.2 SSL Certificate

Cloudflare automatically provides SSL certificates for custom domains.

## 📊 Step 7: Monitoring

### 7.1 Cloudflare Analytics

- View analytics in Cloudflare Pages dashboard
- Monitor performance and errors
- Set up alerts for build failures

### 7.2 Backend Monitoring

- Railway/Render/Heroku provide built-in monitoring
- Set up health checks for your API
- Monitor response times and errors

## 🔧 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check build logs in Cloudflare Pages
   - Verify all dependencies are in `package.json`
   - Ensure environment variables are set

2. **API Connection Issues**
   - Verify backend URL is correct
   - Check CORS settings in backend
   - Ensure API keys are valid

3. **Google Maps Not Loading**
   - Verify API key restrictions
   - Check domain is allowed in Google Cloud Console
   - Ensure Maps JavaScript API is enabled

### Debug Commands

```bash
# Test build locally
cd jewgo-frontend
npm run build

# Test backend locally
python app.py

# Check environment variables
echo $NEXT_PUBLIC_GOOGLE_MAPS_API_KEY
```

## 🎉 Success!

Your JewGo app is now deployed and accessible at:
- **Frontend**: `https://your-app-name.pages.dev`
- **Backend**: `https://your-backend-url.com`

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review Cloudflare Pages build logs
3. Check backend deployment logs
4. Create an issue in the GitHub repository

---

**Happy Deploying! 🚀** 