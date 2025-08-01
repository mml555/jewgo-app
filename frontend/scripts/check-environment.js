#!/usr/bin/env node

/**
 * Environment Variables Check Script
 * 
 * This script checks if all required environment variables are properly configured.
 * Run this script to verify your setup before starting the application.
 */

const fs = require('fs');
const path = require('path');

// Required environment variables
const requiredEnvVars = {
  'NEXT_PUBLIC_GOOGLE_MAPS_API_KEY': 'Google Maps API key for maps and places functionality',
  'NEXT_PUBLIC_BACKEND_URL': 'Backend API URL (optional, has default)',
  'NEXTAUTH_URL': 'NextAuth URL (optional, has default)',
  'NEXTAUTH_SECRET': 'NextAuth secret (optional, has default)',
};

// Check if .env.local exists
const envPath = path.join(process.cwd(), '.env.local');
const envExists = fs.existsSync(envPath);

console.log('🔍 Checking environment configuration...\n');

if (!envExists) {
  console.log('⚠️  .env.local file not found');
  console.log('   Create a .env.local file in the frontend directory with the following variables:\n');
} else {
  console.log('✅ .env.local file found');
  
  // Load and parse .env.local
  const envContent = fs.readFileSync(envPath, 'utf8');
  const envVars = {};
  
  envContent.split('\n').forEach(line => {
    const [key, ...valueParts] = line.split('=');
    if (key && valueParts.length > 0) {
      envVars[key.trim()] = valueParts.join('=').trim();
    }
  });
  
  console.log('\n📋 Environment variables status:\n');
  
  let allGood = true;
  
  Object.entries(requiredEnvVars).forEach(([key, description]) => {
    const value = envVars[key];
    const hasValue = value && value !== '';
    
    if (hasValue) {
      console.log(`✅ ${key}: ${value.substring(0, 10)}...`);
    } else {
      console.log(`❌ ${key}: Missing`);
      console.log(`   Description: ${description}`);
      allGood = false;
    }
  });
  
  if (allGood) {
    console.log('\n🎉 All required environment variables are configured!');
    console.log('   You can now start the application.');
  } else {
    console.log('\n⚠️  Some environment variables are missing.');
    console.log('   Please add them to your .env.local file before starting the application.');
  }
}

console.log('\n📝 Example .env.local file:');
console.log('```');
Object.entries(requiredEnvVars).forEach(([key, description]) => {
  console.log(`${key}=your_${key.toLowerCase().replace(/next_public_/g, '').replace(/_/g, '_')}_here`);
});
console.log('```');

console.log('\n🔗 Helpful links:');
console.log('   • Google Maps API Setup: https://developers.google.com/maps/documentation/javascript/get-api-key');
console.log('   • NextAuth.js Setup: https://next-auth.js.org/configuration/options');
console.log('   • Environment Variables: https://nextjs.org/docs/basic-features/environment-variables');

process.exit(0); 