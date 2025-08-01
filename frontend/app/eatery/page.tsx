'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import SmartSearch from '@/components/SmartSearch';
import NavTabs from '@/components/NavTabs';
import ActionButtons from '@/components/ActionButtons';
import EateryCard from '@/components/eatery/ui/EateryCard';
import BottomNavigation from '@/components/BottomNavigation';
import { Restaurant } from '@/types/restaurant';
import { fetchRestaurants } from '@/lib/api/restaurants';

export default function EateryExplorePage() {
  const router = useRouter();
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [filteredRestaurants, setFilteredRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState('eatery');
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

  useEffect(() => {
    const loadRestaurants = async () => {
      try {
        setLoading(true);
        const data = await fetchRestaurants();
        setRestaurants(data.restaurants);
        setFilteredRestaurants(data.restaurants);
      } catch (error) {
        console.error('Error loading restaurants:', error);
      } finally {
        setLoading(false);
      }
    };

    loadRestaurants();
  }, []);

  useEffect(() => {
    // Filter restaurants based on search query and category
    let filtered = restaurants;

    // Filter by search query
    if (searchQuery.trim()) {
      filtered = filtered.filter(restaurant =>
        restaurant.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        restaurant.city.toLowerCase().includes(searchQuery.toLowerCase()) ||
        restaurant.certifying_agency.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Filter by category (for now, just show all restaurants for eatery category)
    if (activeTab === 'eatery') {
      // Show all restaurants
    } else {
      // For other categories, you can add specific filtering logic
      filtered = [];
    }

    setFilteredRestaurants(filtered);
  }, [restaurants, searchQuery, activeTab]);

  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
    
    // Navigate to different pages based on the selected tab
    switch (tab) {
      case 'mikvahs':
        router.push('/mikvahs');
        break;
      case 'shuls':
        router.push('/shuls');
        break;
      case 'specials':
        router.push('/specials');
        break;
      case 'eatery':
        // Already on eatery page, just update the tab
        break;
      case 'stores':
        router.push('/stores');
        break;
      default:
        break;
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

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-500">Loading restaurants...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-neutral-50">
      <Header />
      
                   {/* Smart Search with Database */}
             <div className="px-4 sm:px-6 py-4 bg-white border-b border-gray-100">
               <SmartSearch
                 onSearch={handleSearch}
                 placeholder="Search for kosher restaurants, agencies, or locations..."
                 showAdvancedFilters={true}
                 useGoogleAPI={false}
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
      <div className="px-4 py-6">
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
          {filteredRestaurants.map((restaurant) => (
            <EateryCard 
              key={restaurant.id} 
              restaurant={restaurant}
            />
          ))}
        </div>
        
        {/* Empty State */}
        {filteredRestaurants.length === 0 && !loading && (
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