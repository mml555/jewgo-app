#!/usr/bin/env python3
"""
Fix Compatibility Issues - Address identified compatibility problems
"""

import subprocess
import sys
import os
from datetime import datetime

class CompatibilityFixer:
    def __init__(self):
        self.fixes_applied = []
        self.errors = []
    
    def fix_gunicorn_missing(self):
        """Fix missing gunicorn package"""
        print("🔧 Fixing missing gunicorn package")
        print("=" * 40)
        
        try:
            # Install gunicorn
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', 'gunicorn'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ gunicorn installed successfully")
                self.fixes_applied.append("Installed gunicorn")
                return True
            else:
                print(f"❌ Failed to install gunicorn: {result.stderr}")
                self.errors.append("Failed to install gunicorn")
                return False
                
        except Exception as e:
            print(f"❌ Error installing gunicorn: {e}")
            self.errors.append(f"Error installing gunicorn: {e}")
            return False
    
    def fix_sqlalchemy_compatibility(self):
        """Fix SQLAlchemy 2.x compatibility issues"""
        print("\n🔧 Fixing SQLAlchemy compatibility")
        print("=" * 40)
        
        try:
            # Check current SQLAlchemy version
            import sqlalchemy
            current_version = sqlalchemy.__version__
            print(f"Current SQLAlchemy version: {current_version}")
            
            if current_version.startswith('2.'):
                print("⚠️ SQLAlchemy 2.x detected - downgrading to 1.4.53 for compatibility")
                
                # Downgrade to SQLAlchemy 1.4.53
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', 'SQLAlchemy==1.4.53'
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("✅ SQLAlchemy downgraded to 1.4.53")
                    self.fixes_applied.append("Downgraded SQLAlchemy to 1.4.53")
                    return True
                else:
                    print(f"❌ Failed to downgrade SQLAlchemy: {result.stderr}")
                    self.errors.append("Failed to downgrade SQLAlchemy")
                    return False
            else:
                print("✅ SQLAlchemy version is compatible")
                return True
                
        except Exception as e:
            print(f"❌ Error fixing SQLAlchemy: {e}")
            self.errors.append(f"Error fixing SQLAlchemy: {e}")
            return False
    
    def fix_runtime_txt_version(self):
        """Fix runtime.txt version mismatch"""
        print("\n🔧 Fixing runtime.txt version")
        print("=" * 40)
        
        try:
            # Read current runtime.txt
            with open('runtime.txt', 'r') as f:
                current_runtime = f.read().strip()
            
            print(f"Current runtime.txt: {current_runtime}")
            
            if 'python-3.11.9' in current_runtime:
                print("⚠️ Updating runtime.txt to Python 3.13.5")
                
                # Update runtime.txt
                with open('runtime.txt', 'w') as f:
                    f.write('python-3.13.5\n')
                
                print("✅ runtime.txt updated to python-3.13.5")
                self.fixes_applied.append("Updated runtime.txt to Python 3.13.5")
                return True
            else:
                print("✅ runtime.txt version is correct")
                return True
                
        except Exception as e:
            print(f"❌ Error fixing runtime.txt: {e}")
            self.errors.append(f"Error fixing runtime.txt: {e}")
            return False
    
    def fix_render_yaml_version(self):
        """Fix render.yaml Python version"""
        print("\n🔧 Fixing render.yaml version")
        print("=" * 40)
        
        try:
            if os.path.exists('render.yaml'):
                with open('render.yaml', 'r') as f:
                    content = f.read()
                
                print("Current render.yaml content:")
                print(content)
                
                if 'pythonVersion: "3.11.9"' in content:
                    print("⚠️ Updating render.yaml to Python 3.13.5")
                    
                    # Update Python version in render.yaml
                    updated_content = content.replace(
                        'pythonVersion: "3.11.9"',
                        'pythonVersion: "3.13.5"'
                    )
                    
                    with open('render.yaml', 'w') as f:
                        f.write(updated_content)
                    
                    print("✅ render.yaml updated to Python 3.13.5")
                    self.fixes_applied.append("Updated render.yaml to Python 3.13.5")
                    return True
                else:
                    print("✅ render.yaml version is correct")
                    return True
            else:
                print("⚠️ render.yaml not found")
                return False
                
        except Exception as e:
            print(f"❌ Error fixing render.yaml: {e}")
            self.errors.append(f"Error fixing render.yaml: {e}")
            return False
    
    def check_backend_recovery(self):
        """Check if backend has recovered"""
        print("\n🔧 Checking backend recovery")
        print("=" * 40)
        
        try:
            import requests
            
            # Test backend health
            response = requests.get('https://jewgo.onrender.com/health', timeout=10)
            
            if response.status_code == 200:
                print("✅ Backend has recovered!")
                self.fixes_applied.append("Backend recovered")
                return True
            else:
                print(f"⚠️ Backend still returning status: {response.status_code}")
                print("💡 Backend may need more time to recover or manual restart")
                return False
                
        except Exception as e:
            print(f"❌ Backend still not accessible: {e}")
            print("💡 Backend may need manual restart via Render dashboard")
            return False
    
    def update_requirements_txt(self):
        """Update requirements.txt with correct versions"""
        print("\n🔧 Updating requirements.txt")
        print("=" * 40)
        
        try:
            # Read current requirements.txt
            with open('requirements.txt', 'r') as f:
                content = f.read()
            
            print("Current requirements.txt:")
            print(content)
            
            # Update SQLAlchemy version if needed
            if 'SQLAlchemy==2.' in content:
                print("⚠️ Updating SQLAlchemy version in requirements.txt")
                
                # Replace SQLAlchemy 2.x with 1.4.53
                updated_content = content.replace(
                    'SQLAlchemy==2.0.42',
                    'SQLAlchemy==1.4.53'
                )
                
                with open('requirements.txt', 'w') as f:
                    f.write(updated_content)
                
                print("✅ requirements.txt updated")
                self.fixes_applied.append("Updated requirements.txt")
                return True
            else:
                print("✅ requirements.txt is correct")
                return True
                
        except Exception as e:
            print(f"❌ Error updating requirements.txt: {e}")
            self.errors.append(f"Error updating requirements.txt: {e}")
            return False
    
    def generate_fix_report(self):
        """Generate fix report"""
        print("\n" + "="*60)
        print("📊 COMPATIBILITY FIX REPORT")
        print("=" * 60)
        
        print(f"Fixes Applied: {len(self.fixes_applied)}")
        print(f"Errors: {len(self.errors)}")
        
        if self.fixes_applied:
            print("\n✅ Fixes Applied:")
            for fix in self.fixes_applied:
                print(f"  • {fix}")
        
        if self.errors:
            print("\n❌ Errors:")
            for error in self.errors:
                print(f"  • {error}")
        
        print(f"\n📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return len(self.errors) == 0
    
    def run_all_fixes(self):
        """Run all compatibility fixes"""
        print("🔧 Running Compatibility Fixes")
        print("=" * 60)
        
        fixes = [
            self.fix_gunicorn_missing,
            self.fix_sqlalchemy_compatibility,
            self.fix_runtime_txt_version,
            self.fix_render_yaml_version,
            self.update_requirements_txt,
            self.check_backend_recovery
        ]
        
        for fix in fixes:
            try:
                fix()
            except Exception as e:
                print(f"❌ Error running {fix.__name__}: {e}")
                self.errors.append(f"Fix failed: {fix.__name__}")
        
        return self.generate_fix_report()

def main():
    """Main function"""
    fixer = CompatibilityFixer()
    success = fixer.run_all_fixes()
    
    if success:
        print("\n🎉 All compatibility fixes completed successfully!")
        print("✅ Your system should now be fully compatible")
        
        print("\n🔄 Next Steps:")
        print("1. Run compatibility check again: python compatibility_check.py")
        print("2. If backend recovered, test restaurant import")
        print("3. Deploy changes to Render if needed")
    else:
        print("\n⚠️ Some fixes failed")
        print("🔧 Please review the errors above and address them manually")
    
    return success

if __name__ == "__main__":
    main() 