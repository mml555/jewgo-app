# Troubleshooting Guide

This guide helps you resolve common issues with the JewGo application.

## Google Maps API Issues

### Error: "Google Maps failed to load within 10 seconds"

**Cause**: Missing or invalid Google Maps API key, or network connectivity issues.

**Solutions**:

1. **Check your environment variables**:
   ```bash
   npm run check-env
   ```

2. **Set up Google Maps API key**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the following APIs:
     - Maps JavaScript API
     - Places API
     - Geocoding API
   - Create credentials (API key)
   - Add the API key to your `.env.local` file:
     ```
     NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_api_key_here
     ```

3. **Verify API key restrictions**:
   - Ensure your API key has the correct restrictions
   - For development: Allow all referrers or add `localhost:3000`
   - For production: Add your domain to allowed referrers

4. **Check network connectivity**:
   - Ensure you have a stable internet connection
   - Try accessing https://maps.googleapis.com in your browser

### Error: "Google Maps API key is missing"

**Cause**: The `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY` environment variable is not set.

**Solution**:
1. Create a `.env.local` file in the frontend directory
2. Add your Google Maps API key:
   ```
   NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_api_key_here
   ```
3. Restart your development server

## Location Permission Issues

### App doesn't prompt for location access

**Cause**: The browser may have blocked location access or the prompt isn't showing.

**Solutions**:

1. **Check browser location settings**:
   - Chrome: Settings > Privacy and security > Site Settings > Location
   - Firefox: Settings > Privacy & Security > Permissions > Location
   - Safari: Preferences > Websites > Location

2. **Reset location permissions**:
   - Clear browser data for your site
   - Refresh the page
   - The location prompt should appear immediately when the page loads

3. **Manual location request**:
   - Click the "Near Me" filter in the action buttons
   - This will trigger a location request

4. **Reset location permission in the app**:
   - If you previously denied location access, the app remembers this
   - Use the location reset feature in the action buttons to show the prompt again

### Location access denied

**Cause**: User denied location permission or browser blocked it.

**Solutions**:

1. **Enable location in browser settings**:
   - Look for the location icon in the address bar
   - Click it and select "Allow"

2. **Reset site permissions**:
   - Clear site data and cookies
   - Refresh the page

3. **Use manual location input**:
   - The app works without location access
   - You can manually search for restaurants by name or address

## Environment Setup Issues

### Missing environment variables

**Solution**:
1. Run the environment check:
   ```bash
   npm run check-env
   ```

2. Create a `.env.local` file with required variables:
   ```
   NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   NEXT_PUBLIC_BACKEND_URL=https://jewgo.onrender.com
   NEXTAUTH_URL=https://jewgo-app.vercel.app
   NEXTAUTH_SECRET=your_nextauth_secret_here
   ```

### Development server won't start

**Solutions**:

1. **Check Node.js version**:
   ```bash
   node --version
   ```
   Ensure you're using Node.js 18.x or higher

2. **Clear Next.js cache**:
   ```bash
   rm -rf .next
   npm run dev
   ```

3. **Reinstall dependencies**:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

## Performance Issues

### Slow loading times

**Solutions**:

1. **Check network connectivity**
2. **Clear browser cache**
3. **Disable browser extensions** that might interfere
4. **Use production build**:
   ```bash
   npm run build
   npm start
   ```

### Maps not loading properly

**Solutions**:

1. **Check console for errors**
2. **Verify API key is valid**
3. **Check API quota usage** in Google Cloud Console
4. **Try incognito/private browsing mode**

## Browser Compatibility

### Supported browsers:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Known issues:
- Some features may not work in older browsers
- Location services require HTTPS in production

## Getting Help

If you're still experiencing issues:

1. **Check the browser console** for error messages
2. **Run the environment check**: `npm run check-env`
3. **Check the logs** in the browser's Network tab
4. **Try a different browser** to isolate the issue

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Google Maps failed to load" | Missing API key | Set `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY` |
| "Geolocation not supported" | Old browser | Update browser or use manual search |
| "Location access denied" | Permission blocked | Enable location in browser settings |
| "Network error" | Connectivity issue | Check internet connection |
| "API quota exceeded" | Too many requests | Check Google Cloud Console usage |

## Development Tips

1. **Always run `npm run check-env`** before starting development
2. **Use browser dev tools** to debug issues
3. **Check the Network tab** for failed requests
4. **Test in incognito mode** to avoid cached issues
5. **Keep your API keys secure** and never commit them to version control 