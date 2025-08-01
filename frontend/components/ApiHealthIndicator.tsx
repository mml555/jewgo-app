'use client';

import React, { useState, useEffect } from 'react';

interface ApiHealthStatus {
  status: 'healthy' | 'unhealthy' | 'checking' | 'unknown';
  message: string;
  lastChecked: Date | null;
}

export default function ApiHealthIndicator() {
  const [healthStatus, setHealthStatus] = useState<ApiHealthStatus>({
    status: 'checking',
    message: 'Checking API status...',
    lastChecked: null
  });

  const checkApiHealth = async () => {
    try {
      setHealthStatus(prev => ({
        ...prev,
        status: 'checking',
        message: 'Checking API status...'
      }));

      const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL 
        ? `${process.env.NEXT_PUBLIC_BACKEND_URL}/health`
        : process.env.NODE_ENV === 'production'
        ? 'https://jewgo.onrender.com/health'
        : 'http://127.0.0.1:8081/health';

      const response = await fetch(apiUrl, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
        // Increase timeout to 15 seconds to handle cold starts
        signal: AbortSignal.timeout(15000)
      });

      if (response.ok) {
        const data = await response.json();
        setHealthStatus({
          status: 'healthy',
          message: `API Healthy - ${data.restaurants_count || 0} restaurants available`,
          lastChecked: new Date()
        });
      } else {
        setHealthStatus({
          status: 'unhealthy',
          message: `API Error - Status ${response.status}`,
          lastChecked: new Date()
        });
      }
    } catch (error) {
      console.error('API health check failed:', error);
      
      // Provide more specific error messages
      let errorMessage = 'API Unavailable - Connection failed';
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          errorMessage = 'API Timeout - Backend may be starting up';
        } else if (error.message.includes('Failed to fetch')) {
          errorMessage = 'API Unreachable - Network issue';
        }
      }
      
      setHealthStatus({
        status: 'unhealthy',
        message: errorMessage,
        lastChecked: new Date()
      });
    }
  };

  useEffect(() => {
    // Initial check with a delay to avoid blocking page load
    const initialCheck = setTimeout(checkApiHealth, 2000);
    
    // Check health every 60 seconds instead of 30 to reduce load
    const interval = setInterval(checkApiHealth, 60000);
    
    return () => {
      clearTimeout(initialCheck);
      clearInterval(interval);
    };
  }, []);

  const getStatusColor = () => {
    switch (healthStatus.status) {
      case 'healthy':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'unhealthy':
        return 'text-red-600 bg-red-50 border-red-200';
      case 'checking':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getStatusIcon = () => {
    switch (healthStatus.status) {
      case 'healthy':
        return '🟢';
      case 'unhealthy':
        return '🔴';
      case 'checking':
        return '🟡';
      default:
        return '⚪';
    }
  };

  return (
    <div className={`fixed bottom-20 right-4 z-50 px-3 py-2 rounded-lg border text-xs font-medium ${getStatusColor()}`}>
      <div className="flex items-center space-x-2">
        <span>{getStatusIcon()}</span>
        <span>{healthStatus.message}</span>
        <button
          onClick={checkApiHealth}
          className="ml-2 px-2 py-1 bg-white rounded text-xs hover:bg-gray-50 transition-colors"
          title="Refresh API status"
        >
          🔄
        </button>
      </div>
      {healthStatus.lastChecked && (
        <div className="text-xs opacity-75 mt-1">
          Last checked: {healthStatus.lastChecked.toLocaleTimeString()}
        </div>
      )}
    </div>
  );
} 