# PostgreSQL Database Requirement

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
