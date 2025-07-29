'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Image from 'next/image';
import { Restaurant, RestaurantSpecial } from '@/types/restaurant';
import Logo from '@/components/Logo';
import Reviews from '@/components/Reviews';
import { formatWeeklyHoursArray, getHoursStatus } from '@/utils/hours';

const RestaurantDetailPage: React.FC = () => {
  const params = useParams();
  const router = useRouter();
  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showFullSchedule, setShowFullSchedule] = useState(false);
  const [showWriteReviewModal, setShowWriteReviewModal] = useState(false);
  const [imageError, setImageError] = useState(false);

  useEffect(() => {
    const fetchRestaurant = async () => {
      try {
        const response = await fetch(`/api/restaurants/${params.id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        if (!response.ok) {
          throw new Error('Restaurant not found');
        }
        const data = await response.json();
        
        if (data.success && data.restaurant) {
          setRestaurant(data.restaurant);
        } else if (data.restaurant) {
          setRestaurant(data.restaurant);
        } else {
          throw new Error('Invalid response format');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load restaurant');
      } finally {
        setLoading(false);
      }
    };

    if (params.id) {
      fetchRestaurant();
    }
  }, [params.id]);

  const getAgencyBadgeClass = (agency: string) => {
    switch (agency?.toUpperCase()) {
      case 'ORB':
        return 'bg-blue-500/90 text-blue-100';
      case 'KM':
        return 'bg-green-500/90 text-green-100';
      case 'KDM':
        return 'bg-yellow-500/90 text-yellow-100';
      case 'DIAMOND K':
        return 'bg-purple-500/90 text-purple-100';
      default:
        return 'bg-gray-500/90 text-gray-100';
    }
  };

  const getKosherBadgeClass = (category: string) => {
    switch (category?.toLowerCase()) {
      case 'meat':
        return 'bg-red-500/90 text-red-100';
      case 'dairy':
        return 'bg-blue-500/90 text-blue-100';
      case 'pareve':
        return 'bg-green-500/90 text-green-100';
      default:
        return 'bg-gray-500/90 text-gray-100';
    }
  };

  const getCertificationWebsite = (agency: string) => {
    switch (agency?.toUpperCase()) {
      case 'KM':
      case 'KDM':
        return 'https://koshermiami.org/';
      case 'ORB':
      case 'DIAMOND K':
        return 'https://www.rabbinicalcouncil.org/';
      default:
        return null;
    }
  };

  const handleCertificationClick = (agency: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const website = getCertificationWebsite(agency);
    if (website) {
      window.open(website, '_blank', 'noopener,noreferrer');
    }
  };

  const formatCompleteAddress = (restaurant: Restaurant) => {
    const parts = [];
    
    // Check if address already contains city, state, zip
    if (restaurant.address && restaurant.address.includes(',')) {
      // Address already contains full information
      return restaurant.address;
    }
    
    if (restaurant.address) {
      parts.push(restaurant.address);
    }
    
    if (restaurant.city) {
      parts.push(restaurant.city);
    }
    
    if (restaurant.state) {
      parts.push(restaurant.state);
    }
    
    // Only add zip_code if it's not empty
    if (restaurant.zip_code && restaurant.zip_code.trim() !== '') {
      parts.push(restaurant.zip_code);
    }
    
    const formattedAddress = parts.length > 0 ? parts.join(', ') : 'Address not available';
    
    // Add note if zip code is missing but we have other address info
    if (parts.length >= 3 && (!restaurant.zip_code || restaurant.zip_code.trim() === '')) {
      return `${formattedAddress} (Zip code not available)`;
    }
    
    return formattedAddress;
  };

  const getHeroImage = (restaurant: Restaurant) => {
    // Check if image_url is a Google Places photo URL that might fail
    const isGooglePlacesUrl = restaurant.image_url?.includes('maps.googleapis.com/maps/api/place/photo');
    
    // If it's a Google Places URL, skip it and use fallbacks to avoid 403 errors
    if (isGooglePlacesUrl) {
      // Skip Google Places URLs and use fallbacks instead
      console.log('Skipping Google Places photo URL to avoid 403 errors');
    } else if (restaurant.image_url && !imageError) {
      // Use non-Google Places image URLs
      return restaurant.image_url;
    }
    
    // Category-specific Unsplash fallbacks with reliable URLs
    const category = restaurant.kosher_category?.toLowerCase() || 'restaurant';
    const fallbackImages = {
      dairy: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?auto=format&fit=crop&w=800&h=400&q=80',
      meat: 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&h=400&q=80',
      pareve: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&h=400&q=80',
      restaurant: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&h=400&q=80'
    };
    
    return fallbackImages[category as keyof typeof fallbackImages] || fallbackImages.restaurant;
  };

  const getGoogleMapsEmbedUrl = (restaurant: Restaurant) => {
    const address = formatCompleteAddress(restaurant);
    const encodedAddress = encodeURIComponent(address);
    const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;
    return `https://www.google.com/maps/embed/v1/place?key=${apiKey}&q=${encodedAddress}`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading restaurant details...</p>
        </div>
      </div>
    );
  }

  if (error || !restaurant) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">🍽️</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Restaurant Not Found</h1>
          <p className="text-gray-600 mb-6">{error || 'The restaurant you\'re looking for doesn\'t exist.'}</p>
          <button
            onClick={() => router.push('/')}
            className="bg-green-600 text-white px-6 py-3 rounded-full font-medium hover:bg-green-700 transition-colors"
          >
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  // Filter out free specials, keep only paid ones
  const paidSpecials = restaurant.specials?.filter(special => special.is_paid) || [];

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => router.push('/')}
              className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7"></path>
              </svg>
              <span className="font-medium">Back</span>
            </button>
            <Logo />
            <div className="w-6"></div> {/* Spacer for centering */}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
        {/* Hero Image Section */}
        <div className="relative h-64 bg-gray-200 rounded-xl overflow-hidden">
          <Image
            src={getHeroImage(restaurant)}
            alt={`${restaurant.name} restaurant hero image`}
            fill
            className="object-cover object-center"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 80vw, 1200px"
            priority
            quality={90}
            onError={() => setImageError(true)}
          />
        </div>

        {/* Restaurant Info Card */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
          <div className="text-center">
            {/* Restaurant Name */}
            <div className="mb-4">
              <h1 className="text-3xl font-bold text-gray-900 leading-tight">{restaurant.name}</h1>
            </div>
            
            {/* Kosher Type and Certification Badges */}
            <div className="flex items-center justify-center space-x-3 mb-4">
              {/* Kosher Type Badge */}
              {restaurant.kosher_category && (
                <span className={`px-3 py-1 rounded-full text-white text-sm font-bold shadow-md ${getKosherBadgeClass(restaurant.kosher_category)}`}>
                  {restaurant.kosher_category.charAt(0).toUpperCase() + restaurant.kosher_category.slice(1)}
                </span>
              )}
              
              {/* Certification Badge */}
              {restaurant.certifying_agency && restaurant.certifying_agency !== 'Unknown' && (
                <button
                  onClick={(e) => handleCertificationClick(restaurant.certifying_agency, e)}
                  className={`px-3 py-1 rounded-full text-white text-sm font-bold shadow-md hover:opacity-80 transition-opacity ${getAgencyBadgeClass(restaurant.certifying_agency)}`}
                  title={`${restaurant.certifying_agency} Kosher Certification - Click to visit website`}
                >
                  {restaurant.certifying_agency}
                </button>
              )}
            </div>
            
            {/* Rating, Price Range, and Cost Information */}
            <div className="flex items-center justify-center space-x-6 mb-4">
              {/* Rating */}
              {(restaurant.google_rating && restaurant.google_rating > 0) || (restaurant.rating && restaurant.rating > 0) ? (
                <div className="flex items-center space-x-2">
                  <div className="flex items-center">
                    {[...Array(5)].map((_, i) => {
                      const rating = restaurant.google_rating || restaurant.rating || 0;
                      return (
                        <svg
                          key={i}
                          className={`w-5 h-5 ${i < Math.floor(rating) ? 'text-yellow-400' : 'text-gray-300'}`}
                          fill="currentColor"
                          viewBox="0 0 20 20"
                        >
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                      );
                    })}
                  </div>
                  <span className="text-lg font-semibold text-gray-700">
                    {(restaurant.google_rating || restaurant.rating || 0).toFixed(1)}
                  </span>
                  {(restaurant.google_review_count && restaurant.google_review_count > 0) || (restaurant.review_count && restaurant.review_count > 0) ? (
                    <span className="text-gray-500">
                      ({(restaurant.google_review_count || restaurant.review_count || 0)} reviews)
                    </span>
                  ) : null}
                </div>
              ) : (
                <div className="text-gray-400">No rating available</div>
              )}

              {/* Average Meal Cost */}
              {restaurant.min_avg_meal_cost && restaurant.max_avg_meal_cost ? (
                <div className="flex items-center space-x-2 group relative">
                  <span className="text-lg font-semibold text-green-700">
                    💰 ${restaurant.min_avg_meal_cost} - ${restaurant.max_avg_meal_cost}
                  </span>
                  <span className="text-sm text-gray-500">
                    avg meal
                  </span>
                  {/* Tooltip */}
                  <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
                    <div className="text-center">
                      <div className="font-semibold mb-1">Meal Cost Calculation</div>
                      <div className="text-xs">
                        <div>• Minimum: Main dish + drink</div>
                        <div>• Maximum: Full meal with appetizer + dessert</div>
                        <div>• Based on typical menu prices</div>
                      </div>
                    </div>
                    <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-4 border-transparent border-t-gray-900"></div>
                  </div>
                </div>
              ) : null}

              {/* Price Range */}
              {restaurant.price_range && (
                <div className="flex items-center">
                  <span className="text-lg font-semibold text-gray-700">
                    {restaurant.price_range}
                  </span>
                </div>
              )}
            </div>
            
            {/* Address */}
            <div className="text-center mb-4">
              <p className="text-gray-600">{formatCompleteAddress(restaurant)}</p>
            </div>
          </div>
        </div>

        {/* Hours of Operation Section */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4 text-center">Hours of Operation</h2>
          {restaurant.hours_open || restaurant.hours_of_operation ? (
            <div className="space-y-4">
              {/* Current Status */}
              {(() => {
                const hoursStatus = getHoursStatus(restaurant.hours_open || restaurant.hours_of_operation);
                return (
                  <div className="text-center mb-4">
                    <span 
                      className={`text-sm font-medium px-3 py-2 rounded-full ${hoursStatus.badge} bg-opacity-10`}
                      title={hoursStatus.tooltip}
                    >
                      {hoursStatus.icon} {hoursStatus.label}
                    </span>
                  </div>
                );
              })()}
              
              {/* Dropdown for Full Weekly Schedule */}
              {(() => {
                const weeklyHours = formatWeeklyHoursArray(restaurant.hours_open || restaurant.hours_of_operation);
                return weeklyHours ? (
                  <div className="max-w-md mx-auto">
                    <details className="group">
                      <summary className="cursor-pointer text-center text-sm text-blue-600 hover:text-blue-800 font-medium flex items-center justify-center space-x-1">
                        <span>View full weekly schedule</span>
                        <svg className="w-4 h-4 transition-transform group-open:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path>
                        </svg>
                      </summary>
                      <div className="mt-4 pt-4 border-t border-gray-100">
                        <div className="grid grid-cols-1 gap-2">
                          {weeklyHours.map((day, index) => (
                            <div key={day.day} className="flex justify-between items-center py-2 px-3 bg-gray-50 rounded-lg">
                              <span className="font-medium text-gray-700">{day.day}</span>
                              <span className="text-gray-600">{day.hours}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </details>
                  </div>
                ) : (
                  <p className="text-center text-gray-500">Weekly schedule not available</p>
                );
              })()}
            </div>
          ) : (
            <p className="text-center text-gray-500">Hours information not available</p>
          )}
        </div>

        {/* Cost Information Section */}
        {restaurant.min_avg_meal_cost && restaurant.max_avg_meal_cost && (
          <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4 text-center">Cost Information</h2>
            <div className="max-w-md mx-auto">
              <div className="grid grid-cols-1 gap-4">
                {/* Minimum Cost */}
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 group relative">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-semibold text-green-800">Minimum Meal Cost</h3>
                      <p className="text-sm text-green-600">Main dish + drink</p>
                    </div>
                    <div className="text-right">
                      <span className="text-2xl font-bold text-green-700">${restaurant.min_avg_meal_cost}</span>
                    </div>
                  </div>
                  {/* Info Icon */}
                  <div className="absolute top-2 right-2">
                    <svg className="w-4 h-4 text-green-600 opacity-60 group-hover:opacity-100 transition-opacity" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
                
                {/* Maximum Cost */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 group relative">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-semibold text-blue-800">Maximum Meal Cost</h3>
                      <p className="text-sm text-blue-600">Main dish + drink + appetizer + dessert</p>
                    </div>
                    <div className="text-right">
                      <span className="text-2xl font-bold text-blue-700">${restaurant.max_avg_meal_cost}</span>
                    </div>
                  </div>
                  {/* Info Icon */}
                  <div className="absolute top-2 right-2">
                    <svg className="w-4 h-4 text-blue-600 opacity-60 group-hover:opacity-100 transition-opacity" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
              </div>
              
              <div className="mt-4 text-center">
                <p className="text-sm text-gray-600">
                  💡 These are average costs based on typical meal combinations
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Map Section */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4 text-center">Location</h2>
          <div className="h-64 rounded-lg overflow-hidden">
            <iframe
              src={getGoogleMapsEmbedUrl(restaurant)}
              width="100%"
              height="100%"
              style={{ border: 0 }}
              allowFullScreen
              loading="lazy"
              referrerPolicy="no-referrer-when-downgrade"
              title={`${restaurant.name} location`}
            />
          </div>
        </div>

        {/* Specials Section */}
        {paidSpecials.length > 0 && (
          <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4 text-center">Our Specials</h2>
            <div className="flex space-x-4 overflow-x-auto pb-2 justify-center">
              {paidSpecials.slice(0, 3).map((special, index) => (
                <div key={special.id} className="bg-white border rounded-lg overflow-hidden shadow-sm flex-shrink-0 w-48 hover:shadow-md hover:scale-105 transition-all duration-200">
                  <div className="h-32 bg-gray-200 relative">
                    <div className="w-full h-full bg-gradient-to-br from-orange-100 to-red-100 flex items-center justify-center">
                      <div className="text-center">
                        <div className="text-4xl mb-2" role="img" aria-label="Food">🍔</div>
                      </div>
                    </div>
                  </div>
                  <div className="p-3">
                    <h3 className="font-semibold text-sm text-gray-900 mb-2 leading-tight">{special.title}</h3>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Action Buttons Card */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4 text-center">Get in Touch</h2>
          <div className="flex space-x-4 max-w-md mx-auto">
            {restaurant.website ? (
              <a 
                href={restaurant.website}
                target="_blank"
                rel="noopener noreferrer"
                className="flex-1 border-2 border-black text-black py-4 rounded-full font-medium flex items-center justify-center space-x-2 hover:bg-black hover:text-white transition-all duration-200"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9"></path>
                </svg>
                <span>Website</span>
              </a>
            ) : (
              <button className="flex-1 border-2 border-gray-300 text-gray-400 py-4 rounded-full font-medium flex items-center justify-center space-x-2 cursor-not-allowed">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9"></path>
                </svg>
                <span>Website</span>
              </button>
            )}

            <button className="flex-1 border-2 border-green-600 text-green-600 py-4 rounded-full font-medium flex items-center justify-center space-x-2 hover:bg-green-600 hover:text-white transition-all duration-200">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
              </svg>
              <span>Order</span>
            </button>

            {restaurant.phone_number ? (
              <a 
                href={`tel:${restaurant.phone_number}`}
                className="flex-1 border-2 border-black text-black py-4 rounded-full font-medium flex items-center justify-center space-x-2 hover:bg-black hover:text-white transition-all duration-200"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                </svg>
                <span>Call</span>
              </a>
            ) : (
              <button className="flex-1 border-2 border-gray-300 text-gray-400 py-4 rounded-full font-medium flex items-center justify-center space-x-2 cursor-not-allowed">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                </svg>
                <span>Call</span>
              </button>
            )}
          </div>
        </div>

        {/* About Us Section */}
        {restaurant.short_description && (
          <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-6 max-w-2xl mx-auto">
            <h2 className="text-xl font-bold text-gray-900 mb-4 text-center">About {restaurant.name}</h2>
            <div className="text-center">
              <p className="text-gray-700 leading-relaxed">
                {restaurant.short_description}
              </p>
            </div>
          </div>
        )}

        {/* Reviews Component */}
        <Reviews restaurant={restaurant} onWriteReview={() => setShowWriteReviewModal(true)} />
      </div>

      {/* Sticky Action Bar for Mobile */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-3 shadow-lg z-50 md:hidden">
        <div className="flex items-center justify-around space-x-2">
          {restaurant.website && (
            <a 
              href={restaurant.website}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 bg-black text-white py-3 rounded-full font-medium text-sm flex items-center justify-center space-x-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9"></path>
              </svg>
              <span>Website</span>
            </a>
          )}
          
          <button className="flex-1 bg-green-600 text-white py-3 rounded-full font-medium text-sm flex items-center justify-center space-x-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
            </svg>
            <span>Order</span>
          </button>

          {restaurant.phone_number && (
            <a 
              href={`tel:${restaurant.phone_number}`}
              className="flex-1 bg-black text-white py-3 rounded-full font-medium text-sm flex items-center justify-center space-x-2"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
              </svg>
              <span>Call</span>
            </a>
          )}
        </div>
      </div>

      {/* Write Review Modal */}
      {showWriteReviewModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-md w-full p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-gray-900">Write a Review</h3>
              <button
                onClick={() => setShowWriteReviewModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            <div className="text-center">
              <p className="text-gray-600 mb-4">
                Reviews help other customers make informed decisions about {restaurant.name}.
              </p>
              <div className="space-y-3">
                <button
                  onClick={() => {
                    // Redirect to Google Reviews
                    const googleReviewUrl = `https://search.google.com/local/writereview?name=${encodeURIComponent(restaurant.name)}&address=${encodeURIComponent(restaurant.address)}`;
                    window.open(googleReviewUrl, '_blank', 'noopener,noreferrer');
                    setShowWriteReviewModal(false);
                  }}
                  className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
                >
                  Write Google Review
                </button>
                <button
                  onClick={() => {
                    // Redirect to Yelp Reviews
                    const yelpReviewUrl = `https://www.yelp.com/search?find_desc=${encodeURIComponent(restaurant.name)}&find_loc=${encodeURIComponent(restaurant.address)}`;
                    window.open(yelpReviewUrl, '_blank', 'noopener,noreferrer');
                    setShowWriteReviewModal(false);
                  }}
                  className="w-full bg-red-600 text-white py-3 rounded-lg font-medium hover:bg-red-700 transition-colors"
                >
                  Write Yelp Review
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Bottom Navigation Bar */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-2 shadow-lg md:block hidden">
        <div className="flex items-center justify-around">
          <button 
            onClick={() => router.push('/')}
            className="flex flex-col items-center"
            aria-label="Go to home page"
          >
            <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            <span className="text-xs text-gray-400">Home</span>
          </button>
          
          <div className="flex flex-col items-center">
            <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <span className="text-xs text-green-600 font-medium">Explore</span>
          </div>
          
          <div className="flex flex-col items-center">
            <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            <span className="text-xs text-gray-400">Favorites</span>
          </div>
          
          <div className="flex flex-col items-center">
            <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
            </svg>
            <span className="text-xs text-gray-400">Specials</span>
          </div>
          
          <div className="flex flex-col items-center">
            <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <span className="text-xs text-gray-400">Profile</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RestaurantDetailPage; 