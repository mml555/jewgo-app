'use client';

import React, { useState } from 'react';
import Header from '@/components/Header';
import GoogleMapsStyleSearch from '@/components/GoogleMapsStyleSearch';
import NavTabs from '@/components/NavTabs';
import ActionButtons from '@/components/ActionButtons';
import EateryCard from '@/components/eatery/ui/EateryCard';
import BottomNavigation from '@/components/BottomNavigation';
import { Restaurant } from '@/types/restaurant';

// Sample data for demo
const sampleRestaurants: Restaurant[] = [
  {
    id: 1,
    name: "Milano's Pizza",
    address: "123 Main St",
    city: "New York",
    state: "NY",
    zip_code: "10001",
    phone_number: "(555) 123-4567",
    certifying_agency: "OU",
    kosher_category: "dairy",
    listing_type: "restaurant",
    status: "active",
    price_range: "$10 - $35",
    rating: 4.43,
    image_url: "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=300&fit=crop&crop=center"
  },
  {
    id: 2,
    name: "JZ Steakhouse",
    address: "456 Oak Ave",
    city: "Los Angeles",
    state: "CA",
    zip_code: "90210",
    phone_number: "(555) 987-6543",
    certifying_agency: "Star-K",
    kosher_category: "meat",
    listing_type: "restaurant",
    status: "active",
    price_range: "$60 - $135",
    rating: 4.88,
    image_url: "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400&h=300&fit=crop&crop=center"
  },
  {
    id: 3,
    name: "Yum Berry",
    address: "789 Pine St",
    city: "Chicago",
    state: "IL",
    zip_code: "60601",
    phone_number: "(555) 456-7890",
    certifying_agency: "CRC",
    kosher_category: "dairy",
    listing_type: "restaurant",
    status: "active",
    price_range: "$15 - $40",
    rating: 4.33,
    image_url: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop&crop=center"
  },
  {
    id: 4,
    name: "Sushi House",
    address: "321 Elm St",
    city: "Miami",
    state: "FL",
    zip_code: "33101",
    phone_number: "(555) 321-6540",
    certifying_agency: "OK",
    kosher_category: "meat",
    listing_type: "restaurant",
    status: "active",
    price_range: "$20 - $55",
    rating: 4.76,
    image_url: "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400&h=300&fit=crop&crop=center"
  }
];

export default function DemoPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState('eatery');
  const [filteredRestaurants, setFilteredRestaurants] = useState(sampleRestaurants);
  const [activeFilters, setActiveFilters] = useState<{
    agency?: string;
    kosherType?: string;
    openNow?: boolean;
    category?: string;
    nearMe?: boolean;
    distanceRadius?: number;
    is_cholov_yisroel?: boolean;
    is_pas_yisroel?: boolean;
    is_glatt?: boolean;
    is_mehadrin?: boolean;
    is_bishul_yisroel?: boolean;
  }>({});

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    if (query.trim()) {
      const filtered = sampleRestaurants.filter(restaurant =>
        restaurant.name.toLowerCase().includes(query.toLowerCase()) ||
        restaurant.city.toLowerCase().includes(query.toLowerCase())
      );
      setFilteredRestaurants(filtered);
    } else {
      setFilteredRestaurants(sampleRestaurants);
    }
  };

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
    // For demo, show all restaurants for eatery category
    if (tab === 'eatery') {
      setFilteredRestaurants(sampleRestaurants);
    } else {
      setFilteredRestaurants([]);
    }
  };

  const handleFilterChange = (key: string, value: any) => {
    setActiveFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleToggleFilter = (key: string, value: boolean) => {
    setActiveFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleDistanceChange = (distance: number) => {
    setActiveFilters(prev => ({ ...prev, distanceRadius: distance }));
  };

  const handleClearAll = () => {
    setActiveFilters({});
  };

  const hasActiveFilters = () => {
    return Object.values(activeFilters).some(value => 
      value !== undefined && value !== false && value !== ''
    );
  };

  return (
    <div className="min-h-screen bg-neutral-50">
      <Header />
      
      {/* Demo Header */}
      <div className="px-4 sm:px-6 py-4 bg-white border-b border-gray-100">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Mobile-First Demo</h1>
          <p className="text-gray-600">New Eatery Explore Page Components</p>
        </div>
      </div>
      
      {/* Google Maps Style Search */}
      <div className="px-4 sm:px-6 py-4 bg-white border-b border-gray-100">
        <GoogleMapsStyleSearch
          onSearch={handleSearch}
          onResultsUpdate={(results) => {
            console.log('Google Maps search results:', results.length, 'restaurants');
            setFilteredRestaurants(results);
          }}
          onLocationSelect={(location) => {
            console.log('Location selected:', location);
            // You can use this to center the map or filter by location
          }}
          placeholder="Search for kosher restaurants, agencies, or locations..."
          showAdvancedFilters={true}
        />
      </div>

      {/* Navigation Tabs */}
      <div className="px-4 sm:px-6 py-2 bg-white border-b border-gray-100">
        <NavTabs activeTab={activeTab} onTabChange={handleTabChange} />
      </div>

      {/* Action Buttons */}
      <div className="px-4 sm:px-6 py-3 bg-white border-b border-gray-100">
        <ActionButtons
          onShowFilters={() => {}}
          onShowMap={() => window.location.href = '/live-map'}
          onAddEatery={() => window.location.href = '/add-eatery'}
          onFilterChange={handleFilterChange}
          onToggleFilter={handleToggleFilter}
          onDistanceChange={handleDistanceChange}
          onClearAll={handleClearAll}
          onLocationReset={() => {}}
          activeFilters={activeFilters}
          userLocation={null}
          locationLoading={false}
          hasActiveFilters={hasActiveFilters()}
          isOnMapPage={false}
        />
      </div>

      {/* Results Count */}
      <div className="px-4 sm:px-6 py-3 bg-gray-50 text-sm text-gray-600 border-b border-gray-200">
        {filteredRestaurants.length} {filteredRestaurants.length === 1 ? 'restaurant' : 'restaurants'} found
      </div>

      {/* Restaurant Grid */}
      <div className="px-4 sm:px-6 py-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredRestaurants.map((restaurant) => (
            <EateryCard 
              key={restaurant.id} 
              restaurant={restaurant}
            />
          ))}
        </div>
        
        {/* Empty State */}
        {filteredRestaurants.length === 0 && (
          <div className="text-center py-16">
            <div className="text-gray-500 text-lg mb-3 font-medium">
              No restaurants found
            </div>
            <div className="text-gray-400 text-sm">
              Try adjusting your search or filters
            </div>
          </div>
        )}
      </div>

      {/* Bottom Navigation */}
      <BottomNavigation />
    </div>
  );
} 