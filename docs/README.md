# JewGo App - Complete Documentation

## 🎯 Project Overview

**JewGo** is a comprehensive kosher restaurant discovery platform that helps users find and explore kosher dining options worldwide. The application features advanced filtering, real-time data, interactive maps, and detailed restaurant information with kosher certification details.

### 🌟 Key Features
- **Restaurant Discovery**: Browse and search kosher restaurants globally
- **Advanced Filtering**: Filter by kosher type, certification agency, location, and more
- **Interactive Maps**: Real-time maps with restaurant locations and custom markers
- **Detailed Information**: Comprehensive restaurant details including kosher specifications
- **User Favorites**: Save and manage favorite restaurants
- **Admin Panel**: Restaurant management and approval system
- **Mobile-First Design**: Responsive design optimized for all devices

---

## 📚 Documentation Index

### 🎨 UI/UX Documentation
- **[UI/UX Enhancements](./UI_UX_ENHANCEMENTS.md)** - Complete RestaurantCard redesign and frontend improvements
- **[Component Architecture](./COMPONENT_ARCHITECTURE.md)** - Frontend component structure and patterns

### 🗄️ Database Documentation
- **[Database Schema Changes](./DATABASE_SCHEMA_CHANGES.md)** - Complete database evolution and schema documentation
- **[Data Migration Guide](./DATA_MIGRATION_GUIDE.md)** - Step-by-step migration procedures

### 🕷️ Scraping Documentation
- **[ORB Scraping Process](./ORB_SCRAPING_PROCESS.md)** - Comprehensive web scraping system documentation
- **[Data Pipeline](./DATA_PIPELINE.md)** - Data processing and enrichment workflows

### 🔧 Technical Documentation
- **[API Documentation](./API_DOCUMENTATION.md)** - RESTful API endpoints and usage
- **[Deployment Guide](./DEPLOYMENT_GUIDE.md)** - Production deployment procedures
- **[Performance Optimization](./PERFORMANCE_OPTIMIZATION.md)** - Performance tuning and monitoring

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ (Frontend)
- **Python** 3.11 (Backend)
- **PostgreSQL** 14+ (Database)
- **Git** (Version Control)

### Installation

#### 1. Clone Repository
```bash
git clone https://github.com/mml555/jewgo-app.git
cd jewgo-app
```

#### 2. Frontend Setup
```bash
# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your configuration

# Start development server
npm run dev
```

#### 3. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
python manage.py migrate

# Start development server
python app.py
```

#### 4. Database Setup
```bash
# Create database
createdb jewgo_app

# Run schema setup
psql -d jewgo_app -f schema.sql

# Import initial data (optional)
python scripts/import_orb_data.py
```

---

## 🏗️ Architecture Overview

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Database      │
│   (Next.js)     │◄──►│   (Python)      │◄──►│   (PostgreSQL)  │
│                 │    │                 │    │                 │
│ • React         │    │ • FastAPI       │    │ • Restaurants   │
│ • TypeScript    │    │ • SQLAlchemy    │    │ • Users         │
│ • Tailwind CSS  │    │ • Pydantic      │    │ • Reviews       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   External      │    │   Scraping      │    │   Monitoring    │
│   Services      │    │   System        │    │   & Analytics   │
│                 │    │                 │    │                 │
│ • Google Maps   │    │ • ORB Scraper   │    │ • Sentry        │
│ • Geocoding     │    │ • Data Pipeline │    │ • Analytics     │
│ • Weather API   │    │ • Validation    │    │ • Health Checks │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack

#### Frontend
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context + Local Storage
- **Maps**: Google Maps API + Leaflet
- **Authentication**: NextAuth.js

#### Backend
- **Framework**: FastAPI (Python)
- **Database ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Authentication**: JWT Tokens
- **Caching**: Redis (optional)
- **Task Queue**: Celery (optional)

#### Database
- **Primary**: PostgreSQL 14+
- **Migrations**: Alembic
- **Backup**: Automated daily backups
- **Monitoring**: pg_stat_statements

#### Infrastructure
- **Hosting**: Vercel (Frontend) + Railway (Backend)
- **Database**: Railway PostgreSQL
- **CDN**: Vercel Edge Network
- **Monitoring**: Sentry + Custom Analytics

---

## 📊 Data Flow

### Restaurant Data Pipeline
```
1. ORB Website Scraping
   ↓
2. Data Extraction & Validation
   ↓
3. Data Cleaning & Standardization
   ↓
4. Data Enrichment (Geocoding, Google Integration)
   ↓
5. Database Storage
   ↓
6. API Serving
   ↓
7. Frontend Display
```

### User Interaction Flow
```
1. User Search/Filter
   ↓
2. API Query Processing
   ↓
3. Database Query Optimization
   ↓
4. Results Formatting
   ↓
5. Frontend Rendering
   ↓
6. User Interaction
```

---

## 🔧 Development Workflow

### Code Standards
- **Frontend**: ESLint + Prettier + TypeScript strict mode
- **Backend**: Black + isort + mypy
- **Database**: SQL formatting standards
- **Git**: Conventional commits

### Testing Strategy
- **Unit Tests**: Jest (Frontend) + pytest (Backend)
- **Integration Tests**: API endpoint testing
- **E2E Tests**: Playwright for critical user flows
- **Performance Tests**: Lighthouse CI

### Deployment Pipeline
```
1. Code Commit
   ↓
