#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function aggregateMetrics() {
  const metricsFile = path.join(__dirname, '../logs/metrics.json');
  const aggregatedFile = path.join(__dirname, '../logs/aggregated-metrics.json');
  
  if (fs.existsSync(metricsFile)) {
    const metrics = JSON.parse(fs.readFileSync(metricsFile, 'utf8'));
    
    const aggregated = {
      timestamp: new Date().toISOString(),
      summary: {
        totalChecks: metrics.checks,
        totalFailures: metrics.failures,
        availability: metrics.availability,
        avgResponseTime: metrics.responseTimes.length > 0
          ? metrics.responseTimes.reduce((sum, time) => sum + time, 0) / metrics.responseTimes.length
          : 0,
      },
      hourly: {
        checks: metrics.checks,
        failures: metrics.failures,
        avgResponseTime: metrics.responseTimes.length > 0
          ? metrics.responseTimes.reduce((sum, time) => sum + time, 0) / metrics.responseTimes.length
          : 0,
      },
    };
    
    fs.writeFileSync(aggregatedFile, JSON.stringify(aggregated, null, 2));
    console.log('Metrics aggregated successfully');
  }
}

aggregateMetrics();
