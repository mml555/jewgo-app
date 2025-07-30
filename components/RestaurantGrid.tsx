'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import RestaurantCard from './RestaurantCard';
import RestaurantCardSkeleton from './RestaurantCardSkeleton';
import { RestaurantGridProps } from '@/types/restaurant';

interface ExtendedRestaurantGridProps extends RestaurantGridProps {
  userLocation?: { latitude: number; longitude: number } | null;
  loading?: boolean;
}

const RestaurantGrid: React.FC<ExtendedRestaurantGridProps> = ({ 
  restaurants, 
  currentPage = 1, 
  totalPages = 1, 
  onPageChange,
  totalRestaurants = 0,
  userLocation,
  loading = false
}) => {
  const router = useRouter();

  const handleCardClick = (restaurant: any) => {
    // Navigate to the restaurant detail page
    router.push(`/restaurant/${restaurant.id}`);
  };

  const handlePageChange = (page: number) => {
    if (process.env.NODE_ENV === 'development') {
      console.log('=== RestaurantGrid handlePageChange called ===');
      console.log('Page requested:', page);
      console.log('Current page:', currentPage);
      console.log('Total pages:', totalPages);
    }
    
    if (onPageChange) {
      if (process.env.NODE_ENV === 'development') {
        console.log('Calling onPageChange with page:', page);
      }
      onPageChange(page);
    } else {
      if (process.env.NODE_ENV === 'development') {
        console.log('onPageChange is not defined!');
      }
    }
  };

  if (restaurants.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-500 mb-4">
          <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">No restaurants found</h3>
        <p className="text-gray-500">Try adjusting your search criteria</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Responsive Grid - Mobile-first design */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4 sm:gap-6">
        {loading ? (
          // Show skeleton loaders while loading
          Array.from({ length: 20 }).map((_, index) => (
            <RestaurantCardSkeleton key={`skeleton-${index}`} />
          ))
        ) : (
          restaurants.map((restaurant, index) => (
          <RestaurantCard
            key={restaurant.id}
            restaurant={restaurant}
              onClick={() => handleCardClick(restaurant)}
              userLocation={userLocation}
              index={index}
          />
          ))
        )}
      </div>

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="flex flex-col items-center space-y-4 pt-4">
          {/* Page Info */}
          <div className="text-sm text-gray-600 text-center">
            Page {currentPage} of {totalPages} • {totalRestaurants} restaurants total
          </div>
        
          {/* Pagination Buttons */}
          <div className="flex items-center space-x-2">
            {/* Previous Button */}
            <button
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage <= 1}
              className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors min-w-[44px]"
            >
              Prev
            </button>

            {/* Page Numbers */}
            <div className="flex items-center space-x-1">
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                let pageNum;
                if (totalPages <= 5) {
                  pageNum = i + 1;
                } else if (currentPage <= 3) {
                  pageNum = i + 1;
                } else if (currentPage >= totalPages - 2) {
                  pageNum = totalPages - 4 + i;
                } else {
                  pageNum = currentPage - 2 + i;
                }

                return (
                  <button
                    key={pageNum}
                    onClick={() => handlePageChange(pageNum)}
                    className={`px-3 py-2 text-sm font-medium rounded-md transition-colors min-w-[44px] ${
                      currentPage === pageNum
                        ? 'bg-mint-green text-white'
                        : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
                    }`}
                  >
                    {pageNum}
                  </button>
                );
              })}
            </div>

            {/* Next Button */}
            <button
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage >= totalPages}
              className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors min-w-[44px]"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default RestaurantGrid; 