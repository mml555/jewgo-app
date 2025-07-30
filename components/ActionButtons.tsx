'use client';

import React, { useState } from 'react';
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
}

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
  isOnMapPage = false
}: ActionButtonsProps) {
  const [showFilters, setShowFilters] = useState(false);
  const [expandedSections, setExpandedSections] = useState({
    distance: false,
    agencies: false,
    dietary: false,
    categories: false
  });
  const [customDistance, setCustomDistance] = useState('');

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
      default:
        return '';
    }
  };

  const getSelectedCount = (section: string) => {
    switch (section) {
      case 'agencies':
        return activeFilters?.agency && activeFilters.agency !== 'all' ? 1 : 0;
      case 'dietary':
        return activeFilters?.dietary && activeFilters.dietary !== 'all' ? 1 : 0;
      case 'categories':
        return activeFilters?.category && activeFilters.category !== 'all' ? 1 : 0;
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

  return (
    <>
      {/* Action Buttons Bar */}
      <div className="px-3 sm:px-4 mb-4 sm:mb-6">
        <div className="flex space-x-2 sm:space-x-3 bg-white rounded-full shadow-lg border border-gray-200 p-1">
          <button
            onClick={onShowMap}
            className="flex items-center justify-center gap-1 sm:gap-2 bg-transparent text-black border border-black px-3 sm:px-6 py-2.5 sm:py-3 rounded-full text-xs sm:text-sm font-medium shadow-sm hover:bg-green-100 hover:border-green-400 transition-all duration-200 hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-300/20 flex-1"
          >
            {isOnMapPage ? (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                </svg>
                <span>View List</span>
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
              className="flex items-center justify-center gap-1 sm:gap-2 bg-transparent text-black border border-black px-3 sm:px-6 py-2.5 sm:py-3 rounded-full text-xs sm:text-sm font-medium shadow-sm hover:bg-green-100 hover:border-green-400 transition-all duration-200 hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-300/20 flex-1"
            >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <span>Add Eatery</span>
          </button>

          <button
            onClick={() => setShowFilters(true)}
            className="flex items-center justify-center gap-1 sm:gap-2 bg-transparent text-black border border-black px-3 sm:px-6 py-2.5 sm:py-3 rounded-full text-xs sm:text-sm font-medium shadow-sm hover:bg-green-100 hover:border-green-400 transition-all duration-200 hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-300/20 relative flex-1"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            <span>Advanced Filters</span>
            {hasActiveFilters && (
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full border-2 border-black"></div>
            )}
          </button>
        </div>
      </div>

      {/* Filters Modal */}
      {showFilters && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-1 sm:p-2 md:p-4">
          <div className="bg-white rounded-[1.5rem] sm:rounded-[2rem] w-full max-w-md max-h-[98vh] sm:max-h-[95vh] md:max-h-[90vh] flex flex-col shadow-2xl">
            {/* Header */}
            <div className="flex items-center justify-between p-4 sm:p-6 border-b border-gray-100">
              <h2 className="text-lg sm:text-xl font-bold text-gray-900">Advanced Filters</h2>
              <button
                onClick={() => setShowFilters(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors p-1"
              >
                <svg className="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Scrollable Content */}
            <div className="flex-1 overflow-y-auto max-h-[calc(98vh-200px)] sm:max-h-[calc(95vh-200px)] md:max-h-[calc(90vh-200px)]">
              <div className="px-3 sm:px-4 md:px-6 py-2 sm:py-3 md:py-4 space-y-3 sm:space-y-4 md:space-y-6">
                {/* Quick Filters Section */}
                <div>
                  <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4 flex items-center">
                    <svg className="w-4 h-4 sm:w-5 sm:h-5 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    Quick Filters
                  </h3>
                  <div className="space-y-3">
                    <button
                      onClick={() => onToggleFilter?.('openNow', !activeFilters?.openNow)}
                      disabled={locationLoading}
                      className={cn(
                        "w-full flex justify-between items-center py-2.5 sm:py-3 px-3 sm:px-4 rounded-full transition-all duration-200",
                        "hover:scale-[1.02] active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-green-500/20",
                        activeFilters?.openNow
                          ? "bg-black text-green-300 border-2 border-green-300"
                          : "bg-gray-100 text-gray-700 border-2 border-gray-200 hover:bg-gray-200"
                      )}
                    >
                      <span className="flex items-center text-sm sm:text-base">
                        <span className="w-2 h-2 rounded-full bg-green-500 mr-2 sm:mr-3"></span>
                        Open Now
                      </span>
                      <div className={cn(
                        "w-4 h-4 sm:w-5 sm:h-5 border-2 rounded-full transition-colors",
                        activeFilters?.openNow
                          ? "border-green-300 bg-green-300"
                          : "border-gray-400"
                      )} />
                    </button>
                  </div>
                </div>

                {/* Distance Section */}
                <div>
                  <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4 flex items-center">
                    <svg className="w-4 h-4 sm:w-5 sm:h-5 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    Distance
                  </h3>
                  <button
                    onClick={() => toggleSection('distance')}
                    disabled={!userLocation || locationLoading}
                    title={!userLocation ? 'Enable location to use this sort option' : ''}
                    className={cn(
                      "w-full flex justify-between items-center py-2.5 sm:py-3 px-3 sm:px-4 rounded-full transition-all duration-200",
                      "hover:scale-[1.02] active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-green-500/20",
                      !userLocation || locationLoading ? "opacity-50 cursor-not-allowed" : "",
                      expandedSections.distance
                        ? "bg-black text-green-300 border-2 border-green-300"
                        : activeFilters?.distanceRadius
                        ? "bg-black text-green-300 border-2 border-green-300"
                        : "bg-gray-100 text-gray-700 border-2 border-gray-200 hover:bg-gray-200"
                    )}
                  >
                    <span className="flex items-center text-sm sm:text-base">
                      <span>{getDistanceLabel()}</span>
                      {activeFilters?.distanceRadius && (
                        <span className="ml-2 bg-green-300 text-black text-xs font-bold px-2 py-1 rounded-full">
                          {activeFilters.distanceRadius}mi
                        </span>
                      )}
                    </span>
                    <svg 
                      className={cn(
                        "w-4 h-4 sm:w-5 sm:h-5 transition-transform duration-200",
                        expandedSections.distance ? "rotate-180" : ""
                      )} 
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                  
                  {expandedSections.distance && (
                    <div className="mt-3 sm:mt-4 space-y-3 sm:space-y-4 animate-in slide-in-from-top-2 duration-200">
                      {/* Distance Slider */}
                      <div className="px-2">
                        <div className="flex justify-between items-center mb-3">
                          <span className="text-sm font-medium text-gray-700">Distance</span>
                          <span className="text-sm font-bold text-green-600">
                            {activeFilters?.distanceRadius || 10} miles
                          </span>
                        </div>
                        <div className="relative">
                          <input
                            type="range"
                            min="1"
                            max="50"
                            value={activeFilters?.distanceRadius || 10}
                            onChange={(e) => handleDistanceSelect(parseInt(e.target.value))}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                            style={{
                              background: `linear-gradient(to right, #10b981 0%, #10b981 ${((activeFilters?.distanceRadius || 10) - 1) / 49 * 100}%, #e5e7eb ${((activeFilters?.distanceRadius || 10) - 1) / 49 * 100}%, #e5e7eb 100%)`
                            }}
                          />
                          <div className="flex justify-between text-xs text-gray-500 mt-2">
                            <span>1 mi</span>
                            <span>25 mi</span>
                            <span>50 mi</span>
                          </div>
                        </div>
                      </div>

                      {/* Quick Distance Buttons */}
                      <div className="grid grid-cols-3 gap-1.5 sm:gap-2">
                        {[5, 10, 15, 20, 25, 30].map((distance) => (
                          <button
                            key={distance}
                            onClick={() => handleDistanceSelect(distance)}
                            className={cn(
                              "py-1.5 sm:py-2 px-2 sm:px-3 rounded-full border-2 transition-colors text-xs sm:text-sm font-medium",
                              activeFilters?.distanceRadius === distance
                                ? "border-green-300 bg-black text-green-300"
                                : "border-gray-300 text-gray-700 hover:border-green-300 hover:bg-black hover:text-green-300"
                            )}
                          >
                            {distance} mi
                          </button>
                        ))}
                      </div>

                      {/* Custom Distance Input */}
                      <div className="pt-2 border-t border-gray-200">
                        <div className="flex items-center space-x-2">
                          <input
                            type="number"
                            min="1"
                            max="100"
                            placeholder="Custom miles"
                            value={customDistance}
                            onChange={(e) => setCustomDistance(e.target.value)}
                            className="flex-1 px-2 sm:px-3 py-1.5 sm:py-2 border border-gray-300 rounded-lg text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-green-500/20"
                            onKeyPress={(e) => e.key === 'Enter' && handleCustomDistanceSubmit()}
                          />
                          <button
                            onClick={handleCustomDistanceSubmit}
                            disabled={!customDistance || parseFloat(customDistance) <= 0 || parseFloat(customDistance) > 100}
                            className="px-2 sm:px-3 py-1.5 sm:py-2 bg-black text-green-300 text-xs sm:text-sm rounded-full hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed border border-green-300"
                          >
                            Set
                          </button>
                        </div>
                        <p className="text-xs text-gray-500 mt-1">Enter 1-100 miles</p>
                      </div>
                    </div>
                  )}
                </div>

                {/* Certifying Agencies Section */}
                <div>
                  <h3 className="text-base sm:text-lg font-semibold text-gray-900 mb-3 sm:mb-4 flex items-center">
                    <svg className="w-4 h-4 sm:w-5 sm:h-5 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Certifying Agencies
                  </h3>
                  <button
                    onClick={() => toggleSection('agencies')}
                    className={cn(
                      "w-full flex justify-between items-center py-2.5 sm:py-3 px-3 sm:px-4 rounded-full transition-all duration-200",
                      "hover:scale-[1.02] active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-green-500/20",
                      expandedSections.agencies
                        ? "bg-black text-green-300 border-2 border-green-300"
                        : activeFilters?.agency && activeFilters.agency !== 'all'
                        ? "bg-black text-green-300 border-2 border-green-300"
                        : "bg-gray-100 text-gray-700 border-2 border-gray-200 hover:bg-gray-200"
                    )}
                  >
                    <span className="flex items-center text-sm sm:text-base">
                      <span>{getSelectedLabel('agencies')}</span>
                      {getSelectedCount('agencies') > 0 && (
                        <span className="ml-2 bg-green-300 text-black text-xs font-bold px-2 py-1 rounded-full">
                          {getSelectedCount('agencies')}
                        </span>
                      )}
                    </span>
                    <svg 
                      className={cn(
                        "w-4 h-4 sm:w-5 sm:h-5 transition-transform duration-200",
                        expandedSections.agencies ? "rotate-180" : ""
                      )} 
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                  
                  {expandedSections.agencies && (
                    <div className="mt-2 sm:mt-3 space-y-1.5 sm:space-y-2 animate-in slide-in-from-top-2 duration-200">
                                              <button
                          onClick={() => onFilterChange?.('agency', 'all')}
                          className={cn(
                            "w-full flex justify-between items-center py-1.5 sm:py-2 px-3 sm:px-4 rounded-full transition-all duration-200",
                            "hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500/20",
                            !activeFilters?.agency
                              ? "bg-black text-green-300 border border-green-300"
                              : "text-gray-700 border border-gray-200"
                          )}
                        >
                          <span className="text-sm sm:text-base">All Agencies</span>
                          <div className={cn(
                            "w-3 h-3 sm:w-4 sm:h-4 border-2 rounded-full transition-colors",
                            !activeFilters?.agency
                              ? "border-green-300 bg-green-300"
                              : "border-gray-300"
                          )} />
                        </button>
                      
                                              <button
                          onClick={() => onFilterChange?.('agency', 'ORB')}
                          className={cn(
                            "w-full flex justify-between items-center py-1.5 sm:py-2 px-3 sm:px-4 rounded-full transition-all duration-200",
                            "hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500/20",
                            activeFilters?.agency === 'ORB'
                              ? "bg-black text-green-300 border border-green-300"
                              : "text-gray-700 border border-gray-200"
                          )}
                          title="Orthodox Union Rabbinical Board"
                        >
                          <span className="text-sm sm:text-base">ORB</span>
                          <div className={cn(
                            "w-3 h-3 sm:w-4 sm:h-4 border-2 rounded-full transition-colors",
                            activeFilters?.agency === 'ORB'
                              ? "border-green-300 bg-green-300"
                              : "border-gray-300"
                          )} />
                        </button>
                      
                                              <button
                          onClick={() => onFilterChange?.('agency', 'KM')}
                          className={cn(
                            "w-full flex justify-between items-center py-1.5 sm:py-2 px-3 sm:px-4 rounded-full transition-all duration-200",
                            "hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500/20",
                            activeFilters?.agency === 'KM'
                              ? "bg-black text-green-300 border border-green-300"
                              : "text-gray-700 border border-gray-200"
                          )}
                          title="Cholov Yisroel only"
                        >
                          <span className="text-sm sm:text-base">KM</span>
                          <div className={cn(
                            "w-3 h-3 sm:w-4 sm:h-4 border-2 rounded-full transition-colors",
                            activeFilters?.agency === 'KM'
                              ? "border-green-300 bg-green-300"
                              : "border-gray-300"
                          )} />
                        </button>
                      
                                              <button
                          onClick={() => onFilterChange?.('agency', 'KDM')}
                          className={cn(
                            "w-full flex justify-between items-center py-1.5 sm:py-2 px-3 sm:px-4 rounded-full transition-all duration-200",
                            "hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500/20",
                            activeFilters?.agency === 'KDM'
                              ? "bg-black text-green-300 border border-green-300"
                              : "text-gray-700 border border-gray-200"
                          )}
                          title="Not exclusively Cholov Yisroel"
                        >
                          <span className="text-sm sm:text-base">KDM</span>
                          <div className={cn(
                            "w-3 h-3 sm:w-4 sm:h-4 border-2 rounded-full transition-colors",
                            activeFilters?.agency === 'KDM'
                              ? "border-green-300 bg-green-300"
                              : "border-gray-300"
                          )} />
                        </button>
                        
                        <button
                          onClick={() => onFilterChange?.('agency', 'Diamond K')}
                          className={cn(
                            "w-full flex justify-between items-center py-1.5 sm:py-2 px-3 sm:px-4 rounded-full transition-all duration-200",
                            "hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500/20",
                            activeFilters?.agency === 'Diamond K'
                              ? "bg-black text-green-300 border border-green-300"
                              : "text-gray-700 border border-gray-200"
                          )}
                          title="ORB subsidiary, not Cholov Yisroel"
                        >
                          <span className="text-sm sm:text-base">Diamond K</span>
                          <div className={cn(
                            "w-3 h-3 sm:w-4 sm:h-4 border-2 rounded-full transition-colors",
                            activeFilters?.agency === 'Diamond K'
                              ? "border-green-300 bg-green-300"
                              : "border-gray-300"
                          )} />
                        </button>
                    </div>
                  )}
                </div>

                {/* Dietary Preferences Section */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <svg className="w-5 h-5 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                    Dietary Preferences
                  </h3>
                  <button
                    onClick={() => toggleSection('dietary')}
                    className={cn(
                      "w-full flex justify-between items-center py-3 px-4 rounded-full transition-all duration-200",
                      "hover:scale-[1.02] active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-green-500/20",
                      expandedSections.dietary
                        ? "bg-black text-green-300 border-2 border-green-300"
                        : activeFilters?.dietary && activeFilters.dietary !== 'all'
                        ? "bg-black text-green-300 border-2 border-green-300"
                        : "bg-gray-100 text-gray-700 border-2 border-gray-200 hover:bg-gray-200"
                    )}
                  >
                    <span className="flex items-center">
                      <span>{getSelectedLabel('dietary')}</span>
                      {getSelectedCount('dietary') > 0 && (
                        <span className="ml-2 bg-green-300 text-black text-xs font-bold px-2 py-1 rounded-full">
                          {getSelectedCount('dietary')}
                        </span>
                      )}
                    </span>
                    <svg 
                      className={cn(
                        "w-5 h-5 transition-transform duration-200",
                        expandedSections.dietary ? "rotate-180" : ""
                      )} 
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                  
                  {expandedSections.dietary && (
                    <div className="mt-3 space-y-2 animate-in slide-in-from-top-2 duration-200">
                      <button
                        onClick={() => onFilterChange?.('dietary', 'all')}
                        className={cn(
                          "w-full flex justify-between items-center py-2 px-4 rounded-full transition-all duration-200",
                          "hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500/20",
                          !activeFilters?.dietary
                            ? "bg-black text-green-300 border border-green-300"
                            : "text-gray-700 border border-gray-200"
                        )}
                      >
                        <span>All Types</span>
                        <div className={cn(
                          "w-4 h-4 border-2 rounded-full transition-colors",
                          !activeFilters?.dietary
                            ? "border-green-300 bg-green-300"
                            : "border-gray-300"
                        )} />
                      </button>
                      
                      <button
                        onClick={() => onFilterChange?.('dietary', 'meat')}
                        className={cn(
                          "w-full flex justify-between items-center py-2 px-4 rounded-full transition-all duration-200",
                          "hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500/20",
                          activeFilters?.dietary === 'meat'
                            ? "bg-black text-green-300 border border-green-300"
                            : "text-gray-700 border border-gray-200"
                        )}
                      >
                        <span>Meat</span>
                        <div className={cn(
                          "w-4 h-4 border-2 rounded-full transition-colors",
                          activeFilters?.dietary === 'meat'
                            ? "border-green-300 bg-green-300"
                            : "border-gray-300"
                        )} />
                      </button>
                      
                      <button
                        onClick={() => onFilterChange?.('dietary', 'dairy')}
                        className={cn(
                          "w-full flex justify-between items-center py-2 px-4 rounded-full transition-all duration-200",
                          "hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500/20",
                          activeFilters?.dietary === 'dairy'
                            ? "bg-black text-green-300 border border-green-300"
                            : "text-gray-700 border border-gray-200"
                        )}
                      >
                        <span>Dairy</span>
                        <div className={cn(
                          "w-4 h-4 border-2 rounded-full transition-colors",
                          activeFilters?.dietary === 'dairy'
                            ? "border-green-300 bg-green-300"
                            : "border-gray-300"
                        )} />
                      </button>
                      
                      <button
                        onClick={() => onFilterChange?.('dietary', 'pareve')}
                        className={cn(
                          "w-full flex justify-between items-center py-2 px-4 rounded-full transition-all duration-200",
                          "hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500/20",
                          activeFilters?.dietary === 'pareve'
                            ? "bg-black text-green-300 border border-green-300"
                            : "text-gray-700 border border-gray-200"
                        )}
                      >
                        <span>Pareve</span>
                        <div className={cn(
                          "w-4 h-4 border-2 rounded-full transition-colors",
                          activeFilters?.dietary === 'pareve'
                            ? "border-green-300 bg-green-300"
                            : "border-gray-300"
                        )} />
                      </button>
                    </div>
                  )}
                </div>

                {/* Categories Section */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <svg className="w-5 h-5 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                    Categories
                  </h3>
                  <button
                    onClick={() => toggleSection('categories')}
                    className={cn(
                      "w-full flex justify-between items-center py-3 px-4 rounded-full transition-all duration-200",
                      "hover:scale-[1.02] active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-green-500/20",
                      expandedSections.categories
                        ? "bg-black text-green-300 border-2 border-green-300"
                        : activeFilters?.category && activeFilters.category !== 'all'
                        ? "bg-black text-green-300 border-2 border-green-300"
                        : "bg-gray-100 text-gray-700 border-2 border-gray-200 hover:bg-gray-200"
                    )}
                  >
                    <span className="flex items-center">
                      <span>{getSelectedLabel('categories')}</span>
                      {getSelectedCount('categories') > 0 && (
                        <span className="ml-2 bg-green-300 text-black text-xs font-bold px-2 py-1 rounded-full">
                          {getSelectedCount('categories')}
                        </span>
                      )}
                    </span>
                    <svg 
                      className={cn(
                        "w-5 h-5 transition-transform duration-200",
                        expandedSections.categories ? "rotate-180" : ""
                      )} 
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                  
                  {expandedSections.categories && (
                    <div className="mt-3 space-y-2 animate-in slide-in-from-top-2 duration-200">
                      <button
                        onClick={() => onFilterChange?.('category', 'all')}
                        className={cn(
                          "w-full flex justify-between items-center py-2 px-4 rounded-full transition-all duration-200",
                          "hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500/20",
                          !activeFilters?.category
                            ? "bg-black text-green-300 border border-green-300"
                            : "text-gray-700 border border-gray-200"
                        )}
                      >
                        <span>All Categories</span>
                        <div className={cn(
                          "w-4 h-4 border-2 rounded-full transition-colors",
                          !activeFilters?.category
                            ? "border-green-300 bg-green-300"
                            : "border-gray-300"
                        )} />
                      </button>
                      
                      <button
                        onClick={() => onFilterChange?.('category', 'restaurant')}
                        className={cn(
                          "w-full flex justify-between items-center py-2 px-4 rounded-full transition-all duration-200",
                          "hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500/20",
                          activeFilters?.category === 'restaurant'
                            ? "bg-black text-green-300 border border-green-300"
                            : "text-gray-700 border border-gray-200"
                        )}
                      >
                        <span>Restaurants</span>
                        <div className={cn(
                          "w-4 h-4 border-2 rounded-full transition-colors",
                          activeFilters?.category === 'restaurant'
                            ? "border-green-300 bg-green-300"
                            : "border-gray-300"
                        )} />
                      </button>
                      
                      <button
                        onClick={() => onFilterChange?.('category', 'bakery')}
                        className={cn(
                          "w-full flex justify-between items-center py-2 px-4 rounded-full transition-all duration-200",
                          "hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500/20",
                          activeFilters?.category === 'bakery'
                            ? "bg-black text-green-300 border border-green-300"
                            : "text-gray-700 border border-gray-200"
                        )}
                      >
                        <span>Bakeries</span>
                        <div className={cn(
                          "w-4 h-4 border-2 rounded-full transition-colors",
                          activeFilters?.category === 'bakery'
                            ? "border-green-300 bg-green-300"
                            : "border-gray-300"
                        )} />
                      </button>
                      
                      <button
                        onClick={() => onFilterChange?.('category', 'grocery')}
                        className={cn(
                          "w-full flex justify-between items-center py-2 px-4 rounded-full transition-all duration-200",
                          "hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500/20",
                          activeFilters?.category === 'grocery'
                            ? "bg-black text-green-300 border border-green-300"
                            : "text-gray-700 border border-gray-200"
                        )}
                      >
                        <span>Grocery Stores</span>
                        <div className={cn(
                          "w-4 h-4 border-2 rounded-full transition-colors",
                          activeFilters?.category === 'grocery'
                            ? "border-green-300 bg-green-300"
                            : "border-gray-300"
                        )} />
                      </button>
                      
                      <button
                        onClick={() => onFilterChange?.('category', 'catering')}
                        className={cn(
                          "w-full flex justify-between items-center py-2 px-4 rounded-full transition-all duration-200",
                          "hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500/20",
                          activeFilters?.category === 'catering'
                            ? "bg-black text-green-300 border border-green-300"
                            : "text-gray-700 border border-gray-200"
                        )}
                      >
                        <span>Catering</span>
                        <div className={cn(
                          "w-4 h-4 border-2 rounded-full transition-colors",
                          activeFilters?.category === 'catering'
                            ? "border-green-300 bg-green-300"
                            : "border-gray-300"
                        )} />
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Sticky Footer with CTA */}
            <div className="sticky bottom-0 bg-white rounded-b-[1.5rem] sm:rounded-b-[2rem] px-3 sm:px-4 md:px-6 py-2 sm:py-3 md:py-4 border-t border-gray-100">
              {hasActiveFilters && (
                <div className="mb-2 sm:mb-3">
                  <span className="text-xs sm:text-sm text-gray-600">
                    {Object.values(activeFilters || {}).filter(f => f !== undefined && f !== false).length} active filter(s)
                  </span>
                </div>
              )}
              <div className="flex space-x-2 sm:space-x-3">
                {hasActiveFilters && onClearAll && (
                  <button
                    onClick={onClearAll}
                    className="flex-1 border-2 border-black text-black hover:bg-black hover:text-white font-semibold py-3 sm:py-4 rounded-full transition-colors touch-manipulation active:scale-95 text-sm sm:text-base"
                  >
                    Reset Filters
                  </button>
                )}
                <button
                  onClick={() => setShowFilters(false)}
                  className="flex-1 bg-black text-green-300 hover:bg-gray-800 font-semibold py-3 sm:py-4 rounded-full transition-colors touch-manipulation active:scale-95 border border-green-300 text-sm sm:text-base"
                >
                  Apply Filters
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Custom Slider Styles */}
      <style jsx>{sliderStyles}</style>
    </>
  );
} 