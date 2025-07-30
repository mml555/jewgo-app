#!/usr/bin/env node

/**
 * JewGo API Optimization Script
 * Helps optimize API response times and performance
 */

const https = require('https');

// Performance monitoring
class PerformanceMonitor {
  constructor() {
    this.metrics = [];
  }

  async measureEndpoint(url, name) {
    const startTime = Date.now();
    
    return new Promise((resolve) => {
      const req = https.request(url, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          const responseTime = Date.now() - startTime;
          const metric = {
            name,
            url,
            status: res.statusCode,
            responseTime,
            timestamp: new Date().toISOString(),
            size: data.length
          };
          
          this.metrics.push(metric);
          resolve(metric);
        });
      });

      req.on('error', (error) => {
        const responseTime = Date.now() - startTime;
        const metric = {
          name,
          url,
          status: 'ERROR',
          responseTime,
          error: error.message,
          timestamp: new Date().toISOString()
        };
        
        this.metrics.push(metric);
        resolve(metric);
      });

      req.setTimeout(10000, () => {
        req.destroy();
        const responseTime = Date.now() - startTime;
        const metric = {
          name,
          url,
          status: 'TIMEOUT',
          responseTime,
          error: 'Request timeout',
          timestamp: new Date().toISOString()
        };
        
        this.metrics.push(metric);
        resolve(metric);
      });

      req.end();
    });
  }

  getAverageResponseTime() {
    const validMetrics = this.metrics.filter(m => m.status === 200);
    if (validMetrics.length === 0) return 0;
    
    const total = validMetrics.reduce((sum, m) => sum + m.responseTime, 0);
    return total / validMetrics.length;
  }

  getSlowestEndpoint() {
    return this.metrics.reduce((slowest, current) => 
      current.responseTime > slowest.responseTime ? current : slowest
    );
  }

  printReport() {
    console.log('\n📊 API Performance Report');
    console.log('========================\n');
    
    this.metrics.forEach(metric => {
      const status = metric.status === 200 ? '✅' : '❌';
      console.log(`${status} ${metric.name}: ${metric.responseTime}ms (${metric.status})`);
    });
    
    console.log(`\n📈 Average Response Time: ${this.getAverageResponseTime().toFixed(0)}ms`);
    
    const slowest = this.getSlowestEndpoint();
    console.log(`🐌 Slowest Endpoint: ${slowest.name} (${slowest.responseTime}ms)`);
    
    // Recommendations
    console.log('\n💡 Optimization Recommendations:');
    if (this.getAverageResponseTime() > 3000) {
      console.log('⚠️  Consider implementing caching (Redis/Memcached)');
      console.log('⚠️  Optimize database queries');
      console.log('⚠️  Add response compression');
    } else if (this.getAverageResponseTime() > 2000) {
      console.log('⚠️  Consider adding response caching');
      console.log('⚠️  Review database query performance');
    } else {
      console.log('✅ Response times are acceptable');
    }
  }
}

// Cache optimization suggestions
function generateCacheConfig() {
  console.log('\n🔧 Cache Configuration Suggestions:');
  console.log('===================================\n');
  
  console.log('1. **Redis Cache Setup:**');
  console.log('   - Cache restaurant data for 5-10 minutes');
  console.log('   - Cache search results for 2-5 minutes');
  console.log('   - Cache health check results for 30 seconds');
  
  console.log('\n2. **CDN Configuration:**');
  console.log('   - Use Cloudflare or similar for static assets');
  console.log('   - Enable gzip compression');
  console.log('   - Set appropriate cache headers');
  
  console.log('\n3. **Database Optimization:**');
  console.log('   - Add database indexes on frequently queried fields');
  console.log('   - Implement query result caching');
  console.log('   - Consider read replicas for heavy traffic');
}

// Main execution
async function main() {
  console.log('🚀 JewGo API Optimization Analysis\n');
  
  const monitor = new PerformanceMonitor();
  
  // Test key endpoints
  const endpoints = [
    { url: 'https://jewgo.onrender.com/health', name: 'Health Check' },
    { url: 'https://jewgo.onrender.com/api/restaurants', name: 'Restaurants API' },
    { url: 'https://jewgo.onrender.com/ping', name: 'Ping Endpoint' }
  ];
  
  console.log('Testing endpoints...\n');
  
  for (const endpoint of endpoints) {
    await monitor.measureEndpoint(endpoint.url, endpoint.name);
    // Small delay between requests
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  // Generate reports
  monitor.printReport();
  generateCacheConfig();
  
  console.log('\n✅ Optimization analysis complete!');
}

// Run the analysis
main().catch(console.error); 