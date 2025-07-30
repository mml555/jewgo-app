#!/usr/bin/env node

/**
 * JewGo Monitoring Setup Script
 * Sets up comprehensive monitoring for the JewGo application
 */

const fs = require('fs');
const path = require('path');

// Monitoring configuration
const monitoringConfig = {
  // Upptime configuration for uptime monitoring
  upptime: {
    enabled: true,
    endpoints: [
      'https://jewgo-app.vercel.app',
      'https://jewgo.onrender.com/health',
      'https://jewgo.onrender.com/api/restaurants'
    ],
    checkInterval: 300, // 5 minutes
    notifications: ['slack', 'email']
  },
  
  // Sentry configuration for error tracking
  sentry: {
    enabled: true,
    dsn: process.env.SENTRY_DSN || 'your-sentry-dsn-here',
    environment: process.env.NODE_ENV || 'production'
  },
  
  // Health check configuration
  healthChecks: {
    enabled: true,
    interval: 60000, // 1 minute
    timeout: 10000, // 10 seconds
    endpoints: [
      {
        name: 'Frontend',
        url: 'https://jewgo-app.vercel.app',
        expectedStatus: 200
      },
      {
        name: 'Backend Health',
        url: 'https://jewgo.onrender.com/health',
        expectedStatus: 200
      },
      {
        name: 'Backend API',
        url: 'https://jewgo.onrender.com/api/restaurants',
        expectedStatus: 200
      }
    ]
  }
};

// Create monitoring files
function createMonitoringFiles() {
  console.log('🔧 Setting up monitoring files...\n');
  
  // 1. Create .github/workflows/monitor.yml for Upptime
  const upptimeWorkflow = `name: Upptime

on:
  schedule:
    - cron: '*/5 * * * *'  # Every 5 minutes
  workflow_dispatch:

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: upptime/uptime-monitor@master
        with:
          url: https://jewgo-app.vercel.app
          name: JewGo Frontend
          method: GET
          expectedStatus: 200
          timeout: 10000
          
      - uses: upptime/uptime-monitor@master
        with:
          url: https://jewgo.onrender.com/health
          name: JewGo Backend Health
          method: GET
          expectedStatus: 200
          timeout: 10000
          
      - uses: upptime/uptime-monitor@master
        with:
          url: https://jewgo.onrender.com/api/restaurants
          name: JewGo Backend API
          method: GET
          expectedStatus: 200
          timeout: 10000`;

  // 2. Create monitoring configuration
  const monitoringSetup = `// JewGo Monitoring Configuration
export const monitoringConfig = ${JSON.stringify(monitoringConfig, null, 2)};

// Health check function
export async function performHealthCheck() {
  const results = [];
  
  for (const endpoint of monitoringConfig.healthChecks.endpoints) {
    try {
      const startTime = Date.now();
      const response = await fetch(endpoint.url, {
        method: 'GET',
        signal: AbortSignal.timeout(monitoringConfig.healthChecks.timeout)
      });
      const responseTime = Date.now() - startTime;
      
      results.push({
        name: endpoint.name,
        url: endpoint.url,
        status: response.status,
        responseTime,
        healthy: response.status === endpoint.expectedStatus,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      results.push({
        name: endpoint.name,
        url: endpoint.url,
        status: 'ERROR',
        responseTime: 0,
        healthy: false,
        error: error.message,
        timestamp: new Date().toISOString()
      });
    }
  }
  
  return results;
}

// Alert function
export function sendAlert(message, level = 'warning') {
  // Implement your alert mechanism here
  // Slack, email, SMS, etc.
  console.log(\`[\${level.toUpperCase()}] \${message}\`);
}

// Main monitoring function
export async function runMonitoring() {
  const healthResults = await performHealthCheck();
  const unhealthyServices = healthResults.filter(r => !r.healthy);
  
  if (unhealthyServices.length > 0) {
    const message = \`JewGo System Alert: \${unhealthyServices.length} service(s) are down\\n\` +
                   unhealthyServices.map(s => \`- \${s.name}: \${s.status}\`).join('\\n');
    sendAlert(message, 'error');
  }
  
  return healthResults;
}`;

  // 3. Create package.json scripts
  const packageJsonPath = path.join(process.cwd(), 'package.json');
  if (fs.existsSync(packageJsonPath)) {
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
    
    // Add monitoring scripts
    packageJson.scripts = {
      ...packageJson.scripts,
      'monitor:health': 'node scripts/health-monitor.js',
      'monitor:setup': 'node scripts/setup-monitoring.js',
      'monitor:test': 'node scripts/test-monitoring.js'
    };
    
    fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
    console.log('✅ Updated package.json with monitoring scripts');
  }

  // 4. Create health monitor script
  const healthMonitor = `#!/usr/bin/env node

/**
 * JewGo Health Monitor
 * Continuous health monitoring for all services
 */

const { performHealthCheck, sendAlert } = require('./monitoring-config.js');

class HealthMonitor {
  constructor() {
    this.isRunning = false;
    this.checkInterval = 60000; // 1 minute
  }

  async start() {
    if (this.isRunning) {
      console.log('⚠️  Monitor is already running');
      return;
    }

    console.log('🚀 Starting JewGo Health Monitor...');
    this.isRunning = true;

    while (this.isRunning) {
      try {
        const results = await performHealthCheck();
        this.logResults(results);
        
        // Check for unhealthy services
        const unhealthy = results.filter(r => !r.healthy);
        if (unhealthy.length > 0) {
          const message = \`Health Check Failed: \${unhealthy.length} service(s) down\`;
          sendAlert(message, 'error');
        }
        
        // Wait for next check
        await new Promise(resolve => setTimeout(resolve, this.checkInterval));
      } catch (error) {
        console.error('❌ Monitor error:', error);
        sendAlert(\`Monitor Error: \${error.message}\`, 'error');
        await new Promise(resolve => setTimeout(resolve, 30000)); // Wait 30s on error
      }
    }
  }

  stop() {
    console.log('🛑 Stopping JewGo Health Monitor...');
    this.isRunning = false;
  }

  logResults(results) {
    const timestamp = new Date().toLocaleString();
    console.log(\`\\n[\\${timestamp}] Health Check Results:\`);
    
    results.forEach(result => {
      const status = result.healthy ? '✅' : '❌';
      console.log(\`  \${status} \${result.name}: \${result.responseTime}ms (\${result.status})\`);
    });
  }
}

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\\n🛑 Received SIGINT, shutting down...');
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\\n🛑 Received SIGTERM, shutting down...');
  process.exit(0);
});

// Start the monitor
const monitor = new HealthMonitor();
monitor.start().catch(console.error);`;

  // Write files
  const workflowsDir = path.join(process.cwd(), '.github', 'workflows');
  if (!fs.existsSync(workflowsDir)) {
    fs.mkdirSync(workflowsDir, { recursive: true });
  }

  fs.writeFileSync(path.join(workflowsDir, 'monitor.yml'), upptimeWorkflow);
  fs.writeFileSync(path.join(process.cwd(), 'scripts', 'monitoring-config.js'), monitoringSetup);
  fs.writeFileSync(path.join(process.cwd(), 'scripts', 'health-monitor.js'), healthMonitor);

  console.log('✅ Created monitoring files:');
  console.log('  - .github/workflows/monitor.yml');
  console.log('  - scripts/monitoring-config.js');
  console.log('  - scripts/health-monitor.js');
  console.log('  - Updated package.json scripts\n');
}

