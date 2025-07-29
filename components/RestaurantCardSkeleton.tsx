import React from 'react';

const RestaurantCardSkeleton: React.FC = () => {
  return (
    <div className="bg-white rounded-xl shadow-soft border border-gray-200 overflow-hidden h-[540px] flex flex-col animate-pulse">
      {/* Image Skeleton */}
      <div className="relative h-52 w-full bg-gray-200 flex-shrink-0">
        <div className="absolute inset-0 bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 animate-pulse"></div>
      </div>

      {/* Content Skeleton */}
      <div className="p-4 flex flex-col flex-1">
        {/* Title Skeleton */}
        <div className="mb-4 min-h-[2.5rem] max-h-[2.5rem] overflow-hidden">
          <div className="h-6 bg-gray-200 rounded w-3/4 mb-1"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>

        {/* Description Skeleton */}
        <div className="mb-4 min-h-[2.8rem]">
          <div className="h-4 bg-gray-200 rounded w-full mb-1"></div>
          <div className="h-4 bg-gray-200 rounded w-2/3"></div>
        </div>

        {/* Hours Badge Skeleton */}
        <div className="mb-4 text-center min-h-[1.5rem]">
          <div className="inline-block h-4 bg-gray-200 rounded w-32"></div>
        </div>

        {/* Button Skeleton */}
        <div className="mb-4">
          <div className="h-10 bg-gray-200 rounded-full w-full"></div>
        </div>

        {/* Address Skeleton */}
        <div className="mb-4">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-gray-200 rounded flex-shrink-0"></div>
            <div className="flex-1">
              <div className="h-4 bg-gray-200 rounded w-full"></div>
            </div>
          </div>
        </div>

        {/* Bottom CTA Skeleton */}
        <div className="mt-auto pt-3 border-t border-gray-100">
          <div className="flex items-center justify-between">
            <div className="h-6 bg-gray-200 rounded w-16"></div>
            <div className="h-6 bg-gray-200 rounded w-20"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RestaurantCardSkeleton; 