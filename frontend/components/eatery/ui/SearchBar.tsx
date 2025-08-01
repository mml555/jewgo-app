'use client';

import React, { useState } from 'react';
import { Search, SlidersHorizontal } from 'lucide-react';

interface SearchBarProps {
  onSearch: (query: string) => void;
  onFilterClick?: () => void;
  placeholder?: string;
  className?: string;
}

export default function SearchBar({ 
  onSearch, 
  onFilterClick, 
  placeholder = "Find your Eatery",
  className = "" 
}: SearchBarProps) {
  const [query, setQuery] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    onSearch(value);
  };

  const handleFilterClick = () => {
    if (onFilterClick) {
      onFilterClick();
    }
  };

  return (
    <div className={`relative w-full ${className}`}>
      <div className="relative flex items-center">
        {/* Search Icon */}
        <div className="absolute left-3 text-gray-500">
          <Search className="w-5 h-5" />
        </div>
        
        {/* Input Field */}
        <input
          type="text"
          value={query}
          onChange={handleInputChange}
          placeholder={placeholder}
          className="w-full pl-10 pr-12 py-3 bg-gray-50 border border-gray-200 rounded-full text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
        />
        
        {/* Filter Icon */}
        <button
          onClick={handleFilterClick}
          className="absolute right-3 p-1 text-gray-500 hover:text-gray-700 transition-colors duration-200"
          aria-label="Filter options"
        >
          <SlidersHorizontal className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
} 