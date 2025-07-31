# Jewgo Frontend

A modern, mobile-first restaurant directory application built with Next.js, TypeScript, and Tailwind CSS.

## Features

- **Modern UI**: Clean, responsive design matching the Jewgo brand
- **Restaurant Directory**: Browse 246+ kosher restaurants
- **Search & Filter**: Find restaurants by name, category, and location
- **Mobile-First**: Optimized for mobile devices with touch-friendly interface
- **Real-time Data**: Connected to Flask backend API
- **Kosher Categories**: Meat, Dairy, Pareve, and Unknown classifications
- **Star Ratings**: Restaurant ratings and reviews
- **Price Ranges**: Average price information for each restaurant

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Backend**: Flask API (running on port 8081)

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Flask backend running on port 8081

### Installation

1. **Install dependencies**:
   ```bash
   cd jewgo-frontend
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm run dev
   ```

3. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
jewgo-frontend/
├── app/                    # Next.js App Router
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── Header.tsx         # App header with logo
│   ├── SearchBar.tsx      # Search functionality
│   ├── CategoryNav.tsx    # Category navigation
│   ├── ActionButtons.tsx  # Action buttons
│   ├── RestaurantCard.tsx # Restaurant card component
│   ├── RestaurantGrid.tsx # Restaurant grid layout
│   └── BottomNavigation.tsx # Bottom navigation
├── types/                 # TypeScript type definitions
│   └── restaurant.ts      # Restaurant data types
├── public/                # Static assets
└── package.json           # Dependencies and scripts
```

## API Integration

The frontend connects to the Flask backend API running on port 8081:

- **Restaurants**: `/api/restaurants`
- **Search**: `/api/restaurants?query=...`
- **Statistics**: `/api/statistics`
- **States**: `/api/states`

## Design System

### Colors
- **Primary**: `#4ade80` (Light mint green)
- **Secondary**: `#374151` (Dark grey)
- **Accent**: `#10b981` (Darker green)

### Kosher Type Colors
- **Meat**: `#ef4444` (Red)
- **Dairy**: `#3b82f6` (Blue)
- **Pareve**: `#f59e0b` (Yellow)
- **Unknown**: `#6b7280` (Grey)

## Features in Detail

### 1. Search & Discovery
- Real-time search with instant results
- Category-based filtering (Mikvahs, Shuls, Specials, Eatery, Stores)
- Advanced filters for location and kosher type

### 2. Restaurant Cards
- High-quality restaurant images
- Kosher type badges
- Star ratings and price ranges
- Short descriptions
- "View Eatery" links

### 3. Mobile Navigation
- Bottom navigation bar
- Touch-friendly interface
- Responsive grid layout (2 columns on mobile)

### 4. Data Integration
- 246+ restaurants from database
- Real-time API calls
- Error handling and loading states

## Development

### Adding New Features

1. **New Components**: Add to `components/` directory
2. **Types**: Extend `types/restaurant.ts`
3. **Styling**: Use Tailwind classes or extend `globals.css`
4. **API**: Update backend endpoints as needed

### Code Style

- Use TypeScript for all components
- Follow React functional component patterns
- Use Tailwind CSS for styling
- Implement proper error handling
- Add loading states for better UX

## Deployment

### Vercel (Recommended)
```bash
npm run build
vercel --prod
```

### Other Platforms
The app can be deployed to any platform that supports Next.js:
- Netlify
- AWS Amplify
- DigitalOcean App Platform
- Self-hosted servers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the Jewgo restaurant directory application.

## Support

For support or questions, please contact the development team. 