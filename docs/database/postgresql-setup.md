# 🗄️ PostgreSQL Database Setup Guide

## 🚀 **Quick Setup Options**

### **Option 1: Neon (Recommended - Free Tier)**

**Step 1: Create Neon Account**
1. Go to [neon.tech](https://neon.tech)
2. Sign up with GitHub or email
3. Create a new project

**Step 2: Get Database URL**
1. In your Neon dashboard, click on your project
2. Go to "Connection Details"
3. Copy the connection string
4. It will look like: `postgresql://username:password@host.neon.tech:5432/database_name`

**Step 3: Set Environment Variable**
```bash
export DATABASE_URL="postgresql://username:password@host.neon.tech:5432/database_name"
```

### **Option 2: Supabase (Free Tier)**

**Step 1: Create Supabase Account**
1. Go to [supabase.com](https://supabase.com)
2. Sign up with GitHub
3. Create a new project

**Step 2: Get Database URL**
1. In your Supabase dashboard, go to Settings > Database
2. Copy the connection string
3. It will look like: `postgresql://postgres:password@host.supabase.co:5432/postgres`

**Step 3: Set Environment Variable**
```bash
export DATABASE_URL="postgresql://postgres:password@host.supabase.co:5432/postgres"
```

### **Option 3: Railway (Free Tier)**

**Step 1: Create Railway Account**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Create a new project

**Step 2: Add PostgreSQL Service**
1. Click "New Service" > "Database" > "PostgreSQL"
2. Wait for the database to be created
3. Go to the PostgreSQL service > "Variables" tab
4. Copy the `DATABASE_URL`

**Step 3: Set Environment Variable**
```bash
export DATABASE_URL="postgresql://username:password@host.railway.app:5432/database_name"
```

### **Option 4: Local PostgreSQL (Development)**

**Step 1: Install PostgreSQL**
```bash
# macOS with Homebrew
brew install postgresql
brew services start postgresql

# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Step 2: Create Database**
```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE jewgo;
CREATE USER jewgo_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE jewgo TO jewgo_user;
\q
```

**Step 3: Set Environment Variable**
```bash
export DATABASE_URL="postgresql://jewgo_user:your_password@localhost:5432/jewgo"
```

## 🔧 **Setup Your Database**

Once you have your PostgreSQL URL, run the setup script:

```bash
# Make sure you're in the project directory
cd "/Users/mendell/jewgo app"

# Activate virtual environment
source venv/bin/activate

# Set your database URL
export DATABASE_URL="your_postgresql_url_here"

# Run the setup script
python setup_database.py
```

## 📝 **Environment Configuration**

Create or update your `.env` file:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database_name

# Flask Configuration
FLASK_ENV=development
FLASK_SECRET_KEY=your-secret-key-here

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:3002

# Google API Keys
GOOGLE_PLACES_API_KEY=your-google-places-api-key
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

## 🧪 **Test Your Setup**

### **Test Database Connection**
```bash
python setup_database.py
```

### **Test API Endpoints**
```bash
# Start the production Flask app
python app_production.py

# In another terminal, test the API
curl http://localhost:8081/
curl http://localhost:8081/health
curl http://localhost:8081/api/restaurants
```

### **Test with Frontend**
```bash
# Start the frontend (if not already running)
cd jewgo-frontend
npm run dev
```

## 🔄 **Migrate Existing Data**

If you have existing data in SQLite, the setup script will offer to migrate it:

```bash
python setup_database.py
# When prompted, type 'y' to migrate data
```

## 🚨 **Troubleshooting**

### **Connection Issues**
- Check your database URL format
- Verify network connectivity
- Ensure database credentials are correct
- Check if the database service is running

### **Permission Issues**
- Make sure your database user has proper permissions
- Check if the database exists
- Verify the connection string format

### **Migration Issues**
- Ensure your SQLite database file exists
- Check that the old database manager can connect
- Verify the new PostgreSQL database is accessible

## 📊 **Database Statistics**

After setup, you can check your database statistics:

```bash
curl http://localhost:8081/api/statistics
```

This will show:
- Total restaurants
- Active restaurants
- Categories count
- States count
- Agencies count

## 🎉 **Success Indicators**

✅ Database connection successful  
✅ Tables created successfully  
✅ Data migrated (if applicable)  
✅ API endpoints responding  
✅ Frontend connecting to backend  

---

**Your PostgreSQL database is now ready for production! 🚀** 