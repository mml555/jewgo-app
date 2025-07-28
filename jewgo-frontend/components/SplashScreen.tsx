'use client';

import { useState, useEffect } from 'react';
import Logo from './Logo';

interface SplashScreenProps {
  onComplete?: () => void;
  duration?: number;
}

export default function SplashScreen({ onComplete, duration = 2000 }: SplashScreenProps) {
  const [isVisible, setIsVisible] = useState(true);
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsAnimating(true);
      setTimeout(() => {
        setIsVisible(false);
        onComplete?.();
      }, 500);
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onComplete]);

  if (!isVisible) return null;

  return (
    <div className={`fixed inset-0 z-50 bg-white flex items-center justify-center transition-opacity duration-500 ${
      isAnimating ? 'opacity-0' : 'opacity-100'
    }`}>
      <div className="flex flex-col items-center space-y-6">
        {/* Logo with animation */}
        <div className={`transform transition-all duration-700 ${
          isAnimating ? 'scale-75 opacity-0' : 'scale-100 opacity-100'
        }`}>
          <Logo size="xl" className="w-24 h-24" />
        </div>
        
        {/* App name with fade in */}
        <div className={`transition-all duration-700 delay-300 ${
          isAnimating ? 'opacity-0 translate-y-4' : 'opacity-100 translate-y-0'
        }`}>
          <h1 
            className="text-3xl font-bold text-mint-green tracking-wide"
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
          <p className="text-gray-500 text-center mt-2">
            Find Your Kosher Eatery
          </p>
        </div>

        {/* Loading dots */}
        <div className={`flex space-x-2 transition-opacity duration-700 delay-500 ${
          isAnimating ? 'opacity-0' : 'opacity-100'
        }`}>
          <div className="w-2 h-2 bg-mint-green rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-mint-green rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
          <div className="w-2 h-2 bg-mint-green rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        </div>
      </div>
    </div>
  );
} 