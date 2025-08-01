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

  const getKosherBadgeClass = (category: string) => {
    const typeLower = category.toLowerCase();
    if (typeLower === 'dairy') {
      return 'bg-blue-100 text-blue-800 border-blue-200';
    } else if (typeLower === 'meat') {
      return 'bg-red-100 text-red-800 border-red-200';
    } else {
      return 'bg-green-100 text-green-800 border-green-200';
    }
  };

  const getKosherLabel = (category: string) => {
    const typeLower = category.toLowerCase();
    if (typeLower === 'dairy') {
      return 'Dairy';
    } else if (typeLower === 'meat') {
      return 'Meat';
    } else {
      return 'Pareve';
    }
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
    // Use a placeholder image if no image or image failed to load
    return 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&h=300&fit=crop&crop=center';
  };

  return (
    <div 
      className={`bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden cursor-pointer hover:shadow-md transition-all duration-200 ${className}`}
      onClick={handleCardClick}
    >
      {/* Image Container */}
      <div className="relative aspect-[4/3] overflow-hidden">
        <img
          src={getHeroImage()}
          alt={restaurant.name}
          className="w-full h-full object-cover"
          onError={() => setImageError(true)}
        />
        
        {/* Kosher Category Badge */}
        <div className="absolute top-2 left-2">
          <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getKosherBadgeClass(restaurant.kosher_category)}`}>
            {getKosherLabel(restaurant.kosher_category)}
          </span>
        </div>
        
        {/* Favorite Button */}
        <button
          onClick={handleFavoriteClick}
          className="absolute top-2 right-2 p-1 bg-white bg-opacity-80 rounded-full hover:bg-opacity-100 transition-all duration-200"
          aria-label={isFavorited ? 'Remove from favorites' : 'Add to favorites'}
        >
          <Heart 
            className={`w-5 h-5 ${isFavorited ? 'fill-red-500 text-red-500' : 'text-gray-400'}`} 
          />
        </button>
      </div>
      
      {/* Content */}
      <div className="p-3">
        {/* Restaurant Name */}
        <h3 className="font-semibold text-gray-900 text-sm mb-1 line-clamp-1">
          {restaurant.name}
        </h3>
        
        {/* Price Range and Rating */}
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-600">
            {formatPriceRange()}
          </span>
          
          <div className="flex items-center space-x-1">
            <Star className="w-3 h-3 text-yellow-400 fill-current" />
            <span className="text-xs text-gray-600 font-medium">
              {getRating().toFixed(2)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
} 