'use client';

import { useState } from 'react';
import Logo from './Logo';

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-soft border-b border-gray-200 sticky top-0 z-50 backdrop-blur-lg bg-white/95 w-full">
      <div className="px-4 py-3 sm:px-6 sm:py-4">
        <div className="flex items-center justify-between">
          {/* Logo and Brand */}
          <div className="flex items-center space-x-3">
            {/* Logo Container */}
            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gray-800 rounded-xl flex items-center justify-center shadow-medium overflow-hidden">
              <Logo size="sm" className="w-6 h-6 sm:w-8 sm:h-8" />
            </div>
            
            {/* Brand Text */}
            <div>
              <h1 
                className="text-lg sm:text-xl font-bold text-mint-green tracking-wide"
                style={{ 
                  fontFamily: '"Comic Sans MS", "Chalkboard SE", "Marker Felt", "Arial Rounded MT Bold", "Helvetica Rounded", sans-serif',
                  fontWeight: '700',
                  letterSpacing: '0.025em',
                  fontStyle: 'normal',
                  textShadow: '0 1px 2px rgba(0,0,0,0.1)'
                }}
              >
                Jewgo
              </h1>
              <p className="text-xs text-gray-500 -mt-1 hidden sm:block">Find Your Kosher Eatery</p>
            </div>
          </div>

          {/* Right Side Actions */}
          <div className="flex items-center space-x-2 sm:space-x-3">
            {/* Search Icon - Hidden on mobile since search bar is prominent */}
            <button className="hidden sm:block p-2 text-gray-600 hover:text-mint-green hover:bg-mint-green/10 rounded-lg transition-all duration-200 focus-ring">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </button>

            {/* Notifications */}
            <button className="p-2 text-gray-600 hover:text-mint-green hover:bg-mint-green/10 rounded-lg transition-all duration-200 focus-ring relative">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 17h5l-5 5v-5z"></path>
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
              </svg>
              {/* Notification Badge */}
              <span className="absolute -top-1 -right-1 w-3 h-3 bg-mint-green rounded-full border-2 border-white"></span>
            </button>

            {/* Menu Button */}
            <button 
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="p-2 text-gray-600 hover:text-mint-green hover:bg-mint-green/10 rounded-lg transition-all duration-200 focus-ring"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path>
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="mt-3 pt-3 border-t border-gray-200 animate-fade-in-up">
            <div className="space-y-1">
              <button className="w-full text-left px-3 py-2.5 text-gray-700 hover:bg-gray-50 hover:text-mint-green rounded-lg transition-colors duration-200">
                <div className="flex items-center space-x-3">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                  <span className="text-sm font-medium">Profile</span>
                </div>
              </button>
              <button className="w-full text-left px-3 py-2.5 text-gray-700 hover:bg-gray-50 hover:text-mint-green rounded-lg transition-colors duration-200">
                <div className="flex items-center space-x-3">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                  <span className="text-sm font-medium">Settings</span>
                </div>
              </button>
              <button className="w-full text-left px-3 py-2.5 text-gray-700 hover:bg-gray-50 hover:text-mint-green rounded-lg transition-colors duration-200">
                <div className="flex items-center space-x-3">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span className="text-sm font-medium">Help</span>
                </div>
              </button>
            </div>
          </div>
        )}
      </div>
    </header>
  );
} 