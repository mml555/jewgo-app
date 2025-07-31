# 🍽️ JewGo - Kosher Restaurant Finder

A comprehensive web application for finding and discovering kosher restaurants with detailed kosher supervision information.

## 📁 Project Structure

```
jewgo-app/
├── 📁 backend/                    # Backend services and API
│   ├── 📁 database/              # Database management and setup
│   │   ├── database_manager_v3.py    # Main database manager
│   │   ├── init_database.py          # Database initialization
│   │   ├── setup_neon.py             # Neon database setup
│   │   ├── setup_database.py         # Database setup utilities
│   │   └── migrations/               # Database migration files
│   ├── 📁 scrapers/               # Web scraping services
│   │   └── orb_scraper_v2.py         # ORB Kosher scraper
│   ├── 📁 config/                 # Configuration files
│   │   ├── config.py                  # Main configuration
│   │   ├── gunicorn.conf.py           # Gunicorn server config
│   │   ├── env.production.example     # Environment variables template
│   │   └── ngrok.yml                  # Ngrok configuration
│   ├── 📁 utils/                  # Backend utilities
│   │   └── [utility scripts]
│   ├── 📁 scraper_env/            # Scraper virtual environment
│   └── 📁 venv/                   # Backend virtual environment
├── 📁 frontend/                   # Next.js frontend application
│   ├── 📁 components/             # React components
│   ├── 📁 pages/                  # Next.js pages
│   ├── 📁 styles/                 # CSS and styling
│   ├── 📁 utils/                  # Frontend utilities
│   ├── 📁 public/                 # Static assets
│   ├── 📁 types/                  # TypeScript type definitions
│   ├── 📁 lib/                    # Frontend libraries
│   ├── 📁 .next/                  # Next.js build output
│   ├── 📁 node_modules/           # Node.js dependencies
│   ├── 📁 out/                    # Static export output
│   ├── 📁 coverage/               # Test coverage reports
│   ├── 📁 .swc/                   # SWC compiler cache
│   ├── next.config.js             # Next.js configuration
│   ├── tailwind.config.js         # Tailwind CSS configuration
│   ├── postcss.config.js          # PostCSS configuration
│   ├── package.json               # Frontend dependencies
│   ├── package-lock.json          # Locked dependencies
│   ├── next-env.d.ts              # Next.js TypeScript config
│   ├── .nvmrc                     # Node.js version
│   ├── _headers                   # Vercel headers
│   ├── _redirects                 # Vercel redirects
│   ├── .vercelignore              # Vercel ignore rules
│   └── index.html                 # Main HTML file
├── 📁 docs/                       # Documentation
│   ├── 📁 api/                    # API documentation
│   ├── 📁 database/               # Database documentation
│   ├── 📁 deployment/             # Deployment guides
│   ├── 📁 development/            # Development guides
│   ├── ORB_SCRAPER_V2_README.md   # ORB scraper documentation
│   ├── FINAL_ORB_IMPLEMENTATION_SUMMARY.md
│   ├── CURRENT_ORB_SYSTEM_STATUS.md
│   ├── UPDATED_SCRIPTS_AND_DOCUMENTATION_SUMMARY.md
│   ├── DATABASE_CLEANUP_AND_ORGANIZATION_SUMMARY.md
│   ├── CLEANUP_SUMMARY.md
│   ├── HEALTH_CHECK_SUMMARY.md
│   ├── AUTH_ERRORS_FIX_SUMMARY.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── MONITORING.md
│   ├── COLOR_SYSTEM_GUIDE.md
│   ├── COMPATIBILITY_ANALYSIS_SUMMARY.md
│   └── README.md                  # This file
├── 📁 scripts/                    # Utility and maintenance scripts
│   ├── 📁 database/               # Database scripts
│   ├── 📁 deployment/             # Deployment scripts
│   ├── 📁 testing/                # Testing scripts
│   └── 📁 maintenance/            # Maintenance and cleanup scripts
├── 📁 data/                       # Data files and exports
│   ├── 📁 exports/                # Data exports
│   ├── 📁 backups/                # Database backups
│   └── 📁 test/                   # Test data
├── 📁 monitoring/                 # Monitoring and health checks
│   ├── 📁 logs/                   # Log files
│   └── 📁 health_checks/          # Health check scripts
├── 📁 .github/                    # GitHub configuration
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Python project configuration
├── .python-version                # Python version
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11
- Node.js 18+
- PostgreSQL database (Neon recommended)

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r ../requirements.txt

# Set up environment variables
cp config/env.production.example .env
# Edit .env with your database credentials

# Initialize database
python database/init_database.py
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🗄️ Database

### Current State
- **Total restaurants**: 107
- **Dairy restaurants**: 99
- **Pareve restaurants**: 8
- **Chalav Yisroel**: 104
- **Chalav Stam**: 3
- **Pas Yisroel**: 22

### Schema
The database uses a consolidated `restaurants` table with 28 optimized columns:
- Core restaurant information (name, address, contact)
- Kosher supervision details (Chalav Yisroel, Pas Yisroel, etc.)
- ORB certification information
- Timestamps and metadata

## 🔧 Key Components

### Backend
- **Database Manager**: Handles all database operations with SQLAlchemy
- **ORB Scraper**: Extracts kosher restaurant data from ORB Kosher website
- **API Server**: Provides RESTful endpoints for frontend consumption

### Frontend
- **Next.js Application**: Modern React-based frontend
- **Restaurant Cards**: Display kosher supervision information
- **Filtering System**: Filter by kosher type and supervision level
- **Responsive Design**: Mobile-friendly interface

## 📊 Data Sources

### ORB Kosher
- Primary data source for kosher restaurant information
- Automated scraping with duplicate prevention
- Real-time kosher supervision categorization
- Manual curation for Chalav Yisroel and Pas Yisroel status

## 🛠️ Development

### Adding New Features
1. Create feature branch from `main`
2. Implement changes in appropriate directory
3. Update documentation in `docs/`
4. Test thoroughly
5. Submit pull request

### Code Organization
- **Backend**: Python with SQLAlchemy and FastAPI
- **Frontend**: Next.js with TypeScript and Tailwind CSS
- **Database**: PostgreSQL with optimized schema
- **Documentation**: Markdown files in `docs/`

## 📈 Monitoring

### Health Checks
- Database connectivity monitoring
- API endpoint health checks
- Scraper status monitoring
- Performance metrics tracking

### Logs
- Structured logging with `structlog`
- Error tracking and alerting
- Performance monitoring
- User activity analytics

## 🚀 Deployment

### Backend Deployment
- **Platform**: Render.com
- **Database**: Neon PostgreSQL
- **Environment**: Production with SSL

### Frontend Deployment
- **Platform**: Vercel
- **CDN**: Global edge network
- **Performance**: Optimized builds

## 📚 Documentation

### API Documentation
- RESTful endpoints documentation
- Request/response schemas
- Authentication details
- Rate limiting information

### Database Documentation
- Schema design and relationships
- Migration procedures
- Backup and recovery
- Performance optimization

### Development Guides
- Local development setup
- Testing procedures
- Code style guidelines
- Contribution workflow

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the documentation in `docs/`
- Review existing issues
- Create a new issue with detailed information

---

**JewGo** - Making kosher dining discovery easy and reliable! 🍽️✡️ 