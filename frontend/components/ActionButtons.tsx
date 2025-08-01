'use client';

import React, { useState, useEffect } from 'react';
import { cn } from '@/utils/cn';

// Custom slider styles
const sliderStyles = `
  .slider::-webkit-slider-thumb {
    appearance: none;
    height: 20px;
    width: 20px;
    border-radius: 50%;
    background: #10b981;
    cursor: pointer;
    border: 2px solid white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }
  
  .slider::-moz-range-thumb {
    height: 20px;
    width: 20px;
    border-radius: 50%;
    background: #10b981;
    cursor: pointer;
    border: 2px solid white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }
  
  .slider:focus {
    outline: none;
  }
  
  .slider:focus::-webkit-slider-thumb {
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.3);
  }
  
  .slider:focus::-moz-range-thumb {
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.3);
  }
`;

interface ActionButtonsProps {
  onShowFilters: () => void;
  onShowMap: () => void;
  onAddEatery: () => void;
  activeFilters?: any;
  onFilterChange?: (key: string, value: any) => void;
  onToggleFilter?: (key: string, value: boolean) => void;
  onDistanceChange?: (distance: number) => void;
  onClearAll?: () => void;
  userLocation?: { lat: number; lng: number } | null;
  locationLoading?: boolean;
  hasActiveFilters?: boolean;
  isOnMapPage?: boolean;
  onLocationReset?: () => void;
}

// Enhanced filter options - Updated to match actual database data
const FILTER_OPTIONS = {
  agencies: [
    { value: 'all', label: 'All Agencies' },
    { value: 'ORB', label: 'ORB (Orthodox Rabbinical Board)' },
    { value: 'KM', label: 'KM (Kosher Miami)' },
    { value: 'Star-K', label: 'Star-K' },
    { value: 'CRC', label: 'CRC (Chicago Rabbinical Council)' },
    { value: 'Kof-K', label: 'KOF-K' },
    { value: 'Diamond K', label: 'Diamond K' },
    { value: 'OU', label: 'OU (Orthodox Union)' },
    { value: 'OK', label: 'OK Kosher' },
    { value: 'Chabad', label: 'Chabad' },
    { value: 'Local Rabbi', label: 'Local Rabbi' }
  ],
  kosherTypes: [
    { value: 'all', label: 'All Kosher Types' },
    { value: 'dairy', label: 'Dairy' },
    { value: 'meat', label: 'Meat' },
    { value: 'pareve', label: 'Pareve' }
  ],
  categories: [
    { value: 'all', label: 'All Categories' },
    { value: 'restaurant', label: 'Restaurant' },
    { value: 'bakery', label: 'Bakery' },
    { value: 'catering', label: 'Catering' },
    { value: 'grocery', label: 'Grocery Store' },
    { value: 'market', label: 'Market' },
    { value: 'deli', label: 'Deli' },
    { value: 'pizza', label: 'Pizza' },
    { value: 'ice cream', label: 'Ice Cream' },
    { value: 'coffee shop', label: 'Coffee Shop' },
    { value: 'food truck', label: 'Food Truck' },
    { value: 'synagogue', label: 'Synagogue' }
  ],
  priceRanges: [
    { value: 'all', label: 'All Prices' },
    { value: '$', label: '$ (Under $15)' },
    { value: '$$', label: '$$ ($15-$30)' },
    { value: '$$$', label: '$$$ ($30-$60)' },
    { value: '$$$$', label: '$$$$ (Over $60)' }
  ],
  kosherFeatures: [
    { value: 'is_cholov_yisroel', label: 'Chalav Yisroel' },
    { value: 'is_pas_yisroel', label: 'Pas Yisroel' },
    { value: 'is_glatt', label: 'Glatt Kosher' },
    { value: 'is_mehadrin', label: 'Mehadrin' },
    { value: 'is_bishul_yisroel', label: 'Bishul Yisroel' }
  ],
  features: [
    { value: 'delivery', label: 'Delivery Available' },
    { value: 'takeout', label: 'Takeout Available' },
    { value: 'dine-in', label: 'Dine-in Available' },
    { value: 'outdoor-seating', label: 'Outdoor Seating' },
    { value: 'parking', label: 'Free Parking' },
    { value: 'wifi', label: 'Free WiFi' },
    { value: 'accessible', label: 'Wheelchair Accessible' },
    { value: 'family-friendly', label: 'Family Friendly' }
  ]
};

