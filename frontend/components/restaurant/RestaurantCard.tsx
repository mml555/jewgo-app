'use client';

import React from 'react';
import { Star, MapPin, Clock, Phone, ExternalLink } from 'lucide-react';
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
      className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow cursor-pointer"
      onClick={onClick}
    >
      {/* Image Section */}
      <div className="relative h-48 bg-gradient-to-br from-gray-100 to-gray-200">
        {restaurant.image_url ? (
          <img
            src={restaurant.image_url}
            alt={restaurant.name}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <div className="text-gray-400 text-4xl">🍽️</div>
          </div>
        )}
        
        {/* Kosher Type Badge */}
        {restaurant.kosher_category && (
          <div className="absolute top-3 left-3">
            <span className={`px-2 py-1 rounded-lg text-xs font-medium ${getKosherTypeColor(restaurant.kosher_category)}`}>
              {restaurant.kosher_category}
            </span>
          </div>
        )}

        {/* Status Badge */}
        <div className="absolute top-3 right-3">
          <span className={`px-2 py-1 rounded-lg text-xs font-medium bg-white/90 ${getStatusColor(restaurant.is_open || false)}`}>
            {getStatusText(restaurant.is_open || false)}
          </span>
        </div>

        {/* Rating */}
        {restaurant.rating && (
          <div className="absolute bottom-3 left-3 bg-white/90 rounded-lg px-2 py-1 flex items-center space-x-1">
            <Star size={12} className="text-yellow-500 fill-current" />
            <span className="text-xs font-medium text-gray-700">
              {restaurant.rating.toFixed(1)}
            </span>
          </div>
        )}
      </div>

      {/* Content Section */}
      <div className="p-4">
        {/* Restaurant Name and Agency */}
        <div className="mb-2">
          <h3 className="font-semibold text-gray-900 text-lg mb-1 line-clamp-1">
            {restaurant.name}
          </h3>
          {restaurant.certifying_agency && (
            <p className="text-sm text-blue-600 font-medium">
              {restaurant.certifying_agency}
            </p>
          )}
        </div>

        {/* Location */}
        <div className="flex items-start space-x-2 mb-3">
          <MapPin size={14} className="text-gray-400 mt-0.5 flex-shrink-0" />
          <p className="text-sm text-gray-600 line-clamp-2">
            {restaurant.address}, {restaurant.city}, {restaurant.state} {restaurant.zip_code}
          </p>
        </div>

        {/* Hours */}
        {restaurant.hours_of_operation && (
          <div className="flex items-center space-x-2 mb-3">
            <Clock size={14} className="text-gray-400 flex-shrink-0" />
            <p className="text-sm text-gray-600">
              {restaurant.hours_of_operation}
            </p>
          </div>
        )}

        {/* Phone */}
        {restaurant.phone_number && (
          <div className="flex items-center space-x-2 mb-3">
            <Phone size={14} className="text-gray-400 flex-shrink-0" />
            <a 
              href={`tel:${restaurant.phone_number}`}
              className="text-sm text-blue-600 hover:text-blue-800"
              onClick={(e) => e.stopPropagation()}
            >
              {formatPhone(restaurant.phone_number)}
            </a>
          </div>
        )}

        {/* Website */}
        {restaurant.website && (
          <div className="flex items-center space-x-2">
            <ExternalLink size={14} className="text-gray-400 flex-shrink-0" />
            <a 
              href={restaurant.website}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-blue-600 hover:text-blue-800 line-clamp-1"
              onClick={(e) => e.stopPropagation()}
            >
              Visit Website
            </a>
          </div>
        )}
      </div>
    </div>
  );
} 