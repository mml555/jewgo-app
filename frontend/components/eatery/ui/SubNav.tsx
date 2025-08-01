'use client';

import React from 'react';
import { MapPin, Plus, SlidersHorizontal } from 'lucide-react';
import { useRouter } from 'next/navigation';

interface SubNavProps {
  className?: string;
}

export default function SubNav({ className = "" }: SubNavProps) {
  const router = useRouter();

  const navItems = [
    {
      id: 'live-map',
      label: 'Live Map',
      icon: MapPin,
      onClick: () => router.push('/live-map'),
    },
    {
      id: 'add-eatery',
      label: 'Add a Eatery',
      icon: Plus,
      onClick: () => router.push('/add-eatery'),
    },
    {
      id: 'advanced-filters',
      label: 'Advanced Filters',
      icon: SlidersHorizontal,
      onClick: () => {
        // This could open a modal or navigate to filters page
        console.log('Advanced filters clicked');
      },
    },
  ];

  return (
    <div className={`w-full ${className}`}>
      <div className="flex flex-col sm:flex-row gap-2 sm:gap-3">
        {navItems.map((item) => {
          const IconComponent = item.icon;
          
          return (
            <button
              key={item.id}
              onClick={item.onClick}
              className="flex items-center justify-center space-x-2 px-4 py-3 bg-white border border-gray-300 rounded-lg hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 flex-1 sm:flex-none"
            >
              <IconComponent className="w-4 h-4 text-gray-700" />
              <span className="text-sm font-medium text-gray-900">{item.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
} 