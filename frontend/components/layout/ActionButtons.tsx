'use client';

import React from 'react';
import { Map, Plus, Filter, X } from 'lucide-react';

interface ActionButtonsProps {
  onShowFilters: () => void;
  onShowMap: () => void;
  onAddEatery: () => void;
  hasActiveFilters: boolean;
  onClearFilters?: () => void;
  isOnMapPage?: boolean;
}

export default function ActionButtons({
  onShowFilters,
  onShowMap,
  onAddEatery,
  hasActiveFilters,
  onClearFilters,
  isOnMapPage = false
}: ActionButtonsProps) {
  return (
    <div className="bg-white border-b border-gray-100 px-4 py-3">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between">
          {/* Left side - Filter and Clear */}
          <div className="flex items-center space-x-2">
            <button
              onClick={onShowFilters}
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl transition-all duration-200 ${
                hasActiveFilters
                  ? 'bg-blue-50 text-blue-600 border border-blue-200'
                  : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Filter size={16} />
              <span className="text-sm font-medium">Filters</span>
              {hasActiveFilters && (
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              )}
            </button>
            
            {hasActiveFilters && onClearFilters && (
              <button
                onClick={onClearFilters}
                className="flex items-center space-x-1 px-3 py-2 text-gray-500 hover:text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
              >
                <X size={14} />
                <span className="text-sm">Clear</span>
              </button>
            )}
          </div>

          {/* Right side - Map and Add */}
          <div className="flex items-center space-x-2">
            <button
              onClick={onShowMap}
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl transition-all duration-200 ${
                isOnMapPage
                  ? 'bg-blue-50 text-blue-600 border border-blue-200'
                  : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Map size={16} />
              <span className="text-sm font-medium">Map</span>
            </button>
            
            <button
              onClick={onAddEatery}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors"
            >
              <Plus size={16} />
              <span className="text-sm font-medium">Add Eatery</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
} 