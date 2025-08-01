'use client';

import React from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { Home, Map, Heart, User, Plus } from 'lucide-react';

const navigationItems = [
  {
    id: 'home',
    label: 'Home',
    icon: Home,
    href: '/eatery'
  },
  {
    id: 'map',
    label: 'Map',
    icon: Map,
    href: '/live-map'
  },
  {
    id: 'add',
    label: 'Add',
    icon: Plus,
    href: '/add-eatery'
  },
  {
    id: 'favorites',
    label: 'Favorites',
    icon: Heart,
    href: '/favorites'
  },
  {
    id: 'profile',
    label: 'Profile',
    icon: User,
    href: '/profile'
  }
];

export default function BottomNavigation() {
  const router = useRouter();
  const pathname = usePathname();

  const handleNavigation = (href: string) => {
    router.push(href);
  };

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-around py-2">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            
            return (
              <button
                key={item.id}
                onClick={() => handleNavigation(item.href)}
                className={`flex flex-col items-center space-y-1 px-3 py-2 rounded-lg transition-colors ${
                  isActive
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <Icon size={20} />
                <span className="text-xs font-medium">{item.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
} 