'use client';
import React from 'react';
import SmartSearch from '@/components/SmartSearch';

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
               <SmartSearch
           onSearch={onSearch}
           placeholder={placeholder}
           showAdvancedFilters={!!onFilterClick}
           className=""
           useGoogleAPI={false}
         />
    </div>
  );
} 