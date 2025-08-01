'use client';

import React from 'react';
import LazyRestaurantList from './LazyRestaurantList';
import LazyEateryList from './LazyEateryList';
import { Restaurant } from '@/types/restaurant';

interface LazyLoadingDemoProps {
  restaurants: Restaurant[];
  onRestaurantSelect?: (restaurant: Restaurant) => void;
  showDistance?: boolean;
  distances?: Record<number, number>;
  className?: string;
}

export default function LazyLoadingDemo({
  restaurants,
  onRestaurantSelect,
  showDistance = false,
  distances = {},
  className = ""
}: LazyLoadingDemoProps) {
  return (
    <div className={`space-y-8 ${className}`}>
      {/* Restaurant List with Lazy Loading */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Restaurants with Lazy Loading
        </h2>
        <LazyRestaurantList
          restaurants={restaurants}
          onRestaurantSelect={onRestaurantSelect}
          showDistance={showDistance}
          distances={distances}
          initialLoadCount={6}
          itemsPerPage={8}
        />
      </div>

      {/* Eatery List with Lazy Loading */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Eateries with Lazy Loading
        </h2>
        <LazyEateryList
          restaurants={restaurants}
          onRestaurantSelect={onRestaurantSelect}
          initialLoadCount={6}
          itemsPerPage={8}
        />
      </div>
    </div>
  );
} 