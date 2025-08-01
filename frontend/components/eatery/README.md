# Eatery Explore Page - Mobile-First Implementation

This directory contains the new mobile-first Eatery explore page components that match the design from the provided screenshot.

## Components

### `/ui/` Directory

- **SearchBar.tsx** - Rounded pill-style search bar with search icon, placeholder text, and filter toggle
- **CategoryTabs.tsx** - Horizontally scrollable category pills (Mikvahs, Shuls, Specials, Eatery, Stores)
- **SubNav.tsx** - Secondary navigation buttons (Live Map, Add a Eatery, Advanced Filters)
- **EateryCard.tsx** - Restaurant card with image, kosher badge, favorite heart, name, price range, and rating
- **BottomTabBar.tsx** - Fixed bottom navigation with 5 tabs (Explore, Favorites, Specials, Notifications, Profile)

## Features

### Mobile-First Design
- Responsive grid layout (1 column on mobile, 2+ on larger screens)
- Touch-friendly buttons with 44px minimum touch targets
- Mobile-only bottom tab bar (hidden on desktop)
- Safe area support for devices with notches

### Search & Filtering
- Real-time search across restaurant names, cities, and certifying agencies
- Category-based filtering (currently shows all restaurants for "Eatery" category)
- Advanced filters placeholder for future implementation

### Restaurant Cards
- Kosher category badges (Dairy/Meat/Pareve) with appropriate colors
- Favorite heart toggle functionality
- Star ratings display
- Price range formatting
- Fallback image handling

### Navigation
- Category tabs with active state indicators
- Secondary action buttons for map, add eatery, and filters
- Bottom tab bar with proper active states

## Usage

The main page is located at `/app/eatery/page.tsx` and the root page (`/`) redirects to it.

### Importing Components

```tsx
import { 
  SearchBar, 
  CategoryTabs, 
  SubNav, 
  EateryCard, 
  BottomTabBar 
} from '@/components/eatery/ui';
```

### Data Integration

The page uses the existing `fetchRestaurants()` function from `@/lib/api/restaurants` and the `Restaurant` type from `@/types/restaurant`.

## Responsive Breakpoints

- **Mobile**: 1 column grid, mobile-only bottom nav
- **Tablet**: 2 column grid
- **Desktop**: 3-4 column grid, no bottom nav

## Styling

Uses Tailwind CSS with:
- Custom color variables for kosher categories
- Responsive utilities
- Smooth transitions and hover effects
- Accessibility-focused design

## Future Enhancements

- Advanced filters modal/page
- Category-specific data filtering
- Favorites persistence
- Image optimization
- Performance optimizations 