'use client';

import React, { useState, useEffect } from 'react';
import { MapPin, X, CheckCircle, AlertCircle } from 'lucide-react';

interface LocationPermissionPromptProps {
  onLocationGranted: (location: { latitude: number; longitude: number }) => void;
  onLocationDenied: () => void;
  onDismiss: () => void;
}

export default function LocationPermissionPrompt({
  onLocationGranted,
  onLocationDenied,
  onDismiss
}: LocationPermissionPromptProps) {
  const [isRequesting, setIsRequesting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const requestLocation = () => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by this browser');
      return;
    }

    setIsRequesting(true);
    setError(null);

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setIsRequesting(false);
        const location = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        };
        onLocationGranted(location);
      },
      (error) => {
        setIsRequesting(false);
        let errorMessage = 'Unable to get your location';
        
        switch (error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = 'Location access was denied. Please enable location services in your browser settings.';
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage = 'Location information is unavailable. Please try again.';
            break;
          case error.TIMEOUT:
            errorMessage = 'Location request timed out. Please try again.';
            break;
        }
        
        setError(errorMessage);
        onLocationDenied();
      },
      {
        enableHighAccuracy: true,
        timeout: 15000,
        maximumAge: 300000, // 5 minutes
      }
    );
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-md w-full p-6 border border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="bg-jewgo-primary/10 p-2 rounded-full">
              <MapPin className="h-6 w-6 text-jewgo-primary" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900">
              Enable Location Access
            </h3>
          </div>
          <button
            onClick={onDismiss}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="mb-6">
          <p className="text-gray-600 mb-4">
            To provide you with the best experience, we'd like to access your location to:
          </p>
          <ul className="space-y-2 text-sm text-gray-600">
            <li className="flex items-start space-x-2">
              <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
              <span>Show restaurants near you</span>
            </li>
            <li className="flex items-start space-x-2">
              <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
              <span>Calculate accurate distances</span>
            </li>
            <li className="flex items-start space-x-2">
              <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
              <span>Provide personalized recommendations</span>
            </li>
          </ul>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
            <div className="flex items-center space-x-2">
              <AlertCircle className="h-4 w-4 text-red-500" />
              <span className="text-sm text-red-700">{error}</span>
            </div>
          </div>
        )}

        <div className="flex space-x-3">
          <button
            onClick={onDismiss}
            className="flex-1 px-4 py-3 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-all duration-200 font-medium"
          >
            Not Now
          </button>
          <button
            onClick={requestLocation}
            disabled={isRequesting}
            className="flex-1 px-4 py-3 bg-green-500 text-white hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-all duration-200 font-medium shadow-sm hover:shadow-md"
          >
            {isRequesting ? (
              <div className="flex items-center justify-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Getting Location...</span>
              </div>
            ) : (
              'Enable Location'
            )}
          </button>
        </div>
      </div>
    </div>
  );
} 