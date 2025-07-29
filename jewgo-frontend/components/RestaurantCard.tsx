'use client';

import Image from 'next/image';
import { useRouter } from 'next/navigation';
import { Restaurant } from '@/types/restaurant';
import LogoIcon from './LogoIcon';
import SpecialsCard from './SpecialsCard';
import { getRestaurantDistance, formatDistance } from '@/utils/distance';
import { getHoursStatus } from '@/utils/hours';
import { useState, useEffect } from 'react';

interface RestaurantCardProps {
  restaurant: Restaurant;
  onClick?: () => void;
  userLocation?: { latitude: number; longitude: number } | null;
  index?: number;
}

export default function RestaurantCard({ restaurant, onClick, userLocation, index }: RestaurantCardProps) {
  const router = useRouter();
  const [imageError, setImageError] = useState(false);
  const [isNavigating, setIsNavigating] = useState(false);

  // Helper functions - defined before use
  const getCategoryEmoji = (name: string, category?: string) => {
    const lowerName = name.toLowerCase();
    const lowerCategory = category?.toLowerCase() || '';
    
    // Check for specific food types in name
    if (lowerName.includes('sushi') || lowerName.includes('japanese')) return '🍣';
    if (lowerName.includes('pizza') || lowerName.includes('italian')) return '🍕';
    if (lowerName.includes('burger') || lowerName.includes('american')) return '🍔';
    if (lowerName.includes('ice cream') || lowerName.includes('dessert')) return '🍦';
    if (lowerName.includes('coffee') || lowerName.includes('cafe')) return '☕';
    if (lowerName.includes('bakery') || lowerName.includes('bread')) return '🥖';
    if (lowerName.includes('steak') || lowerName.includes('grill')) return '🥩';
    if (lowerName.includes('salad') || lowerName.includes('healthy')) return '🥗';
    if (lowerName.includes('chicken') || lowerName.includes('poultry')) return '🍗';
    if (lowerName.includes('fish') || lowerName.includes('seafood')) return '🐟';
    
    // Check category
    if (lowerCategory.includes('dairy')) return '🥛';
    if (lowerCategory.includes('meat')) return '🥩';
    if (lowerCategory.includes('pareve')) return '🥬';
    
    // Default restaurant emoji
    return '🍽️';
  };

  const getHeroImage = (restaurant: Restaurant) => {
    // Check if image_url is a Google Places photo URL that might fail
    const isGooglePlacesUrl = restaurant.image_url?.includes('maps.googleapis.com/maps/api/place/photo');
    
    // If it's a Google Places URL, skip it and use fallbacks to avoid 403 errors
    if (isGooglePlacesUrl) {
      // Skip Google Places URLs and use fallbacks instead
      console.log('Skipping Google Places photo URL to avoid 403 errors');
    } else if (restaurant.image_url) {
      // Use non-Google Places image URLs
      return restaurant.image_url;
    }
    
    // Category-specific Unsplash fallbacks with reliable URLs
    const category = restaurant.kosher_category?.toLowerCase() || 'restaurant';
    const fallbackImages = {
      dairy: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=400&h=300&q=80',
      meat: 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=400&h=300&q=80',
      pareve: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=400&h=300&q=80',
      restaurant: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=400&h=300&q=80'
    };
    
    return fallbackImages[category as keyof typeof fallbackImages] || fallbackImages.restaurant;
  };

  const handleClick = () => {
    if (onClick) {
      onClick();
    } else {
      router.push(`/restaurant/${restaurant.id}`);
    }
  };

  // Calculate distance if location is available
  const distance = userLocation ? getRestaurantDistance(restaurant, userLocation) : null;
  const formattedDistance = distance ? formatDistance(distance) : null;
  
  // Get category emoji for fallback display
  const categoryEmoji = getCategoryEmoji(restaurant.name, restaurant.kosher_category);

  const getAgencyBadgeClass = (agency: string) => {
    switch (agency?.toUpperCase()) {
      case 'ORB':
        return 'border-blue-500 text-white hover:bg-blue-500 hover:text-white border-white';
      case 'KM':
        return 'border-green-500 text-green-500 hover:bg-green-500 hover:text-white';
      case 'KDM':
        return 'border-yellow-500 text-yellow-500 hover:bg-yellow-500 hover:text-white';
      case 'DIAMOND K':
        return 'border-purple-300 text-purple-300 hover:bg-purple-300 hover:text-white';
      default:
        return 'border-gray-500 text-gray-500 hover:bg-gray-500 hover:text-white';
    }
  };

  const getKosherBadgeClass = (category: string) => {
    switch (category?.toLowerCase()) {
      case 'meat':
        return 'bg-red-500 text-white';
      case 'dairy':
        return 'bg-blue-500 text-white';
      case 'pareve':
        return 'bg-orange-500 text-white';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  const formatAddress = (address: string, city?: string, state?: string) => {
    const parts = [address, city, state].filter(Boolean);
    const fullAddress = parts.join(', ');
    
    // Truncate very long addresses to prevent overflow
    if (fullAddress.length > 50) {
      return fullAddress.substring(0, 47) + '...';
    }
    
    return fullAddress;
  };

  const getGoogleMapsUrl = (name: string, address?: string) => {
    const searchQuery = encodeURIComponent(`${name} ${address || ''}`.trim());
    return `https://www.google.com/maps/search/${searchQuery}`;
  };

  // Get hours status using the utility function
  const hoursStatus = getHoursStatus(restaurant.hours_open || restaurant.hours_of_operation);


  const getCertificationWebsite = (agency: string) => {
    switch (agency?.toUpperCase()) {
      case 'ORB': return 'https://www.orbkosher.com';
      case 'KM': return 'https://koshermiami.org';
      case 'KDM': return 'https://koshermiami.org';
      case 'DIAMOND K': return 'https://www.orbkosher.com';
      case 'OU': return 'https://oukosher.org';
      case 'STAR-K': return 'https://www.star-k.org';
      case 'CRC': return 'https://www.crcweb.org';
      default: return null;
    }
  };

  const handleCertificationClick = (agency: string, e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent card click
    const website = getCertificationWebsite(agency);
    if (website) {
      window.open(website, '_blank', 'noopener,noreferrer');
    }
  };







  return (
    <div className="relative">
      <div className="bg-white rounded-xl shadow-soft border border-gray-200 overflow-hidden hover:shadow-medium hover:scale-[1.02] transition-all duration-300 group h-[520px] flex flex-col">
        {/* Image Section */}
        <div className="relative h-52 w-full overflow-hidden flex-shrink-0">
          {!imageError ? (
            <Image
              src={getHeroImage(restaurant)}
              alt={`${restaurant.name} restaurant image`}
              fill
              className="object-cover object-center group-hover:scale-105 transition-transform duration-300"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
              onError={() => setImageError(true)}
              unoptimized
              priority={index !== undefined && index < 4}
              loading={index !== undefined && index < 4 ? "eager" : "lazy"}
              placeholder="blur"
              blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAAIAAoDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAhEAACAQMDBQAAAAAAAAAAAAABAgMABAUGIWGRkqGx0f/EABUBAQEAAAAAAAAAAAAAAAAAAAMF/8QAGhEAAgIDAAAAAAAAAAAAAAAAAAECEgMRkf/aAAwDAQACEQMRAD8AltJagyeH0AthI5xdrLcNM91BF5pX2HaH9bcfaSXWGaRmknyJckliyjqTzSlT54b6bk+h0R//2Q=="
              quality={85}
            />
          ) : (
            <div className="w-full h-full bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center">
              <span className="text-5xl" aria-label={`${restaurant.name} food category`}>{categoryEmoji}</span>
            </div>
          )}
          
          {/* Overlay with badges */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent">

            {/* Certification Badge - Bottom-left corner */}
            {restaurant.certifying_agency && restaurant.certifying_agency !== 'Unknown' && (
              <div className="absolute bottom-2 left-2 z-30">
                <button
                  onClick={(e) => handleCertificationClick(restaurant.certifying_agency, e)}
                  className={`px-2 py-1 rounded-full text-xs font-bold shadow-lg backdrop-blur-sm border-2 transition-all duration-200 max-w-[100px] truncate ${getAgencyBadgeClass(restaurant.certifying_agency)}`}
                  title={`${restaurant.certifying_agency} Kosher Certification - Click to visit website`}
                  aria-label={`${restaurant.certifying_agency} kosher certification badge - click to visit website`}
                >
                  {restaurant.certifying_agency}
                </button>
              </div>
            )}
            
            {/* Kosher Type Badge - Bottom-right corner */}
            {restaurant.kosher_category && (
              <div className="absolute bottom-2 right-2 z-30 flex flex-row gap-1">
                <span className={`px-2 py-1 rounded-full text-xs font-bold shadow-lg backdrop-blur-sm max-w-[60px] truncate ${getKosherBadgeClass(restaurant.kosher_category)}`} aria-label={`${restaurant.kosher_category} kosher category`}>
                  {restaurant.kosher_category.charAt(0).toUpperCase() + restaurant.kosher_category.slice(1)}
                </span>
                
                {/* Cholov Yisroel Badge - Show if dairy and certified by ORB or KM */}
                {restaurant.kosher_category.toLowerCase() === 'dairy' && 
                 (restaurant.certifying_agency?.toUpperCase() === 'ORB' || restaurant.certifying_agency?.toUpperCase() === 'KM') && (
                  <span className="px-2 py-1 rounded-full text-xs font-bold shadow-lg backdrop-blur-sm bg-blue-300 text-white max-w-[120px] truncate" aria-label="Cholov Yisroel certified">
                    Cholov Yisroel
                  </span>
                )}
                
                {/* Cholov Stam Badge - Show if dairy and certified by KDM or Diamond K */}
                {restaurant.kosher_category.toLowerCase() === 'dairy' && 
                 (restaurant.certifying_agency?.toUpperCase() === 'KDM' || restaurant.certifying_agency?.toUpperCase() === 'DIAMOND K') && (
                  <span className="px-2 py-1 rounded-full text-xs font-bold shadow-lg backdrop-blur-sm bg-gray-400 text-white max-w-[120px] truncate" aria-label="Cholov Stam certified">
                    Cholov Stam
                  </span>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Content Section */}
        <div className="p-4 flex flex-col flex-1">
          {/* Top Content: Name, Description, Hours, Address */}
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Store Name */}
            <div className="mb-3 min-h-[2.5rem] max-h-[2.5rem] overflow-hidden">
              <div className="flex items-start gap-2">
                <h3 className="font-semibold text-lg text-gray-900 leading-tight flex-1 overflow-hidden" style={{
                  display: '-webkit-box',
                  WebkitLineClamp: 2,
                  WebkitBoxOrient: 'vertical',
                  textOverflow: 'ellipsis',
                  lineHeight: '1.25',
                  maxHeight: '2.5rem',
                  wordBreak: 'break-word'
                }}>
                  {restaurant.name}
                </h3>
                {formattedDistance && (
                  <button
                    onClick={async (e) => {
                      e.stopPropagation();
                      
                      // Validate coordinates before navigation
                      const lat = restaurant.latitude;
                      const lng = restaurant.longitude;
                      
                      if (!lat || !lng || isNaN(Number(lat)) || isNaN(Number(lng))) {
                        console.warn('Invalid coordinates for restaurant:', restaurant.name, { lat, lng });
                        // Fallback to Google Maps with address
                        const mapsUrl = getGoogleMapsUrl(restaurant.name, restaurant.address);
                        window.open(mapsUrl, '_blank', 'noopener,noreferrer');
                        return;
                      }
                      
                      // Validate coordinate ranges
                      const latNum = Number(lat);
                      const lngNum = Number(lng);
                      
                      if (latNum < -90 || latNum > 90 || lngNum < -180 || lngNum > 180) {
                        console.warn('Coordinates out of valid range for restaurant:', restaurant.name, { lat: latNum, lng: lngNum });
                        // Fallback to Google Maps with address
                        const mapsUrl = getGoogleMapsUrl(restaurant.name, restaurant.address);
                        window.open(mapsUrl, '_blank', 'noopener,noreferrer');
                        return;
                      }
                      
                      setIsNavigating(true);
                      console.log('Navigating to live map for restaurant:', {
                        name: restaurant.name,
                        lat: latNum,
                        lng: lngNum
                      });
                      
                      try {
                        await router.push(`/live-map?lat=${latNum}&lng=${lngNum}&name=${encodeURIComponent(restaurant.name)}`);
                      } catch (error) {
                        console.error('Navigation error:', error);
                        // Fallback to Google Maps
                        const mapsUrl = getGoogleMapsUrl(restaurant.name, restaurant.address);
                        window.open(mapsUrl, '_blank', 'noopener,noreferrer');
                      } finally {
                        setIsNavigating(false);
                      }
                    }}
                    disabled={isNavigating}
                    className={`text-sm font-normal whitespace-nowrap flex-shrink-0 mt-0.5 transition-colors cursor-pointer hover:bg-gray-100 px-1 py-0.5 rounded ${
                      isNavigating 
                        ? 'text-gray-400 cursor-not-allowed' 
                        : 'text-gray-500 hover:text-jewgo-primary hover:underline'
                    }`}
                    title={`View ${restaurant.name} on Live Map`}
                    aria-label={`View ${restaurant.name} on live map`}
                  >
                    {isNavigating ? '⏳' : '•'} {formattedDistance}
                  </button>
                )}
              </div>
            </div>

            {/* Store Description */}
            <div className="mb-3 min-h-[2.8rem]">
              {restaurant.short_description ? (
                <p className="text-sm text-gray-600 overflow-hidden" style={{
                  display: '-webkit-box',
                  WebkitLineClamp: 2,
                  WebkitBoxOrient: 'vertical',
                  textOverflow: 'ellipsis',
                  lineHeight: '1.4',
                  maxHeight: '2.8rem'
                }}>
                  {restaurant.short_description}
                </p>
              ) : null}
            </div>

            {/* Current Hours Info - Clean Design */}
            {hoursStatus && hoursStatus.type !== 'unknown' ? (
              <div className="mb-3 min-h-[1.5rem]">
                <div className="flex items-center justify-center">
                  <span 
                    className={`text-xs font-medium px-2 py-1 rounded-full ${hoursStatus.badge} bg-opacity-10`}
                    title={hoursStatus.tooltip}
                    aria-label={`Restaurant hours status: ${hoursStatus.label}`}
                  >
                    {hoursStatus.icon} {hoursStatus.label}
                  </span>
                </div>
              </div>
            ) : (
              <div className="mb-3 min-h-[1.5rem] flex items-center justify-center">
                <span className="text-xs text-gray-400 px-2 py-1 rounded-full bg-gray-100">
                  ⏰ Hours not available
                </span>
              </div>
            )}

            {/* View Full Listing Button */}
            <button
              onClick={handleClick}
              className="w-full border-2 border-jewgo-primary text-jewgo-primary py-2 px-4 rounded-full text-sm font-medium hover:bg-jewgo-primary hover:text-white transition-all duration-200 mb-3"
              aria-label={`View full listing for ${restaurant.name}`}
            >
              View More
            </button>

            {/* Address - Single Line */}
            {restaurant.address ? (
              <div className="flex items-center space-x-2 mb-3 min-h-[1.5rem]">
                <svg className="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
                <p className="text-sm text-gray-500 line-clamp-1 leading-tight">
                  {formatAddress(restaurant.address, restaurant.city, restaurant.state)}
                </p>
              </div>
            ) : (
              <div className="mb-3 min-h-[1.5rem]"></div>
            )}
          </div>

                      {/* Compact Footer */}
          <div className="mt-auto pt-3 pb-2 px-4 border-t border-gray-200 bg-gray-50">
            <div className="flex items-center justify-between">
              {/* Left side: View Map */}
              <a
                href={getGoogleMapsUrl(restaurant.name, restaurant.address)}
                target="_blank"
                rel="noopener noreferrer"
                onClick={(e) => e.stopPropagation()}
                className="inline-flex items-center px-2 py-1.5 border border-gray-300 text-gray-700 text-xs font-medium rounded-full hover:bg-gray-100 transition-colors bg-white"
                title="View on Google Maps"
                aria-label="View on Google Maps"
              >
                <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-1.447-.894L15 4m0 13V4m-6 3l6-3"></path>
                </svg>
                View Map
              </a>

              {/* Right side: Verified */}
              <div className="flex items-center space-x-1 text-gray-600 text-xs" title="JewGo Verified">
                <LogoIcon size="xs" />
                <span className="font-medium">Verified</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 