import React, { useState, useEffect } from 'react';
import { cn } from '@/utils/cn';
import { safeFilter } from '@/utils/validation';

export interface FilterState {
  // Basic filters
  search?: string;
  city?: string;
  state?: string;
  
  // Kosher filters
  certifying_agency?: string;
  kosher_category?: 'meat' | 'dairy' | 'pareve' | 'fish' | 'unknown';
  is_cholov_yisroel?: boolean;
  
  // Business filters
  listing_type?: string;
  price_range?: string;
  
  // Rating filters
  min_rating?: number;
  has_reviews?: boolean;
  
  // Location filters
  near_me?: boolean;
  radius?: number;
  
  // Status filters
  status?: string;
  
  // Hours filters
  open_now?: boolean;
  
  // Distance filters
  max_distance?: number;
}

interface EnhancedFiltersProps {
  filters: FilterState;
  onFiltersChange: (filters: FilterState) => void;
  onClearAll: () => void;
  userLocation: { latitude: number; longitude: number } | null;
  locationLoading: boolean;
  availableData?: {
    cities: string[];
    states: string[];
    agencies: string[];
    listingTypes: string[];
    priceRanges: string[];
  };
}

const EnhancedFilters: React.FC<EnhancedFiltersProps> = ({
  filters,
  onFiltersChange,
  onClearAll,
  userLocation,
  locationLoading,
  availableData = {
    cities: [],
    states: [],
    agencies: ['ORB', 'KM', 'Star-K', 'CRC', 'Kof-K', 'Diamond K'],
    listingTypes: ['restaurant', 'bakery', 'catering', 'grocery', 'market'],
    priceRanges: ['$', '$$', '$$$', '$$$$']
  }
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [localFilters, setLocalFilters] = useState<FilterState>(filters);

  // Update local filters when props change
  useEffect(() => {
    setLocalFilters(filters);
  }, [filters]);

  const hasActiveFilters = Object.values(filters).some(
    filter => filter !== undefined && filter !== false && filter !== ''
  );

  const updateFilter = (key: keyof FilterState, value: any) => {
    const newFilters = { ...localFilters, [key]: value };
    setLocalFilters(newFilters);
    onFiltersChange(newFilters);
  };

  const clearFilter = (key: keyof FilterState) => {
    const newFilters = { ...localFilters };
    delete newFilters[key];
    setLocalFilters(newFilters);
    onFiltersChange(newFilters);
  };

  const getActiveFilterCount = () => {
    return safeFilter(Object.values(filters), 
      filter => filter !== undefined && filter !== false && filter !== ''
    ).length;
  };

  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center">
          <svg className="w-5 h-5 mr-2 text-jewgo-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          <h3 className="text-lg font-semibold text-gray-900">Advanced Filters</h3>
          {hasActiveFilters && (
            <span className="ml-2 px-2 py-1 bg-jewgo-primary text-white text-xs rounded-full">
              {getActiveFilterCount()}
            </span>
          )}
        </div>
        <div className="flex items-center space-x-2">
          {hasActiveFilters && (
            <button
              onClick={onClearAll}
              className="text-sm text-jewgo-primary hover:text-jewgo-primary-dark transition-colors font-medium"
            >
              Clear All
            </button>
          )}
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-sm text-gray-600 hover:text-gray-800 transition-colors"
          >
            {isExpanded ? 'Show Less' : 'Show More'}
          </button>
        </div>
      </div>

      {/* Quick Filters - Always Visible */}
      <div className="space-y-4">
        {/* Search */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
          <input
            type="text"
            placeholder="Search restaurants..."
            value={filters.search || ''}
            onChange={(e) => updateFilter('search', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
          />
        </div>

        {/* Location Filters */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">City</label>
            <select
              value={filters.city || ''}
              onChange={(e) => updateFilter('city', e.target.value || undefined)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
            >
              <option value="">All Cities</option>
              {availableData.cities.map(city => (
                <option key={city} value={city}>{city}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">State</label>
            <select
              value={filters.state || ''}
              onChange={(e) => updateFilter('state', e.target.value || undefined)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
            >
              <option value="">All States</option>
              {availableData.states.map(state => (
                <option key={state} value={state}>{state}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Quick Toggle Filters */}
        <div className="flex flex-wrap gap-3">
          <button
            onClick={() => updateFilter('open_now', !filters.open_now)}
            disabled={locationLoading}
            className={cn(
              "px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 flex items-center space-x-2",
              "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
              filters.open_now
                ? "bg-green-100 text-green-800 border-2 border-green-200"
                : "bg-gray-100 text-gray-700 border-2 border-gray-200 hover:bg-gray-200"
            )}
          >
            <span className="w-2 h-2 rounded-full bg-green-500"></span>
            <span>Open Now</span>
          </button>
          
          <button
            onClick={() => updateFilter('near_me', !filters.near_me)}
            disabled={!userLocation || locationLoading}
            title={!userLocation ? 'Enable location to use this filter' : ''}
            className={cn(
              "px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 flex items-center space-x-2",
              "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
              !userLocation || locationLoading ? "opacity-50 cursor-not-allowed" : "",
              filters.near_me
                ? "bg-blue-100 text-blue-800 border-2 border-blue-200"
                : "bg-gray-100 text-gray-700 border-2 border-gray-200 hover:bg-gray-200"
            )}
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span>Near Me</span>
          </button>

          <button
            onClick={() => updateFilter('has_reviews', !filters.has_reviews)}
            className={cn(
              "px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 flex items-center space-x-2",
              "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
              filters.has_reviews
                ? "bg-yellow-100 text-yellow-800 border-2 border-yellow-200"
                : "bg-gray-100 text-gray-700 border-2 border-gray-200 hover:bg-gray-200"
            )}
          >
            <span className="text-yellow-500">★</span>
            <span>Has Reviews</span>
          </button>
        </div>
      </div>

      {/* Expanded Filters */}
      {isExpanded && (
        <div className="mt-6 pt-6 border-t border-gray-200 space-y-6">
          {/* Kosher Certification */}
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
              <svg className="w-4 h-4 mr-2 text-jewgo-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Kosher Certification
            </h4>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => clearFilter('certifying_agency')}
                className={cn(
                  "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                  "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                  !filters.certifying_agency
                    ? "bg-jewgo-primary text-white shadow-md"
                    : "bg-gray-200 text-gray-600 hover:bg-gray-300"
                )}
              >
                All Agencies
              </button>
              {availableData.agencies.map(agency => (
                <button
                  key={agency}
                  onClick={() => updateFilter('certifying_agency', agency)}
                  className={cn(
                    "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                    "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                    filters.certifying_agency === agency
                      ? "bg-blue-100 text-blue-800 border-2 border-blue-200"
                      : "bg-gray-200 text-gray-600 hover:bg-gray-300"
                  )}
                >
                  {agency}
                </button>
              ))}
            </div>
          </div>

          {/* Kosher Category */}
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
              <svg className="w-4 h-4 mr-2 text-jewgo-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
              Kosher Category
            </h4>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => clearFilter('kosher_category')}
                className={cn(
                  "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                  "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                  !filters.kosher_category
                    ? "bg-jewgo-primary text-white shadow-md"
                    : "bg-gray-200 text-gray-600 hover:bg-gray-300"
                )}
              >
                All Types
              </button>
              <button
                onClick={() => updateFilter('kosher_category', 'meat')}
                className={cn(
                  "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                  "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                  filters.kosher_category === 'meat'
                    ? "bg-red-100 text-red-800 border-2 border-red-200"
                    : "bg-gray-200 text-gray-600 hover:bg-gray-300"
                )}
              >
                Meat
              </button>
              <button
                onClick={() => updateFilter('kosher_category', 'dairy')}
                className={cn(
                  "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                  "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                  filters.kosher_category === 'dairy'
                    ? "bg-blue-100 text-blue-800 border-2 border-blue-200"
                    : "bg-gray-200 text-gray-600 hover:bg-gray-300"
                )}
              >
                Dairy
              </button>
              <button
                onClick={() => updateFilter('kosher_category', 'pareve')}
                className={cn(
                  "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                  "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                  filters.kosher_category === 'pareve'
                    ? "bg-green-100 text-green-800 border-2 border-green-200"
                    : "bg-gray-200 text-gray-600 hover:bg-gray-300"
                )}
              >
                Pareve
              </button>
              <button
                onClick={() => updateFilter('kosher_category', 'fish')}
                className={cn(
                  "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                  "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                  filters.kosher_category === 'fish'
                    ? "bg-cyan-100 text-cyan-800 border-2 border-cyan-200"
                    : "bg-gray-200 text-gray-600 hover:bg-gray-300"
                )}
              >
                Fish
              </button>
            </div>
          </div>

          {/* Chalav Yisrael Filter */}
          {filters.kosher_category === 'dairy' && (
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-3">Chalav Yisrael</h4>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => clearFilter('is_cholov_yisroel')}
                  className={cn(
                    "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                    "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                    filters.is_cholov_yisroel === undefined
                      ? "bg-jewgo-primary text-white shadow-md"
                      : "bg-gray-200 text-gray-600 hover:bg-gray-300"
                  )}
                >
                  All Dairy
                </button>
                <button
                  onClick={() => updateFilter('is_cholov_yisroel', true)}
                  className={cn(
                    "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                    "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                    filters.is_cholov_yisroel === true
                      ? "bg-cyan-100 text-cyan-800 border-2 border-cyan-200"
                      : "bg-gray-200 text-gray-600 hover:bg-gray-300"
                  )}
                >
                  Chalav Yisrael
                </button>
                <button
                  onClick={() => updateFilter('is_cholov_yisroel', false)}
                  className={cn(
                    "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                    "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                    filters.is_cholov_yisroel === false
                      ? "bg-orange-100 text-orange-800 border-2 border-orange-200"
                      : "bg-gray-200 text-gray-600 hover:bg-gray-300"
                  )}
                >
                  Chalav Stam
                </button>
              </div>
            </div>
          )}

          {/* Business Type */}
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
              <svg className="w-4 h-4 mr-2 text-jewgo-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              Business Type
            </h4>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => clearFilter('listing_type')}
                className={cn(
                  "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                  "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                  !filters.listing_type
                    ? "bg-jewgo-primary text-white shadow-md"
                    : "bg-gray-200 text-gray-600 hover:bg-gray-300"
                )}
              >
                All Types
              </button>
              {availableData.listingTypes.map(type => (
                <button
                  key={type}
                  onClick={() => updateFilter('listing_type', type)}
                  className={cn(
                    "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                    "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                    filters.listing_type === type
                      ? "bg-indigo-100 text-indigo-800 border-2 border-indigo-200"
                      : "bg-gray-200 text-gray-600 hover:bg-gray-300"
                  )}
                >
                  {type.charAt(0).toUpperCase() + type.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Price Range */}
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-3">Price Range</h4>
            <div className="flex flex-wrap gap-2">
              <button
                onClick={() => clearFilter('price_range')}
                className={cn(
                  "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                  "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                  !filters.price_range
                    ? "bg-jewgo-primary text-white shadow-md"
                    : "bg-gray-200 text-gray-600 hover:bg-gray-300"
                )}
              >
                All Prices
              </button>
              {availableData.priceRanges.map(price => (
                <button
                  key={price}
                  onClick={() => updateFilter('price_range', price)}
                  className={cn(
                    "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                    "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                    filters.price_range === price
                      ? "bg-emerald-100 text-emerald-800 border-2 border-emerald-200"
                      : "bg-gray-200 text-gray-600 hover:bg-gray-300"
                  )}
                >
                  {price}
                </button>
              ))}
            </div>
          </div>

          {/* Rating Filter */}
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-3">Minimum Rating</h4>
            <div className="flex items-center space-x-4">
              <input
                type="range"
                min="0"
                max="5"
                step="0.5"
                value={filters.min_rating || 0}
                onChange={(e) => updateFilter('min_rating', parseFloat(e.target.value))}
                className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              />
              <span className="text-sm font-medium text-gray-700 min-w-[3rem]">
                {filters.min_rating || 0}+
              </span>
            </div>
          </div>

          {/* Distance Filter */}
          {filters.near_me && (
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-3">Max Distance</h4>
              <div className="flex items-center space-x-4">
                <input
                  type="range"
                  min="1"
                  max="50"
                  step="1"
                  value={filters.max_distance || 10}
                  onChange={(e) => updateFilter('max_distance', parseInt(e.target.value))}
                  className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                />
                <span className="text-sm font-medium text-gray-700 min-w-[4rem]">
                  {filters.max_distance || 10} mi
                </span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Active Filters Summary */}
      {hasActiveFilters && (
        <div className="mt-6 pt-4 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex flex-wrap gap-2">
              {Object.entries(filters).map(([key, value]) => {
                if (value === undefined || value === false || value === '') return null;
                
                let displayValue = value;
                if (key === 'min_rating') displayValue = `${value}+ stars`;
                if (key === 'max_distance') displayValue = `${value} mi`;
                if (key === 'is_cholov_yisroel') displayValue = value ? 'Chalav Yisrael' : 'Chalav Stam';
                
                return (
                  <span
                    key={key}
                    className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-jewgo-primary/10 text-jewgo-primary border border-jewgo-primary/20"
                  >
                    {key.replace(/_/g, ' ')}: {displayValue}
                    <button
                      onClick={() => clearFilter(key as keyof FilterState)}
                      className="ml-1 hover:text-jewgo-primary-dark"
                    >
                      ×
                    </button>
                  </span>
                );
              })}
            </div>
            <button
              onClick={onClearAll}
              className="text-sm text-jewgo-primary hover:text-jewgo-primary-dark transition-colors font-medium"
            >
              Clear All
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default EnhancedFilters; 