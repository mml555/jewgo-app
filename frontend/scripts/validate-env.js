#!/usr/bin/env node

/**
 * Environment Variable Validation Script
 * Validates that required environment variables are set for Vercel deployment
 */

const requiredEnvVars = [
  'NEXT_PUBLIC_GOOGLE_MAPS_API_KEY',
  'NEXTAUTH_SECRET',
  'NEXTAUTH_URL',
  'NEXT_PUBLIC_BACKEND_URL'
];

const optionalEnvVars = [
  'NEXT_PUBLIC_GA_MEASUREMENT_ID',
  'NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME',
  'GOOGLE_CLIENT_ID',
  'GOOGLE_CLIENT_SECRET'
];

console.log('🔍 Validating environment variables...\n');

let hasErrors = false;

// Check required environment variables
requiredEnvVars.forEach(envVar => {
  const value = process.env[envVar];
  if (!value) {
    console.error(`❌ Missing required environment variable: ${envVar}`);
    hasErrors = true;
  } else {
    console.log(`✅ ${envVar}: ${value.substring(0, 10)}...`);
  }
});

// Check optional environment variables
console.log('\n📋 Optional environment variables:');
optionalEnvVars.forEach(envVar => {
  const value = process.env[envVar];
  if (!value) {
    console.log(`⚠️  ${envVar}: Not set (optional)`);
  } else {
    console.log(`✅ ${envVar}: ${value.substring(0, 10)}...`);
  }
});

// Check Node environment
console.log(`\n🌍 NODE_ENV: ${process.env.NODE_ENV || 'development'}`);

if (hasErrors) {
  console.error('\n❌ Environment validation failed! Please set the missing required environment variables.');
  process.exit(1);
} else {
  console.log('\n✅ Environment validation passed!');
} 