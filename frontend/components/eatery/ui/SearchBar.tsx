'use client';
import React from 'react';
import GoogleMapsStyleSearch from '@/components/GoogleMapsStyleSearch';

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
  return (
    <div className={`w-full ${className}`}>
      <GoogleMapsStyleSearch
        onSearch={onSearch}
        onResultsUpdate={() => {}}
        placeholder={placeholder}
        showAdvancedFilters={!!onFilterClick}
        className=""
      />
    </div>
  );
} 