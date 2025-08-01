'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Restaurant } from '@/types/restaurant';
import EateryCard from './eatery/ui/EateryCard';

interface LazyEateryListProps {
  restaurants: Restaurant[];
  onRestaurantSelect?: (restaurant: Restaurant) => void;
  className?: string;
  itemsPerPage?: number;
  initialLoadCount?: number;
}

export default function LazyEateryList({
  restaurants,
  onRestaurantSelect,
  className = "",
  itemsPerPage = 10,
  initialLoadCount = 6
}: LazyEateryListProps) {
  const [visibleCount, setVisibleCount] = useState(initialLoadCount);
  const [isLoading, setIsLoading] = useState(false);
  const observerRef = useRef<IntersectionObserver | null>(null);
  const loadingRef = useRef<HTMLDivElement>(null);

  // Intersection Observer for infinite scroll
  const handleObserver = useCallback((entries: IntersectionObserverEntry[]) => {
    const [target] = entries;
    if (target.isIntersecting && visibleCount < restaurants.length && !isLoading) {
      setIsLoading(true);
      
      // Simulate loading delay for smoother feel
      setTimeout(() => {
        setVisibleCount(prev => Math.min(prev + itemsPerPage, restaurants.length));
        setIsLoading(false);
      }, 300);
    }
  }, [visibleCount, restaurants.length, isLoading, itemsPerPage]);

  useEffect(() => {
    const observer = new IntersectionObserver(handleObserver, {
      root: null,
      rootMargin: '100px',
      threshold: 0.1
    });

    if (loadingRef.current) {
      observer.observe(loadingRef.current);
    }

    observerRef.current = observer;

    return () => {
      if (observerRef.current) {
        observerRef.current.disconnect();
      }
    };
  }, [handleObserver]);

  // Reset visible count when restaurants change
  useEffect(() => {
    setVisibleCount(initialLoadCount);
  }, [restaurants, initialLoadCount]);

  const visibleRestaurants = restaurants.slice(0, visibleCount);
  const hasMore = visibleCount < restaurants.length;

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Eatery Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4">
        {visibleRestaurants.map((restaurant) => (
          <EateryCard
            key={restaurant.id}
            restaurant={restaurant}
            className="w-full"
          />
        ))}
      </div>

      {/* Loading Indicator */}
      {hasMore && (
        <div 
          ref={loadingRef}
          className="flex justify-center items-center py-8"
        >
          {isLoading ? (
            <div className="flex items-center space-x-2">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-green-500"></div>
              <span className="text-gray-600 text-sm">Loading more eateries...</span>
            </div>
          ) : (
            <div className="text-gray-400 text-sm">
              Scroll to load more
            </div>
          )}
        </div>
      )}

      {/* End of List */}
      {!hasMore && restaurants.length > 0 && (
        <div className="text-center py-8">
          <div className="text-gray-400 text-sm">
            You've reached the end of the list
          </div>
        </div>
      )}

      {/* Empty State */}
      {restaurants.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 text-lg mb-2">🍽️</div>
          <div className="text-gray-600">No eateries found</div>
        </div>
      )}
    </div>
  );
} 