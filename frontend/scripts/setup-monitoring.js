#!/usr/bin/env node

/**
 * Monitoring Setup Script for JewGo Frontend
 * Configures monitoring tools and alerts
 */

const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  // Directories
  logsDir: path.join(__dirname, '../logs'),
  configDir: path.join(__dirname, '../config'),
  
  // Monitoring services
  services: {
    // Uptime monitoring
    uptime: {
      enabled: true,
      interval: 300, // 5 minutes
      endpoints: [
        'https://jewgo-app.vercel.app',
        'https://jewgo-app.vercel.app/health',
        'https://jewgo.onrender.com/health',
      ],
    },
    
    // Performance monitoring
    performance: {
      enabled: true,
      interval: 900, // 15 minutes
      metrics: ['responseTime', 'availability', 'errorRate'],
    },
    
    // Error tracking
    errors: {
      enabled: true,
      captureUnhandled: true,
      logLevel: 'error',
    },
  },
  
  // Alerting
  alerts: {
    email: {
      enabled: false,
      recipients: [],
    },
    slack: {
      enabled: false,
      webhook: '',
    },
    webhook: {
      enabled: false,
      url: '',
    },
  },
};

/**
 * Create directory structure
 */
function createDirectories() {
  console.log('📁 Creating directory structure...');
  
  const dirs = [
    CONFIG.logsDir,
    CONFIG.configDir,
    path.join(CONFIG.logsDir, 'monitoring'),
    path.join(CONFIG.logsDir, 'errors'),
    path.join(CONFIG.logsDir, 'performance'),
  ];
  
  dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
      console.log(`  ✅ Created: ${dir}`);
    } else {
      console.log(`  ℹ️  Exists: ${dir}`);
    }
  });
}

/**
 * Create monitoring configuration files
 */
function createConfigFiles() {
  console.log('⚙️  Creating configuration files...');
  
  // Main monitoring config
  const monitoringConfig = {
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    services: CONFIG.services,
    alerts: CONFIG.alerts,
  };
  
  fs.writeFileSync(
    path.join(CONFIG.configDir, 'monitoring.json'),
    JSON.stringify(monitoringConfig, null, 2)
  );
  console.log('  ✅ Created: monitoring.json');
  
  // Health check config
  const healthConfig = {
    endpoints: CONFIG.services.uptime.endpoints,
    interval: CONFIG.services.uptime.interval,
    timeout: 10000,
    retries: 3,
  };
  
  fs.writeFileSync(
    path.join(CONFIG.configDir, 'health.json'),
    JSON.stringify(healthConfig, null, 2)
  );
  console.log('  ✅ Created: health.json');
  
  // Performance config
  const performanceConfig = {
    metrics: CONFIG.services.performance.metrics,
    interval: CONFIG.services.performance.interval,
    thresholds: {
      responseTime: 3000,
      availability: 0.99,
      errorRate: 0.05,
    },
  };
  
  fs.writeFileSync(
    path.join(CONFIG.configDir, 'performance.json'),
    JSON.stringify(performanceConfig, null, 2)
  );
  console.log('  ✅ Created: performance.json');
}

/**
 * Create log rotation configuration
 */
function createLogRotation() {
  console.log('📋 Creating log rotation configuration...');
  
  const logRotationConfig = {
    logs: [
      {
        path: path.join(CONFIG.logsDir, 'health-monitor.log'),
        maxSize: '10MB',
        maxFiles: 5,
        compress: true,
      },
      {
        path: path.join(CONFIG.logsDir, 'errors/error.log'),
        maxSize: '5MB',
        maxFiles: 10,
        compress: true,
      },
      {
        path: path.join(CONFIG.logsDir, 'performance/performance.log'),
        maxSize: '10MB',
        maxFiles: 7,
        compress: true,
      },
    ],
  };
  
  fs.writeFileSync(
    path.join(CONFIG.configDir, 'log-rotation.json'),
    JSON.stringify(logRotationConfig, null, 2)
  );
  console.log('  ✅ Created: log-rotation.json');
}

