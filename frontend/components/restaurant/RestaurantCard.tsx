'use client';

import React from 'react';
import { Star, MapPin, Clock, Phone, ExternalLink, Heart } from 'lucide-react';
import { Restaurant } from '@/types/restaurant';

interface RestaurantCardProps {
  restaurant: Restaurant;
  onClick?: () => void;
}

export default function RestaurantCard({ restaurant, onClick }: RestaurantCardProps) {
  const getKosherTypeColor = (type: string) => {
    switch (type.toLowerCase()) {
      case 'glatt':
        return 'bg-red-100 text-red-800';
      case 'mehadrin':
        return 'bg-purple-100 text-purple-800';
      case 'cholov yisroel':
        return 'bg-blue-100 text-blue-800';
      case 'pas yisroel':
        return 'bg-green-100 text-green-800';
      case 'bishul yisroel':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusColor = (isOpen: boolean) => {
    return isOpen ? 'text-green-600' : 'text-red-600';
  };

  const getStatusText = (isOpen: boolean) => {
    return isOpen ? 'Open' : 'Closed';
  };

  const formatPhone = (phone: string) => {
    if (!phone) return '';
    return phone.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
  };

  return (
    <div 
      className="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg transition min-w-0 cursor-pointer"
      onClick={onClick}
    >
      {/* Image Section */}
      <div className="relative aspect-[4/3] bg-gradient-to-br from-gray-100 to-gray-200">
        {restaurant.image_url ? (
          <img
            src={restaurant.image_url}
            alt={restaurant.name}
            className="w-full h-full object-cover rounded-t-xl"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <div className="text-gray-400 text-4xl">🍽️</div>
          </div>
        )}
        
        {/* Kosher Type Badge */}
        {restaurant.kosher_category && (
          <div className="absolute top-2 left-2">
            <span className="px-2 py-1 text-[11px] font-medium rounded-full shadow-sm bg-white text-gray-700">
              {restaurant.kosher_category}
            </span>
          </div>
        )}

        {/* Favorite Button */}
        <div className="absolute top-2 right-2">
          <button 
            className="bg-white p-1 rounded-full shadow hover:scale-105 transition"
            aria-label="Add to favorites"
            onClick={(e) => e.stopPropagation()}
          >
            <Heart size={16} className="w-5 h-5 text-red-500" />
          </button>
        </div>

        {/* Rating */}
        {restaurant.rating && (
          <div className="absolute bottom-2 left-2 bg-white/90 rounded-lg px-2 py-1 flex items-center gap-1 text-yellow-500 text-sm">
            <Star size={12} className="fill-current" />
            <span className="text-xs font-medium text-gray-700">
              {restaurant.rating.toFixed(1)}
            </span>
          </div>
        )}
      </div>

      {/* Content Section */}
      <div className="px-3 py-2 flex flex-col gap-1">
        {/* Restaurant Name */}
        <h3 className="text-sm font-medium truncate text-gray-900">
          {restaurant.name}
        </h3>
        
        {/* Price and Agency */}
        <p className="text-xs text-gray-500 truncate">
          {restaurant.certifying_agency && `${restaurant.certifying_agency} • `}
          {restaurant.kosher_category}
        </p>
        
        {/* Location */}
        <p className="text-xs text-gray-500 truncate">
          {restaurant.city}, {restaurant.state}
        </p>
        
        {/* Status */}
        <div className="flex items-center gap-1">
          <div className={`w-2 h-2 rounded-full ${restaurant.is_open ? 'bg-green-500' : 'bg-red-500'}`}></div>
          <span className="text-xs text-gray-500">
            {getStatusText(restaurant.is_open || false)}
          </span>
        </div>
      </div>
    </div>
  );
} 