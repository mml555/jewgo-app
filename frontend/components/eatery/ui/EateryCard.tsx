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
      className={`bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden cursor-pointer hover:shadow-lg hover:scale-[1.02] transition-all duration-300 ${className}`}
      onClick={handleCardClick}
    >
      {/* Image Container */}
      <div className="relative aspect-[4/3] overflow-hidden">
        <img
          src={getHeroImage()}
          alt={restaurant.name}
          className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
          onError={() => setImageError(true)}
        />
        
        {/* Kosher Category Badge */}
        <div className="absolute top-3 left-3">
          <span className={`px-3 py-1.5 rounded-full text-xs font-semibold border shadow-sm ${getKosherBadgeClass(restaurant.kosher_category)}`}>
            {getKosherLabel(restaurant.kosher_category)}
          </span>
        </div>
        
        {/* Favorite Button */}
        <button
          onClick={handleFavoriteClick}
          className="absolute top-3 right-3 p-2 bg-white bg-opacity-90 rounded-full hover:bg-opacity-100 hover:scale-110 transition-all duration-200 shadow-sm"
          aria-label={isFavorited ? 'Remove from favorites' : 'Add to favorites'}
        >
          <Heart 
            className={`w-4 h-4 ${isFavorited ? 'fill-red-500 text-red-500' : 'text-gray-500 hover:text-red-400'}`} 
          />
        </button>
      </div>
      
      {/* Content */}
      <div className="p-4">
        {/* Restaurant Name */}
        <h3 className="font-semibold text-gray-900 text-sm mb-2 line-clamp-1">
          {restaurant.name}
        </h3>
        
        {/* Price Range and Rating */}
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500 font-medium">
            {formatPriceRange()}
          </span>
          
          <div className="flex items-center space-x-1.5">
            <Star className="w-3.5 h-3.5 text-yellow-400 fill-current" />
            <span className="text-xs text-gray-700 font-semibold">
              {getRating().toFixed(1)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
} 