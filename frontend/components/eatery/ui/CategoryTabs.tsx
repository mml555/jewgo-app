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
      <div className="flex space-x-2 overflow-x-auto scrollbar-hide pb-2">
        {categories.map((category) => {
          const IconComponent = category.icon;
          const isActive = activeCategory === category.id;
          
          return (
            <button
              key={category.id}
              onClick={() => onCategoryChange(category.id)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-full border transition-all duration-200 whitespace-nowrap flex-shrink-0 ${
                isActive
                  ? 'bg-black text-white border-black'
                  : 'bg-white text-black border-gray-300 hover:border-gray-400'
              }`}
            >
              <IconComponent className="w-4 h-4" />
              <span className="text-sm font-medium">{category.label}</span>
            </button>
          );
        })}
      </div>
      
      {/* Active indicator line */}
      <div className="relative mt-2">
        <div className="h-0.5 bg-gray-200 rounded-full">
          <div 
            className="h-full bg-black rounded-full transition-all duration-300"
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