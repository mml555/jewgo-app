'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import SearchHeader from '@/components/layout/SearchHeader';
import CategoryTabs from '@/components/layout/CategoryTabs';
import ActionButtons from '@/components/layout/ActionButtons';
import RestaurantGrid from '@/components/restaurant/RestaurantGrid';
import BottomNavigation from '@/components/layout/BottomNavigation';
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
      {/* Search Header */}
      <SearchHeader
        onSearch={handleSearch}
        placeholder="Search for kosher restaurants, agencies, or locations..."
        showFilters={true}
        onShowFilters={() => {}}
      />

      {/* Category Tabs */}
      <CategoryTabs activeTab={activeTab} onTabChange={handleTabChange} />

      {/* Action Buttons */}
      <ActionButtons
        onShowFilters={() => {}}
        onShowMap={() => window.location.href = '/live-map'}
        onAddEatery={() => window.location.href = '/add-eatery'}
        hasActiveFilters={hasActiveFilters()}
        onClearFilters={handleClearAll}
        isOnMapPage={false}
      />

      {/* Results Count */}
      <div className="px-4 sm:px-6 py-3 bg-gray-50 text-sm text-gray-600 border-b border-gray-200">
        {filteredRestaurants.length} {filteredRestaurants.length === 1 ? 'restaurant' : 'restaurants'} found
      </div>

      {/* Restaurant Grid */}
      <RestaurantGrid
        restaurants={filteredRestaurants}
        loading={loading}
        onRestaurantClick={(restaurant) => {
          // Handle restaurant click - could navigate to detail page
          console.log('Restaurant clicked:', restaurant.name);
        }}
      />

      {/* Bottom Navigation */}
      <BottomNavigation />
    </div>
  );
} 