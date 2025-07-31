#!/usr/bin/env node

/**
 * Health Monitoring Script for JewGo Frontend
 * Monitors application health, performance, and availability
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  // Application URLs to monitor
  urls: {
    production: 'https://jewgo-app.vercel.app',
    health: 'https://jewgo-app.vercel.app/health',
    api: 'https://jewgo.onrender.com/health',
  },
  // Monitoring intervals (in milliseconds)
  intervals: {
    health: 5 * 60 * 1000, // 5 minutes
    performance: 15 * 60 * 1000, // 15 minutes
    detailed: 60 * 60 * 1000, // 1 hour
  },
  // Thresholds
  thresholds: {
    responseTime: 3000, // 3 seconds
    errorRate: 0.05, // 5%
    availability: 0.99, // 99%
  },
  // Logging
  logFile: path.join(__dirname, '../logs/health-monitor.log'),
  metricsFile: path.join(__dirname, '../logs/metrics.json'),
};

// Metrics storage
let metrics = {
  checks: 0,
  failures: 0,
  responseTimes: [],
  lastCheck: null,
  uptime: {
    start: Date.now(),
    lastFailure: null,
  },
};

// Ensure logs directory exists
const logsDir = path.dirname(CONFIG.logFile);
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir, { recursive: true });
}

/**
 * Logging utility
 */
function log(level, message, data = {}) {
  const timestamp = new Date().toISOString();
  const logEntry = {
    timestamp,
    level,
    message,
    ...data,
  };
  
  console.log(`[${timestamp}] ${level.toUpperCase()}: ${message}`);
  
  // Write to file
  fs.appendFileSync(CONFIG.logFile, JSON.stringify(logEntry) + '\n');
}

/**
 * Make HTTP request with timeout
 */
function makeRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const startTime = Date.now();
    const timeout = options.timeout || 10000;
    
    const protocol = url.startsWith('https:') ? https : http;
    const req = protocol.get(url, { timeout }, (res) => {
      const responseTime = Date.now() - startTime;
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          responseTime,
          data,
          headers: res.headers,
        });
      });
    });
    
    req.on('error', (error) => {
      const responseTime = Date.now() - startTime;
      reject({
        error: error.message,
        responseTime,
        url,
      });
    });
    
    req.on('timeout', () => {
      req.destroy();
      reject({
        error: 'Request timeout',
        responseTime: timeout,
        url,
      });
    });
  });
}

/**
 * Health check for a single endpoint
 */
async function healthCheck(url, name) {
  try {
    log('info', `Starting health check for ${name}`, { url });
    
    const result = await makeRequest(url);
    
    if (result.statusCode >= 200 && result.statusCode < 300) {
      log('info', `Health check passed for ${name}`, {
        statusCode: result.statusCode,
        responseTime: result.responseTime,
      });
      
      return {
        success: true,
        responseTime: result.responseTime,
        statusCode: result.statusCode,
      };
    } else {
      throw new Error(`HTTP ${result.statusCode}`);
    }
  } catch (error) {
    log('error', `Health check failed for ${name}`, {
      error: error.error || error.message,
      responseTime: error.responseTime,
    });
    
    return {
      success: false,
      error: error.error || error.message,
      responseTime: error.responseTime,
    };
  }
}

/**
 * Performance check
 */
async function performanceCheck() {
  log('info', 'Starting performance check');
  
  const results = {};
  
  for (const [name, url] of Object.entries(CONFIG.urls)) {
    const startTime = Date.now();
    const result = await healthCheck(url, name);
    const totalTime = Date.now() - startTime;
    
    results[name] = {
      ...result,
      totalTime,
    };
  }
  
  // Calculate performance metrics
  const avgResponseTime = Object.values(results)
    .filter(r => r.success)
    .reduce((sum, r) => sum + r.responseTime, 0) / 
    Object.values(results).filter(r => r.success).length;
  
  const successRate = Object.values(results)
    .filter(r => r.success).length / Object.keys(results).length;
  
  log('info', 'Performance check completed', {
    avgResponseTime: Math.round(avgResponseTime),
    successRate: Math.round(successRate * 100) + '%',
    results,
  });
  
  return results;
}

/**
 * Update metrics
 */
function updateMetrics(checkResult) {
  metrics.checks++;
  metrics.lastCheck = Date.now();
  
  if (!checkResult.success) {
    metrics.failures++;
    metrics.uptime.lastFailure = Date.now();
  }
  
  if (checkResult.responseTime) {
    metrics.responseTimes.push(checkResult.responseTime);
    // Keep only last 100 response times
    if (metrics.responseTimes.length > 100) {
      metrics.responseTimes.shift();
    }
  }
  
  // Calculate availability
  metrics.availability = (metrics.checks - metrics.failures) / metrics.checks;
  
  // Save metrics to file
  fs.writeFileSync(CONFIG.metricsFile, JSON.stringify(metrics, null, 2));
}

