'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import BottomNavigation from '@/components/BottomNavigation';

export default function AdvancedFiltersPage() {
  const [filters, setFilters] = useState({
    priceRange: '',
    distance: '',
    rating: '',
    openNow: false,
    hasDelivery: false,
    hasTakeout: false,
    hasParking: false,
    hasWifi: false,
    isWheelchairAccessible: false,
    acceptsReservations: false,
    cuisineTypes: [] as string[],
    mealTypes: [] as string[],
    specialFeatures: [] as string[]
  });

  const handleFilterChange = (key: string, value: any) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleArrayFilterChange = (key: string, value: string) => {
    setFilters(prev => {
      const currentArray = prev[key as keyof typeof prev] as string[];
      return {
        ...prev,
        [key]: currentArray.includes(value)
          ? currentArray.filter(item => item !== value)
          : [...currentArray, value]
      };
    });
  };

  const resetFilters = () => {
    setFilters({
      priceRange: '',
      distance: '',
      rating: '',
      openNow: false,
      hasDelivery: false,
      hasTakeout: false,
      hasParking: false,
      hasWifi: false,
      isWheelchairAccessible: false,
      acceptsReservations: false,
      cuisineTypes: [],
      mealTypes: [],
      specialFeatures: []
    });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Header />
      
      {/* Content */}
      <div className="px-4 py-6 pb-24">
        <div className="max-w-2xl mx-auto">
          {/* Page Header */}
          <div className="text-center mb-8">
            <div className="text-4xl mb-4">🔍</div>
            <h1 className="text-2xl font-bold text-gray-800 mb-2">Advanced Filters</h1>
            <p className="text-gray-600">Fine-tune your search with detailed options</p>
          </div>

          {/* Filters Form */}
          <div className="bg-white rounded-lg shadow-lg p-6 space-y-8">
            {/* Basic Filters */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Basic Filters</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Price Range</label>
                  <select
                    value={filters.priceRange}
                    onChange={(e) => handleFilterChange('priceRange', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                  >
                    <option value="">Any Price</option>
                    <option value="$">$ (Under $10)</option>
                    <option value="$$">$$ ($10-$25)</option>
                    <option value="$$$">$$$ ($25-$50)</option>
                    <option value="$$$$">$$$$ (Over $50)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Distance</label>
                  <select
                    value={filters.distance}
                    onChange={(e) => handleFilterChange('distance', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                  >
                    <option value="">Any Distance</option>
                    <option value="1">Within 1 mile</option>
                    <option value="5">Within 5 miles</option>
                    <option value="10">Within 10 miles</option>
                    <option value="25">Within 25 miles</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Minimum Rating</label>
                  <select
                    value={filters.rating}
                    onChange={(e) => handleFilterChange('rating', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                  >
                    <option value="">Any Rating</option>
                    <option value="4.5">4.5+ Stars</option>
                    <option value="4.0">4.0+ Stars</option>
                    <option value="3.5">3.5+ Stars</option>
                    <option value="3.0">3.0+ Stars</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Availability */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Availability</h3>
              <div className="space-y-3">
                <label className="flex items-center space-x-3">
                  <input
                    type="checkbox"
                    checked={filters.openNow}
                    onChange={(e) => handleFilterChange('openNow', e.target.checked)}
                    className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                  />
                  <span className="text-sm text-gray-700">Open Now</span>
                </label>
                <label className="flex items-center space-x-3">
                  <input
                    type="checkbox"
                    checked={filters.hasDelivery}
                    onChange={(e) => handleFilterChange('hasDelivery', e.target.checked)}
                    className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                  />
                  <span className="text-sm text-gray-700">Offers Delivery</span>
                </label>
                <label className="flex items-center space-x-3">
                  <input
                    type="checkbox"
                    checked={filters.hasTakeout}
                    onChange={(e) => handleFilterChange('hasTakeout', e.target.checked)}
                    className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                  />
                  <span className="text-sm text-gray-700">Offers Takeout</span>
                </label>
                <label className="flex items-center space-x-3">
                  <input
                    type="checkbox"
                    checked={filters.acceptsReservations}
                    onChange={(e) => handleFilterChange('acceptsReservations', e.target.checked)}
                    className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                  />
                  <span className="text-sm text-gray-700">Accepts Reservations</span>
                </label>
              </div>
            </div>

            {/* Amenities */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Amenities</h3>
              <div className="space-y-3">
                <label className="flex items-center space-x-3">
                  <input
                    type="checkbox"
                    checked={filters.hasParking}
                    onChange={(e) => handleFilterChange('hasParking', e.target.checked)}
                    className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                  />
                  <span className="text-sm text-gray-700">Free Parking</span>
                </label>
                <label className="flex items-center space-x-3">
                  <input
                    type="checkbox"
                    checked={filters.hasWifi}
                    onChange={(e) => handleFilterChange('hasWifi', e.target.checked)}
                    className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                  />
                  <span className="text-sm text-gray-700">Free WiFi</span>
                </label>
                <label className="flex items-center space-x-3">
                  <input
                    type="checkbox"
                    checked={filters.isWheelchairAccessible}
                    onChange={(e) => handleFilterChange('isWheelchairAccessible', e.target.checked)}
                    className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                  />
                  <span className="text-sm text-gray-700">Wheelchair Accessible</span>
                </label>
              </div>
            </div>

            {/* Cuisine Types */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Cuisine Types</h3>
              <div className="grid grid-cols-2 gap-3">
                {['Israeli', 'Mediterranean', 'Italian', 'Mexican', 'Asian', 'American', 'Middle Eastern', 'European'].map((cuisine) => (
                  <label key={cuisine} className="flex items-center space-x-3">
                    <input
                      type="checkbox"
                      checked={filters.cuisineTypes.includes(cuisine)}
                      onChange={() => handleArrayFilterChange('cuisineTypes', cuisine)}
                      className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                    />
                    <span className="text-sm text-gray-700">{cuisine}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Meal Types */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Meal Types</h3>
              <div className="grid grid-cols-2 gap-3">
                {['Breakfast', 'Lunch', 'Dinner', 'Brunch', 'Dessert', 'Coffee'].map((meal) => (
                  <label key={meal} className="flex items-center space-x-3">
                    <input
                      type="checkbox"
                      checked={filters.mealTypes.includes(meal)}
                      onChange={() => handleArrayFilterChange('mealTypes', meal)}
                      className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                    />
                    <span className="text-sm text-gray-700">{meal}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Special Features */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Special Features</h3>
              <div className="grid grid-cols-2 gap-3">
                {['Gluten-Free Options', 'Vegan Options', 'Organic', 'Kosher for Passover', 'Shabbat Meals', 'Catering'].map((feature) => (
                  <label key={feature} className="flex items-center space-x-3">
                    <input
                      type="checkbox"
                      checked={filters.specialFeatures.includes(feature)}
                      onChange={() => handleArrayFilterChange('specialFeatures', feature)}
                      className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                    />
                    <span className="text-sm text-gray-700">{feature}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex space-x-4 pt-6">
              <button
                onClick={resetFilters}
                className="flex-1 bg-gray-100 text-gray-700 py-3 px-6 rounded-lg font-medium hover:bg-gray-200 transition-colors"
              >
                Reset All
              </button>
              <button
                onClick={() => alert('Filters applied! (This would update the main search results)')}
                className="flex-1 bg-jewgo-primary text-white py-3 px-6 rounded-lg font-medium hover:bg-jewgo-primary-dark transition-colors"
              >
                Apply Filters
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Navigation */}
      <BottomNavigation />
    </div>
  );
} 