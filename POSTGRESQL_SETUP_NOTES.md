# PostgreSQL Setup Notes

## Database URL Format

When setting the DATABASE_URL environment variable in Render, use this format:

```
postgresql://neondb_owner:npg_75MGzUgStfuO@ep-snowy-firefly-aeeo0tbc-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

The application will automatically convert this to use the psycopg3 driver internally.

## Environment Variables for Render

Set these environment variables in your Render service:

1. **DATABASE_URL**: The PostgreSQL connection string (see above)
2. **FLASK_ENV**: Set to `production`

## Testing

After setting the environment variables, the backend should show:
- Database: PostgreSQL (instead of SQLite)
- Environment: production (instead of development)
