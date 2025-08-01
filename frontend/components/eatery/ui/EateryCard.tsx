'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Heart, Star } from 'lucide-react';
import { Restaurant } from '@/types/restaurant';

interface EateryCardProps {
  restaurant: Restaurant;
  className?: string;
}

export default function EateryCard({ restaurant, className = "" }: EateryCardProps) {
  const router = useRouter();
  const [isFavorited, setIsFavorited] = useState(false);
  const [imageError, setImageError] = useState(false);

  const handleCardClick = () => {
    router.push(`/restaurant/${restaurant.id}`);
  };

  const handleFavoriteClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsFavorited(!isFavorited);
  };

  // Get category-based placeholder image
  const getCategoryPlaceholder = (category: string) => {
    const categoryLower = category?.toLowerCase() || '';
    if (categoryLower.includes('pizza')) return '/images/placeholders/pizza-placeholder.jpg';
    if (categoryLower.includes('sushi') || categoryLower.includes('japanese')) return '/images/placeholders/sushi-placeholder.jpg';
    if (categoryLower.includes('grill') || categoryLower.includes('steak')) return '/images/placeholders/grill-placeholder.jpg';
    if (categoryLower.includes('bakery')) return '/images/placeholders/bakery-placeholder.jpg';
    if (categoryLower.includes('cafe') || categoryLower.includes('coffee')) return '/images/placeholders/cafe-placeholder.jpg';
    if (categoryLower.includes('ice cream') || categoryLower.includes('dessert')) return '/images/placeholders/dessert-placeholder.jpg';
    return '/images/default-restaurant.jpg';
  };

  // Get kosher type color for tag
  const getKosherTypeColor = (kosherType: string) => {
    const typeLower = kosherType?.toLowerCase() || '';
    if (typeLower === 'dairy') return 'bg-blue-500';
    if (typeLower === 'meat') return 'bg-[#A70000]';
    if (typeLower === 'pareve') return 'bg-green-500';
    return 'bg-gray-500';
  };

  // Title case function
  const titleCase = (str: string) => {
    if (!str) return '';
    return str.replace(/\w\S*/g, (txt) => 
      txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
    );
  };

  const formatPriceRange = () => {
    if (restaurant.price_range) {
      return restaurant.price_range;
    }
    
    if (restaurant.min_avg_meal_cost && restaurant.max_avg_meal_cost) {
      return `$${restaurant.min_avg_meal_cost} - $${restaurant.max_avg_meal_cost}`;
    }
    
    return 'Price not available';
  };

  const getRating = () => {
    return restaurant.rating || restaurant.star_rating || restaurant.google_rating || 0;
  };

  const getHeroImage = () => {
    if (restaurant.image_url && !imageError) {
      return restaurant.image_url;
    }
    return getCategoryPlaceholder(restaurant.kosher_category || restaurant.listing_type);
  };

  return (
    <div 
      className={`bg-white rounded-xl shadow-md overflow-hidden cursor-pointer hover:shadow-lg hover:scale-[1.01] transition-all duration-200 ${className}`}
      onClick={handleCardClick}
    >
      {/* Image Container */}
      <div className="relative aspect-[4/3] overflow-hidden">
        <img
          src={getHeroImage()}
          alt={restaurant.name}
          className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
          onError={() => setImageError(true)}
          loading="lazy"
        />
        
        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent" />
        
        {/* Kosher Category Badge - Top Left */}
        {restaurant.kosher_category && (
          <div className="absolute top-2 left-2">
            <span className={`px-2 py-1 rounded-full text-xs font-medium text-white ${getKosherTypeColor(restaurant.kosher_category)}`}>
              {titleCase(restaurant.kosher_category)}
            </span>
          </div>
        )}
        
        {/* Favorite Button - Top Right */}
        <button
          onClick={handleFavoriteClick}
          className="absolute top-2 right-2 bg-white rounded-full p-1 shadow-md transition-all duration-200 hover:scale-110"
          aria-label={isFavorited ? 'Remove from favorites' : 'Add to favorites'}
        >
          <Heart 
            className={`w-4 h-4 ${isFavorited ? 'fill-pink-500 text-pink-500' : 'text-gray-800 hover:text-pink-500'}`} 
          />
        </button>
      </div>
      
      {/* Content */}
      <div className="px-3 py-2">
        {/* Restaurant Name */}
        <h3 className="text-[15px] font-semibold leading-snug text-gray-900 mb-2 line-clamp-2 group-hover:text-green-600 transition-colors tracking-tight">
          {titleCase(restaurant.name)}
        </h3>
        
        {/* Price Range and Rating - Aligned in one row */}
        <div className="flex items-center gap-1 text-sm text-gray-500 mb-2">
          {formatPriceRange() && (
            <span>{formatPriceRange()}</span>
          )}
          {formatPriceRange() && getRating() > 0 && (
            <span>•</span>
          )}
          {getRating() > 0 && (
            <span className="inline-flex items-center gap-1">
              <Star className="w-3.5 h-3.5 text-yellow-500 fill-current" />
              <span className="text-sm font-medium">{getRating().toFixed(1)}</span>
            </span>
          )}
        </div>
      </div>
    </div>
  );
} 