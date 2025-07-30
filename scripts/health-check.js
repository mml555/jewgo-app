#!/usr/bin/env node

/**
 * JewGo Health Check Script
 * Comprehensive health monitoring for all JewGo services
 */

const https = require('https');

// Service endpoints to check
const services = [
  {
    name: 'Frontend (Vercel)',
    url: 'https://jewgo-app.vercel.app',
    expectedStatus: 200,
    timeout: 10000
  },
  {
    name: 'Backend Health Endpoint',
    url: 'https://jewgo.onrender.com/health',
    expectedStatus: 200,
    timeout: 10000
  },
  {
    name: 'Backend API (Restaurants)',
    url: 'https://jewgo.onrender.com/api/restaurants',
    expectedStatus: 200,
    timeout: 10000
  },
  {
    name: 'Backend Ping',
    url: 'https://jewgo.onrender.com/ping',
    expectedStatus: 200,
    timeout: 10000
  },
  {
    name: 'Frontend Health Page',
    url: 'https://jewgo-app.vercel.app/health',
    expectedStatus: 200,
    timeout: 10000
  }
];

// Health check function
async function checkService(service) {
  const startTime = Date.now();
  
  return new Promise((resolve) => {
    const timeout = setTimeout(() => {
      resolve({
        name: service.name,
        url: service.url,
        status: 'TIMEOUT',
        responseTime: Date.now() - startTime,
        healthy: false,
        error: 'Request timeout'
      });
    }, service.timeout);

    const req = https.request(service.url, (res) => {
      clearTimeout(timeout);
      let data = '';
      
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const responseTime = Date.now() - startTime;
        const healthy = res.statusCode === service.expectedStatus;
        
        resolve({
          name: service.name,
          url: service.url,
          status: res.statusCode,
          responseTime,
          healthy,
          data: data.substring(0, 200) // First 200 chars for debugging
        });
      });
    });

    req.on('error', (error) => {
      clearTimeout(timeout);
      resolve({
        name: service.name,
        url: service.url,
        status: 'ERROR',
        responseTime: Date.now() - startTime,
        healthy: false,
        error: error.message
      });
    });

    req.setTimeout(service.timeout, () => {
      clearTimeout(timeout);
      req.destroy();
      resolve({
        name: service.name,
        url: service.url,
        status: 'TIMEOUT',
        responseTime: Date.now() - startTime,
        healthy: false,
        error: 'Request timeout'
      });
    });

    req.end();
  });
}

// Main health check function
async function runHealthChecks() {
  console.log('🏥 JewGo Health Check Starting...\n');
  
  const results = [];
  const startTime = Date.now();
  
  // Check each service
  for (const service of services) {
    console.log(`🔍 Checking ${service.name}...`);
    const result = await checkService(service);
    results.push(result);
    
    // Small delay between requests
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  const totalTime = Date.now() - startTime;
  
  // Generate report
  console.log('\n📊 Health Check Results:');
  console.log('========================\n');
  
  let healthyCount = 0;
  let totalResponseTime = 0;
  
  results.forEach(result => {
    const status = result.healthy ? '✅' : '❌';
    const statusText = result.healthy ? 'HEALTHY' : 'DEGRADED';
    
    console.log(`${status} ${result.name}: ${statusText} (${result.responseTime}ms)`);
    
    if (result.healthy) {
      healthyCount++;
      totalResponseTime += result.responseTime;
    } else {
      console.log(`   Error: ${result.error || `Status ${result.status}`}`);
    }
  });
  
  // Summary
  const healthPercentage = (healthyCount / services.length) * 100;
  const avgResponseTime = healthyCount > 0 ? totalResponseTime / healthyCount : 0;
  
  console.log('\n📈 Summary:');
  console.log('===========');
  console.log(`Overall Health: ${healthPercentage.toFixed(0)}% (${healthyCount}/${services.length} services healthy)`);
  console.log(`Average Response Time: ${avgResponseTime.toFixed(0)}ms`);
  console.log(`Total Check Time: ${totalTime}ms`);
  
  // Recommendations
  console.log('\n💡 Recommendations:');
  console.log('==================');
  
  if (healthPercentage === 100) {
    console.log('✅ All services are healthy! System is fully operational.');
  } else if (healthPercentage >= 80) {
    console.log('⚠️  Most services are healthy. Check the failing services above.');
  } else if (healthPercentage >= 60) {
    console.log('⚠️  Several services are down. Review deployment configurations.');
  } else {
    console.log('❌ Critical system failure. Immediate attention required.');
  }
  
  if (avgResponseTime > 3000) {
    console.log('⚠️  Response times are slow. Consider implementing caching.');
  }
  
  // Exit with appropriate code
  const exitCode = healthPercentage >= 80 ? 0 : 1;
  
  console.log(`\n🏁 Health check completed with exit code: ${exitCode}`);
  return { results, healthPercentage, avgResponseTime, exitCode };
}

// Run the health checks
runHealthChecks()
  .then(({ results, healthPercentage, avgResponseTime, exitCode }) => {
    // Save results to file for CI/CD
    const fs = require('fs');
    const healthReport = {
      timestamp: new Date().toISOString(),
      healthPercentage,
      avgResponseTime,
      services: results,
      summary: {
        total: results.length,
        healthy: results.filter(r => r.healthy).length,
        degraded: results.filter(r => !r.healthy).length
      }
    };
    
    fs.writeFileSync('health-report.json', JSON.stringify(healthReport, null, 2));
    console.log('📄 Health report saved to health-report.json');
    
    process.exit(exitCode);
  })
  .catch(error => {
    console.error('❌ Health check failed:', error);
    process.exit(1);
  }); 