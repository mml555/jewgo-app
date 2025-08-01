'use client';

import React, { useState } from 'react';
import SearchBar from '@/components/eatery/ui/SearchBar';
import CategoryTabs from '@/components/eatery/ui/CategoryTabs';
import SubNav from '@/components/eatery/ui/SubNav';
import EateryCard from '@/components/eatery/ui/EateryCard';
import BottomTabBar from '@/components/eatery/ui/BottomTabBar';
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
  const [activeCategory, setActiveCategory] = useState('eatery');
  const [filteredRestaurants, setFilteredRestaurants] = useState(sampleRestaurants);

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

  const handleCategoryChange = (category: string) => {
    setActiveCategory(category);
    // For demo, show all restaurants for eatery category
    if (category === 'eatery') {
      setFilteredRestaurants(sampleRestaurants);
    } else {
      setFilteredRestaurants([]);
    }
  };

  const handleFilterClick = () => {
    alert('Advanced filters clicked! This would open a filter modal.');
  };

  return (
    <div className="min-h-screen bg-gray-50 pb-28 px-4 md:px-8 lg:px-16">
      <div className="pt-4 space-y-4">
        {/* Header */}
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Mobile-First Demo</h1>
          <p className="text-gray-600">New Eatery Explore Page Components</p>
        </div>
        
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
        {filteredRestaurants.length === 0 && (
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