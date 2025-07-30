'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Restaurant } from '@/types/restaurant';
import { cn } from '@/utils/cn';

interface RestaurantCardProps {
  restaurant: Restaurant;
  onSelect?: (restaurant: Restaurant) => void;
  showDistance?: boolean;
  distance?: number;
  isOnMapPage?: boolean;
  className?: string;
}

export default function RestaurantCard({
  restaurant,
  onSelect,
  showDistance = false,
  distance,
  isOnMapPage = false,
  className
}: RestaurantCardProps) {
  const router = useRouter();
  const [imageError, setImageError] = useState(false);
  const [isPressed, setIsPressed] = useState(false);

  const handleCardClick = () => {
    if (onSelect) {
      onSelect(restaurant);
    } else {
      router.push(`/restaurant/${restaurant.id}`);
    }
  };

  const handleTouchStart = () => setIsPressed(true);
  const handleTouchEnd = () => setIsPressed(false);

  const getAgencyBadgeClass = (agency: string) => {
    const agencyLower = agency.toLowerCase();
    if (agencyLower.includes('ou') || agencyLower.includes('orthodox union')) {
      return 'bg-blue-100 text-blue-800 border-blue-200';
    } else if (agencyLower.includes('ok') || agencyLower.includes('ok kosher')) {
      return 'bg-green-100 text-green-800 border-green-200';
    } else if (agencyLower.includes('star-k') || agencyLower.includes('star k')) {
      return 'bg-purple-100 text-purple-800 border-purple-200';
    } else if (agencyLower.includes('crc') || agencyLower.includes('chicago rabbinical')) {
      return 'bg-orange-100 text-orange-800 border-orange-200';
    } else if (agencyLower.includes('kof-k')) {
      return 'bg-red-100 text-red-800 border-red-200';
    }
    return 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getKosherBadgeClass = (category: string) => {
    const categoryLower = category.toLowerCase();
    if (categoryLower.includes('glatt')) {
      return 'bg-emerald-100 text-emerald-800 border-emerald-200';
    } else if (categoryLower.includes('chassidish')) {
      return 'bg-indigo-100 text-indigo-800 border-indigo-200';
    } else if (categoryLower.includes('mehadrin')) {
      return 'bg-amber-100 text-amber-800 border-amber-200';
    } else if (categoryLower.includes('chalav yisrael') || categoryLower.includes('chalav yisroel')) {
      return 'bg-cyan-100 text-cyan-800 border-cyan-200';
    }
    return 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const formatDistance = (distance: number) => {
    if (distance < 1) {
      return `${Math.round(distance * 5280)} ft`;
    }
    return `${distance.toFixed(1)} mi`;
  };

  const getHeroImage = () => {
    if (imageError || !restaurant.image_url) {
      return '/images/default-restaurant.jpg';
    }
    return restaurant.image_url;
  };

  const getCategoryIcon = (category: string) => {
    const categoryLower = category.toLowerCase();
    if (categoryLower.includes('restaurant')) {
      return (
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
        </svg>
      );
    } else if (categoryLower.includes('bakery')) {
      return (
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      );
    } else if (categoryLower.includes('cafe')) {
      return (
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
        </svg>
      );
    } else if (categoryLower.includes('grocery')) {
      return (
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
        </svg>
      );
    }
    return (
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
      </svg>
    );
  };

  return (
    <div
      className={cn(
        "group relative bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden transition-all duration-200",
        "hover:shadow-lg hover:border-gray-300 active:scale-[0.98]",
        "focus-within:ring-2 focus-within:ring-green-500 focus-within:ring-offset-2",
        "touch-manipulation cursor-pointer",
        isPressed && "scale-[0.98] shadow-md",
        className
      )}
      onClick={handleCardClick}
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
      onMouseDown={() => setIsPressed(true)}
      onMouseUp={() => setIsPressed(false)}
      onMouseLeave={() => setIsPressed(false)}
      role="button"
      tabIndex={0}
      aria-label={`View details for ${restaurant.name}`}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          handleCardClick();
        }
      }}
    >
      {/* Image Section */}
      <div className="relative h-48 sm:h-52 overflow-hidden bg-gray-100">
        <img
          src={getHeroImage()}
          alt={`${restaurant.name} restaurant`}
          className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
          onError={() => setImageError(true)}
          loading="lazy"
        />
        
        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent" />
        
        {/* Distance Badge */}
        {showDistance && distance !== undefined && (
          <div className="absolute top-3 right-3 bg-white/90 backdrop-blur-sm text-gray-800 px-2 py-1 rounded-full text-xs font-medium shadow-sm">
            {formatDistance(distance)}
          </div>
        )}
        
        {/* Category Icon */}
        <div className="absolute top-3 left-3 bg-white/90 backdrop-blur-sm text-gray-700 p-2 rounded-full shadow-sm">
          {getCategoryIcon(restaurant.listing_type || 'restaurant')}
        </div>
        
        {/* Quick Action Buttons */}
        <div className="absolute bottom-3 right-3 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          <button
            className="bg-white/90 backdrop-blur-sm text-gray-700 p-2 rounded-full shadow-sm hover:bg-white transition-colors"
            onClick={(e) => {
              e.stopPropagation();
              // Add to favorites functionality
            }}
            aria-label="Add to favorites"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </button>
          <button
            className="bg-white/90 backdrop-blur-sm text-gray-700 p-2 rounded-full shadow-sm hover:bg-white transition-colors"
            onClick={(e) => {
              e.stopPropagation();
              // Share functionality
            }}
            aria-label="Share restaurant"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
            </svg>
          </button>
        </div>
      </div>

      {/* Content Section */}
      <div className="p-4 sm:p-5">
        {/* Header */}
        <div className="mb-3">
          <h3 className="text-lg sm:text-xl font-bold text-gray-900 mb-2 line-clamp-2 group-hover:text-green-600 transition-colors">
            {restaurant.name}
          </h3>
          
          {/* Address */}
          <div className="flex items-start gap-2 text-sm text-gray-600 mb-3">
            <svg className="w-4 h-4 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span className="line-clamp-2">
              {restaurant.address}, {restaurant.city}, {restaurant.state}
            </span>
          </div>
        </div>

        {/* Badges */}
        <div className="flex flex-wrap gap-2 mb-4">
          {/* Certifying Agency */}
          {restaurant.certifying_agency && (
            <span className={cn(
              "inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border",
              getAgencyBadgeClass(restaurant.certifying_agency)
            )}>
              {restaurant.certifying_agency}
            </span>
          )}
          
          {/* Kosher Category */}
          {restaurant.kosher_category && (
            <span className={cn(
              "inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium border",
              getKosherBadgeClass(restaurant.kosher_category)
            )}>
              {restaurant.kosher_category}
            </span>
          )}
          
          {/* Listing Type */}
          {restaurant.listing_type && (
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800 border border-gray-200">
              {restaurant.listing_type}
            </span>
          )}
        </div>

        {/* Additional Info */}
        <div className="space-y-2 text-sm text-gray-600">
          {/* Phone */}
          {restaurant.phone_number && (
            <div className="flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              <a 
                href={`tel:${restaurant.phone_number}`}
                onClick={(e) => e.stopPropagation()}
                className="hover:text-green-600 transition-colors"
              >
                {restaurant.phone_number}
              </a>
            </div>
          )}
          
          {/* Website */}
          {restaurant.website && (
            <div className="flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9" />
              </svg>
              <a 
                href={restaurant.website}
                target="_blank"
                rel="noopener noreferrer"
                onClick={(e) => e.stopPropagation()}
                className="hover:text-green-600 transition-colors truncate"
              >
                Visit Website
              </a>
            </div>
          )}
        </div>

        {/* Action Button */}
        <div className="mt-4 pt-4 border-t border-gray-100">
          <button
            className="w-full bg-green-500 text-white py-2.5 px-4 rounded-lg font-medium hover:bg-green-600 transition-colors focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 touch-manipulation"
            onClick={(e) => {
              e.stopPropagation();
              handleCardClick();
            }}
          >
            View Details
          </button>
        </div>
      </div>

      {/* Hover Effect Overlay */}
      <div className="absolute inset-0 bg-green-500 opacity-0 group-hover:opacity-5 transition-opacity duration-200 pointer-events-none" />
    </div>
  );
} 