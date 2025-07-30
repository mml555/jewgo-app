#!/usr/bin/env node

/**
 * JewGo Comprehensive Health Check
 * Tests all services and endpoints to verify system status
 */

const https = require('https');
const http = require('http');

// Colors for console output
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m',
  bold: '\x1b[1m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function makeRequest(url, options = {}) {
  return new Promise((resolve) => {
    const startTime = Date.now();
    const protocol = url.startsWith('https') ? https : http;
    
    const req = protocol.request(url, options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const responseTime = Date.now() - startTime;
        resolve({
          status: res.statusCode,
          responseTime,
          data: data,
          headers: res.headers
        });
      });
    });

    req.on('error', (error) => {
      const responseTime = Date.now() - startTime;
      resolve({
        status: 'ERROR',
        responseTime,
        error: error.message,
        data: null
      });
    });

    req.setTimeout(10000, () => {
      req.destroy();
      resolve({
        status: 'TIMEOUT',
        responseTime: 10000,
        error: 'Request timeout',
        data: null
      });
    });

    req.end();
  });
}

async function checkService(name, url, expectedStatus = 200) {
  log(`\n🔍 Checking ${name}...`, 'blue');
  log(`   URL: ${url}`, 'blue');
  
  try {
    const result = await makeRequest(url);
    
    if (result.status === expectedStatus) {
      log(`   ✅ ${name}: HEALTHY (${result.responseTime}ms)`, 'green');
      return { status: 'healthy', responseTime: result.responseTime };
    } else if (result.status === 'ERROR' || result.status === 'TIMEOUT') {
      log(`   ❌ ${name}: DOWN - ${result.error}`, 'red');
      return { status: 'down', error: result.error };
    } else {
      log(`   ⚠️  ${name}: DEGRADED (Status: ${result.status}, ${result.responseTime}ms)`, 'yellow');
      return { status: 'degraded', statusCode: result.status, responseTime: result.responseTime };
    }
  } catch (error) {
    log(`   ❌ ${name}: ERROR - ${error.message}`, 'red');
    return { status: 'error', error: error.message };
  }
}

async function runHealthChecks() {
  log('\n🏥 JEWGO COMPREHENSIVE HEALTH CHECK', 'bold');
  log('=====================================\n', 'bold');

  const services = [
    {
      name: 'Frontend (Vercel)',
      url: 'https://jewgo-app.vercel.app',
      expectedStatus: 200
    },
    {
      name: 'Backend Health Endpoint',
      url: 'https://jewgo.onrender.com/health',
      expectedStatus: 200
    },
    {
      name: 'Backend API (Restaurants)',
      url: 'https://jewgo.onrender.com/api/restaurants',
      expectedStatus: 200
    },
    {
      name: 'Backend Ping',
      url: 'https://jewgo.onrender.com/ping',
      expectedStatus: 200
    },
    {
      name: 'Frontend Health Page',
      url: 'https://jewgo-app.vercel.app/health',
      expectedStatus: 200
    }
  ];

  const results = [];
  
  for (const service of services) {
    const result = await checkService(service.name, service.url, service.expectedStatus);
    results.push({ ...service, ...result });
  }

  // Summary
  log('\n📊 HEALTH CHECK SUMMARY', 'bold');
  log('========================\n', 'bold');

  const healthy = results.filter(r => r.status === 'healthy').length;
  const degraded = results.filter(r => r.status === 'degraded').length;
  const down = results.filter(r => r.status === 'down' || r.status === 'error').length;

  log(`✅ Healthy: ${healthy}`, 'green');
  log(`⚠️  Degraded: ${degraded}`, 'yellow');
  log(`❌ Down: ${down}`, 'red');

  if (down === 0 && degraded === 0) {
    log('\n🎉 ALL SYSTEMS OPERATIONAL!', 'green');
  } else if (down === 0) {
    log('\n⚠️  SYSTEM PARTIALLY OPERATIONAL - Some services degraded', 'yellow');
  } else {
    log('\n🚨 SYSTEM ISSUES DETECTED - Some services are down', 'red');
  }

  // Detailed results
  log('\n📋 DETAILED RESULTS:', 'bold');
  results.forEach(result => {
    const statusIcon = result.status === 'healthy' ? '✅' : 
                      result.status === 'degraded' ? '⚠️' : '❌';
    const statusColor = result.status === 'healthy' ? 'green' : 
                       result.status === 'degraded' ? 'yellow' : 'red';
    
    log(`${statusIcon} ${result.name}: ${result.status.toUpperCase()}`, statusColor);
    if (result.responseTime) {
      log(`   Response Time: ${result.responseTime}ms`);
    }
    if (result.error) {
      log(`   Error: ${result.error}`);
    }
  });

  return results;
}

// Run the health checks
runHealthChecks().catch(console.error); 