/**
 * Create monitoring dashboard configuration
 */
function createDashboardConfig() {
  console.log('📊 Creating dashboard configuration...');
  
  const dashboardConfig = {
    title: 'JewGo Frontend Monitoring',
    refreshInterval: 30000, // 30 seconds
    widgets: [
      {
        type: 'uptime',
        title: 'Application Uptime',
        endpoints: CONFIG.services.uptime.endpoints,
        position: { x: 0, y: 0, w: 6, h: 4 },
      },
      {
        type: 'responseTime',
        title: 'Response Times',
        metrics: ['avg', 'p95', 'p99'],
        position: { x: 6, y: 0, w: 6, h: 4 },
      },
      {
        type: 'errorRate',
        title: 'Error Rate',
        threshold: 0.05,
        position: { x: 0, y: 4, w: 6, h: 3 },
      },
      {
        type: 'alerts',
        title: 'Recent Alerts',
        maxItems: 10,
        position: { x: 6, y: 4, w: 6, h: 3 },
      },
    ],
  };
  
  fs.writeFileSync(
    path.join(CONFIG.configDir, 'dashboard.json'),
    JSON.stringify(dashboardConfig, null, 2)
  );
  console.log('  ✅ Created: dashboard.json');
}

/**
 * Create environment-specific configurations
 */
function createEnvironmentConfigs() {
  console.log('🌍 Creating environment configurations...');
  
  const environments = ['development', 'staging', 'production'];
  
  environments.forEach(env => {
    const envConfig = {
      environment: env,
      urls: {
        frontend: env === 'production' 
          ? 'https://jewgo-app.vercel.app'
          : env === 'staging'
          ? 'https://staging.jewgo-app.vercel.app'
          : 'http://localhost:3000',
        backend: env === 'production'
          ? 'https://jewgo.onrender.com'
          : env === 'staging'
          ? 'https://staging.jewgo.onrender.com'
          : 'http://localhost:5000',
      },
      monitoring: {
        enabled: env === 'production',
        interval: env === 'production' ? 300 : 60,
        alerts: env === 'production',
      },
    };
    
    fs.writeFileSync(
      path.join(CONFIG.configDir, `${env}.json`),
      JSON.stringify(envConfig, null, 2)
    );
    console.log(`  ✅ Created: ${env}.json`);
  });
}

/**
 * Create monitoring scripts
 */
function createMonitoringScripts() {
  console.log('📜 Creating monitoring scripts...');
  
  // Log rotation script
  const logRotationScript = `#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Simple log rotation
function rotateLogs() {
  const logsDir = path.join(__dirname, '../logs');
  const config = require('../config/log-rotation.json');
  
  config.logs.forEach(logConfig => {
    if (fs.existsSync(logConfig.path)) {
      const stats = fs.statSync(logConfig.path);
      const sizeInMB = stats.size / (1024 * 1024);
      
      if (sizeInMB > parseInt(logConfig.maxSize)) {
        // Rotate log file
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const rotatedPath = \`\${logConfig.path}.\${timestamp}\`;
        
        fs.renameSync(logConfig.path, rotatedPath);
        console.log(\`Rotated log: \${logConfig.path}\`);
      }
    }
  });
}

rotateLogs();
`;
  
  fs.writeFileSync(
    path.join(__dirname, 'rotate-logs.js'),
    logRotationScript
  );
  fs.chmodSync(path.join(__dirname, 'rotate-logs.js'), '755');
  console.log('  ✅ Created: rotate-logs.js');
  
  // Metrics aggregation script
  const metricsScript = `#!/usr/bin/env node

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
`;
  
  fs.writeFileSync(
    path.join(__dirname, 'aggregate-metrics.js'),
    metricsScript
  );
  fs.chmodSync(path.join(__dirname, 'aggregate-metrics.js'), '755');
  console.log('  ✅ Created: aggregate-metrics.js');
}

/**
 * Update package.json scripts
 */
