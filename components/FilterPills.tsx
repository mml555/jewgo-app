'use client';

import React from 'react';
import { cn } from '@/utils/cn';

interface FilterPillsProps {
  selectedFilters: string[];
  onFilterChange: (filter: string) => void;
  className?: string;
}

const availableFilters = [
  { id: 'open-now', label: 'Open Now', icon: '🕒' },
  { id: 'dairy', label: 'Dairy', icon: '🥛' },
  { id: 'meat', label: 'Meat', icon: '🥩' },
  { id: 'pareve', label: 'Pareve', icon: '🥗' },
  { id: 'budget-friendly', label: 'Budget-Friendly', icon: '💰' },
  { id: 'family-friendly', label: 'Family Friendly', icon: '👨‍👩‍👧‍👦' },
  { id: 'glatt', label: 'Glatt', icon: '✅' },
  { id: 'cholov-yisroel', label: 'Cholov Yisroel', icon: '🥛' },
];

export default function FilterPills({ selectedFilters, onFilterChange, className }: FilterPillsProps) {
  return (
    <div className={cn("flex flex-wrap gap-2 mb-4", className)}>
      {availableFilters.map((filter) => {
        const isSelected = selectedFilters.includes(filter.id);
        return (
          <button
            key={filter.id}
            onClick={() => onFilterChange(filter.id)}
            className={cn(
              "inline-flex items-center px-3 py-1.5 rounded-full text-sm font-medium border transition-all duration-200",
              "hover:shadow-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2",
              isSelected
                ? "bg-green-500 text-white border-green-600 shadow-sm"
                : "bg-white text-gray-700 border-gray-300 hover:bg-gray-50"
            )}
          >
            <span className="mr-1.5">{filter.icon}</span>
            {filter.label}
          </button>
        );
      })}
    </div>
  );
} 