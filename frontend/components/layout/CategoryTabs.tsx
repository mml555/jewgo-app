'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { Utensils, Store, Building2, Droplets, Star } from 'lucide-react';

interface CategoryTabsProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

const categories = [
  {
    id: 'eatery',
    label: 'Eatery',
    icon: Utensils,
    href: '/eatery',
    color: 'text-orange-600'
  },
  {
    id: 'stores',
    label: 'Stores',
    icon: Store,
    href: '/stores',
    color: 'text-green-600'
  },
  {
    id: 'shuls',
    label: 'Shuls',
    icon: Building2,
    href: '/shuls',
    color: 'text-blue-600'
  },
  {
    id: 'mikvahs',
    label: 'Mikvahs',
    icon: Droplets,
    href: '/mikvahs',
    color: 'text-purple-600'
  },
  {
    id: 'specials',
    label: 'Specials',
    icon: Star,
    href: '/specials',
    color: 'text-yellow-600'
  }
];

export default function CategoryTabs({ activeTab, onTabChange }: CategoryTabsProps) {
  const router = useRouter();

  const handleTabClick = (category: typeof categories[0]) => {
    onTabChange(category.id);
    router.push(category.href);
  };

  return (
    <div className="bg-white border-b border-gray-100 px-4 py-3">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center space-x-1 overflow-x-auto scrollbar-hide">
          {categories.map((category) => {
            const Icon = category.icon;
            const isActive = activeTab === category.id;
            
            return (
              <button
                key={category.id}
                onClick={() => handleTabClick(category)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-xl transition-all duration-200 whitespace-nowrap ${
                  isActive
                    ? 'bg-blue-50 text-blue-600 border border-blue-200'
                    : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
                }`}
              >
                <Icon size={18} className={isActive ? category.color : 'text-gray-500'} />
                <span className="font-medium text-sm">{category.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
} 