function updatePackageScripts() {
  console.log('📦 Updating package.json scripts...');
  
  const packagePath = path.join(__dirname, '../package.json');
  
  if (fs.existsSync(packagePath)) {
    const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
    
    const newScripts = {
      ...packageJson.scripts,
      'monitor:setup': 'node scripts/setup-monitoring.js',
      'monitor:start': 'node scripts/health-monitor.js start',
      'monitor:check': 'node scripts/health-monitor.js check',
      'monitor:report': 'node scripts/health-monitor.js report',
      'monitor:rotate-logs': 'node scripts/rotate-logs.js',
      'monitor:aggregate': 'node scripts/aggregate-metrics.js',
      'monitor:cleanup': 'node scripts/cleanup-logs.js',
    };
    
    packageJson.scripts = newScripts;
    
    fs.writeFileSync(packagePath, JSON.stringify(packageJson, null, 2));
    console.log('  ✅ Updated: package.json scripts');
  }
}

/**
 * Create README for monitoring
 */
function createMonitoringReadme() {
  console.log('📖 Creating monitoring documentation...');
  
  const readme = `# JewGo Frontend Monitoring

This directory contains monitoring configuration and scripts for the JewGo frontend application.

## Configuration Files

- \`monitoring.json\` - Main monitoring configuration
- \`health.json\` - Health check configuration
- \`performance.json\` - Performance monitoring configuration
- \`log-rotation.json\` - Log rotation settings
- \`dashboard.json\` - Dashboard configuration

## Scripts

- \`health-monitor.js\` - Main health monitoring script
- \`rotate-logs.js\` - Log rotation utility
- \`aggregate-metrics.js\` - Metrics aggregation
- \`setup-monitoring.js\` - Setup script (this file)

## Usage

### Start Monitoring
\`\`\`bash
npm run monitor:start
\`\`\`

### Run Health Check
\`\`\`bash
npm run monitor:check
\`\`\`

### Generate Report
\`\`\`bash
npm run monitor:report
\`\`\`

### Rotate Logs
\`\`\`bash
npm run monitor:rotate-logs
\`\`\`

## Logs

Logs are stored in the \`../logs\` directory:
- \`health-monitor.log\` - Health monitoring logs
- \`errors/\` - Error logs
- \`performance/\` - Performance metrics
- \`metrics.json\` - Current metrics
- \`aggregated-metrics.json\` - Aggregated metrics

## Alerts

The monitoring system can send alerts via:
- Email (configured in monitoring.json)
- Slack webhook (configured in monitoring.json)
- Custom webhook (configured in monitoring.json)

## Dashboard

A monitoring dashboard is available at \`/monitoring\` (if implemented in the frontend).

## Environment Variables

- \`NODE_ENV\` - Environment (development/staging/production)
- \`MONITORING_ENABLED\` - Enable/disable monitoring
- \`ALERT_WEBHOOK_URL\` - Custom webhook for alerts
`;
  
  fs.writeFileSync(
    path.join(__dirname, 'MONITORING_README.md'),
    readme
  );
  console.log('  ✅ Created: MONITORING_README.md');
}

/**
 * Main setup function
 */
function setup() {
  console.log('🚀 Setting up monitoring for JewGo Frontend...\n');
  
  try {
    createDirectories();
    console.log('');
    
    createConfigFiles();
    console.log('');
    
    createLogRotation();
    console.log('');
    
    createDashboardConfig();
    console.log('');
    
    createEnvironmentConfigs();
    console.log('');
    
    createMonitoringScripts();
    console.log('');
    
    updatePackageScripts();
    console.log('');
    
    createMonitoringReadme();
    console.log('');
    
    console.log('✅ Monitoring setup completed successfully!');
    console.log('');
    console.log('Next steps:');
    console.log('1. Review configuration files in scripts/config/');
    console.log('2. Update alert settings in monitoring.json');
    console.log('3. Start monitoring with: npm run monitor:start');
    console.log('4. Check logs in scripts/logs/');
    
  } catch (error) {
    console.error('❌ Setup failed:', error.message);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  setup();
}

module.exports = {
  setup,
  CONFIG,
}; 