#!/usr/bin/env python3
"""
Monitor Periodic Hours Update System
====================================

Monitors the performance and status of the periodic hours update system.
Provides insights into update frequency, success rates, and system health.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
import structlog

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

class PeriodicUpdateMonitor:
    """Monitor for the periodic hours update system."""
    
    def __init__(self, database_url: str = None):
        self.database_url = database_url or "postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    
    def get_hours_coverage_stats(self):
        """Get statistics about hours coverage."""
        try:
            engine = create_engine(self.database_url)
            
            with engine.connect() as conn:
                # Total restaurants
                total_result = conn.execute(text("SELECT COUNT(*) as total FROM restaurants"))
                total_restaurants = total_result.fetchone().total
                
                # Restaurants with hours
                with_hours_result = conn.execute(text("""
                    SELECT COUNT(*) as count 
                    FROM restaurants 
                    WHERE hours_open IS NOT NULL 
                    AND hours_open != '' 
                    AND hours_open != 'None'
                """))
                restaurants_with_hours = with_hours_result.fetchone().count
                
                # Restaurants without hours
                without_hours_result = conn.execute(text("""
                    SELECT COUNT(*) as count 
                    FROM restaurants 
                    WHERE hours_open IS NULL 
                    OR hours_open = '' 
                    OR hours_open = 'None'
                """))
                restaurants_without_hours = without_hours_result.fetchone().count
                
                # Recently updated (last 7 days)
                recent_result = conn.execute(text("""
                    SELECT COUNT(*) as count 
                    FROM restaurants 
                    WHERE updated_at >= NOW() - INTERVAL '7 days'
                """))
                recently_updated = recent_result.fetchone().count
                
                # Old hours (older than 7 days)
                old_result = conn.execute(text("""
                    SELECT COUNT(*) as count 
                    FROM restaurants 
                    WHERE updated_at < NOW() - INTERVAL '7 days'
                    AND hours_open IS NOT NULL 
                    AND hours_open != '' 
                    AND hours_open != 'None'
                """))
                old_hours = old_result.fetchone().count
                
                return {
                    'total_restaurants': total_restaurants,
                    'with_hours': restaurants_with_hours,
                    'without_hours': restaurants_without_hours,
                    'recently_updated': recently_updated,
                    'old_hours': old_hours,
                    'coverage_percentage': round((restaurants_with_hours / total_restaurants * 100), 2) if total_restaurants > 0 else 0
                }
                
        except Exception as e:
            logger.error(f"Error getting hours coverage stats", error=str(e))
            return None
    
    def get_update_frequency_stats(self):
        """Get statistics about update frequency."""
        try:
            engine = create_engine(self.database_url)
            
            with engine.connect() as conn:
                # Last update time
                last_update_result = conn.execute(text("""
                    SELECT MAX(updated_at) as last_update 
                    FROM restaurants 
                    WHERE updated_at IS NOT NULL
                """))
                last_update = last_update_result.fetchone().last_update
                
                # Average time between updates
                avg_time_result = conn.execute(text("""
                    SELECT AVG(EXTRACT(EPOCH FROM (NOW() - updated_at))) as avg_seconds
                    FROM restaurants 
                    WHERE updated_at IS NOT NULL
                """))
                avg_seconds = avg_time_result.fetchone().avg_seconds
                
                # Restaurants needing updates (older than 7 days)
                needing_updates_result = conn.execute(text("""
                    SELECT COUNT(*) as count 
                    FROM restaurants 
                    WHERE updated_at < NOW() - INTERVAL '7 days'
                    OR hours_open IS NULL 
                    OR hours_open = '' 
                    OR hours_open = 'None'
                """))
                needing_updates = needing_updates_result.fetchone().count
                
                return {
                    'last_update': last_update,
                    'avg_time_since_update': avg_seconds,
                    'needing_updates': needing_updates,
                    'days_since_last_update': (datetime.utcnow() - last_update).days if last_update else None
                }
                
        except Exception as e:
            logger.error(f"Error getting update frequency stats", error=str(e))
            return None
    
    def analyze_log_file(self, log_file_path: str = "logs/periodic_hours_update.log"):
        """Analyze the log file for recent activity."""
        if not os.path.exists(log_file_path):
            return {
                'log_file_exists': False,
                'last_run': None,
                'total_runs': 0,
                'success_rate': 0,
                'errors': 0
            }
        
        try:
            with open(log_file_path, 'r') as f:
                lines = f.readlines()
            
            # Find last run
            last_run = None
            total_runs = 0
            successful_runs = 0
            error_count = 0
            
            for line in lines:
                if "Starting periodic hours update" in line:
                    total_runs += 1
                    # Extract timestamp
                    try:
                        timestamp_str = line.split(':')[0]
                        last_run = datetime.strptime(timestamp_str.strip(), "%a %b %d %H:%M:%S %Z %Y")
                    except:
                        pass
                
                if "Total processed:" in line and "Updated:" in line:
                    # Parse results
                    try:
                        parts = line.split()
                        total_processed = int(parts[2])
                        updated = int(parts[4])
                        errors = int(parts[12])
                        
                        if total_processed > 0:
                            successful_runs += 1
                        error_count += errors
                    except:
                        pass
            
            success_rate = (successful_runs / total_runs * 100) if total_runs > 0 else 0
            
            return {
                'log_file_exists': True,
                'last_run': last_run,
                'total_runs': total_runs,
                'successful_runs': successful_runs,
                'success_rate': round(success_rate, 2),
                'errors': error_count
            }
            
        except Exception as e:
            logger.error(f"Error analyzing log file", error=str(e))
            return {
                'log_file_exists': True,
                'last_run': None,
                'total_runs': 0,
                'success_rate': 0,
                'errors': 0
            }
    
    def get_system_health_score(self):
        """Calculate a system health score based on various metrics."""
        coverage_stats = self.get_hours_coverage_stats()
        frequency_stats = self.get_update_frequency_stats()
        log_stats = self.analyze_log_file()
        
        if not coverage_stats or not frequency_stats:
            return {
                'overall_score': 0,
                'coverage_score': 0,
                'freshness_score': 0,
                'reliability_score': 0,
                'recommendations': ['Database connection issues detected']
            }
        
        # Coverage score (0-100)
        coverage_score = coverage_stats['coverage_percentage']
        
        # Freshness score (0-100)
        if frequency_stats['days_since_last_update'] is None:
            freshness_score = 0
        elif frequency_stats['days_since_last_update'] <= 1:
            freshness_score = 100
        elif frequency_stats['days_since_last_update'] <= 7:
            freshness_score = 80
        elif frequency_stats['days_since_last_update'] <= 14:
            freshness_score = 60
        elif frequency_stats['days_since_last_update'] <= 30:
            freshness_score = 40
        else:
            freshness_score = 20
        
        # Reliability score (0-100)
        reliability_score = log_stats['success_rate']
        
        # Overall score (weighted average)
        overall_score = (coverage_score * 0.4 + freshness_score * 0.3 + reliability_score * 0.3)
        
        # Generate recommendations
        recommendations = []
        
        if coverage_score < 70:
            recommendations.append("Hours coverage is low - consider running bulk update")
        
        if freshness_score < 60:
            recommendations.append("Data is getting stale - check update frequency")
        
        if reliability_score < 80:
            recommendations.append("System reliability issues detected - check logs")
        
        if frequency_stats['needing_updates'] > 0:
            recommendations.append(f"{frequency_stats['needing_updates']} restaurants need updates")
        
        return {
            'overall_score': round(overall_score, 2),
            'coverage_score': coverage_score,
            'freshness_score': freshness_score,
            'reliability_score': reliability_score,
            'recommendations': recommendations
        }
    
    def generate_report(self):
        """Generate a comprehensive monitoring report."""
        print("📊 Periodic Hours Update System - Monitoring Report")
        print("=" * 60)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Hours Coverage
        coverage_stats = self.get_hours_coverage_stats()
        if coverage_stats:
            print("📈 Hours Coverage Statistics")
            print("-" * 30)
            print(f"Total Restaurants: {coverage_stats['total_restaurants']}")
            print(f"With Hours: {coverage_stats['with_hours']}")
            print(f"Without Hours: {coverage_stats['without_hours']}")
            print(f"Coverage: {coverage_stats['coverage_percentage']}%")
            print(f"Recently Updated (7 days): {coverage_stats['recently_updated']}")
            print(f"Old Hours (>7 days): {coverage_stats['old_hours']}")
            print()
        else:
            print("❌ Could not retrieve coverage statistics")
            print()
        
        # Update Frequency
        frequency_stats = self.get_update_frequency_stats()
        if frequency_stats:
            print("⏰ Update Frequency Statistics")
            print("-" * 30)
            print(f"Last Update: {frequency_stats['last_update']}")
            print(f"Days Since Last Update: {frequency_stats['days_since_last_update']}")
            print(f"Restaurants Needing Updates: {frequency_stats['needing_updates']}")
            if frequency_stats['avg_time_since_update']:
                avg_days = frequency_stats['avg_time_since_update'] / 86400
                print(f"Average Days Since Update: {avg_days:.1f}")
            print()
        else:
            print("❌ Could not retrieve frequency statistics")
            print()
        
        # Log Analysis
        log_stats = self.analyze_log_file()
        print("📋 Log Analysis")
        print("-" * 30)
        if log_stats['log_file_exists']:
            print(f"Log File: ✅ Found")
            print(f"Total Runs: {log_stats['total_runs']}")
            print(f"Successful Runs: {log_stats['successful_runs']}")
            print(f"Success Rate: {log_stats['success_rate']}%")
            print(f"Total Errors: {log_stats['errors']}")
            if log_stats['last_run']:
                print(f"Last Run: {log_stats['last_run']}")
        else:
            print("Log File: ❌ Not found")
        print()
        
        # System Health
        health_score = self.get_system_health_score()
        print("🏥 System Health Score")
        print("-" * 30)
        print(f"Overall Score: {health_score['overall_score']}/100")
        print(f"Coverage Score: {health_score['coverage_score']}/100")
        print(f"Freshness Score: {health_score['freshness_score']}/100")
        print(f"Reliability Score: {health_score['reliability_score']}/100")
        print()
        
        if health_score['recommendations']:
            print("💡 Recommendations")
            print("-" * 30)
            for i, rec in enumerate(health_score['recommendations'], 1):
                print(f"{i}. {rec}")
            print()
        
        # Cron Job Status
        print("⏰ Scheduled Jobs Status")
        print("-" * 30)
        try:
            import subprocess
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            if result.stdout and "periodic_hours_updater.py" in result.stdout:
                print("✅ Cron job is configured")
                for line in result.stdout.split('\n'):
                    if "periodic_hours_updater.py" in line:
                        print(f"   Schedule: {line.strip()}")
            else:
                print("❌ No cron job found")
        except:
            print("❌ Could not check cron job status")
        print()

def main():
    """Main function."""
    monitor = PeriodicUpdateMonitor()
    monitor.generate_report()

if __name__ == "__main__":
    main() 