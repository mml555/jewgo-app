#!/usr/bin/env python3
"""
Cleanup Old ORB Scripts
Delete all old ORB-related scripts that are no longer needed.
"""

import os
import shutil

def cleanup_old_scripts():
    """Delete old ORB-related scripts."""
    
    # List of old scripts to delete
    old_scripts = [
        # Old ORB scrapers
        'orb_kosher_scraper.py',
        'orb_scraper.py',
        'orb_static_scraper.py',
        'basic_orb_scraper.py',
        'simple_orb_scraper.py',
        'selenium_orb_scraper.py',
        'test_orb_scraper.py',
        'test_orb_scraper_no_db.py',
        'test_orb_categories.py',
        'test_orb_website.py',
        'test_page_structure.py',
        'test_scraper.py',
        
        # Old data processing scripts
        'fix_chalav_yisroel_local.py',
        'fix_kosher_categories.py',
        'fix_kosher_categories_from_orb.py',
        'revert_kosher_categories.py',
        'replace_with_orb_data.py',
        'check_pareve.py',
        'update_cholov_yisroel.py',
        'fix_kosher_types.py',
        'update_kosher_types_simple.py',
        'populate_kosher_types.py',
        'fix_restaurants_schema.sql',
        'consolidate_data.py',
        'format_for_postgresql.py',
        'format_restaurant_data.py',
        'improve_frontend_display.py',
        'fix_restaurant_data_quality.py',
        'enhanced_restaurants.json',
        'orb_restaurants_20250730_182452.json',
        'orb_scraped_data.json',
        'local_restaurants.json',
        'local_restaurants_backup_20250730_232240.json',
        'local_restaurants_backup_20250730_231546.json',
        'local_restaurants_backup_20250730_231112.json',
        'local_restaurants_backup_20250730_233246.json',
        'local_restaurants_backup_20250730_233316.json',
        
        # Old test files
        'test_updated_api.py',
        'test_import_errors.py',
        'test_orb_page.py',
        'test_session.py',
        'test_schema_fix_local.py',
        'test_extra_kosher_info.py',
        'test_postgresql_restaurant.json',
        'test_orb_screenshot.png',
        'orb_page_full.html',
        'orb_page_sample.html',
        'orb_page_source.html',
        
        # Old requirements files
        'orb_scraper_requirements.txt',
        'selenium_requirements.txt',
        'simple_scraper_requirements.txt',
        'scraper_requirements.txt',
        'simple_requirements.txt',
        
        # Old setup files
        'setup_orb_scraper.py',
        'setup_scraper.sh',
        'check_python_version.py',
        'check_and_create_tables.py',
        'check_database_schema.py',
        'verify_database_url.py',
        'fix_database_schema.py',
        'enhanced_database_fix.py',
        'final_database_fix.py',
        
        # Old import/export files
        'import_orb_data.py',
        'simple_import.py',
        'export_restaurant_data.py',
        'manual_orb_data_entry.py',
        
        # Old schema files
        'orb_schema.sql',
        'schema.sql',
        
        # Old log files
        'orb_scraper.log',
        
        # Old documentation files
        'ORB_SCRAPER_README.md',
        'CHALAV_YISROEL_FIX_SUMMARY.md',
        'COMPREHENSIVE_KOSHER_STATUS_UPDATE.md',
        'FINAL_KOSHER_STATUS_FIX.md',
        'COMPLETION_SUMMARY.md',
        'VALIDATION_SUMMARY.md',
        'CODE_UPDATE_SUMMARY.md',
        'CONSOLIDATION_SUMMARY.md',
        'FRONTEND_FIXES_SUMMARY.md',
        'IMAGE_ISSUES_FIX_SUMMARY.md',
        'VERCEL_BUILD_FIX_SUMMARY.md',
        'CORS_FIX_SUMMARY.md',
        'ISSUES_FIXED_REPORT.md',
        'REACT_ERRORS_FIX_FINAL_SUMMARY.md',
        'FINAL_DEPLOYMENT_SUMMARY.md',
        'DEPLOY_WITHOUT_SHELL_GUIDE.md',
        'DEPLOYMENT_STATUS_SUMMARY.md',
        'CONTINUE_DEPLOYMENT_GUIDE.md',
        'COMPREHENSIVE_UPDATE_DOCUMENTATION.md',
        'UI_UX_ENHANCEMENTS.md',
        'ADD_EATERY_WORKFLOW.md',
        
        # Old database managers
        'database_manager.py',
        'database_manager_v2.py',
        
        # Old app files
        'app.py',
        'app_production.py',
        
        # Old hours files
        'add_sample_hours.py',
        'assign_sample_hours.py',
        'simple_hours_updater.py',
        'postgresql_hours_updater.py',
        
        # Old health files
        'health-report.json',
        
        # Old migration files
        'add_eatery_workflow.sql',
        'migrations/add_eatery_workflow.sql',
    ]
    
    deleted_count = 0
    not_found_count = 0
    
    print("🧹 Cleaning up old ORB scripts...")
    
    for script in old_scripts:
        if os.path.exists(script):
            try:
                if os.path.isdir(script):
                    shutil.rmtree(script)
                else:
                    os.remove(script)
                print(f"✅ Deleted: {script}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Failed to delete {script}: {e}")
        else:
            not_found_count += 1
    
    print(f"\n📊 Cleanup Summary:")
    print(f"✅ Deleted: {deleted_count} files")
    print(f"ℹ️  Not found: {not_found_count} files")
    print(f"📁 Total processed: {len(old_scripts)} files")
    
    # Keep only the new ORB scraper
    print(f"\n✅ Keeping: orb_scraper_v2.py (the new correct scraper)")

if __name__ == "__main__":
    cleanup_old_scripts() 