'use client';

import React from 'react';
import { cn } from '@/utils/cn';

interface MapToggleProps {
  isMapView: boolean;
  onToggle: () => void;
  className?: string;
}

export default function MapToggle({ isMapView, onToggle, className }: MapToggleProps) {
  return (
    <div className={cn("flex items-center gap-2", className)}>
      <button
        onClick={onToggle}
        className={cn(
          "inline-flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium border transition-all duration-200",
          "hover:shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2",
          isMapView
            ? "bg-green-500 text-white border-green-600 shadow-sm"
            : "bg-white text-gray-700 border-gray-300 hover:bg-gray-50"
        )}
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-1.447-.894L15 4m0 13V4m0 0L9 7" />
        </svg>
        {isMapView ? 'List View' : 'Map View'}
      </button>
    </div>
  );
} 