2. Automated Testing
   ↓
3. Code Quality Checks
   ↓
4. Build Process
   ↓
5. Staging Deployment
   ↓
6. Production Deployment
   ↓
7. Health Checks
```

---

## 📈 Performance Metrics

### Current Performance
- **Frontend Load Time**: < 2 seconds
- **API Response Time**: < 500ms average
- **Database Query Time**: < 100ms average
- **Image Optimization**: WebP format with fallbacks
- **Caching**: 95% cache hit rate

### Optimization Strategies
- **Code Splitting**: Lazy loading of components
- **Image Optimization**: Next.js Image component
- **Database Indexing**: Optimized query performance
- **CDN**: Global content delivery
- **Caching**: Multi-layer caching strategy

---

## 🔒 Security Features

### Authentication & Authorization
- **JWT Tokens**: Secure session management
- **Role-based Access**: Admin vs user permissions
- **Password Security**: Hashing and salting
- **Session Management**: Secure session handling

### Data Protection
- **Input Validation**: Prevent injection attacks
- **CORS Configuration**: Proper cross-origin settings
- **HTTPS Enforcement**: Secure data transmission
- **Environment Variables**: Secure configuration management

### API Security
- **Rate Limiting**: Prevent abuse and DDoS
- **Input Sanitization**: Clean user inputs
- **Error Handling**: Secure error messages
- **Audit Logging**: Track security events

---

## 📱 Mobile Experience

### Responsive Design
- **Mobile-First**: Optimized for mobile devices
- **Touch-Friendly**: Large touch targets
- **Progressive Web App**: Offline capabilities
- **Fast Loading**: Optimized for slow connections

### Mobile Features
- **Location Services**: GPS-based restaurant discovery
- **Offline Maps**: Cached map data
- **Push Notifications**: Restaurant updates
- **Native Feel**: Smooth animations and transitions

---

## 🌍 Internationalization

### Multi-Language Support
- **Languages**: English, Hebrew (planned)
- **RTL Support**: Right-to-left text direction
- **Localization**: Date, time, and number formatting
- **Cultural Adaptation**: Kosher-specific terminology

### Global Features
- **Multi-Currency**: Price display in local currency
- **Time Zones**: Local time display
- **Regional Content**: Location-specific information
- **Cultural Sensitivity**: Respectful content presentation

---

## 🔮 Roadmap

### Short Term (Next 3 Months)
- [ ] User review system
- [ ] Advanced search filters
- [ ] Restaurant photo galleries
- [ ] Push notifications
- [ ] Offline mode improvements

### Medium Term (3-6 Months)
- [ ] Mobile app development
- [ ] Social features
- [ ] Restaurant owner portal
- [ ] Advanced analytics
- [ ] Machine learning recommendations

### Long Term (6+ Months)
- [ ] International expansion
- [ ] API marketplace
- [ ] White-label solutions
- [ ] Advanced AI features
- [ ] Blockchain integration

---

## 🤝 Contributing

### Getting Started
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Development Guidelines
- Follow the existing code style
- Write comprehensive tests
- Update documentation
- Ensure accessibility compliance
- Test on multiple devices

### Code Review Process
1. Automated checks pass
2. Code review by maintainers
3. Testing in staging environment
4. Merge to main branch
5. Deploy to production

---

## 📞 Support & Contact

### Documentation
- **Technical Docs**: This documentation
- **API Docs**: `/api/docs` (when running)
- **Component Library**: Storybook (planned)

### Community
- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: General questions and ideas
- **Contributing**: Development guidelines

### Contact Information
- **Email**: support@jewgo.app
- **GitHub**: https://github.com/mml555/jewgo-app
- **Website**: https://jewgo.app

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

## 🙏 Acknowledgments

### Open Source Libraries
- **Next.js**: React framework
- **Tailwind CSS**: Utility-first CSS framework
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Reliable database system
- **BeautifulSoup**: Web scraping library

### Community Contributors
- **ORB**: Kosher certification data
- **Google Maps**: Mapping and geolocation services
- **Open Source Community**: Various libraries and tools

---

*Last Updated: January 2025*
*Version: 1.0.0*

---

## 📋 Quick Reference

### Common Commands
```bash
# Frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run test         # Run tests
npm run lint         # Lint code

# Backend
python app.py        # Start development server
python -m pytest     # Run tests
python manage.py migrate  # Run database migrations

# Database
psql -d jewgo_app    # Connect to database
python scripts/import_orb_data.py  # Import ORB data
```

### Environment Variables
```bash
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_key
NEXTAUTH_SECRET=your_secret

# Backend (.env)
DATABASE_URL=postgresql://user:pass@localhost/jewgo_app
JWT_SECRET=your_jwt_secret
GOOGLE_MAPS_API_KEY=your_key
```

### API Endpoints
```
GET  /api/restaurants          # List restaurants
GET  /api/restaurants/{id}     # Get restaurant details
POST /api/restaurants          # Add restaurant (admin)
PUT  /api/restaurants/{id}     # Update restaurant (admin)
GET  /api/health              # Health check
``` 