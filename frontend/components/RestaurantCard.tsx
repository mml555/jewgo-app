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
  const [isFavorited, setIsFavorited] = useState(false);

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

  const getKosherTypeBadgeClass = (kosherType: string) => {
    const typeLower = kosherType.toLowerCase();
    if (typeLower === 'dairy') {
      return 'bg-blue-500 text-white border-blue-600';
    } else if (typeLower === 'meat') {
      return 'bg-red-500 text-white border-red-600';
    } else if (typeLower === 'pareve') {
      return 'bg-green-500 text-white border-green-600';
    }
    return 'bg-gray-500 text-white border-gray-600';
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

  // Clean address formatting - remove trailing commas
  const formatAddress = (address: string, city: string, state: string) => {
    const cleanAddress = address.replace(/,\s*$/, ''); // Remove trailing comma
    const cleanCity = city.replace(/,\s*$/, ''); // Remove trailing comma
    return `${cleanAddress}, ${cleanCity}, ${state}`;
  };

  // Enhanced rating display with stars
  const renderRating = () => {
    const rating = restaurant.google_rating || restaurant.rating;
    if (!rating) return null;
    
    const stars = '★'.repeat(Math.floor(rating)) + '☆'.repeat(5 - Math.floor(rating));
    return (
      <span className="inline-flex items-center gap-1">
        <span className="text-yellow-500">{stars}</span>
        <span className="text-sm font-medium">{rating}/5</span>
      </span>
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
      <div className="relative h-44 sm:h-48 overflow-hidden bg-gray-100">
        <img
          src={getHeroImage()}
          alt={`${restaurant.name} restaurant`}
          className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
          onError={() => setImageError(true)}
          loading="lazy"
        />
        
        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent" />
        
        {/* Heart/Share Buttons - Top Right */}
        <div className="absolute top-3 right-3 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          <button
            className={cn(
              "p-1.5 rounded-full shadow-sm transition-colors border",
              isFavorited 
                ? "bg-pink-200 text-pink-600 border-white" 
                : "bg-transparent text-white border-white hover:bg-pink-200 hover:text-pink-600"
            )}
            onClick={(e) => {
              e.stopPropagation();
              setIsFavorited(!isFavorited);
            }}
            aria-label={isFavorited ? "Remove from favorites" : "Add to favorites"}
          >
            <svg className="w-3.5 h-3.5" fill={isFavorited ? "currentColor" : "none"} stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </button>
          <button
            className="bg-transparent text-white border border-white p-1.5 rounded-full shadow-sm hover:bg-white hover:text-gray-700 transition-colors"
            onClick={(e) => {
              e.stopPropagation();
              // Share functionality
              if (navigator.share) {
                navigator.share({
                  title: restaurant.name,
                  text: `Check out ${restaurant.name} on JewGo!`,
                  url: `${window.location.origin}/restaurant/${restaurant.id}`
                });
              } else {
                // Fallback: copy to clipboard
                navigator.clipboard.writeText(`${window.location.origin}/restaurant/${restaurant.id}`);
              }
            }}
            aria-label="Share restaurant"
          >
            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
            </svg>
          </button>
        </div>
        
        {/* Bottom Badges - Split layout with spacing */}
        <div className="absolute bottom-3 left-3">
          {/* Certification Badge - Left side */}
          {restaurant.certifying_agency && (
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-transparent text-white border border-black shadow-sm hover:bg-white hover:text-gray-900 transition-colors duration-200">
              {restaurant.certifying_agency === 'ORB Kosher' ? 'ORB' : restaurant.certifying_agency}
            </span>
          )}
        </div>
        
        {/* Kosher Type and Chalav Badges - Right side */}
        <div className="absolute bottom-3 right-3 flex flex-row gap-2">
          {/* Kosher Type Badge */}
          {restaurant.kosher_category && (
            <span className={cn(
              "inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold border shadow-sm",
              getKosherTypeBadgeClass(restaurant.kosher_category)
            )}>
              {restaurant.kosher_category.charAt(0).toUpperCase() + restaurant.kosher_category.slice(1)}
            </span>
          )}
          
          {/* Chalav Yisrael/Chalav Stam Badge - Only for dairy restaurants */}
          {restaurant.kosher_category === 'dairy' && (
            <span className={cn(
              "inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold border shadow-sm",
              restaurant.is_cholov_yisroel 
                ? "bg-cyan-100 text-cyan-800 border-cyan-200" 
                : "bg-orange-100 text-orange-800 border-orange-200"
            )}>
              {restaurant.is_cholov_yisroel ? "Chalav Yisrael" : "Chalav Stam"}
            </span>
          )}
          
          {/* Pas Yisroel Badge - Only for specific restaurants that are Pas Yisroel */}
          {(restaurant.kosher_category === 'meat' || restaurant.kosher_category === 'pareve') && 
           restaurant.is_pas_yisroel === true && (
            <span className={cn(
              "inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold border shadow-sm",
              "bg-purple-100 text-purple-800 border-purple-200"
            )}>
              Pas Yisroel
            </span>
          )}
        </div>
        
        {/* Distance Badge (if needed) */}
        {showDistance && distance !== undefined && (
          <div className="absolute top-12 right-3 bg-white/90 backdrop-blur-sm text-gray-800 px-2 py-1 rounded-full text-xs font-medium shadow-sm">
            {formatDistance(distance)}
          </div>
        )}
      </div>

      {/* Content Section */}
      <div className="p-3 sm:p-4">
        {/* Header */}
        <div className="mb-4">
          {/* Restaurant Name - Enhanced styling */}
          <h3 className="text-xl sm:text-2xl font-bold text-gray-900 mb-3 line-clamp-2 group-hover:text-green-600 transition-colors leading-tight">
            {restaurant.name}
          </h3>
          
          {/* Rating and Description */}
          <div className="text-sm text-gray-600 mb-3 space-y-1">
            {renderRating() && (
              <div className="flex items-center gap-2">
                {renderRating()}
                {restaurant.price_range && (
                  <span className="text-gray-500">•</span>
                )}
                {restaurant.price_range && (
                  <span className="capitalize">{restaurant.price_range} pricing</span>
                )}
              </div>
            )}
            <div>
              {restaurant.short_description ? (
                <span>{restaurant.short_description}</span>
              ) : (
                <span>Specializes in {(restaurant.listing_type || 'Restaurant').charAt(0).toUpperCase() + (restaurant.listing_type || 'Restaurant').slice(1)}.</span>
              )}
            </div>
          </div>
          
          {/* Open/Closed Status with Icon */}
          <div className="mb-3">
            {restaurant.hours_open ? (
              <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 border border-green-200">
                <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Open • {restaurant.hours_open}
              </span>
            ) : restaurant.hours_of_operation ? (
              <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800 border border-red-200">
                <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
                Closed now • {restaurant.hours_of_operation}
              </span>
            ) : (
              <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800 border border-gray-200">
                <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Hours not available
              </span>
            )}
          </div>
          
          {/* Address */}
          <div className="flex items-start gap-2 text-sm text-gray-600 mb-3">
            <svg className="w-4 h-4 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span className="line-clamp-2">
              {formatAddress(restaurant.address, restaurant.city, restaurant.state)}
            </span>
          </div>
          
          {/* Action Button - Below Address */}
          <div className="mb-4">
            <button
              className="w-full bg-transparent text-green-600 py-2 px-4 rounded-full font-semibold border-2 border-green-300 hover:bg-green-100 hover:border-green-400 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-green-300 focus:ring-offset-2 touch-manipulation shadow-sm"
              onClick={(e) => {
                e.stopPropagation();
                handleCardClick();
              }}
            >
              View More
            </button>
          </div>
        </div>

        {/* Badges Section - Only show unique badges, no redundancy */}
        <div className="flex flex-wrap gap-2 mb-4">
          {/* Listing Type - Only if no certifying agency to avoid duplication */}
          {restaurant.listing_type && !restaurant.certifying_agency && (
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800 border border-gray-200">
              <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              {restaurant.listing_type.charAt(0).toUpperCase() + restaurant.listing_type.slice(1)}
            </span>
          )}
        </div>

        {/* Contact Information */}
        <div className="space-y-2 text-sm text-gray-600 mb-4">
          {/* Phone */}
          {restaurant.phone_number && (
            <div className="flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              <a 
                href={`tel:${restaurant.phone_number}`}
                onClick={(e) => e.stopPropagation()}
                className="text-green-600 hover:text-green-700 underline transition-colors"
              >
                {restaurant.phone_number}
              </a>
            </div>
          )}
          
          {/* Website and Additional Links */}
          <div className="flex items-center justify-between">
            {/* Website Link - Left */}
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
                  className="text-green-600 hover:text-green-700 underline transition-colors truncate"
                >
                  Visit Website
                </a>
              </div>
            )}
            
            {/* Verified Badge - Center */}
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-black text-white border border-gray-800">
              <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              Verified
            </span>
            
            {/* Maps Button - Right */}
            <button
              className="inline-flex items-center gap-1 px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium hover:bg-gray-200 transition-colors"
              onClick={(e) => {
                e.stopPropagation();
                if (restaurant.google_listing_url) {
                  window.open(restaurant.google_listing_url, '_blank');
                } else {
                  // Fallback to Google Maps search
                  const address = formatAddress(restaurant.address, restaurant.city, restaurant.state);
                  const mapsUrl = `https://maps.google.com/?q=${encodeURIComponent(address)}`;
                  window.open(mapsUrl, '_blank');
                }
              }}
            >
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-1.447-.894L15 4m0 13V4m0 0L9 7" />
              </svg>
              Maps
            </button>
          </div>
        </div>


      </div>

      {/* Hover Effect Overlay */}
      <div className="absolute inset-0 bg-green-500 opacity-0 group-hover:opacity-5 transition-opacity duration-200 pointer-events-none" />
    </div>
  );
} 