# PostgreSQL Setup Notes

## Database URL Format

When setting the DATABASE_URL environment variable in Render, use this format:

```
postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

The application uses SQLAlchemy 1.4.53 with psycopg3, which works with the standard postgresql:// URL format.

## Environment Variables for Render

Set these environment variables in your Render service:

1. **DATABASE_URL**: The PostgreSQL connection string (see above)
2. **FLASK_ENV**: Set to `production`

## Testing

After setting the environment variables, the backend should show:
- Database: PostgreSQL (instead of SQLite)
- Environment: production (instead of development)

## Technical Details

- SQLAlchemy 1.4.53
- psycopg3 3.2.9
- Python 3.13.5
- Standard postgresql:// URL format
