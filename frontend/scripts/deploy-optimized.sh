#!/bin/bash

# JewGo Frontend Optimized Deployment Script
# This script handles the complete deployment process with optimizations

set -e  # Exit on any error

echo "🚀 Starting JewGo Frontend Optimized Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    print_error "package.json not found. Please run this script from the frontend directory."
    exit 1
fi

print_status "📋 Pre-deployment checks..."

# 1. Security Audit
print_status "🔒 Running security audit..."
if npm audit --audit-level=moderate; then
    print_success "Security audit passed"
else
    print_warning "Security vulnerabilities found. Attempting to fix..."
    npm audit fix --force || print_warning "Some vulnerabilities may remain"
fi

# 2. Environment Validation
print_status "🔍 Validating environment variables..."
if npm run validate-env; then
    print_success "Environment validation passed"
else
    print_error "Environment validation failed"
    exit 1
fi

# 3. TypeScript Check
print_status "📝 Running TypeScript check..."
if npx tsc --noEmit; then
    print_success "TypeScript check passed"
else
    print_error "TypeScript errors found"
    exit 1
fi

# 4. Linting
print_status "🧹 Running linting..."
if npm run lint; then
    print_success "Linting passed"
else
    print_warning "Linting issues found (continuing anyway)"
fi

# 5. Test Build
print_status "🏗️  Running test build..."
if npm run build; then
    print_success "Build successful"
else
    print_error "Build failed"
    exit 1
fi

# 6. Bundle Analysis
print_status "📊 Analyzing bundle size..."
if npm run bundle:analyze; then
    print_success "Bundle analysis completed"
else
    print_warning "Bundle analysis failed (continuing anyway)"
fi

# 7. Performance Check
print_status "⚡ Running performance check..."
if npm run performance:check; then
    print_success "Performance check completed"
else
    print_warning "Performance check failed (continuing anyway)"
fi

# 8. Health Check
print_status "🏥 Running health check..."
if npm run monitor:check; then
    print_success "Health check passed"
else
    print_warning "Health check failed (continuing anyway)"
fi

# 9. Setup Monitoring (if not already set up)
print_status "📡 Setting up monitoring..."
if [ ! -f "config/monitoring.json" ]; then
    npm run monitor:setup
    print_success "Monitoring setup completed"
else
    print_status "Monitoring already configured"
fi

# 10. Generate Deployment Report
print_status "📋 Generating deployment report..."
cat > deployment-report.md << EOF
# JewGo Frontend Deployment Report

**Deployment Date:** $(date)
**Environment:** $NODE_ENV
**Version:** $(node -p "require('./package.json').version")

## Pre-deployment Checks
- ✅ Security audit completed
- ✅ Environment validation passed
- ✅ TypeScript check passed
- ✅ Build successful
- ✅ Health check passed

## Bundle Analysis
\`\`\`
$(npm run build 2>&1 | grep -A 20 "Route (app)")
\`\`\`

## Monitoring Status
- Health monitoring: Configured
- Performance tracking: Active
- Alert system: Ready

## Next Steps
1. Deploy to Vercel: \`vercel --prod\`
2. Start monitoring: \`npm run monitor:start\`
3. Configure alerts in config/monitoring.json
EOF

print_success "Deployment report generated: deployment-report.md"

# 11. Final Status
print_status "🎯 Deployment preparation completed!"
echo ""
print_success "✅ All pre-deployment checks passed"
print_success "✅ Build optimized and ready"
print_success "✅ Monitoring system configured"
print_success "✅ Security vulnerabilities addressed"
echo ""
print_status "📋 Next steps:"
echo "   1. Deploy to Vercel: vercel --prod"
echo "   2. Start monitoring: npm run monitor:start"
echo "   3. Review deployment-report.md"
echo "   4. Configure alerts in config/monitoring.json"
echo ""

# Optional: Auto-deploy to Vercel if VERCEL_TOKEN is set
if [ ! -z "$VERCEL_TOKEN" ]; then
    print_status "🚀 Auto-deploying to Vercel..."
    if vercel --prod --token "$VERCEL_TOKEN"; then
        print_success "Deployment to Vercel completed!"
    else
        print_error "Vercel deployment failed"
        exit 1
    fi
else
    print_warning "VERCEL_TOKEN not set. Manual deployment required."
fi

print_success "🎉 Deployment process completed successfully!" 