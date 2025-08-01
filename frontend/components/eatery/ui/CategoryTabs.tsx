'use client';

import React from 'react';
import { Building2, Star, Ticket, Utensils, ShoppingCart } from 'lucide-react';

interface CategoryTabsProps {
  activeCategory: string;
  onCategoryChange: (category: string) => void;
  className?: string;
}

const categories = [
  {
    id: 'mikvahs',
    label: 'Mikvahs',
    icon: Building2,
  },
  {
    id: 'shuls',
    label: 'Shuls',
    icon: Star,
  },
  {
    id: 'specials',
    label: 'Specials',
    icon: Ticket,
  },
  {
    id: 'eatery',
    label: 'Eatery',
    icon: Utensils,
  },
  {
    id: 'stores',
    label: 'Stores',
    icon: ShoppingCart,
  },
];

export default function CategoryTabs({ 
  activeCategory, 
  onCategoryChange, 
  className = "" 
}: CategoryTabsProps) {
  return (
    <div className={`w-full ${className}`}>
      <div className="flex space-x-3 overflow-x-auto scrollbar-hide pb-3">
        {categories.map((category) => {
          const IconComponent = category.icon;
          const isActive = activeCategory === category.id;
          
          return (
            <button
              key={category.id}
              onClick={() => onCategoryChange(category.id)}
              className={`flex items-center space-x-2.5 px-5 py-3 rounded-full border transition-all duration-300 whitespace-nowrap flex-shrink-0 shadow-sm ${
                isActive
                  ? 'bg-black text-white border-black shadow-md'
                  : 'bg-white text-gray-700 border-gray-200 hover:border-gray-300 hover:shadow-md hover:bg-gray-50'
              }`}
            >
              <IconComponent className={`w-4 h-4 ${isActive ? 'text-white' : 'text-gray-600'}`} />
              <span className="text-sm font-semibold">{category.label}</span>
            </button>
          );
        })}
      </div>
      
      {/* Active indicator line */}
      <div className="relative mt-3">
        <div className="h-1 bg-gray-100 rounded-full">
          <div 
            className="h-full bg-black rounded-full transition-all duration-500 ease-out"
            style={{
              width: '20%',
              transform: `translateX(${categories.findIndex(c => c.id === activeCategory) * 100}%)`
            }}
          />
        </div>
      </div>
    </div>
  );
} 