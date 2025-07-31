# 🛠️ Development Guide

## 📋 Overview

This guide provides comprehensive instructions for developing and maintaining the JewGo application. The project is organized into a clean, modular structure with clear separation of concerns.

## 🏗️ Project Architecture

### Backend Architecture
```
backend/
├── database/          # Database management and models
├── scrapers/          # Web scraping services
├── config/           # Configuration files
├── utils/            # Utility functions
├── venv/             # Python virtual environment
└── scraper_env/      # Scraper-specific environment
```

### Frontend Architecture
```
frontend/
├── components/       # React components
├── pages/           # Next.js pages
├── styles/          # CSS and styling
├── utils/           # Frontend utilities
├── public/          # Static assets
├── types/           # TypeScript definitions
└── lib/             # Frontend libraries
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11
- Node.js 18+
- PostgreSQL database
- Git

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd jewgo-app
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r ../requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Variables**
   ```bash
   # Backend
   cp config/env.production.example .env
   # Edit .env with your database credentials
   
   # Frontend
   cp .env.example .env.local
   # Edit .env.local with your API endpoints
   ```

## 🗄️ Database Development

### Schema Management
The database uses a consolidated `restaurants` table with 28 optimized columns:

```python
# Key fields for kosher categorization
is_cholov_yisroel: Boolean    # Chalav Yisroel status
is_pas_yisroel: Boolean       # Pas Yisroel status
kosher_type: String           # dairy, meat, pareve
```

### Database Operations
```python
from backend.database.database_manager_v3 import EnhancedDatabaseManager

# Initialize database manager
db = EnhancedDatabaseManager()
db.connect()

# Add restaurant
restaurant_data = {
    'name': 'Restaurant Name',
    'address': '123 Main St',
    'kosher_type': 'dairy',
    'is_cholov_yisroel': True,
    'is_pas_yisroel': False
}
db.add_restaurant(restaurant_data)
```

### Running Database Scripts
```bash
# Initialize database
python backend/database/init_database.py

# Run scraper
python backend/scrapers/orb_scraper_v2.py

# Database cleanup
python scripts/maintenance/database_cleanup.py
```

## 🔧 Backend Development

### Code Organization
- **Models**: `backend/database/database_manager_v3.py`
- **Scrapers**: `backend/scrapers/`
- **Configuration**: `backend/config/`
- **Utilities**: `backend/utils/`

### Adding New Features

1. **Database Changes**
   ```python
   # Add new column to Restaurant model
   class Restaurant(Base):
       new_field = Column(String(100))
   ```

2. **New Scrapers**
   ```python
   # Create new scraper in backend/scrapers/
   class NewScraper:
       def __init__(self):
           self.db_manager = DatabaseManager()
   ```

3. **API Endpoints**
   ```python
   # Add to your API server
   @app.get("/api/restaurants")
   def get_restaurants():
       return db_manager.get_restaurants()
   ```

### Testing
```bash
# Run backend tests
cd backend
python -m pytest tests/

# Run specific test
python -m pytest tests/test_database.py
```

## 🎨 Frontend Development

### Component Structure
```typescript
// components/RestaurantCard.tsx
interface RestaurantCardProps {
  restaurant: Restaurant;
  showKosherStatus: boolean;
}

export const RestaurantCard: React.FC<RestaurantCardProps> = ({
  restaurant,
  showKosherStatus
}) => {
  // Component implementation
};
```

### Adding New Pages
```typescript
// pages/new-page.tsx
import { NextPage } from 'next';

const NewPage: NextPage = () => {
  return (
    <div>
      <h1>New Page</h1>
    </div>
  );
};

export default NewPage;
```

### Styling
The project uses Tailwind CSS for styling:
```css
/* Custom styles in frontend/styles/ */
.restaurant-card {
  @apply bg-white rounded-lg shadow-md p-4;
}
```

## 📊 Data Management

### Kosher Categorization
The system supports multiple kosher supervision levels:

1. **Chalav Yisroel/Stam**
   - Chalav Yisroel: 104 restaurants
   - Chalav Stam: 3 restaurants (manually curated)

2. **Pas Yisroel**
   - Pas Yisroel: 22 restaurants (manually curated)
   - Regular Pas: All other restaurants

### Data Sources
- **ORB Kosher**: Primary data source
- **Manual Curation**: Chalav Stam and Pas Yisroel lists
- **Google Places**: Additional business information

### Data Validation
```python
# Validate restaurant data
def validate_restaurant_data(data: Dict) -> bool:
    required_fields = ['name', 'address', 'kosher_type']
    return all(field in data for field in required_fields)
```

## 🔍 Monitoring and Logging

### Structured Logging
```python
import structlog

logger = structlog.get_logger()
logger.info("Operation completed", 
           restaurant_count=107, 
           kosher_type="dairy")
```

### Health Checks
```bash
# Run health checks
python monitoring/health_checks/health-check.js

# Check database status
python scripts/testing/test_database_connection.py
```

## 🚀 Deployment

### Backend Deployment
```bash
# Deploy to Render
cd backend
git push origin main

# Environment variables in Render dashboard
DATABASE_URL=postgresql://...
```

### Frontend Deployment
```bash
# Deploy to Vercel
cd frontend
vercel --prod

# Environment variables in Vercel dashboard
NEXT_PUBLIC_API_URL=https://...
```

## 🧪 Testing

### Backend Testing
```python
# Unit tests
def test_add_restaurant():
    db = DatabaseManager()
    result = db.add_restaurant(test_data)
    assert result == True
```

### Frontend Testing
```typescript
// Component tests
import { render, screen } from '@testing-library/react';
import { RestaurantCard } from '../RestaurantCard';

test('renders restaurant name', () => {
  render(<RestaurantCard restaurant={mockRestaurant} />);
  expect(screen.getByText('Restaurant Name')).toBeInTheDocument();
});
```

## 📝 Code Style

### Python Style Guide
- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Use structured logging

### TypeScript Style Guide
- Use strict TypeScript
- Prefer functional components
- Use Tailwind CSS for styling
- Add proper interfaces

### Git Workflow
```bash
# Feature development
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature
# Create pull request
```

## 🔧 Maintenance

### Database Maintenance
```bash
# Clean unused columns
python scripts/maintenance/cleanup_unused_columns.py

# Remove duplicates
python scripts/maintenance/remove_duplicates.py

# Backup database
python scripts/maintenance/backup_database.py
```

### Code Maintenance
```bash
# Update dependencies
pip install -r requirements.txt --upgrade
npm update

# Run linters
flake8 backend/
npm run lint

# Run tests
python -m pytest
npm test
```

## 📚 Documentation

### Code Documentation
- Add docstrings to all functions
- Include type hints
- Document complex algorithms
- Update README files

### API Documentation
- Document all endpoints
- Include request/response examples
- Add authentication details
- Update OpenAPI specs

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection**
   ```bash
   # Check DATABASE_URL
   echo $DATABASE_URL
   
   # Test connection
   python scripts/testing/test_database_connection.py
   ```

2. **Scraper Issues**
   ```bash
   # Check Playwright installation
   playwright install chromium
   
   # Run scraper with debug
   python backend/scrapers/orb_scraper_v2.py --debug
   ```

3. **Frontend Build Issues**
   ```bash
   # Clear cache
   rm -rf frontend/.next
   npm run build
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit pull request

### Pull Request Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Performance impact considered

---

For more information, see the other documentation files in the `docs/` directory. 