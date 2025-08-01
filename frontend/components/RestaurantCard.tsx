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
    if (!rating || rating === 0) return null;
    
    return (
      <span className="inline-flex items-center gap-1">
        <span className="text-yellow-500">★</span>
        <span className="text-xs font-medium">{typeof rating === 'number' ? rating.toFixed(1) : rating}</span>
      </span>
    );
  };

  return (
    <div
      className={cn(
        "group relative bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg hover:scale-[1.01] transition-all duration-200",
        "focus-within:ring-2 focus-within:ring-green-500 focus-within:ring-offset-2",
        "touch-manipulation cursor-pointer",
        isPressed && "scale-[0.98] shadow-lg",
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
        
        {/* Kosher Type Tag - Top Left */}
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
        
        {/* Heart Button - Top Right */}
        <button
          className={cn(
            "absolute top-2 right-2 bg-white p-1 rounded-full shadow hover:scale-105 transition-all duration-200",
            isFavorited 
              ? "text-red-500" 
              : "text-red-400"
          )}
          onClick={(e) => {
            e.stopPropagation();
            setIsFavorited(!isFavorited);
          }}
          aria-label={isFavorited ? "Remove from favorites" : "Add to favorites"}
        >
          <svg className="w-5 h-5" fill={isFavorited ? "currentColor" : "none"} stroke="currentColor" viewBox="0 0 24 24">
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
      <div className="p-3">
        {/* Restaurant Name */}
        <h3 className="text-sm font-medium truncate mb-1 group-hover:text-green-600 transition-colors">
          {titleCase(restaurant.name)}
        </h3>
        
        {/* Price Range */}
        {restaurant.price_range && (
          <p className="text-xs text-gray-500 truncate mb-1">
            Price range {restaurant.price_range}
          </p>
        )}
        
        {/* Rating */}
        {renderRating() && (
          <div className="flex items-center gap-1 text-yellow-500 text-sm">
            <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
            <span className="text-gray-700">{restaurant.rating?.toFixed(2) || '0.00'}</span>
          </div>
        )}
      </div>
    </div>
  );
} 