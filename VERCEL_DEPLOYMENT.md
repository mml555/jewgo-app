# 🚀 Vercel Deployment Guide for JewGo Frontend

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Node.js**: Version 18+ (Vercel will handle this automatically)

## Step 1: Prepare Your Repository

### 1.1 Push to GitHub
```bash
# If not already done, push your code to GitHub
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### 1.2 Verify Configuration Files
- ✅ `next.config.js` - Updated for Vercel
- ✅ `vercel.json` - Deployment configuration
- ✅ `package.json` - Dependencies and scripts

## Step 2: Deploy to Vercel

### 2.1 Connect to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Select the `jewgo-frontend` directory

### 2.2 Configure Environment Variables
In the Vercel dashboard, add these environment variables:

```
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=AIzaSyA12xiUBIe9EJmuP8pEmWgj_Fsv0FkUiqA
NEXT_PUBLIC_BACKEND_URL=https://jewgo.onrender.com
NEXT_PUBLIC_APP_ENV=production
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### 2.3 Deploy Settings
- **Framework Preset**: Next.js
- **Root Directory**: `jewgo-frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

## Step 3: Post-Deployment Configuration

### 3.1 Custom Domain (Optional)
1. In Vercel dashboard, go to your project
2. Click "Settings" → "Domains"
3. Add your custom domain (e.g., `jewgo.com`)

### 3.2 Environment Variables Verification
After deployment, verify these are working:
- Google Maps loading correctly
- API calls to backend working
- Images loading properly

## Step 4: Testing Your Live Site

### 4.1 Test All Features
- ✅ Restaurant search and filtering
- ✅ Interactive maps
- ✅ Favorites functionality
- ✅ Restaurant details pages
- ✅ Mobile responsiveness

### 4.2 Performance Check
- ✅ Page load times
- ✅ Image optimization
- ✅ API response times

## Troubleshooting

### Common Issues

**1. Build Failures**
```bash
# Check build logs in Vercel dashboard
# Common fixes:
npm install
npm run build
```

**2. Environment Variables Not Working**
- Verify variables are set in Vercel dashboard
- Check for typos in variable names
- Ensure `NEXT_PUBLIC_` prefix for client-side variables

**3. API Connection Issues**
- Verify backend URL is correct
- Check CORS settings on backend
- Test API endpoints directly

**4. Google Maps Not Loading**
- Verify API key is correct
- Check API key restrictions
- Ensure billing is enabled for Google Cloud

## Performance Optimization

### 1. Image Optimization
- Vercel automatically optimizes images
- Use Next.js Image component
- Implement lazy loading

### 2. Bundle Optimization
- Code splitting is automatic
- Monitor bundle size in Vercel analytics
- Remove unused dependencies

### 3. Caching
- Vercel provides automatic caching
- Configure cache headers if needed
- Use ISR for static pages

## Monitoring and Analytics

### 1. Vercel Analytics
- Enable in project settings
- Monitor performance metrics
- Track user behavior

### 2. Error Monitoring
- Set up error tracking (Sentry)
- Monitor API failures
- Track user experience issues

## Security Considerations

### 1. Environment Variables
- Never commit API keys to repository
- Use Vercel's secure environment variable storage
- Rotate keys regularly

### 2. API Security
- Implement rate limiting
- Use HTTPS for all API calls
- Validate user inputs

## Next Steps After Deployment

1. **Set up monitoring** and error tracking
2. **Configure custom domain** for branding
3. **Set up analytics** to track user behavior
4. **Implement SEO optimization** for better discoverability
5. **Plan for scaling** as user base grows

## Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Next.js Documentation**: [nextjs.org/docs](https://nextjs.org/docs)
- **JewGo Backend**: Ensure backend is deployed and accessible

---

**🎉 Congratulations! Your JewGo frontend is now live and accessible to users worldwide!** 