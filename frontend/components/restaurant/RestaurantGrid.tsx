'use client';

import React from 'react';
import { Restaurant } from '@/types/restaurant';
import RestaurantCard from './RestaurantCard';

interface RestaurantGridProps {
  restaurants: Restaurant[];
  loading?: boolean;
  onRestaurantClick?: (restaurant: Restaurant) => void;
}

export default function RestaurantGrid({ 
  restaurants, 
  loading = false, 
  onRestaurantClick 
}: RestaurantGridProps) {
  if (loading) {
    return (
      <div className="px-4 py-6 pb-24">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4">
          {Array.from({ length: 8 }).map((_, index) => (
            <div key={index} className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden animate-pulse">
              <div className="h-48 bg-gray-200"></div>
              <div className="p-4 space-y-3">
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                <div className="h-3 bg-gray-200 rounded w-full"></div>
                <div className="h-3 bg-gray-200 rounded w-2/3"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (restaurants.length === 0) {
    return (
      <div className="px-4 py-6 pb-24">
        <div className="text-center py-16">
          <div className="text-gray-400 text-6xl mb-4">🍽️</div>
          <div className="text-gray-500 text-lg mb-3 font-medium">
            No restaurants found
          </div>
          <div className="text-gray-400 text-sm">
            Try adjusting your search or filters
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="px-4 py-6 pb-24">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4">
        {restaurants.map((restaurant) => (
          <RestaurantCard
            key={restaurant.id}
            restaurant={restaurant}
            onClick={() => onRestaurantClick?.(restaurant)}
          />
        ))}
      </div>
    </div>
  );
} 