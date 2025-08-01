'use client';

import { useState, useEffect } from 'react';
import { checkApiEndpoints } from '@/lib/api/health';

interface HealthStatus {
  isHealthy: boolean;
  response?: any;
  error?: string;
  responseTime: number;
}

interface ApiStatus {
  health: HealthStatus;
  restaurants: {
    success: boolean;
    error?: string;
    responseTime: number;
  };
}

export default function HealthPage() {
  const [status, setStatus] = useState<ApiStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [lastChecked, setLastChecked] = useState<Date | null>(null);

  const checkStatus = async () => {
    setLoading(true);
    try {
      const result = await checkApiEndpoints();
      setStatus(result);
      setLastChecked(new Date());
    } catch (error) {
      console.error('Health check failed:', error);
      setStatus({
        health: {
          isHealthy: false,
          error: error instanceof Error ? error.message : 'Unknown error',
          responseTime: 0
        },
        restaurants: {
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error',
          responseTime: 0
        }
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkStatus();
  }, []);

  const getStatusColor = (isHealthy: boolean) => {
    return isHealthy ? 'text-green-600' : 'text-red-600';
  };

  const getStatusIcon = (isHealthy: boolean) => {
    return isHealthy ? '✅' : '❌';
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-3xl font-bold text-gray-900">Backend Health Check</h1>
            <button
              onClick={checkStatus}
              disabled={loading}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Checking...' : 'Refresh'}
            </button>
          </div>

          {lastChecked && (
            <p className="text-sm text-gray-600 mb-6">
              Last checked: {lastChecked.toLocaleString()}
            </p>
          )}

          {status && (
            <div className="space-y-6">
              {/* Health Endpoint */}
              <div className="border rounded-lg p-4">
                <h2 className="text-xl font-semibold mb-3 flex items-center">
                  <span className="mr-2">{getStatusIcon(status.health.isHealthy)}</span>
                  Health Endpoint
                  <span className={`ml-2 text-sm ${getStatusColor(status.health.isHealthy)}`}>
                    ({status.health.responseTime}ms)
                  </span>
                </h2>
                
                {status.health.isHealthy ? (
                  <div className="space-y-2">
                    <p className="text-green-600 font-medium">✅ Backend is healthy</p>
                    {status.health.response && (
                      <div className="bg-gray-50 p-3 rounded">
                        <pre className="text-sm overflow-auto">
                          {JSON.stringify(status.health.response, null, 2)}
                        </pre>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="space-y-2">
                    <p className="text-red-600 font-medium">❌ Backend is unhealthy</p>
                    {status.health.error && (
                      <p className="text-red-600 text-sm">{status.health.error}</p>
                    )}
                  </div>
                )}
              </div>

              {/* Restaurants Endpoint */}
              <div className="border rounded-lg p-4">
                <h2 className="text-xl font-semibold mb-3 flex items-center">
                  <span className="mr-2">{getStatusIcon(status.restaurants.success)}</span>
                  Restaurants API
                  <span className={`ml-2 text-sm ${getStatusColor(status.restaurants.success)}`}>
                    ({status.restaurants.responseTime}ms)
                  </span>
                </h2>
                
                {status.restaurants.success ? (
                  <p className="text-green-600 font-medium">✅ Restaurants API is working</p>
                ) : (
                  <div className="space-y-2">
                    <p className="text-red-600 font-medium">❌ Restaurants API is not working</p>
                    {status.restaurants.error && (
                      <p className="text-red-600 text-sm">{status.restaurants.error}</p>
                    )}
                  </div>
                )}
              </div>

              {/* Overall Status */}
              <div className="border rounded-lg p-4 bg-gray-50">
                <h2 className="text-xl font-semibold mb-3">Overall Status</h2>
                <div className="space-y-2">
                  <p className="font-medium">
                    Backend Health: 
                    <span className={`ml-2 ${getStatusColor(status.health.isHealthy)}`}>
                      {status.health.isHealthy ? 'Healthy' : 'Unhealthy'}
                    </span>
                  </p>
                  <p className="font-medium">
                    API Endpoints: 
                    <span className={`ml-2 ${getStatusColor(status.restaurants.success)}`}>
                      {status.restaurants.success ? 'Working' : 'Not Working'}
                    </span>
                  </p>
                  
                  {!status.health.isHealthy && (
                    <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded">
                      <h3 className="font-medium text-yellow-800 mb-2">Troubleshooting Tips:</h3>
                      <ul className="text-sm text-yellow-700 space-y-1">
                        <li>• The backend server may be in sleep mode (common with free hosting)</li>
                        <li>• Try refreshing the page in a few minutes</li>
                        <li>• Check if the backend service is running on Render</li>
                        <li>• Database connection issues may be causing the timeout</li>
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {loading && (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-2 text-gray-600">Checking backend status...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 