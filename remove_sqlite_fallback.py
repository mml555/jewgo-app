#!/usr/bin/env python3
"""
Remove SQLite Fallback - Update database manager to only use PostgreSQL
"""

import os
import re

def remove_sqlite_fallback():
    """Remove SQLite fallback logic from database_manager_v2.py"""
    print("🔧 Removing SQLite Fallback from Database Manager")
    print("=" * 50)
    
    # Read the current file
    with open('database_manager_v2.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Store original content for backup
    with open('database_manager_v2.py.backup', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ Created backup: database_manager_v2.py.backup")
    
    # Process the file line by line
    new_lines = []
    skip_lines = False
    changes_made = []
    
    for i, line in enumerate(lines):
        # Skip lines that are part of SQLite fallback logic
        if skip_lines:
            if 'logger.warning' in line and 'SQLite fallback' in line:
                skip_lines = False
                changes_made.append("Removed SQLite fallback logic")
            continue
        
        # Update docstring
        if 'support for both SQLite and PostgreSQL' in line:
            line = line.replace('support for both SQLite and PostgreSQL', 'PostgreSQL support only')
            changes_made.append("Updated docstring")
        
        # Update default database URL
        if "os.environ.get('DATABASE_URL', 'sqlite:///restaurants.db')" in line:
            line = line.replace("os.environ.get('DATABASE_URL', 'sqlite:///restaurants.db')", "os.environ.get('DATABASE_URL')")
            changes_made.append("Updated default database URL")
        
        # Remove SQLite configuration block
        if 'if \'sqlite\' in self.database_url.lower():' in line:
            # Skip the entire SQLite configuration block
            skip_lines = True
            # Replace with PostgreSQL-only configuration
            line = "            # PostgreSQL configuration with enhanced error handling\n"
            line += "            try:\n"
            changes_made.append("Removed SQLite configuration logic")
            continue
        
        # Remove the 'else:' clause since we're making PostgreSQL the main config
        if line.strip() == 'else:' and 'PostgreSQL configuration' in ''.join(lines[i:i+3]):
            line = "            # PostgreSQL configuration with enhanced error handling\n"
            line += "            try:\n"
            changes_made.append("Updated PostgreSQL configuration to be main configuration")
            continue
        
        # Add validation after the database_url assignment
        if 'self.database_url = database_url or os.environ.get(\'DATABASE_URL\')' in line:
            # Add validation code after this line
            new_lines.append(line)
            new_lines.append('\n')
            new_lines.append('        # Validate that DATABASE_URL is provided\n')
            new_lines.append('        if not self.database_url:\n')
            new_lines.append('            raise ValueError("DATABASE_URL environment variable is required for PostgreSQL connection")\n')
            new_lines.append('\n')
            new_lines.append('        # Ensure we\'re using PostgreSQL\n')
            new_lines.append('        if not self.database_url.startswith(\'postgresql://\'):\n')
            new_lines.append('            raise ValueError("DATABASE_URL must be a PostgreSQL connection string (postgresql://...)")\n')
            new_lines.append('\n')
            changes_made.append("Added PostgreSQL validation")
            continue
        
        # Skip SQLite fallback error handling
        if 'PostgreSQL connection completely failed, falling back to SQLite' in line:
            skip_lines = True
            continue
        
        new_lines.append(line)
    
    # Write the updated content
    with open('database_manager_v2.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✅ Made {len(changes_made)} changes to remove SQLite fallback:")
    for change in changes_made:
        print(f"   • {change}")
    
    return len(changes_made) > 0

def update_config_file():
    """Update config.py to remove SQLite references"""
    print("\n🔧 Updating config.py")
    print("=" * 30)
    
    try:
        with open('config.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create backup
        with open('config.py.backup', 'w', encoding='utf-8') as f:
            f.write(content)
        
        changes_made = []
        
        # Update any SQLite references to PostgreSQL
        if 'sqlite' in content.lower():
            # Replace any SQLite default URLs with PostgreSQL requirement
            content = re.sub(r'sqlite:///[^"\s]+', 'postgresql://', content)
            changes_made.append("Updated SQLite URLs to PostgreSQL")
        
        # Add comment about PostgreSQL requirement
        if '# Database configuration' in content:
            content = content.replace('# Database configuration', 
                                    '# Database configuration (PostgreSQL required)')
            changes_made.append("Added PostgreSQL requirement comment")
        
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated config.py with {len(changes_made)} changes")
        return True
        
    except Exception as e:
        print(f"❌ Error updating config.py: {e}")
        return False

def create_postgresql_only_readme():
    """Create a README section about PostgreSQL requirement"""
    print("\n📝 Creating PostgreSQL requirement documentation")
    print("=" * 50)
    
    readme_content = """# PostgreSQL Database Requirement

## Overview
The JewGo application now requires PostgreSQL as the primary database. SQLite fallback has been removed to ensure production stability and performance.

## Database Setup

### Environment Variables
Set the following environment variable in your deployment:

```bash
DATABASE_URL=postgresql://username:password@host:port/database_name
```

### Example for Neon.tech
```bash
DATABASE_URL=postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

### Requirements
- PostgreSQL 12 or higher
- psycopg3 driver (automatically installed via requirements.txt)
- SSL connection support

## Migration from SQLite
If you were previously using SQLite:
1. Export your data from SQLite
2. Import the data into PostgreSQL
3. Update your DATABASE_URL environment variable
4. Restart the application

## Benefits of PostgreSQL-Only
- Better performance for concurrent users
- ACID compliance for data integrity
- Advanced query capabilities
- Better scalability
- Production-ready reliability

## Troubleshooting
If you encounter database connection issues:
1. Verify DATABASE_URL is correctly formatted
2. Ensure PostgreSQL server is running and accessible
3. Check firewall and network connectivity
4. Verify SSL certificate if using SSL connections
"""
    
    with open('POSTGRESQL_REQUIREMENT.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Created POSTGRESQL_REQUIREMENT.md")

def main():
    """Main function to remove SQLite fallback"""
    print("🚀 Removing SQLite Fallback from JewGo System")
    print("=" * 60)
    
    # Remove SQLite fallback from database manager
    if remove_sqlite_fallback():
        print("\n✅ Successfully removed SQLite fallback from database manager")
    else:
        print("\n⚠️  No changes made to database manager (may already be PostgreSQL-only)")
    
    # Update config file
    if update_config_file():
        print("\n✅ Successfully updated config.py")
    else:
        print("\n⚠️  Config file update failed or not needed")
    
    # Create documentation
    create_postgresql_only_readme()
    
    print("\n🎉 SQLite Fallback Removal Complete!")
    print("📋 Summary:")
    print("   • Removed SQLite fallback logic from database_manager_v2.py")
    print("   • Updated configuration to require PostgreSQL")
    print("   • Created PostgreSQL requirement documentation")
    print("   • Backups created for both files")
    print("\n🔧 Next Steps:")
    print("   • Ensure DATABASE_URL environment variable is set")
    print("   • Test the application with PostgreSQL only")
    print("   • Deploy the updated code")

if __name__ == "__main__":
    main() 