# JewGo App Documentation

## Overview

JewGo is a comprehensive kosher restaurant discovery and management platform that helps users find kosher restaurants, bakeries, and other food establishments. The platform includes advanced filtering, location-based search, and comprehensive kosher supervision information.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.11
- PostgreSQL database
- Google Places API key

### Development Setup
```bash
# Clone the repository
git clone https://github.com/mml555/jewgo-app.git
cd jewgo-app

# Frontend setup
cd frontend
npm install
npm run dev

# Backend setup
cd ../backend
pip install -r requirements.txt
python app.py
```

## 📁 Documentation Structure

### [Deployment](./deployment/README.md)
- Render deployment configuration
- Neon database setup
- Environment configuration
- Troubleshooting guides

### [Development](./development/README.md)
- Development environment setup
- Architecture overview
- Contributing guidelines
- Code standards

### [API](./api/README.md)
- API endpoints documentation
- Authentication
- Request/response formats
- Error handling

### [Database](./database/README.md)
- Database schema
- Migration guides
- Data management
- Backup procedures

### [Features](./features/README.md)
- ORB scraper system
- Advanced filtering
- Authentication system
- Monitoring and health checks

### [Maintenance](./maintenance/README.md)
- Data cleanup procedures
- Update processes
- System maintenance
- Performance optimization

## 🏗️ Architecture

### Frontend
- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React hooks
- **Maps**: Google Maps API
- **Authentication**: NextAuth.js

### Backend
- **Framework**: Flask (Python)
- **Database**: PostgreSQL with SQLAlchemy
- **ORM**: SQLAlchemy 1.4
- **API**: RESTful endpoints
- **Scraping**: ORB data integration

### Database
- **Primary**: PostgreSQL (Neon)
- **Schema**: 28 optimized columns
- **Features**: Kosher supervision flags, location data, reviews

## 🔧 Key Features

### Restaurant Discovery
- Advanced filtering by kosher type, certifying agency, location
- Map-based search with distance calculations
- Real-time availability and hours
- User reviews and ratings

### Kosher Information
- Comprehensive kosher supervision details
- Chalav Yisroel, Pas Yisroel, Glatt kosher flags
- Certifying agency information
- Kosher certificate links

### User Experience
- Mobile-responsive design
- Location-based recommendations
- Favorites system
- Add new restaurant submissions

## 📊 Current Status

- **Total Restaurants**: 107
- **Dairy Restaurants**: 99
- **Pareve Restaurants**: 8
- **Chalav Yisroel**: 104
- **Pas Yisroel**: 22

## 🔗 Quick Links

- [Live Application](https://jewgo-app.vercel.app)
- [Backend API](https://jewgo.onrender.com)
- [GitHub Repository](https://github.com/mml555/jewgo-app)

## 📞 Support

For questions or issues:
- Check the [troubleshooting guide](./deployment/troubleshooting.md)
- Review [maintenance procedures](./maintenance/README.md)
- Open an issue on GitHub

---

*Last updated: July 2024* 