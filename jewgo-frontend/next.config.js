/** @type {import('next').NextConfig} */
const nextConfig = {
  // Vercel deployment configuration
  // Using server-side rendering for better performance and SEO
  // Vercel automatically handles SSR/SSG optimization
  
  // Ensure trailing slashes for consistency
  trailingSlash: true,
  
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
  
  // Enable webpack build worker for faster builds
  experimental: {
    webpackBuildWorker: true,
  },
};

module.exports = nextConfig; 