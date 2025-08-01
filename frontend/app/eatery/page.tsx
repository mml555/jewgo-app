'use client';

import React, { useState, useEffect } from 'react';
import SearchBar from '@/components/eatery/ui/SearchBar';
import CategoryTabs from '@/components/eatery/ui/CategoryTabs';
import SubNav from '@/components/eatery/ui/SubNav';
import EateryCard from '@/components/eatery/ui/EateryCard';
import BottomTabBar from '@/components/eatery/ui/BottomTabBar';
import { Restaurant } from '@/types/restaurant';
import { fetchRestaurants } from '@/lib/api/restaurants';

export default function EateryExplorePage() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [filteredRestaurants, setFilteredRestaurants] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('eatery');

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
    if (activeCategory === 'eatery') {
      // Show all restaurants
    } else {
      // For other categories, you can add specific filtering logic
      filtered = [];
    }

    setFilteredRestaurants(filtered);
  }, [restaurants, searchQuery, activeCategory]);

  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  const handleCategoryChange = (category: string) => {
    setActiveCategory(category);
  };

  const handleFilterClick = () => {
    // This could open advanced filters modal
    console.log('Advanced filters clicked');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 pb-28 px-4 md:px-8 lg:px-16">
        <div className="pt-4 space-y-4">
          <div className="h-12 bg-gray-200 rounded-full animate-pulse" />
          <div className="h-8 bg-gray-200 rounded animate-pulse" />
          <div className="h-12 bg-gray-200 rounded animate-pulse" />
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-64 bg-gray-200 rounded-lg animate-pulse" />
            ))}
          </div>
        </div>
        <BottomTabBar />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-28 px-4 md:px-8 lg:px-16">
      <div className="pt-4 space-y-4">
        {/* Search Bar */}
        <SearchBar 
          onSearch={handleSearch}
          onFilterClick={handleFilterClick}
          placeholder="Find your Eatery"
        />
        
        {/* Category Tabs */}
        <CategoryTabs 
          activeCategory={activeCategory}
          onCategoryChange={handleCategoryChange}
        />
        
        {/* Sub Navigation */}
        <SubNav />
        
        {/* Results Count */}
        <div className="text-sm text-gray-600">
          {filteredRestaurants.length} {filteredRestaurants.length === 1 ? 'restaurant' : 'restaurants'} found
        </div>
        
        {/* Restaurant Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filteredRestaurants.map((restaurant) => (
            <EateryCard 
              key={restaurant.id} 
              restaurant={restaurant}
            />
          ))}
        </div>
        
        {/* Empty State */}
        {filteredRestaurants.length === 0 && !loading && (
          <div className="text-center py-12">
            <div className="text-gray-500 text-lg mb-2">
              No restaurants found
            </div>
            <div className="text-gray-400 text-sm">
              Try adjusting your search or filters
            </div>
          </div>
        )}
      </div>
      
      {/* Bottom Tab Bar */}
      <BottomTabBar />
    </div>
  );
} 