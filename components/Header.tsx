'use client';

import Logo from './Logo';

export default function Header() {
  return (
    <header className="bg-white shadow-soft border-b border-neutral-200 sticky top-0 z-50 backdrop-blur-lg bg-white/95 w-full">
      <div className="px-4 py-3 sm:px-6 sm:py-4">
        <div className="flex items-center justify-between">
          {/* Logo and Brand */}
          <div className="flex items-center space-x-3">
            {/* Logo Container */}
            <div className="w-10 h-10 sm:w-12 sm:h-12 bg-neutral-800 rounded-xl flex items-center justify-center shadow-medium overflow-hidden">
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
              <p className="text-xs text-neutral-500 -mt-1 hidden sm:block">Find Your Kosher Eatery</p>
            </div>
          </div>

          {/* Right Side Actions - Removed for cleaner design */}
        </div>
      </div>
    </header>
  );
} 