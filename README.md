# JewGo - Kosher Restaurant Discovery App

A modern web application for discovering kosher restaurants and eateries with advanced filtering, mapping, and community features.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- Google Maps API key
- Google Places API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mml555/jewgo.git
   cd jewgo
   ```

2. **Install dependencies**
   ```bash
   # Frontend dependencies
   npm install
   
   # Backend dependencies  
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy environment templates
   cp .env.example .env.local
   cp .env.example .env
   
   # Edit with your API keys
   nano .env.local
   nano .env
   ```

4. **Start development servers**
   ```bash
   # Frontend (Next.js)
   npm run dev
   
   # Backend (Flask) - in another terminal
   python app.py
   ```

## 🌟 Features

- **Restaurant Discovery**: Search and filter kosher restaurants
- **Interactive Maps**: Google Maps integration with restaurant locations
- **Advanced Filtering**: Filter by agency, dietary restrictions, categories
- **Community Features**: Add new restaurants, reviews, and specials
- **Mobile Responsive**: Optimized for all device sizes
- **Real-time Data**: Live updates from Google Places API

## 🛠 Tech Stack

### Frontend
- **Next.js 15.3.3** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Google Maps API** - Interactive maps
- **React Leaflet** - Alternative mapping

### Backend  
- **Flask** - Python web framework
- **SQLite** - Database
- **Google Places API** - Restaurant data
- **CORS** - Cross-origin requests

## 📁 Project Structure

```
jewgo/
├── app/                    # Next.js app directory
│   ├── page.tsx           # Main explore page
│   ├── live-map/          # Interactive map view
│   ├── restaurant/[id]/   # Restaurant detail pages
│   └── ...                # Other pages
├── components/            # React components
├── app.py                # Flask backend server
├── database_manager.py   # Database operations
├── requirements.txt      # Python dependencies
└── package.json         # Node.js dependencies
```

## 🚀 Deployment

### Frontend (Cloudflare Pages)
1. Connect GitHub repository to Cloudflare Pages
2. Set build command: `npm run build`
3. Set build output directory: `out`
4. Add environment variables:
   - `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`
   - `NEXT_PUBLIC_BACKEND_URL`
   - `NODE_ENV=production`

### Backend (Render/Railway/Heroku)
1. Deploy to your preferred platform
2. Add environment variables:
   - `FLASK_SECRET_KEY`
   - `GOOGLE_PLACES_API_KEY`
   - `GOOGLE_KNOWLEDGE_GRAPH_API_KEY`

## 🔧 Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_google_maps_api_key
NEXT_PUBLIC_BACKEND_URL=https://your-backend-url.com
```

### Backend (.env)
```env
FLASK_SECRET_KEY=your_flask_secret_key
GOOGLE_PLACES_API_KEY=your_google_places_api_key
GOOGLE_KNOWLEDGE_GRAPH_API_KEY=your_google_knowledge_graph_api_key
DATABASE_URL=sqlite:///restaurants.db
```

## 📝 API Endpoints

### Backend API (Flask)
- `GET /api/restaurants` - Search restaurants
- `GET /api/restaurants/{id}` - Get restaurant details
- `GET /api/categories` - Get restaurant categories
- `GET /api/states` - Get available states
- `GET /health` - Health check

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Last Updated:** 2025-07-29 01:49 UTC - Force Cloudflare Pages to pick up latest commit 