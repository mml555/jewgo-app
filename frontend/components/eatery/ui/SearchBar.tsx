'use client';
import React from 'react';
import FastSearch from '@/components/FastSearch';

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
      <FastSearch
        onSearch={onSearch}
        placeholder={placeholder}
        showAdvancedFilters={!!onFilterClick}
        className=""
      />
    </div>
  );
} 