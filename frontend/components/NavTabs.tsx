'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/utils/cn';

  // Icon components
  const MikvahIcon = () => (
    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      {/* Simple 3-tier ladder going into water */}
      {/* Water surface */}
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M4 18h16" />
      {/* Water waves */}
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M6 19h2" />
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M10 19h2" />
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M14 19h2" />
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M18 19h2" />
      
      {/* Ladder sides */}
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 6v12" />
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 6v12" />
      
      {/* 3 ladder rungs */}
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 8h8" />
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h8" />
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 16h8" />
    </svg>
  );

const ShulIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
  </svg>
);

const SpecialsIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
  </svg>
);

const EateryIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 15.546c-.523 0-1.046.151-1.5.454a2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.701 2.701 0 00-1.5-.454M9 6v2m3-2v2m3-2v2M9 3h.01M12 3h.01M15 3h.01M21 21v-7a2 2 0 00-2-2H5a2 2 0 00-2 2v7h18zM6 10h7a2 2 0 012 2v5H4v-5a2 2 0 012-2z" />
  </svg>
);

const StoreIcon = () => (
  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
  </svg>
);

// Navigation tabs configuration
const navTabs = [
  { key: 'mikvahs', icon: <MikvahIcon />, label: 'Mikvahs' },
  { key: 'shuls', icon: <ShulIcon />, label: 'Shuls' },
  { key: 'specials', icon: <SpecialsIcon />, label: 'Specials' },
  { key: 'eatery', icon: <EateryIcon />, label: 'Eatery' },
  { key: 'stores', icon: <StoreIcon />, label: 'Stores' },
];

interface NavTabsProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
  className?: string;
}

export default function NavTabs({ activeTab, onTabChange, className }: NavTabsProps) {
  return (
    <div className={cn("px-4 py-2 bg-white border-b border-gray-100", className)}>
              <div className="grid grid-cols-3 sm:grid-cols-5 gap-2">
        {navTabs.map(({ key, icon, label }) => (
          <button
            key={key}
            onClick={() => onTabChange(key)}
            className={cn(
              "flex flex-col items-center p-3 rounded-xl transition-all duration-200 w-full",
              "hover:scale-105 active:scale-95",
              activeTab === key
                ? "bg-black text-white shadow-lg"
                : "bg-white text-gray-700 border border-gray-200 hover:bg-gray-50 hover:border-gray-300"
            )}
          >
            <span className="w-6 h-6 mb-1">{icon}</span>
            <span className="text-xs font-medium">{label}</span>
          </button>
        ))}
      </div>
    </div>
  );
} 