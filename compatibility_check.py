#!/usr/bin/env python3
"""
Comprehensive Compatibility Check - Verify all services and languages work together
"""

import requests
import json
import subprocess
import sys
import platform
from datetime import datetime

class CompatibilityChecker:
    def __init__(self):
        self.results = {}
        self.issues = []
        
    def check_python_version(self):
        """Check Python version compatibility"""
        print("🐍 Checking Python Version")
        print("=" * 30)
        
        python_version = sys.version_info
        print(f"Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check if Python 3.13 is compatible with our dependencies
        if python_version.major == 3 and python_version.minor >= 13:
            print("✅ Python 3.13+ detected - compatible with our setup")
            self.results['python_version'] = True
        else:
            print("❌ Python version may have compatibility issues")
            self.results['python_version'] = False
            self.issues.append("Python version compatibility")
        
        return self.results['python_version']
    
    def check_node_version(self):
        """Check Node.js version compatibility"""
        print("\n🟢 Checking Node.js Version")
        print("=" * 30)
        
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                node_version = result.stdout.strip()
                print(f"Node.js Version: {node_version}")
                
                # Parse version (remove 'v' prefix)
                version_parts = node_version.replace('v', '').split('.')
                major = int(version_parts[0])
                minor = int(version_parts[1])
                
                if major >= 18:
                    print("✅ Node.js 18+ detected - compatible with Next.js")
                    self.results['node_version'] = True
                else:
                    print("❌ Node.js version may be too old for Next.js")
                    self.results['node_version'] = False
                    self.issues.append("Node.js version compatibility")
            else:
                print("❌ Node.js not found or not accessible")
                self.results['node_version'] = False
                self.issues.append("Node.js not installed")
                
        except Exception as e:
            print(f"❌ Error checking Node.js: {e}")
            self.results['node_version'] = False
            self.issues.append("Node.js check failed")
        
        return self.results.get('node_version', False)
    
    def check_npm_version(self):
        """Check npm version compatibility"""
        print("\n📦 Checking npm Version")
        print("=" * 30)
        
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                npm_version = result.stdout.strip()
                print(f"npm Version: {npm_version}")
                
                version_parts = npm_version.split('.')
                major = int(version_parts[0])
                
                if major >= 8:
                    print("✅ npm 8+ detected - compatible with modern packages")
                    self.results['npm_version'] = True
                else:
                    print("❌ npm version may be too old")
                    self.results['npm_version'] = False
                    self.issues.append("npm version compatibility")
            else:
                print("❌ npm not found or not accessible")
                self.results['npm_version'] = False
                self.issues.append("npm not installed")
                
        except Exception as e:
            print(f"❌ Error checking npm: {e}")
            self.results['npm_version'] = False
            self.issues.append("npm check failed")
        
        return self.results.get('npm_version', False)
    
    def check_python_dependencies(self):
        """Check Python package compatibility"""
        print("\n🐍 Checking Python Dependencies")
        print("=" * 30)
        
        try:
            # Check key packages
            packages_to_check = [
                'flask', 'sqlalchemy', 'psycopg', 'requests', 'gunicorn'
            ]
            
            for package in packages_to_check:
                try:
                    __import__(package)
                    print(f"✅ {package} - installed")
                except ImportError:
                    print(f"❌ {package} - not installed")
                    self.issues.append(f"Missing Python package: {package}")
            
            # Check specific versions
            import flask
            import sqlalchemy
            import requests
            
            print(f"Flask Version: {flask.__version__}")
            print(f"SQLAlchemy Version: {sqlalchemy.__version__}")
            print(f"Requests Version: {requests.__version__}")
            
            # Check for known compatibility issues
            if sqlalchemy.__version__.startswith('2.'):
                print("⚠️ SQLAlchemy 2.x detected - may have compatibility issues with our setup")
                self.issues.append("SQLAlchemy 2.x compatibility")
            else:
                print("✅ SQLAlchemy 1.x detected - compatible")
            
            self.results['python_dependencies'] = True
            
        except Exception as e:
            print(f"❌ Error checking Python dependencies: {e}")
            self.results['python_dependencies'] = False
            self.issues.append("Python dependencies check failed")
        
        return self.results.get('python_dependencies', False)
    
    def check_node_dependencies(self):
        """Check Node.js package compatibility"""
        print("\n🟢 Checking Node.js Dependencies")
        print("=" * 30)
        
        try:
            # Check if package.json exists
            import os
            if os.path.exists('package.json'):
                with open('package.json', 'r') as f:
                    package_data = json.load(f)
                
                print("✅ package.json found")
                print(f"Project Name: {package_data.get('name', 'Unknown')}")
                print(f"Node Version: {package_data.get('engines', {}).get('node', 'Not specified')}")
                
                # Check key dependencies
                dependencies = package_data.get('dependencies', {})
                dev_dependencies = package_data.get('devDependencies', {})
                
                key_packages = ['next', 'react', 'react-dom']
                for package in key_packages:
                    if package in dependencies:
                        print(f"✅ {package}: {dependencies[package]}")
                    elif package in dev_dependencies:
                        print(f"✅ {package} (dev): {dev_dependencies[package]}")
                    else:
                        print(f"❌ {package} - not found")
                        self.issues.append(f"Missing Node.js package: {package}")
                
                self.results['node_dependencies'] = True
            else:
                print("❌ package.json not found")
                self.results['node_dependencies'] = False
                self.issues.append("package.json not found")
                
        except Exception as e:
            print(f"❌ Error checking Node.js dependencies: {e}")
            self.results['node_dependencies'] = False
            self.issues.append("Node.js dependencies check failed")
        
        return self.results.get('node_dependencies', False)
    
    def check_backend_services(self):
        """Check backend service compatibility"""
        print("\n🔧 Checking Backend Services")
        print("=" * 30)
        
        services = {
            'render_backend': 'https://jewgo.onrender.com/health',
            'vercel_frontend': 'https://jewgo-app.vercel.app',
            'vercel_alt': 'https://jewgo-j953cxrfi-mml555s-projects.vercel.app'
        }
        
        for service_name, url in services.items():
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"✅ {service_name}: {url} - Online")
                    self.results[service_name] = True
                else:
                    print(f"⚠️ {service_name}: {url} - Status {response.status_code}")
                    self.results[service_name] = False
                    self.issues.append(f"{service_name} returned status {response.status_code}")
            except Exception as e:
                print(f"❌ {service_name}: {url} - Error: {e}")
                self.results[service_name] = False
                self.issues.append(f"{service_name} connection failed")
        
        return any(self.results.get(service, False) for service in services.keys())
    
    def check_database_compatibility(self):
        """Check database service compatibility"""
        print("\n🗄️ Checking Database Services")
        print("=" * 30)
        
        try:
            # Check if we can connect to the database via API
            response = requests.get('https://jewgo.onrender.com/api/restaurants?limit=1', timeout=10)
            
            if response.status_code == 200:
                print("✅ Database connection via API - Working")
                self.results['database_api'] = True
            else:
                print(f"⚠️ Database API returned status: {response.status_code}")
                self.results['database_api'] = False
                self.issues.append(f"Database API status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Database API connection failed: {e}")
            self.results['database_api'] = False
            self.issues.append("Database API connection failed")
        
        # Check PostgreSQL compatibility
        try:
            import psycopg
            print("✅ psycopg (PostgreSQL driver) - Available")
            self.results['postgresql_driver'] = True
        except ImportError:
            print("❌ psycopg not available")
            self.results['postgresql_driver'] = False
            self.issues.append("PostgreSQL driver not available")
        
        return self.results.get('database_api', False) and self.results.get('postgresql_driver', False)
    
    def check_platform_compatibility(self):
        """Check platform and OS compatibility"""
        print("\n💻 Checking Platform Compatibility")
        print("=" * 30)
        
        system = platform.system()
        release = platform.release()
        machine = platform.machine()
        
        print(f"OS: {system}")
        print(f"Release: {release}")
        print(f"Architecture: {machine}")
        
        # Check for known compatibility issues
        if system == "Darwin":  # macOS
            print("✅ macOS detected - compatible with our stack")
            self.results['platform'] = True
        elif system == "Linux":
            print("✅ Linux detected - compatible with our stack")
            self.results['platform'] = True
        elif system == "Windows":
            print("⚠️ Windows detected - may have some compatibility issues")
            self.results['platform'] = True
            self.issues.append("Windows platform may have compatibility issues")
        else:
            print(f"❌ Unknown OS: {system}")
            self.results['platform'] = False
            self.issues.append(f"Unknown OS: {system}")
        
        return self.results.get('platform', False)
    
    def check_version_requirements(self):
        """Check version requirements compatibility"""
        print("\n📋 Checking Version Requirements")
        print("=" * 30)
        
        # Check runtime.txt
        try:
            with open('runtime.txt', 'r') as f:
                runtime = f.read().strip()
            print(f"Runtime.txt: {runtime}")
            
            if 'python-3.13' in runtime:
                print("✅ Python 3.13 specified - matches our setup")
                self.results['runtime_txt'] = True
            else:
                print(f"⚠️ Runtime.txt specifies different Python version: {runtime}")
                self.results['runtime_txt'] = False
                self.issues.append(f"Runtime.txt version mismatch: {runtime}")
        except FileNotFoundError:
            print("❌ runtime.txt not found")
            self.results['runtime_txt'] = False
            self.issues.append("runtime.txt not found")
        
        # Check .nvmrc
        try:
            with open('.nvmrc', 'r') as f:
                nvmrc = f.read().strip()
            print(f".nvmrc: {nvmrc}")
            
            if '22' in nvmrc:
                print("✅ Node.js 22 specified - compatible")
                self.results['nvmrc'] = True
            else:
                print(f"⚠️ .nvmrc specifies different Node version: {nvmrc}")
                self.results['nvmrc'] = False
                self.issues.append(f".nvmrc version mismatch: {nvmrc}")
        except FileNotFoundError:
            print("❌ .nvmrc not found")
            self.results['nvmrc'] = False
            self.issues.append(".nvmrc not found")
        
        return self.results.get('runtime_txt', False) and self.results.get('nvmrc', False)
    
    def check_deployment_compatibility(self):
        """Check deployment platform compatibility"""
        print("\n🚀 Checking Deployment Compatibility")
        print("=" * 30)
        
        # Check Render compatibility
        render_files = ['render.yaml', 'Procfile', 'gunicorn.conf.py']
        for file in render_files:
            try:
                with open(file, 'r') as f:
                    print(f"✅ {file} - Found")
                self.results[f'render_{file}'] = True
            except FileNotFoundError:
                print(f"❌ {file} - Not found")
                self.results[f'render_{file}'] = False
                self.issues.append(f"Missing Render file: {file}")
        
        # Check Vercel compatibility
        vercel_files = ['vercel.json', 'next.config.js']
        for file in vercel_files:
            try:
                with open(file, 'r') as f:
                    print(f"✅ {file} - Found")
                self.results[f'vercel_{file}'] = True
            except FileNotFoundError:
                print(f"❌ {file} - Not found")
                self.results[f'vercel_{file}'] = False
                self.issues.append(f"Missing Vercel file: {file}")
        
        return True  # Return True if we can check files
    
    def generate_compatibility_report(self):
        """Generate comprehensive compatibility report"""
        print("\n" + "="*60)
        print("📊 COMPATIBILITY REPORT")
        print("="*60)
        
        total_checks = len(self.results)
        passed_checks = sum(1 for result in self.results.values() if result)
        
        print(f"Total Checks: {total_checks}")
        print(f"Passed: {passed_checks}")
        print(f"Failed: {total_checks - passed_checks}")
        print(f"Success Rate: {(passed_checks/total_checks)*100:.1f}%")
        
        print("\n📋 Detailed Results:")
        for check, result in self.results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {check}: {status}")
        
        if self.issues:
            print(f"\n⚠️ Issues Found ({len(self.issues)}):")
            for issue in self.issues:
                print(f"  • {issue}")
        else:
            print("\n🎉 No compatibility issues found!")
        
        print(f"\n📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return passed_checks == total_checks
    
    def run_all_checks(self):
        """Run all compatibility checks"""
        print("🔍 Comprehensive Compatibility Check")
        print("=" * 60)
        
        checks = [
            self.check_python_version,
            self.check_node_version,
            self.check_npm_version,
            self.check_python_dependencies,
            self.check_node_dependencies,
            self.check_backend_services,
            self.check_database_compatibility,
            self.check_platform_compatibility,
            self.check_version_requirements,
            self.check_deployment_compatibility
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                print(f"❌ Error running {check.__name__}: {e}")
                self.issues.append(f"Check failed: {check.__name__}")
        
        return self.generate_compatibility_report()

def main():
    """Main function"""
    checker = CompatibilityChecker()
    success = checker.run_all_checks()
    
    if success:
        print("\n🎉 All compatibility checks passed!")
        print("✅ Your system is fully compatible with all services")
    else:
        print("\n⚠️ Some compatibility issues found")
        print("🔧 Please review the issues above and address them")
    
    return success

if __name__ == "__main__":
    main() 