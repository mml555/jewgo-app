'use client';

import React from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { Search, Heart, Ticket, Bell, User } from 'lucide-react';

const BottomTabBar: React.FC = () => {
  const router = useRouter();
  const pathname = usePathname();

  const navItems = [
    {
      id: 'explore',
      label: 'Explore',
      path: '/',
      icon: Search,
    },
    {
      id: 'favorites',
      label: 'Favorites',
      path: '/favorites',
      icon: Heart,
    },
    {
      id: 'specials',
      label: 'Specials',
      path: '/specials',
      icon: Ticket,
    },
    {
      id: 'notifications',
      label: 'Notifications',
      path: '/notifications',
      icon: Bell,
    },
    {
      id: 'profile',
      label: 'Profile',
      path: '/profile',
      icon: User,
    },
  ];

  const handleNavigation = (path: string) => {
    router.push(path);
  };

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-2 py-1 z-50 shadow-lg md:hidden">
      <div className="flex justify-around">
        {navItems.map((item) => {
          const IconComponent = item.icon;
          const isActive = pathname === item.path;
          
          return (
            <button
              key={item.id}
              onClick={() => handleNavigation(item.path)}
              className={`flex flex-col items-center space-y-1 py-2 px-2 rounded-lg transition-colors min-h-[44px] justify-center ${
                isActive
                  ? 'text-black'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              <div className={`${isActive ? 'text-black' : 'text-gray-500'}`}>
                <IconComponent className="w-5 h-5" />
              </div>
              <span className={`text-xs font-medium leading-tight ${isActive ? 'text-black' : 'text-gray-500'}`}>
                {item.label}
              </span>
              
              {/* Active indicator */}
              {isActive && (
                <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-8 h-0.5 bg-black rounded-full" />
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
};

export default BottomTabBar; 