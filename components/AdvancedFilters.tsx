import React from 'react';
import { cn } from '@/utils/cn';

interface AdvancedFiltersProps {
  activeFilters: {
    agency?: string;
    dietary?: string;
    openNow?: boolean;
    category?: string;
    nearMe?: boolean;
  };
  onFilterChange: (filterType: 'agency' | 'dietary' | 'category', value: string) => void;
  onToggleFilter: (filterType: 'openNow' | 'nearMe', value: boolean) => void;
  onClearAll: () => void;
  userLocation: { latitude: number; longitude: number } | null;
  locationLoading: boolean;
}

const AdvancedFilters: React.FC<AdvancedFiltersProps> = ({
  activeFilters,
  onFilterChange,
  onToggleFilter,
  onClearAll,
  userLocation,
  locationLoading
}) => {
  const hasActiveFilters = Object.values(activeFilters).some(filter => filter !== undefined && filter !== false);

  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center">
          <svg className="w-5 h-5 mr-2 text-jewgo-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
        </div>
        {hasActiveFilters && (
          <button
            onClick={onClearAll}
            className="text-sm text-jewgo-primary hover:text-jewgo-primary-dark transition-colors font-medium"
          >
            Clear All
          </button>
        )}
      </div>

      <div className="space-y-6">
        {/* Quick Filters */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <svg className="w-4 h-4 mr-2 text-jewgo-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Quick Filters
          </h4>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => onToggleFilter('openNow', !activeFilters.openNow)}
              disabled={locationLoading}
              className={cn(
                "px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 flex items-center space-x-2",
                "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                activeFilters.openNow
                  ? "bg-green-100 text-green-800 border-2 border-green-200"
                  : "bg-gray-100 text-gray-700 border-2 border-gray-200 hover:bg-gray-200"
              )}
            >
              <span className="w-2 h-2 rounded-full bg-green-500"></span>
              <span>Open Now</span>
            </button>
            <button
              onClick={() => onToggleFilter('nearMe', !activeFilters.nearMe)}
              disabled={!userLocation || locationLoading}
              title={!userLocation ? 'Enable location to use this filter' : ''}
              className={cn(
                "px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 flex items-center space-x-2",
                "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                !userLocation || locationLoading ? "opacity-50 cursor-not-allowed" : "",
                activeFilters.nearMe
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
          </div>
        </div>

        {/* Certifying Agencies */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <svg className="w-4 h-4 mr-2 text-jewgo-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Certifying Agencies
          </h4>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => onFilterChange('agency', 'all')}
              className={cn(
                "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                !activeFilters.agency
                  ? "bg-jewgo-primary text-white shadow-md"
                  : "bg-gray-200 text-gray-600 hover:bg-gray-300"
              )}
            >
              All Agencies
            </button>
            <button
              onClick={() => onFilterChange('agency', 'ORB')}
              className={cn(
                "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                activeFilters.agency === 'ORB'
                  ? "bg-blue-100 text-blue-800 border-2 border-blue-200"
                  : "bg-gray-200 text-gray-600 hover:bg-gray-300"
              )}
              title="Orthodox Union Rabbinical Board"
            >
              ORB
            </button>
            <button
              onClick={() => onFilterChange('agency', 'KM')}
              className={cn(
                "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                activeFilters.agency === 'KM'
                  ? "bg-green-100 text-green-800 border-2 border-green-200"
                  : "bg-gray-200 text-gray-600 hover:bg-gray-300"
              )}
              title="Cholov Yisroel only"
            >
              KM
            </button>
            <button
              onClick={() => onFilterChange('agency', 'KDM')}
              className={cn(
                "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                activeFilters.agency === 'KDM'
                  ? "bg-yellow-100 text-yellow-800 border-2 border-yellow-200"
                  : "bg-gray-200 text-gray-600 hover:bg-gray-300"
              )}
              title="Not exclusively Cholov Yisroel"
            >
              KDM
            </button>
            <button
              onClick={() => onFilterChange('agency', 'Diamond K')}
              className={cn(
                "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                activeFilters.agency === 'Diamond K'
                  ? "bg-purple-100 text-purple-800 border-2 border-purple-200"
                  : "bg-gray-200 text-gray-600 hover:bg-gray-300"
              )}
              title="ORB subsidiary, not Cholov Yisroel"
            >
              Diamond K
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            <span className="font-medium">Legend:</span> KM: Cholov Yisroel • KDM: Not exclusively Cholov Yisroel • Diamond K: ORB subsidiary
          </p>
        </div>

        {/* Dietary Preferences */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <svg className="w-4 h-4 mr-2 text-jewgo-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            Dietary Preferences
          </h4>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => onFilterChange('dietary', 'all')}
              className={cn(
                "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                !activeFilters.dietary
                  ? "bg-jewgo-primary text-white shadow-md"
                  : "bg-gray-200 text-gray-600 hover:bg-gray-300"
              )}
            >
              All Types
            </button>
            <button
              onClick={() => onFilterChange('dietary', 'meat')}
              className={cn(
                "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                activeFilters.dietary === 'meat'
                  ? "bg-red-100 text-red-800 border-2 border-red-200"
                  : "bg-gray-200 text-gray-600 hover:bg-gray-300"
              )}
            >
              Meat
            </button>
            <button
              onClick={() => onFilterChange('dietary', 'dairy')}
              className={cn(
                "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                activeFilters.dietary === 'dairy'
                  ? "bg-blue-100 text-blue-800 border-2 border-blue-200"
                  : "bg-gray-200 text-gray-600 hover:bg-gray-300"
              )}
            >
              Dairy
            </button>
            <button
              onClick={() => onFilterChange('dietary', 'pareve')}
              className={cn(
                "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                activeFilters.dietary === 'pareve'
                  ? "bg-orange-100 text-orange-800 border-2 border-orange-200"
                  : "bg-gray-200 text-gray-600 hover:bg-gray-300"
              )}
            >
              Pareve
            </button>
          </div>
        </div>

        {/* Categories */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <svg className="w-4 h-4 mr-2 text-jewgo-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            Categories
          </h4>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => onFilterChange('category', 'all')}
              className={cn(
                "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                !activeFilters.category
                  ? "bg-jewgo-primary text-white shadow-md"
                  : "bg-gray-200 text-gray-600 hover:bg-gray-300"
              )}
            >
              All Categories
            </button>
            <button
              onClick={() => onFilterChange('category', 'restaurant')}
              className={cn(
                "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                activeFilters.category === 'restaurant'
                  ? "bg-indigo-100 text-indigo-800 border-2 border-indigo-200"
                  : "bg-gray-200 text-gray-600 hover:bg-gray-300"
              )}
            >
              Restaurants
            </button>
            <button
              onClick={() => onFilterChange('category', 'bakery')}
              className={cn(
                "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                activeFilters.category === 'bakery'
                  ? "bg-amber-100 text-amber-800 border-2 border-amber-200"
                  : "bg-gray-200 text-gray-600 hover:bg-gray-300"
              )}
            >
              Bakeries
            </button>
            <button
              onClick={() => onFilterChange('category', 'grocery')}
              className={cn(
                "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                activeFilters.category === 'grocery'
                  ? "bg-emerald-100 text-emerald-800 border-2 border-emerald-200"
                  : "bg-gray-200 text-gray-600 hover:bg-gray-300"
              )}
            >
              Grocery Stores
            </button>
            <button
              onClick={() => onFilterChange('category', 'catering')}
              className={cn(
                "px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200",
                "hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-jewgo-primary/20",
                activeFilters.category === 'catering'
                  ? "bg-pink-100 text-pink-800 border-2 border-pink-200"
                  : "bg-gray-200 text-gray-600 hover:bg-gray-300"
              )}
            >
              Catering
            </button>
          </div>
        </div>

        {/* Active Filters Summary */}
        {hasActiveFilters && (
          <div className="pt-4 border-t border-gray-200">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">
                {Object.values(activeFilters).filter(f => f !== undefined && f !== false).length} active filter(s)
              </span>
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
    </div>
  );
};

export default AdvancedFilters; 