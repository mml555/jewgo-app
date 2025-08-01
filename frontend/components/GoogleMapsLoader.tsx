'use client';

import { useEffect, useState } from 'react';

interface GoogleMapsLoaderProps {
  children: React.ReactNode;
}

// Global state to track if Google Maps is being loaded
let globalLoadingState = {
  isLoading: false,
  isLoaded: false,
  scriptElement: null as HTMLScriptElement | null,
};

export default function GoogleMapsLoader({ children }: GoogleMapsLoaderProps) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadGoogleMapsAPI = () => {
      // Check if already loaded globally
      if (globalLoadingState.isLoaded || (window.google && window.google.maps)) {
        setIsLoaded(true);
        setIsLoading(false);
        return;
      }

      // Check if script is already being loaded globally
      if (globalLoadingState.isLoading && globalLoadingState.scriptElement) {
        console.log('Google Maps script already loading globally, waiting...');
        const checkLoaded = () => {
          if (window.google && window.google.maps) {
            globalLoadingState.isLoaded = true;
            globalLoadingState.isLoading = false;
            setIsLoaded(true);
            setIsLoading(false);
          } else {
            setTimeout(checkLoaded, 100);
          }
        };
        checkLoaded();
        return;
      }

      // Check if script is already in DOM
      const existingScript = document.querySelector('script[src*="maps.googleapis.com"]') as HTMLScriptElement;
      if (existingScript) {
        console.log('Google Maps script already in DOM, waiting for load...');
        const checkLoaded = () => {
          if (window.google && window.google.maps) {
            globalLoadingState.isLoaded = true;
            globalLoadingState.isLoading = false;
            setIsLoaded(true);
            setIsLoading(false);
          } else {
            setTimeout(checkLoaded, 100);
          }
        };
        checkLoaded();
        return;
      }

      // Load Google Maps API
      const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;
      console.log('Google Maps API Key:', apiKey ? 'Present' : 'Missing');
      
      if (!apiKey) {
        console.error('Google Maps API key is missing. Please set NEXT_PUBLIC_GOOGLE_MAPS_API_KEY in your environment variables.');
        setIsLoading(false);
        return;
      }
      
      // Set global loading state
      globalLoadingState.isLoading = true;
      
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places,geometry&loading=async`;
      script.async = true;
      script.defer = true;
      
      // Store script element globally
      globalLoadingState.scriptElement = script;
      
      // Add timeout for script loading
      const scriptTimeout = setTimeout(() => {
        console.error('Google Maps script failed to load within 30 seconds');
        globalLoadingState.isLoading = false;
        globalLoadingState.scriptElement = null;
        setIsLoading(false);
      }, 30000);
      
      script.onload = () => {
        clearTimeout(scriptTimeout);
        globalLoadingState.isLoaded = true;
        globalLoadingState.isLoading = false;
        globalLoadingState.scriptElement = null;
        setIsLoaded(true);
        setIsLoading(false);
        console.log('Google Maps script loaded successfully');
      };
      
      script.onerror = () => {
        clearTimeout(scriptTimeout);
        console.error('Failed to load Google Maps API');
        globalLoadingState.isLoading = false;
        globalLoadingState.scriptElement = null;
        setIsLoading(false);
      };

      document.head.appendChild(script);
    };

    loadGoogleMapsAPI();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-jewgo-primary mx-auto mb-4"></div>
          <p className="text-gray-600">Loading maps...</p>
        </div>
      </div>
    );
  }

  if (!isLoaded) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <p className="text-red-600 mb-2">Failed to load Google Maps</p>
          <p className="text-gray-600 text-sm">Please check your internet connection and try again.</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
} 