/**
 * Generate health report
 */
function generateReport() {
  const avgResponseTime = metrics.responseTimes.length > 0
    ? metrics.responseTimes.reduce((sum, time) => sum + time, 0) / metrics.responseTimes.length
    : 0;
  
  const uptime = Date.now() - metrics.uptime.start;
  const uptimeHours = Math.round(uptime / (1000 * 60 * 60));
  
  const report = {
    timestamp: new Date().toISOString(),
    summary: {
      totalChecks: metrics.checks,
      totalFailures: metrics.failures,
      availability: Math.round(metrics.availability * 100) + '%',
      avgResponseTime: Math.round(avgResponseTime) + 'ms',
      uptime: uptimeHours + ' hours',
    },
    alerts: [],
  };
  
  // Check for alerts
  if (metrics.availability < CONFIG.thresholds.availability) {
    report.alerts.push({
      type: 'availability',
      message: `Availability below threshold: ${Math.round(metrics.availability * 100)}%`,
      severity: 'high',
    });
  }
  
  if (avgResponseTime > CONFIG.thresholds.responseTime) {
    report.alerts.push({
      type: 'performance',
      message: `Average response time above threshold: ${Math.round(avgResponseTime)}ms`,
      severity: 'medium',
    });
  }
  
  if (metrics.failures > 0 && metrics.uptime.lastFailure) {
    const timeSinceLastFailure = Date.now() - metrics.uptime.lastFailure;
    if (timeSinceLastFailure < 5 * 60 * 1000) { // 5 minutes
      report.alerts.push({
        type: 'recent_failure',
        message: 'Recent failure detected',
        severity: 'high',
      });
    }
  }
  
  log('info', 'Health report generated', report);
  return report;
}

/**
 * Main monitoring loop
 */
async function startMonitoring() {
  log('info', 'Starting health monitoring', CONFIG);
  
  // Initial health check
  await runHealthCheck();
  
  // Set up intervals
  setInterval(runHealthCheck, CONFIG.intervals.health);
  setInterval(runPerformanceCheck, CONFIG.intervals.performance);
  setInterval(runDetailedCheck, CONFIG.intervals.detailed);
}

/**
 * Run health check
 */
async function runHealthCheck() {
  try {
    const result = await healthCheck(CONFIG.urls.health, 'Health Endpoint');
    updateMetrics(result);
    
    if (!result.success) {
      log('error', 'Health check failed', result);
    }
  } catch (error) {
    log('error', 'Health check error', error);
  }
}

/**
 * Run performance check
 */
async function runPerformanceCheck() {
  try {
    const results = await performanceCheck();
    
    // Update metrics for each endpoint
    Object.values(results).forEach(result => {
      updateMetrics(result);
    });
  } catch (error) {
    log('error', 'Performance check error', error);
  }
}

/**
 * Run detailed check
 */
async function runDetailedCheck() {
  try {
    log('info', 'Starting detailed health check');
    
    const report = generateReport();
    
    // Check all endpoints
    const results = await performanceCheck();
    
    // Log detailed report
    log('info', 'Detailed check completed', {
      report,
      results,
    });
    
    // Send alerts if needed
    if (report.alerts.length > 0) {
      log('warn', 'Alerts detected', report.alerts);
      // Here you could integrate with external alerting services
      // like Slack, email, or monitoring platforms
    }
  } catch (error) {
    log('error', 'Detailed check error', error);
  }
}

/**
 * CLI interface
 */
function main() {
  const command = process.argv[2];
  
  switch (command) {
    case 'start':
      startMonitoring();
      break;
    case 'check':
      runHealthCheck();
      break;
    case 'performance':
      runPerformanceCheck();
      break;
    case 'report':
      console.log(JSON.stringify(generateReport(), null, 2));
      break;
    case 'metrics':
      console.log(JSON.stringify(metrics, null, 2));
      break;
    default:
      console.log(`
Health Monitor for JewGo Frontend

Usage:
  node health-monitor.js <command>

Commands:
  start       Start continuous monitoring
  check       Run single health check
  performance Run performance check
  report      Generate health report
  metrics     Show current metrics

Examples:
  node health-monitor.js start
  node health-monitor.js check
  node health-monitor.js report
      `);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = {
  healthCheck,
  performanceCheck,
  generateReport,
  startMonitoring,
  metrics,
}; 