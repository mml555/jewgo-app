'use client';

import { useState, useEffect } from 'react';
import { performanceMonitor } from '@/lib/analytics/performance';

interface AnalyticsData {
  pageViews: number;
  uniqueUsers: number;
  sessionDuration: number;
  bounceRate: number;
  topPages: Array<{ page: string; views: number }>;
  userInteractions: Array<{ action: string; count: number }>;
  deviceTypes: Array<{ device: string; percentage: number }>;
  timeOfDay: Array<{ hour: number; sessions: number }>;
}

interface AnalyticsDashboardProps {
  className?: string;
  showCharts?: boolean;
}

export default function AnalyticsDashboard({ className = '', showCharts = false }: AnalyticsDashboardProps) {
  const [analytics, setAnalytics] = useState<AnalyticsData>({
    pageViews: 0,
    uniqueUsers: 0,
    sessionDuration: 0,
    bounceRate: 0,
    topPages: [],
    userInteractions: [],
    deviceTypes: [],
    timeOfDay: []
  });

  const [timeRange, setTimeRange] = useState<'24h' | '7d' | '30d'>('24h');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadAnalytics = async () => {
      setIsLoading(true);
      try {
        // Mock analytics data - replace with real API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const mockData: AnalyticsData = {
          pageViews: Math.floor(Math.random() * 1000) + 500,
          uniqueUsers: Math.floor(Math.random() * 200) + 100,
          sessionDuration: Math.floor(Math.random() * 300) + 120,
          bounceRate: Math.random() * 30 + 20,
          topPages: [
            { page: '/', views: 450 },
            { page: '/specials', views: 320 },
            { page: '/favorites', views: 280 },
            { page: '/profile', views: 150 },
            { page: '/live-map', views: 120 }
          ],
          userInteractions: [
            { action: 'Search', count: 1250 },
            { action: 'View Restaurant', count: 890 },
            { action: 'Add to Favorites', count: 340 },
            { action: 'Share Restaurant', count: 180 },
            { action: 'Claim Deal', count: 95 }
          ],
          deviceTypes: [
            { device: 'Mobile', percentage: 65 },
            { device: 'Desktop', percentage: 25 },
            { device: 'Tablet', percentage: 10 }
          ],
          timeOfDay: Array.from({ length: 24 }, (_, i) => ({
            hour: i,
            sessions: Math.floor(Math.random() * 50) + 10
          }))
        };

        setAnalytics(mockData);
      } catch (error) {
        console.error('Failed to load analytics:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadAnalytics();
  }, [timeRange]);

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}m ${secs}s`;
  };

  const formatPercentage = (value: number) => {
    return `${value.toFixed(1)}%`;
  };

  if (isLoading) {
    return (
      <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="h-20 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Analytics Dashboard</h3>
          <p className="text-sm text-gray-600">User behavior and app usage insights</p>
        </div>
        <div className="flex space-x-2">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value as any)}
            className="px-3 py-1 text-sm border border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
          </select>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="text-center p-4 bg-blue-50 rounded-lg">
          <div className="text-2xl font-bold text-blue-600">{analytics.pageViews.toLocaleString()}</div>
          <div className="text-sm text-blue-800">Page Views</div>
        </div>
        <div className="text-center p-4 bg-green-50 rounded-lg">
          <div className="text-2xl font-bold text-green-600">{analytics.uniqueUsers.toLocaleString()}</div>
          <div className="text-sm text-green-800">Unique Users</div>
        </div>
        <div className="text-center p-4 bg-purple-50 rounded-lg">
          <div className="text-2xl font-bold text-purple-600">{formatDuration(analytics.sessionDuration)}</div>
          <div className="text-sm text-purple-800">Avg Session</div>
        </div>
        <div className="text-center p-4 bg-orange-50 rounded-lg">
          <div className="text-2xl font-bold text-orange-600">{formatPercentage(analytics.bounceRate)}</div>
          <div className="text-sm text-orange-800">Bounce Rate</div>
        </div>
      </div>

      {/* Top Pages */}
      <div className="mb-8">
        <h4 className="font-medium text-gray-900 mb-4">Top Pages</h4>
        <div className="space-y-3">
          {analytics.topPages.map((page, index) => (
            <div key={page.page} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center text-xs font-medium text-blue-600">
                  {index + 1}
                </div>
                <span className="font-medium text-gray-900">{page.page}</span>
              </div>
              <div className="text-sm text-gray-600">{page.views.toLocaleString()} views</div>
            </div>
          ))}
        </div>
      </div>

      {/* User Interactions */}
      <div className="mb-8">
        <h4 className="font-medium text-gray-900 mb-4">User Interactions</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {analytics.userInteractions.map((interaction) => (
            <div key={interaction.action} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
              <span className="font-medium text-gray-900">{interaction.action}</span>
              <div className="flex items-center space-x-2">
                <div className="w-16 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full"
                    style={{ width: `${(interaction.count / Math.max(...analytics.userInteractions.map(i => i.count))) * 100}%` }}
                  ></div>
                </div>
                <span className="text-sm text-gray-600">{interaction.count.toLocaleString()}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Device Types */}
      <div className="mb-8">
        <h4 className="font-medium text-gray-900 mb-4">Device Types</h4>
        <div className="space-y-3">
          {analytics.deviceTypes.map((device) => (
            <div key={device.device} className="flex items-center justify-between">
              <span className="text-gray-700">{device.device}</span>
              <div className="flex items-center space-x-3">
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full"
                    style={{ width: `${device.percentage}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium text-gray-900 w-12 text-right">
                  {formatPercentage(device.percentage)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Time of Day Activity */}
      {showCharts && (
        <div className="mb-8">
          <h4 className="font-medium text-gray-900 mb-4">Activity by Hour</h4>
          <div className="h-32 flex items-end space-x-1">
            {analytics.timeOfDay.map((hour) => (
              <div key={hour.hour} className="flex-1 flex flex-col items-center">
                <div 
                  className="w-full bg-blue-500 rounded-t"
                  style={{ height: `${(hour.sessions / Math.max(...analytics.timeOfDay.map(h => h.sessions))) * 100}%` }}
                ></div>
                <span className="text-xs text-gray-500 mt-1">{hour.hour}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Performance Integration */}
      <div className="border-t pt-6">
        <h4 className="font-medium text-gray-900 mb-4">Performance Metrics</h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-lg font-bold text-gray-900">
              {performanceMonitor.getEvents('error').length}
            </div>
            <div className="text-sm text-gray-600">Errors</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-gray-900">
              {performanceMonitor.getEvents('api').length}
            </div>
            <div className="text-sm text-gray-600">API Calls</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-gray-900">
              {performanceMonitor.getEvents('component').length}
            </div>
            <div className="text-sm text-gray-600">Components</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-gray-900">
              {performanceMonitor.getEvents('navigation').length}
            </div>
            <div className="text-sm text-gray-600">Navigations</div>
          </div>
        </div>
      </div>

      {/* Insights */}
      <div className="mt-6 p-4 bg-yellow-50 rounded-lg">
        <h4 className="font-medium text-yellow-900 mb-2">Key Insights</h4>
        <ul className="text-sm text-yellow-800 space-y-1">
          <li>• Most users access the app on mobile devices (65%)</li>
          <li>• Search is the most common user interaction</li>
          <li>• Peak usage occurs during lunch and dinner hours</li>
          <li>• Specials page has high engagement</li>
        </ul>
      </div>
    </div>
  );
} 