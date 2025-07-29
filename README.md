# 🍽️ JewGo - Kosher Restaurant Discovery App

A modern, mobile-first web application for discovering kosher restaurants, bakeries, and grocery stores in your area.

**🚀 Latest Update: Configured for Cloudflare Pages deployment with fixed dependencies (2025-07-29)**

## 🌟 Features

- **Restaurant Discovery**: Find kosher restaurants, bakeries, and grocery stores
- **Advanced Filtering**: Filter by certifying agency, dietary preferences, and distance
- **Interactive Maps**: Live map view with restaurant locations
- **Mobile-First Design**: Optimized for mobile devices with responsive design
- **Real-time Search**: Search restaurants by name, location, and keywords
- **Restaurant Details**: Comprehensive restaurant information including hours, reviews, and contact details
- **Favorites System**: Save and manage your favorite restaurants
- **Location Services**: GPS-based distance calculations and directions

## 🏗️ Tech Stack

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Google Maps API** - Interactive maps and location services

### Backend
- **Python Flask** - RESTful API server
- **SQLite** - Lightweight database
- **Google Places API** - Restaurant data and reviews

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mml555/jewgo.git
   cd jewgo
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Setup Backend**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   
   Create `.env.local` file:
   ```env
   NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8081
   ```

5. **Run Development Servers**
   
   **Backend (Terminal 1):**
   ```bash
   python app.py
   ```
   
   **Frontend (Terminal 2):**
   ```bash
   npm run dev
   ```

6. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8081

## 📱 Features Overview

### 🗺️ Interactive Map
- Real-time restaurant locations
- Distance-based filtering
- Click-to-navigate functionality
- Mobile-optimized map interface

### 🔍 Advanced Search & Filters
- Text-based search
- Certifying agency filters (ORB, KM, KDM, Diamond K)
- Dietary preference filters (Meat, Dairy, Pareve)
- Distance-based filtering
- "Open Now" filter

### 🏪 Restaurant Details
- Comprehensive restaurant information
- Hours of operation
- Contact information
- Google reviews integration
- Cost information
- Kosher certification details

### 📱 Mobile Experience
- Responsive design
- Touch-friendly interface
- Sticky action bars
- Optimized for mobile browsing

## 🏗️ Project Structure

```
jewgo/
├── app/                    # Next.js App Router pages
├── components/             # React components
├── types/                  # TypeScript definitions
├── utils/                  # Utility functions
├── public/                 # Static assets
├── app.py                  # Flask backend server
├── database_manager.py     # Database operations
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Deployment

### Cloudflare Pages Deployment

This app is configured for Cloudflare Pages deployment:

1. **Automatic Deployment**: Connected to GitHub repository
2. **Build Command**: `npm run build`
3. **Build Output Directory**: `out`
4. **Environment Variables**: Set in Cloudflare Pages dashboard

### Backend Deployment

The backend can be deployed to:
- **Railway** - Easy Python deployment
- **Render** - Free tier available
- **Heroku** - Traditional choice
- **DigitalOcean App Platform** - Scalable solution

## 🔧 Configuration

### Google Maps API Setup

1. Create a Google Cloud Project
2. Enable Maps JavaScript API and Places API
3. Create API keys with appropriate restrictions
4. Add keys to environment variables

### Database Setup

The app uses SQLite for simplicity. For production:
- Consider PostgreSQL or MySQL
- Set up proper database migrations
- Configure connection pooling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Maps API for location services
- Unsplash for restaurant images
- The kosher community for feedback and support

## 📞 Support

For support, email support@jewgo.com or create an issue in this repository.

---

**Made with ❤️ for the kosher community** 