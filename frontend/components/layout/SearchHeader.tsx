'use client';

import React, { useState } from 'react';
import { Search, MapPin, Filter } from 'lucide-react';

interface SearchHeaderProps {
  onSearch: (query: string) => void;
  onLocationSelect?: (location: { lat: number; lng: number; address: string }) => void;
  placeholder?: string;
  showFilters?: boolean;
  onShowFilters?: () => void;
}

export default function SearchHeader({
  onSearch,
  onLocationSelect,
  placeholder = "Search for kosher restaurants, agencies, or locations...",
  showFilters = true,
  onShowFilters
}: SearchHeaderProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  const handleLocationClick = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          onLocationSelect?.({
            lat: latitude,
            lng: longitude,
            address: 'Current Location'
          });
        },
        (error) => {
          console.error('Error getting location:', error);
        }
      );
    }
  };

  return (
    <div className="bg-white border-b border-gray-100 px-4 py-4">
      <div className="max-w-4xl mx-auto">
        {/* Logo and Title */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">JG</span>
            </div>
            <h1 className="text-xl font-bold text-gray-900">JewGo</h1>
          </div>
          {showFilters && onShowFilters && (
            <button
              onClick={onShowFilters}
              className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <Filter size={20} />
            </button>
          )}
        </div>

        {/* Search Bar */}
        <form onSubmit={handleSubmit} className="relative">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={placeholder}
              className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50 hover:bg-white transition-colors"
            />
            <button
              type="button"
              onClick={handleLocationClick}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 p-1 text-gray-400 hover:text-gray-600 transition-colors"
            >
              <MapPin size={18} />
            </button>
          </div>
        </form>

        {/* Quick Actions */}
        <div className="flex items-center space-x-4 mt-3">
          <button
            onClick={() => onSearch('kosher restaurants near me')}
            className="text-sm text-blue-600 hover:text-blue-800 font-medium"
          >
            Near me
          </button>
          <button
            onClick={() => onSearch('ORB certified')}
            className="text-sm text-gray-600 hover:text-gray-800"
          >
            ORB certified
          </button>
          <button
            onClick={() => onSearch('dairy restaurants')}
            className="text-sm text-gray-600 hover:text-gray-800"
          >
            Dairy
          </button>
          <button
            onClick={() => onSearch('meat restaurants')}
            className="text-sm text-gray-600 hover:text-gray-800"
          >
            Meat
          </button>
        </div>
      </div>
    </div>
  );
} 