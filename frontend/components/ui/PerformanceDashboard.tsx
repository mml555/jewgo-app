'use client';

import React, { useState, useEffect } from 'react';
import { performanceMonitor, PerformanceMetrics } from '@/lib/analytics/performance';
import { safeFilter } from '@/utils/validation';

interface PerformanceDashboardProps {
  className?: string;
  showDetails?: boolean;
}

export default function PerformanceDashboard({ className = '', showDetails = false }: PerformanceDashboardProps) {
  const [metrics, setMetrics] = useState<PerformanceMetrics>({});
  const [events, setEvents] = useState<any[]>([]);
  const [isExpanded, setIsExpanded] = useState(showDetails);

  useEffect(() => {
    const updateMetrics = () => {
      setMetrics(performanceMonitor.getMetrics());
      setEvents(performanceMonitor.getEvents());
    };

    // Update metrics immediately
    updateMetrics();

    // Update metrics every 5 seconds
    const interval = setInterval(updateMetrics, 5000);

    return () => clearInterval(interval);
  }, []);

  const getScoreColor = (score: number, thresholds: { good: number; needsImprovement: number }) => {
    if (score <= thresholds.good) return 'text-green-600 bg-green-100';
    if (score <= thresholds.needsImprovement) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getScoreLabel = (score: number, thresholds: { good: number; needsImprovement: number }) => {
    if (score <= thresholds.good) return 'Good';
    if (score <= thresholds.needsImprovement) return 'Needs Improvement';
    return 'Poor';
  };

  const formatTime = (ms: number) => {
    if (ms < 1000) return `${Math.round(ms)}ms`;
    return `${(ms / 1000).toFixed(2)}s`;
  };

  const clearData = () => {
    performanceMonitor.clearEvents();
    setMetrics({});
    setEvents([]);
  };

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Performance Dashboard</h3>
          <p className="text-sm text-gray-600">Core Web Vitals & Performance Metrics</p>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="px-3 py-1 text-sm border border-gray-300 rounded hover:bg-gray-50 transition-colors"
          >
            {isExpanded ? 'Hide Details' : 'Show Details'}
          </button>
          <button
            onClick={clearData}
            className="px-3 py-1 text-sm border border-red-300 text-red-600 rounded hover:bg-red-50 transition-colors"
          >
            Clear Data
          </button>
        </div>
      </div>

      {/* Core Web Vitals */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {/* LCP */}
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <h4 className="font-medium text-gray-900">LCP</h4>
            <span className="text-xs text-gray-500">Largest Contentful Paint</span>
          </div>
          {metrics.lcp ? (
            <div className="space-y-2">
              <div className="text-2xl font-bold text-gray-900">
                {formatTime(metrics.lcp)}
              </div>
              <div className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                getScoreColor(metrics.lcp, { good: 2500, needsImprovement: 4000 })
              }`}>
                {getScoreLabel(metrics.lcp, { good: 2500, needsImprovement: 4000 })}
              </div>
            </div>
          ) : (
            <div className="text-gray-400">No data</div>
          )}
        </div>

        {/* FID */}
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <h4 className="font-medium text-gray-900">FID</h4>
            <span className="text-xs text-gray-500">First Input Delay</span>
          </div>
          {metrics.fid ? (
            <div className="space-y-2">
              <div className="text-2xl font-bold text-gray-900">
                {formatTime(metrics.fid)}
              </div>
              <div className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                getScoreColor(metrics.fid, { good: 100, needsImprovement: 300 })
              }`}>
                {getScoreLabel(metrics.fid, { good: 100, needsImprovement: 300 })}
              </div>
            </div>
          ) : (
            <div className="text-gray-400">No data</div>
          )}
        </div>

        {/* CLS */}
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <h4 className="font-medium text-gray-900">CLS</h4>
            <span className="text-xs text-gray-500">Cumulative Layout Shift</span>
          </div>
          {metrics.cls ? (
            <div className="space-y-2">
              <div className="text-2xl font-bold text-gray-900">
                {metrics.cls.toFixed(3)}
              </div>
              <div className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                getScoreColor(metrics.cls, { good: 0.1, needsImprovement: 0.25 })
              }`}>
                {getScoreLabel(metrics.cls, { good: 0.1, needsImprovement: 0.25 })}
              </div>
            </div>
          ) : (
            <div className="text-gray-400">No data</div>
          )}
        </div>
      </div>

      {/* Additional Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="text-center">
          <div className="text-2xl font-bold text-gray-900">
            {metrics.apiResponseTime ? formatTime(metrics.apiResponseTime) : 'N/A'}
          </div>
          <div className="text-sm text-gray-600">Avg API Response</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-gray-900">
            {metrics.errorCount || 0}
          </div>
          <div className="text-sm text-gray-600">Errors</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-600">{safeFilter(events, (e: any) => e.category === 'navigation').length}</div>
          <div className="text-sm text-gray-600">Navigation Events</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-green-600">{safeFilter(events, (e: any) => e.category === 'component').length}</div>
          <div className="text-sm text-gray-600">Component Events</div>
        </div>
      </div>

      {/* Detailed Events */}
      {isExpanded && (
        <div className="border-t pt-6">
          <h4 className="font-medium text-gray-900 mb-4">Recent Events</h4>
          <div className="max-h-64 overflow-y-auto">
            {events.length > 0 ? (
              <div className="space-y-2">
                {events.slice(-10).reverse().map((event, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className={`w-2 h-2 rounded-full ${
                        event.category === 'error' ? 'bg-red-500' :
                        event.category === 'navigation' ? 'bg-blue-500' :
                        event.category === 'api' ? 'bg-green-500' :
                        'bg-gray-500'
                      }`} />
                      <div>
                        <div className="font-medium text-gray-900">{event.name}</div>
                        <div className="text-sm text-gray-600">{event.category}</div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-gray-900">
                        {event.value > 0 ? formatTime(event.value) : '-'}
                      </div>
                      <div className="text-xs text-gray-500">
                        {new Date(event.timestamp).toLocaleTimeString()}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center text-gray-500 py-8">
                No performance events recorded yet
              </div>
            )}
          </div>
        </div>
      )}

      {/* Performance Tips */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h4 className="font-medium text-blue-900 mb-2">Performance Tips</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• LCP should be under 2.5 seconds for good performance</li>
          <li>• FID should be under 100ms for responsive interactions</li>
          <li>• CLS should be under 0.1 for stable layouts</li>
          <li>• Monitor API response times and optimize slow endpoints</li>
        </ul>
      </div>
    </div>
  );
} 