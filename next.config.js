/** @type {import('next').NextConfig} */
const nextConfig = {
  // Vercel deployment configuration
  // Using server-side rendering for better performance and SEO
  // Vercel automatically handles SSR/SSG optimization
  
  // Remove trailing slash requirement to avoid routing issues
  trailingSlash: false,
  
  // Image optimization configuration for Vercel
  images: {
    // Vercel automatically optimizes images
    remotePatterns: [
      { protocol: 'https', hostname: 'www.orbkosher.com' },
      { protocol: 'https', hostname: 'maps.googleapis.com' },
      { protocol: 'https', hostname: 'images.unsplash.com' },
      { protocol: 'https', hostname: 'source.unsplash.com' },
      { protocol: 'http', hostname: 'localhost' },
    ],
  },
  
  // Webpack configuration for better bundle optimization
  webpack: (config, { dev, isServer }) => {
    // Optimize bundle size for production builds
    if (!dev && !isServer) {
      config.optimization.splitChunks = {
        chunks: 'all',
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            chunks: 'all',
          },
        },
      };
    }
    
    return config;
  },
  
  // Disable experimental features that might cause build issues
  experimental: {
    // Remove webpackBuildWorker to avoid build issues
  },
  
  // Ensure proper output configuration for Vercel
  output: 'standalone',
  
  // Disable static optimization for dynamic routes
  staticPageGenerationTimeout: 120,
  
  // Add security headers including geolocation permissions
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=(self)'
          },
          {
            key: 'X-Frame-Options',
            value: 'ALLOWALL'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin'
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=31536000; includeSubDomains'
          }
        ]
      }
    ];
  },
};

module.exports = nextConfig; 