export default function ActionButtons({
  onShowFilters,
  onShowMap,
  onAddEatery,
  activeFilters,
  onFilterChange,
  onToggleFilter,
  onDistanceChange,
  onClearAll,
  userLocation,
  locationLoading,
  hasActiveFilters,
  isOnMapPage = false,
  onLocationReset
}: ActionButtonsProps) {
  const [showFilters, setShowFilters] = useState(false);
  const [expandedSections, setExpandedSections] = useState({
    distance: false,
    agencies: false,
    kosherTypes: false,
    categories: false,
    kosherFeatures: false,
    price: false,
    features: false
  });
  const [customDistance, setCustomDistance] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  // Mobile optimization: Close filters on escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && showFilters) {
        setShowFilters(false);
      }
    };

    if (showFilters) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden'; // Prevent background scroll
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [showFilters]);

  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const getDistanceLabel = () => {
    if (!userLocation) return 'Enable Location';
    if (locationLoading) return 'Loading...';
    return activeFilters?.distanceRadius ? `${activeFilters.distanceRadius} miles` : 'Distance';
  };

  const getSelectedLabel = (section: string) => {
    switch (section) {
      case 'agencies':
        return activeFilters?.agency ? activeFilters.agency : 'Certifying Agency';
      case 'dietary':
        return activeFilters?.dietary ? activeFilters.dietary : 'Dietary Type';
      case 'categories':
        return activeFilters?.category ? activeFilters.category : 'Category';
      case 'price':
        return activeFilters?.priceRange ? activeFilters.priceRange : 'Price Range';
      case 'features':
        return activeFilters?.features?.length > 0 ? `${activeFilters.features.length} features` : 'Features';
      default:
        return '';
    }
  };

  const getSelectedCount = (section: string) => {
    switch (section) {
      case 'agencies':
        return activeFilters?.agency && activeFilters.agency !== 'all' ? 1 : 0;
      case 'kosherTypes':
        return activeFilters?.kosherType && activeFilters.kosherType !== 'all' ? 1 : 0;
      case 'categories':
        return activeFilters?.category && activeFilters.category !== 'all' ? 1 : 0;
      case 'kosherFeatures':
        return Object.values(activeFilters || {}).filter(value => 
          typeof value === 'boolean' && value === true && 
          ['is_cholov_yisroel', 'is_pas_yisroel', 'is_glatt', 'is_mehadrin', 'is_bishul_yisroel'].includes(Object.keys(activeFilters || {}).find(key => activeFilters[key] === value) || '')
        ).length;
      case 'price':
        return activeFilters?.priceRange && activeFilters.priceRange !== 'all' ? 1 : 0;
      case 'features':
        return activeFilters?.features?.length || 0;
      default:
        return 0;
    }
  };

  const handleDistanceSelect = (distance: number) => {
    onDistanceChange?.(distance);
  };

  const handleCustomDistanceSubmit = () => {
    const distance = parseFloat(customDistance);
    if (distance > 0 && distance <= 100) {
      handleDistanceSelect(distance);
      setCustomDistance('');
    }
  };

  const handleFeatureToggle = (feature: string) => {
    const currentFeatures = activeFilters?.features || [];
    const newFeatures = currentFeatures.includes(feature)
      ? currentFeatures.filter((f: string) => f !== feature)
      : [...currentFeatures, feature];
    
    onFilterChange?.('features', newFeatures);
  };

  const handleClearAllFilters = () => {
    onClearAll?.();
    setSearchTerm('');
  };

  const getActiveFiltersCount = () => {
    let count = 0;
    if (activeFilters?.agency && activeFilters.agency !== 'all') count++;
    if (activeFilters?.kosherType && activeFilters.kosherType !== 'all') count++;
    if (activeFilters?.category && activeFilters.category !== 'all') count++;
    if (activeFilters?.priceRange && activeFilters.priceRange !== 'all') count++;
    if (activeFilters?.features?.length > 0) count += activeFilters.features.length;
    if (activeFilters?.distanceRadius) count++;
    
    // Count kosher features
    if (activeFilters?.is_cholov_yisroel) count++;
    if (activeFilters?.is_pas_yisroel) count++;
    if (activeFilters?.is_glatt) count++;
    if (activeFilters?.is_mehadrin) count++;
    if (activeFilters?.is_bishul_yisroel) count++;
    
    return count;
  };

  return (
    <>
      <style>{sliderStyles}</style>
      
      {/* Action Buttons Bar */}
      <div className="px-3 sm:px-4 mb-4 sm:mb-6">
        <div className="flex space-x-2 sm:space-x-3 bg-white rounded-full shadow-lg border border-gray-200 p-1">
          <button
            onClick={onShowMap}
            className="flex items-center justify-center gap-1 sm:gap-2 bg-transparent text-black border border-black px-3 sm:px-6 py-2.5 sm:py-3 rounded-full text-xs sm:text-sm font-medium shadow-sm hover:bg-green-100 hover:border-green-400 transition-all duration-200 hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-green-300/20 flex-1 touch-manipulation"
          >
            {isOnMapPage ? (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                </svg>
                <span className="hidden sm:inline">View List</span>
                <span className="sm:hidden">List</span>
              </>
            ) : (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span>Map</span>
              </>
            )}
          </button>

          <button
            onClick={onAddEatery}
            className="flex items-center justify-center gap-1 sm:gap-2 bg-transparent text-black border border-black px-3 sm:px-6 py-2.5 sm:py-3 rounded-full text-xs sm:text-sm font-medium shadow-sm hover:bg-green-100 hover:border-green-400 transition-all duration-200 hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-green-300/20 flex-1 touch-manipulation"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <span className="hidden sm:inline">Add Eatery</span>
            <span className="sm:hidden">Add</span>
          </button>

          <button
            onClick={() => setShowFilters(true)}
            className="flex items-center justify-center gap-1 sm:gap-2 bg-transparent text-black border border-black px-3 sm:px-6 py-2.5 sm:py-3 rounded-full text-xs sm:text-sm font-medium shadow-sm hover:bg-green-100 hover:border-green-400 transition-all duration-200 hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-green-300/20 relative flex-1 touch-manipulation"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            <span className="hidden sm:inline">Filters</span>
            <span className="sm:hidden">Filters</span>
            {getActiveFiltersCount() > 0 && (
              <div className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full border-2 border-white text-xs text-white flex items-center justify-center font-bold">
                {getActiveFiltersCount()}
              </div>
            )}
          </button>


        </div>
      </div>

      {/* Enhanced Filters Modal */}
      {showFilters && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-1 sm:p-2 md:p-4">
          <div className="bg-white rounded-[1.5rem] sm:rounded-[2rem] w-full max-w-md max-h-[98vh] sm:max-h-[95vh] md:max-h-[90vh] flex flex-col shadow-2xl">
            {/* Header */}
            <div className="flex items-center justify-between p-4 sm:p-6 border-b border-gray-100">
              <div className="flex items-center gap-3">
                <h2 className="text-lg sm:text-xl font-bold text-gray-900">Filters</h2>
                {getActiveFiltersCount() > 0 && (
                  <span className="bg-red-500 text-white text-xs px-2 py-1 rounded-full font-bold">
                    {getActiveFiltersCount()}
                  </span>
                )}
              </div>
              <button
                onClick={() => setShowFilters(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors p-1 touch-manipulation"
              >
                <svg className="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Scrollable Content */}
            <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
              {/* Search Bar */}
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search restaurants..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
                <svg className="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>

              {/* Distance Filter */}
              <div className="border border-gray-200 rounded-lg">
                <button
                  onClick={() => toggleSection('distance')}
                  className="w-full flex items-center justify-between p-4 text-left hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <span className="font-medium">{getDistanceLabel()}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {activeFilters?.distanceRadius && (
                      <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                        {activeFilters.distanceRadius}mi
                      </span>
                    )}
                    <svg className={`w-5 h-5 transition-transform ${expandedSections.distance ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </button>
                
                {expandedSections.distance && (
                  <div className="px-4 pb-4 space-y-3">
                    <div className="grid grid-cols-2 gap-2">
                      {[5, 10, 15, 25, 50].map((distance) => (
                        <button
                          key={distance}
                          onClick={() => handleDistanceSelect(distance)}
                          className={cn(
                            "px-3 py-2 text-sm rounded-lg border transition-colors",
                            activeFilters?.distanceRadius === distance
                              ? "bg-green-500 text-white border-green-500"
                              : "bg-white text-gray-700 border-gray-300 hover:bg-gray-50"
                          )}
                        >
                          {distance} miles
                        </button>
                      ))}
                    </div>
                    
                    <div className="flex gap-2">
                      <input
                        type="number"
                        placeholder="Custom"
                        value={customDistance}
                        onChange={(e) => setCustomDistance(e.target.value)}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                        min="1"
                        max="100"
                      />
                      <button
                        onClick={handleCustomDistanceSubmit}
                        className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
                      >
                        Set
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* Certifying Agencies Filter */}
              <div className="border border-gray-200 rounded-lg">
                <button
                  onClick={() => toggleSection('agencies')}
                  className="w-full flex items-center justify-between p-4 text-left hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span className="font-medium">Certifying Agency</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {getSelectedCount('agencies') > 0 && (
                      <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                        {getSelectedCount('agencies')}
                      </span>
                    )}
                    <svg className={`w-5 h-5 transition-transform ${expandedSections.agencies ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </button>
                
                {expandedSections.agencies && (
                  <div className="px-4 pb-4 space-y-2">
                    {FILTER_OPTIONS.agencies.map((option) => (
                      <button
                        key={option.value}
                        onClick={() => onFilterChange?.('agency', option.value)}
                        className={cn(
                          "w-full text-left px-3 py-2 rounded-lg transition-colors",
                          activeFilters?.agency === option.value
                            ? "bg-blue-500 text-white"
                            : "hover:bg-gray-50"
                        )}
                      >
                        {option.label}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Kosher Types Filter */}
              <div className="border border-gray-200 rounded-lg">
                <button
                  onClick={() => toggleSection('kosherTypes')}
                  className="w-full flex items-center justify-between p-4 text-left hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                    <span className="font-medium">Kosher Type</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {getSelectedCount('kosherTypes') > 0 && (
                      <span className="bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded-full">
                        {getSelectedCount('kosherTypes')}
                      </span>
                    )}
                    <svg className={`w-5 h-5 transition-transform ${expandedSections.kosherTypes ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </button>
                
                {expandedSections.kosherTypes && (
                  <div className="px-4 pb-4 space-y-2">
                    {FILTER_OPTIONS.kosherTypes.map((option) => (
                      <button
                        key={option.value}
                        onClick={() => onFilterChange?.('kosherType', option.value)}
                        className={cn(
                          "w-full text-left px-3 py-2 rounded-lg transition-colors",
                          activeFilters?.kosherType === option.value
                            ? "bg-purple-500 text-white"
                            : "hover:bg-gray-50"
                        )}
                      >
                        {option.label}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Categories Filter */}
              <div className="border border-gray-200 rounded-lg">
                <button
                  onClick={() => toggleSection('categories')}
                  className="w-full flex items-center justify-between p-4 text-left hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                    <span className="font-medium">Category</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {getSelectedCount('categories') > 0 && (
                      <span className="bg-orange-100 text-orange-800 text-xs px-2 py-1 rounded-full">
                        {getSelectedCount('categories')}
                      </span>
                    )}
                    <svg className={`w-5 h-5 transition-transform ${expandedSections.categories ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </button>
                
                {expandedSections.categories && (
                  <div className="px-4 pb-4 space-y-2">
                    {FILTER_OPTIONS.categories.map((option) => (
                      <button
                        key={option.value}
                        onClick={() => onFilterChange?.('category', option.value)}
                        className={cn(
                          "w-full text-left px-3 py-2 rounded-lg transition-colors",
                          activeFilters?.category === option.value
                            ? "bg-orange-500 text-white"
                            : "hover:bg-gray-50"
                        )}
                      >
                        {option.label}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Kosher Features Filter */}
              <div className="border border-gray-200 rounded-lg">
                <button
                  onClick={() => toggleSection('kosherFeatures')}
                  className="w-full flex items-center justify-between p-4 text-left hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span className="font-medium">Kosher Features</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {getSelectedCount('kosherFeatures') > 0 && (
                      <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                        {getSelectedCount('kosherFeatures')}
                      </span>
                    )}
                    <svg className={`w-5 h-5 transition-transform ${expandedSections.kosherFeatures ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </button>
                
                {expandedSections.kosherFeatures && (
                  <div className="px-4 pb-4 space-y-2">
                    {FILTER_OPTIONS.kosherFeatures.map((option) => (
                      <button
                        key={option.value}
                        onClick={() => onToggleFilter?.(option.value, !activeFilters?.[option.value])}
                        className={cn(
                          "w-full text-left px-3 py-2 rounded-lg transition-colors flex items-center justify-between",
                          activeFilters?.[option.value]
                            ? "bg-green-500 text-white"
                            : "hover:bg-gray-50"
                        )}
                      >
                        <span>{option.label}</span>
                        {activeFilters?.[option.value] && (
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                          </svg>
                        )}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Price Range Filter */}
              <div className="border border-gray-200 rounded-lg">
                <button
                  onClick={() => toggleSection('price')}
                  className="w-full flex items-center justify-between p-4 text-left hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                    </svg>
                    <span className="font-medium">Price Range</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {getSelectedCount('price') > 0 && (
                      <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full">
                        {getSelectedCount('price')}
                      </span>
                    )}
                    <svg className={`w-5 h-5 transition-transform ${expandedSections.price ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </button>
                
                {expandedSections.price && (
                  <div className="px-4 pb-4 space-y-2">
                    {FILTER_OPTIONS.priceRanges.map((option) => (
                      <button
                        key={option.value}
                        onClick={() => onFilterChange?.('priceRange', option.value)}
                        className={cn(
                          "w-full text-left px-3 py-2 rounded-lg transition-colors",
                          activeFilters?.priceRange === option.value
                            ? "bg-yellow-500 text-white"
                            : "hover:bg-gray-50"
                        )}
                      >
                        {option.label}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Features Filter */}
              <div className="border border-gray-200 rounded-lg">
                <button
                  onClick={() => toggleSection('features')}
                  className="w-full flex items-center justify-between p-4 text-left hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                    </svg>
                    <span className="font-medium">Features</span>
                  </div>
                  <div className="flex items-center gap-2">
                    {getSelectedCount('features') > 0 && (
                      <span className="bg-indigo-100 text-indigo-800 text-xs px-2 py-1 rounded-full">
                        {getSelectedCount('features')}
                      </span>
                    )}
                    <svg className={`w-5 h-5 transition-transform ${expandedSections.features ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </button>
                
                {expandedSections.features && (
                  <div className="px-4 pb-4 space-y-2">
                    {FILTER_OPTIONS.features.map((option) => (
                      <button
                        key={option.value}
                        onClick={() => handleFeatureToggle(option.value)}
                        className={cn(
                          "w-full text-left px-3 py-2 rounded-lg transition-colors flex items-center justify-between",
                          activeFilters?.features?.includes(option.value)
                            ? "bg-indigo-500 text-white"
                            : "hover:bg-gray-50"
                        )}
                      >
                        <span>{option.label}</span>
                        {activeFilters?.features?.includes(option.value) && (
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                          </svg>
                        )}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Footer */}
            <div className="p-4 sm:p-6 border-t border-gray-100 flex gap-3">
              <button
                onClick={handleClearAllFilters}
                className="flex-1 px-4 py-3 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors font-medium"
              >
                Clear All
              </button>
              <button
                onClick={() => setShowFilters(false)}
                className="flex-1 px-4 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors font-medium"
              >
                Apply Filters
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
} 