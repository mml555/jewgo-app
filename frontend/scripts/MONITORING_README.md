# JewGo Frontend Monitoring

This directory contains monitoring configuration and scripts for the JewGo frontend application.

## Configuration Files

- `monitoring.json` - Main monitoring configuration
- `health.json` - Health check configuration
- `performance.json` - Performance monitoring configuration
- `log-rotation.json` - Log rotation settings
- `dashboard.json` - Dashboard configuration

## Scripts

- `health-monitor.js` - Main health monitoring script
- `rotate-logs.js` - Log rotation utility
- `aggregate-metrics.js` - Metrics aggregation
- `setup-monitoring.js` - Setup script (this file)

## Usage

### Start Monitoring
```bash
npm run monitor:start
```

### Run Health Check
```bash
npm run monitor:check
```

### Generate Report
```bash
npm run monitor:report
```

### Rotate Logs
```bash
npm run monitor:rotate-logs
```

## Logs

Logs are stored in the `../logs` directory:
- `health-monitor.log` - Health monitoring logs
- `errors/` - Error logs
- `performance/` - Performance metrics
- `metrics.json` - Current metrics
- `aggregated-metrics.json` - Aggregated metrics

## Alerts

The monitoring system can send alerts via:
- Email (configured in monitoring.json)
- Slack webhook (configured in monitoring.json)
- Custom webhook (configured in monitoring.json)

## Dashboard

A monitoring dashboard is available at `/monitoring` (if implemented in the frontend).

## Environment Variables

- `NODE_ENV` - Environment (development/staging/production)
- `MONITORING_ENABLED` - Enable/disable monitoring
- `ALERT_WEBHOOK_URL` - Custom webhook for alerts