// Setup instructions
function printSetupInstructions() {
  console.log('📋 Monitoring Setup Instructions:');
  console.log('==================================\n');
  
  console.log('1. **Upptime Setup (Uptime Monitoring):**');
  console.log('   - Go to https://upptime.js.org/');
  console.log('   - Create a new repository with Upptime template');
  console.log('   - Update the endpoints in .github/workflows/monitor.yml');
  console.log('   - Enable GitHub Actions in your repository\n');
  
  console.log('2. **Sentry Setup (Error Tracking):**');
  console.log('   - Sign up at https://sentry.io/');
  console.log('   - Create a new project for JewGo');
  console.log('   - Add SENTRY_DSN to your environment variables\n');
  
  console.log('3. **Slack Notifications (Optional):**');
  console.log('   - Create a Slack app at https://api.slack.com/apps');
  console.log('   - Add webhook URL to your environment variables\n');
  
  console.log('4. **Start Monitoring:**');
  console.log('   npm run monitor:health  # Start health monitoring');
  console.log('   npm run monitor:test    # Test monitoring setup\n');
}

// Main execution
function main() {
  console.log('🔧 JewGo Monitoring Setup\n');
  
  try {
    createMonitoringFiles();
    printSetupInstructions();
    
    console.log('✅ Monitoring setup complete!');
    console.log('\\nNext steps:');
    console.log('1. Configure your monitoring services (Upptime, Sentry)');
    console.log('2. Add environment variables for notifications');
    console.log('3. Test the monitoring with: npm run monitor:test');
    
  } catch (error) {
    console.error('❌ Setup failed:', error);
    process.exit(1);
  }
}

// Run setup
main(); 