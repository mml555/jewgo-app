'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Restaurant } from '@/types/restaurant';
import { cn } from '@/utils/cn';
import { ensureRestaurantWebsite, getFallbackWebsiteLink } from '@/utils/websiteBackup';
import HoursDisplay from '@/components/HoursDisplay';

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
  const [websiteLink, setWebsiteLink] = useState<string | null>(restaurant.website || null);
  const [isFetchingWebsite, setIsFetchingWebsite] = useState(false);

  const handleCardClick = () => {
    if (onSelect) {
      onSelect(restaurant);
    } else {
      router.push(`/restaurant/${restaurant.id}`);
    }
  };

  const handleTouchStart = () => setIsPressed(true);
  const handleTouchEnd = () => setIsPressed(false);

  // Auto-fetch website if missing
  useEffect(() => {
    const fetchWebsiteIfNeeded = async () => {
      // If we already have a website link, don't fetch
      if (websiteLink && websiteLink.length > 10) {
        return;
      }

      // If we're already fetching, don't start another request
      if (isFetchingWebsite) {
        return;
      }

      setIsFetchingWebsite(true);
      try {
        const fetchedWebsite = await ensureRestaurantWebsite(restaurant);
        if (fetchedWebsite) {
          setWebsiteLink(fetchedWebsite);
        }
      } catch (error) {
        console.error('Error fetching website:', error);
      } finally {
        setIsFetchingWebsite(false);
      }
    };

    fetchWebsiteIfNeeded();
  }, [restaurant.id, websiteLink, isFetchingWebsite]);

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

  // Get random placeholder price if missing
  const getPlaceholderPrice = () => {
    const prices = ['$', '$$', '$$$'];
    return prices[Math.floor(Math.random() * prices.length)];
  };

  const formatDistance = (distance: number) => {
    if (distance < 1) {
      return `${Math.round(distance * 5280)} ft`;
    }
    return `${distance.toFixed(1)} mi`;
  };

  const getHeroImage = () => {
    if (imageError || !restaurant.image_url) {
      return getCategoryPlaceholder(restaurant.kosher_category || restaurant.listing_type);
    }
    return restaurant.image_url;
  };

  // Clean address formatting - remove trailing commas
  const formatAddress = (address: string, city: string | null, state: string | null) => {
    const cleanAddress = address?.replace(/,\s*$/, '') || ''; // Remove trailing comma
    const cleanCity = city?.replace(/,\s*$/, '') || ''; // Remove trailing comma
    const cleanState = state || '';
    
    if (cleanCity && cleanState) {
      return `${cleanAddress}, ${cleanCity}, ${cleanState}`;
    } else if (cleanCity) {
      return `${cleanAddress}, ${cleanCity}`;
    } else {
      return cleanAddress;
    }
  };

  // Enhanced rating display with stars
  const renderRating = () => {
    const rating = restaurant.google_rating || restaurant.rating;
    if (!rating) return null;
    
    return (
      <span className="inline-flex items-center gap-1">
        <span className="text-yellow-500">⭐</span>
        <span className="text-sm font-medium">{rating}</span>
      </span>
    );
  };

  return (
    <div
      className={cn(
        "group relative bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden transition-all duration-200",
        "hover:shadow-lg hover:scale-[1.01] active:scale-[0.98]",
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
      <div className="relative aspect-[4/3] overflow-hidden bg-gray-100">
        <img
          src={getHeroImage()}
          alt={`${restaurant.name} restaurant`}
          className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
          onError={() => setImageError(true)}
          loading="lazy"
        />
        
        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent" />
        
        {/* Kosher Type Tag - Top Left */}
        {restaurant.kosher_category && (
          <span className={cn(
            "absolute top-2 left-2 text-white text-xs font-medium px-2 py-1 rounded-full",
            getKosherTypeColor(restaurant.kosher_category)
          )}>
            {titleCase(restaurant.kosher_category)}
          </span>
        )}
        
        {/* Heart Button - Top Right */}
        <button
          className={cn(
            "absolute top-2 right-2 bg-white rounded-full p-1 shadow-md transition-all duration-200",
            isFavorited 
              ? "text-pink-500" 
              : "text-gray-800 hover:text-pink-500"
          )}
          onClick={(e) => {
            e.stopPropagation();
            setIsFavorited(!isFavorited);
          }}
          aria-label={isFavorited ? "Remove from favorites" : "Add to favorites"}
        >
          <svg className="w-4 h-4" fill={isFavorited ? "currentColor" : "none"} stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
        </button>
        
        {/* Distance Badge (if needed) */}
        {showDistance && distance !== undefined && (
          <div className="absolute bottom-2 right-2 bg-white/90 backdrop-blur-sm text-gray-800 px-2 py-1 rounded-full text-xs font-medium shadow-sm">
            {formatDistance(distance)}
          </div>
        )}
      </div>

      {/* Content Section */}
      <div className="px-3 py-2">
        {/* Restaurant Name */}
        <h3 className="text-[15px] font-semibold leading-snug text-gray-900 mb-2 line-clamp-2 group-hover:text-green-600 transition-colors tracking-tight">
          {titleCase(restaurant.name)}
        </h3>
        
        {/* Rating and Price - Aligned in one row */}
        <div className="flex items-center gap-1 text-sm text-gray-500 mb-2">
          {restaurant.price_range && (
            <span>{restaurant.price_range}</span>
          )}
          {restaurant.price_range && renderRating() && (
            <span>•</span>
          )}
          {renderRating()}
        </div>
        
        {/* Hours Display */}
        <div className="mb-2">
          <HoursDisplay 
            hoursOfOperation={restaurant.hours_of_operation}
            hoursJson={restaurant.hours_json ? (typeof restaurant.hours_json === 'string' ? JSON.parse(restaurant.hours_json) : restaurant.hours_json) : undefined}
            hoursLastUpdated={restaurant.hours_last_updated}
          />
        </div>
        
        {/* Address */}
        <div className="flex items-start gap-2 text-sm text-gray-600 mb-2">
          <svg className="w-4 h-4 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span className="line-clamp-2">
            {formatAddress(restaurant.address, restaurant.city, restaurant.state)}
          </span>
        </div>
        
        {/* Phone Number */}
        {restaurant.phone_number && (
          <div className="flex items-center gap-2 text-sm text-gray-600 mb-2">
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
        
        {/* Action Button */}
        <div className="mt-3">
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

        {/* Badges Section - Only show unique badges, no redundancy */}
        <div className="flex flex-wrap gap-2 mt-3">
          {/* Listing Type - Only if no certifying agency to avoid duplication */}
          {restaurant.listing_type && !restaurant.certifying_agency && (
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800 border border-gray-200">
              <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              {titleCase(restaurant.listing_type)}
            </span>
          )}
        </div>

        {/* Contact Information */}
        <div className="space-y-2 text-sm text-gray-600 mt-3">
          {/* Website and Additional Links */}
          <div className="flex items-center justify-between">
            {/* Website Link - Left */}
            {websiteLink ? (
              <div className="flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9" />
                </svg>
                <a 
                  href={websiteLink}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={(e) => e.stopPropagation()}
                  className="text-green-600 hover:text-green-700 underline transition-colors truncate"
                >
                  {isFetchingWebsite ? 'Finding Website...' : 'Visit Website'}
                </a>
              </div>
            ) : (
              // Show fallback options when no website is available
              <div className="flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9" />
                </svg>
                {isFetchingWebsite ? (
                  <span className="text-gray-500 text-sm">Finding website...</span>
                ) : (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      // Try to fetch website manually
                      const fallbackLink = getFallbackWebsiteLink(restaurant);
                      if (fallbackLink) {
                        window.open(fallbackLink, '_blank');
                      }
                    }}
                    className="text-gray-500 hover:text-green-600 underline transition-colors text-sm"
                  >
                    Find on Google
                  </button>
                )}
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