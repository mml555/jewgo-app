# Development Guide

## Overview

This guide covers development setup, architecture, and contributing guidelines for the JewGo application.

## 🚀 Development Setup

### Prerequisites
- Node.js 18+
- Python 3.11
- PostgreSQL (local or Neon)
- Git

### Quick Start
```bash
# Clone repository
git clone https://github.com/mml555/jewgo-app.git
cd jewgo-app

# Frontend setup
cd frontend
npm install
npm run dev

# Backend setup (in new terminal)
cd ../backend
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## 🏗️ Architecture

### Frontend Architecture
```
frontend/
├── app/                    # Next.js App Router
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── Header.tsx         # App header
│   ├── ActionButtons.tsx  # Filter and action buttons
│   ├── RestaurantCard.tsx # Restaurant display
│   └── BottomNavigation.tsx # Mobile navigation
├── types/                 # TypeScript definitions
├── utils/                 # Utility functions
└── public/                # Static assets
```

### Backend Architecture
```
backend/
├── app.py                 # Main Flask application
├── database/              # Database management
│   └── database_manager_v3.py
├── scrapers/              # Data scraping
│   └── orb_scraper_v2.py
├── config/                # Configuration files
└── requirements.txt       # Python dependencies
```

## 🔧 Development Workflow

### 1. Feature Development
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
# Test locally
# Commit changes
git add .
git commit -m "feat: add new feature"

# Push and create PR
git push origin feature/new-feature
```

### 2. Testing
- **Frontend**: `npm run test` (if tests exist)
- **Backend**: Manual testing with Postman/curl
- **Database**: Verify data integrity
- **Integration**: Test frontend-backend communication

### 3. Code Standards

#### Frontend (TypeScript/React)
- Use TypeScript for all components
- Follow React functional component patterns
- Use Tailwind CSS for styling
- Implement proper error handling
- Add loading states for better UX

#### Backend (Python/Flask)
- Follow PEP 8 style guide
- Use type hints where possible
- Implement proper error handling
- Add logging for debugging
- Use SQLAlchemy for database operations

## 📁 Project Structure

### Frontend Structure
```
frontend/
├── app/                   # Next.js App Router pages
│   ├── add-eatery/       # Add restaurant page
│   ├── admin/            # Admin interface
│   ├── api/              # API routes
│   ├── auth/             # Authentication pages
│   ├── favorites/        # User favorites
│   ├── filters/          # Filter pages (removed)
│   ├── live-map/         # Map view
│   ├── profile/          # User profile
│   ├── restaurant/       # Restaurant details
│   └── specials/         # Special offers
├── components/           # Reusable components
├── types/                # TypeScript definitions
├── utils/                # Utility functions
└── public/               # Static assets
```

### Backend Structure
```
backend/
├── app.py                # Main Flask application
├── config/               # Configuration files
├── database/             # Database management
├── scrapers/             # Data scraping tools
├── utils/                # Utility functions
└── requirements.txt      # Python dependencies
```

## 🔍 Debugging

### Frontend Debugging
- Use browser developer tools
- Check console for errors
- Verify API calls in Network tab
- Use React Developer Tools

### Backend Debugging
- Check Flask logs
- Use Python debugger (pdb)
- Verify database connections
- Check environment variables

### Database Debugging
- Connect directly to database
- Check SQLAlchemy logs
- Verify data integrity
- Test queries manually

## 🧪 Testing

### Frontend Testing
```bash
# Run tests (if configured)
npm run test

# Run linting
npm run lint

# Type checking
npm run type-check
```

### Backend Testing
```bash
# Run Python tests (if configured)
python -m pytest

# Check code style
flake8 backend/

# Type checking
mypy backend/
```

## 📊 Performance

### Frontend Optimization
- Use Next.js Image component
- Implement lazy loading
- Optimize bundle size
- Use React.memo for expensive components

### Backend Optimization
- Implement database indexing
- Use connection pooling
- Cache frequently accessed data
- Optimize database queries

## 🔐 Security

### Frontend Security
- Validate all user inputs
- Use HTTPS in production
- Implement proper authentication
- Sanitize data before display

### Backend Security
- Validate all API inputs
- Use environment variables for secrets
- Implement rate limiting
- Use HTTPS in production

## 📝 Contributing

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Update documentation
6. Submit pull request

### Code Review Guidelines
- Review for functionality
- Check code style and standards
- Verify security implications
- Test on different devices/browsers

## 🚨 Common Issues

### Frontend Issues
- **Build errors**: Check Node.js version and dependencies
- **API errors**: Verify backend URL and CORS settings
- **Styling issues**: Check Tailwind CSS configuration

### Backend Issues
- **Database errors**: Check connection strings and permissions
- **Import errors**: Verify Python version and virtual environment
- **API errors**: Check Flask configuration and routes

## 📞 Support

- **Documentation**: Check relevant guide files
- **Issues**: Open GitHub issue with detailed description
- **Discussions**: Use GitHub Discussions for questions

---

*For detailed setup instructions, see individual guide files.* 