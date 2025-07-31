#!/usr/bin/env node

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
        const rotatedPath = `${logConfig.path}.${timestamp}`;
        
        fs.renameSync(logConfig.path, rotatedPath);
        console.log(`Rotated log: ${logConfig.path}`);
      }
    }
  });
}

rotateLogs();
