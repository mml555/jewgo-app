# Deployment Guide

## Overview

This guide covers all aspects of deploying the JewGo application, including backend, frontend, and database setup.

## 🚀 Quick Deploy

### Frontend (Vercel)
```bash
cd frontend
npm run build
vercel --prod
```

### Backend (Render)
- Connect GitHub repository to Render
- Set environment variables
- Deploy automatically on push

### Database (Neon)
- Create PostgreSQL database on Neon
- Run migration scripts
- Configure connection strings

## 📋 Prerequisites

- GitHub repository access
- Vercel account (frontend)
- Render account (backend)
- Neon account (database)
- Google Places API key
- Environment variables configured

## 🔧 Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_BACKEND_URL=https://jewgo.onrender.com
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=https://jewgo-app.vercel.app
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### Backend (Render Environment)
```env
DATABASE_URL=postgresql://user:pass@host:port/db
GOOGLE_PLACES_API_KEY=your-api-key
ENVIRONMENT=production
PORT=5000
```

## 📁 Detailed Guides

### [Render Setup](./render-setup.md)
- Backend deployment configuration
- Environment variable setup
- Health check configuration
- Troubleshooting common issues

### [Neon Database](./neon-setup.md)
- Database creation and setup
- Connection string configuration
- Migration scripts
- Backup procedures

### [Troubleshooting](./troubleshooting.md)
- Common deployment issues
- Error resolution
- Performance optimization
- Monitoring setup

## 🔍 Health Checks

### Frontend Health
- URL: `https://jewgo-app.vercel.app/health`
- Expected: 200 OK with status information

### Backend Health
- URL: `https://jewgo.onrender.com/health`
- Expected: JSON response with database status

### Database Health
- Connection test via backend health endpoint
- Expected: Connected status with restaurant count

## 📊 Monitoring

### Uptime Monitoring
- UptimeRobot configured for both frontend and backend
- 5-minute check intervals
- Email notifications on downtime

### Performance Monitoring
- Vercel Analytics for frontend
- Render logs for backend
- Database query performance tracking

## 🔄 Deployment Process

1. **Development**: Make changes locally
2. **Testing**: Test on development environment
3. **Commit**: Push to GitHub main branch
4. **Auto-deploy**: Render and Vercel deploy automatically
5. **Verification**: Check health endpoints
6. **Monitoring**: Monitor for issues

## 🚨 Emergency Procedures

### Rollback Process
1. Revert to previous commit
2. Push to trigger new deployment
3. Verify health endpoints
4. Monitor for stability

### Database Issues
1. Check Neon dashboard
2. Verify connection strings
3. Run health check scripts
4. Contact support if needed

## 📞 Support

- **Render Issues**: Check Render dashboard and logs
- **Vercel Issues**: Check Vercel dashboard and analytics
- **Database Issues**: Check Neon dashboard and connection
- **General Issues**: Review troubleshooting guide

---

*For detailed setup instructions, see individual guide files.* 