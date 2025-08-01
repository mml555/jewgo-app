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
    const rating = restaurant.rating || restaurant.star_rating || restaurant.google_rating;
    return rating && rating > 0 ? rating : null;
  };

  const getHeroImage = () => {
    if (restaurant.image_url && !imageError) {
      return restaurant.image_url;
    }
    return getCategoryPlaceholder(restaurant.kosher_category || restaurant.listing_type);
  };

  return (
    <div 
      className={`bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg hover:scale-[1.01] transition-all duration-200 cursor-pointer ${className}`}
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
        
        {/* Kosher Category Badge - Top Left */}
        {restaurant.kosher_category && (
          <span className={`absolute top-2 left-2 text-[11px] px-2 py-1 rounded-full shadow-sm font-medium ${
            restaurant.kosher_category === 'meat' ? 'bg-red-100 text-red-800' :
            restaurant.kosher_category === 'dairy' ? 'bg-blue-100 text-blue-800' :
            'bg-green-100 text-green-800'
          }`}>
            {restaurant.kosher_category === 'meat' ? '🥩 Meat' :
             restaurant.kosher_category === 'dairy' ? '🥛 Dairy' :
             '🥬 Pareve'}
          </span>
        )}
        
        {/* Favorite Button - Top Right */}
        <button
          onClick={handleFavoriteClick}
          className="absolute top-2 right-2 bg-white p-1 rounded-full shadow hover:scale-105 transition-all duration-200"
          aria-label={isFavorited ? 'Remove from favorites' : 'Add to favorites'}
        >
          <Heart 
            className={`w-5 h-5 ${isFavorited ? 'fill-red-500 text-red-500' : 'text-red-400'}`} 
          />
        </button>
      </div>
      
      {/* Content */}
      <div className="p-3">
        {/* Restaurant Name */}
        <h3 className="text-sm font-medium truncate mb-1 group-hover:text-green-600 transition-colors">
          {titleCase(restaurant.name)}
        </h3>
        
        {/* Price Range */}
        {formatPriceRange() && (
          <p className="text-xs text-gray-500 truncate mb-1">
            Price range {formatPriceRange()}
          </p>
        )}
        
        {/* Rating */}
        {getRating() && (
          <div className="flex items-center gap-1 text-yellow-500 text-sm">
            <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
            <span className="text-gray-700">{getRating()!.toFixed(2)}</span>
          </div>
        )}
      </div>
    </div>
  );
} 