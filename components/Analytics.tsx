'use client';

import React, { useEffect, useState } from 'react';

interface AnalyticsEvent {
  event: string;
  properties?: Record<string, any>;
  timestamp: number;
}

interface AnalyticsProps {
  userId?: string;
  sessionId?: string;
  pageName?: string;
}

export default function Analytics({ userId, sessionId, pageName }: AnalyticsProps) {
  const [events, setEvents] = useState<AnalyticsEvent[]>([]);
  const [isInitialized, setIsInitialized] = useState(false);

  // Initialize analytics
  useEffect(() => {
    if (typeof window !== 'undefined' && !isInitialized) {
      initializeAnalytics();
      setIsInitialized(true);
    }
  }, [isInitialized]);

  const initializeAnalytics = () => {
    // Initialize Google Analytics if available
    if (typeof window !== 'undefined' && window.gtag) {
      window.gtag('config', process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID || '', {
        page_title: pageName || document.title,
        page_location: window.location.href,
        user_id: userId,
        session_id: sessionId,
      });
    }

    // Track page view
    trackEvent('page_view', {
      page_name: pageName || document.title,
      page_url: window.location.href,
      referrer: document.referrer,
    });

    // Track user engagement metrics
    trackUserEngagement();
  };

  const trackEvent = (eventName: string, properties?: Record<string, any>) => {
    const event: AnalyticsEvent = {
      event: eventName,
      properties: {
        ...properties,
        user_id: userId,
        session_id: sessionId,
        timestamp: Date.now(),
        user_agent: navigator.userAgent,
        screen_resolution: `${screen.width}x${screen.height}`,
        viewport_size: `${window.innerWidth}x${window.innerHeight}`,
      },
      timestamp: Date.now(),
    };

    // Add to local events array
    setEvents(prev => [...prev, event]);

    // Send to Google Analytics
    if (typeof window !== 'undefined' && window.gtag) {
      window.gtag('event', eventName, {
        ...properties,
        user_id: userId,
        session_id: sessionId,
      });
    }

    // Send to custom analytics endpoint
    sendToAnalyticsEndpoint(event);

    console.log('Analytics Event:', event);
  };

  const sendToAnalyticsEndpoint = async (event: AnalyticsEvent) => {
    try {
      const response = await fetch('/api/analytics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(event),
      });

      if (!response.ok) {
        console.warn('Failed to send analytics event:', response.status);
      }
    } catch (error) {
      console.warn('Error sending analytics event:', error);
    }
  };

  const trackUserEngagement = () => {
    let startTime = Date.now();
    let isActive = true;

    // Track time on page
    const trackTimeOnPage = () => {
      if (isActive) {
        const timeOnPage = Date.now() - startTime;
        trackEvent('time_on_page', {
          time_on_page_ms: timeOnPage,
          time_on_page_seconds: Math.round(timeOnPage / 1000),
        });
      }
    };

    // Track scroll depth
    let maxScrollDepth = 0;
    const trackScrollDepth = () => {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrollPercentage = Math.round((scrollTop / scrollHeight) * 100);
      
      if (scrollPercentage > maxScrollDepth) {
        maxScrollDepth = scrollPercentage;
        
        // Track scroll milestones
        if (scrollPercentage >= 25 && maxScrollDepth < 50) {
          trackEvent('scroll_depth', { depth: 25 });
        } else if (scrollPercentage >= 50 && maxScrollDepth < 75) {
          trackEvent('scroll_depth', { depth: 50 });
        } else if (scrollPercentage >= 75 && maxScrollDepth < 100) {
          trackEvent('scroll_depth', { depth: 75 });
        } else if (scrollPercentage >= 100) {
          trackEvent('scroll_depth', { depth: 100 });
        }
      }
    };

    // Track visibility changes
    const handleVisibilityChange = () => {
      if (document.hidden) {
        isActive = false;
        trackTimeOnPage();
      } else {
        isActive = true;
        startTime = Date.now();
      }
    };

    // Track before unload
    const handleBeforeUnload = () => {
      isActive = false;
      trackTimeOnPage();
    };

    // Add event listeners
    window.addEventListener('scroll', trackScrollDepth, { passive: true });
    document.addEventListener('visibilitychange', handleVisibilityChange);
    window.addEventListener('beforeunload', handleBeforeUnload);

    // Cleanup function
    return () => {
      window.removeEventListener('scroll', trackScrollDepth);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  };

  // Expose tracking function globally for other components
  useEffect(() => {
    if (typeof window !== 'undefined') {
      (window as any).trackAnalyticsEvent = trackEvent;
    }

    return () => {
      if (typeof window !== 'undefined') {
        delete (window as any).trackAnalyticsEvent;
      }
    };
  }, [userId, sessionId]);

  // Track specific user interactions
  const trackRestaurantView = (restaurantId: number, restaurantName: string) => {
    trackEvent('restaurant_view', {
      restaurant_id: restaurantId,
      restaurant_name: restaurantName,
    });
  };

  const trackSearch = (query: string, resultsCount: number) => {
    trackEvent('search', {
      query,
      results_count: resultsCount,
      search_type: 'text',
    });
  };

  const trackFilter = (filterType: string, filterValue: string) => {
    trackEvent('filter_applied', {
      filter_type: filterType,
      filter_value: filterValue,
    });
  };

  const trackMapInteraction = (interactionType: string, properties?: Record<string, any>) => {
    trackEvent('map_interaction', {
      interaction_type: interactionType,
      ...properties,
    });
  };

  const trackAddToFavorites = (restaurantId: number, restaurantName: string) => {
    trackEvent('add_to_favorites', {
      restaurant_id: restaurantId,
      restaurant_name: restaurantName,
    });
  };

  const trackShare = (restaurantId: number, shareMethod: string) => {
    trackEvent('share_restaurant', {
      restaurant_id: restaurantId,
      share_method: shareMethod,
    });
  };

  const trackPhoneCall = (restaurantId: number, restaurantName: string) => {
    trackEvent('phone_call', {
      restaurant_id: restaurantId,
      restaurant_name: restaurantName,
    });
  };

  const trackWebsiteVisit = (restaurantId: number, restaurantName: string) => {
    trackEvent('website_visit', {
      restaurant_id: restaurantId,
      restaurant_name: restaurantName,
    });
  };

  const trackDirections = (restaurantId: number, restaurantName: string) => {
    trackEvent('get_directions', {
      restaurant_id: restaurantId,
      restaurant_name: restaurantName,
    });
  };

  // Performance tracking
  const trackPerformance = (metric: string, value: number) => {
    trackEvent('performance_metric', {
      metric,
      value,
      unit: 'milliseconds',
    });
  };

  // Error tracking
  const trackError = (error: Error, context?: Record<string, any>) => {
    trackEvent('error', {
      error_message: error.message,
      error_stack: error.stack,
      error_name: error.name,
      ...context,
    });
  };

  // Expose tracking functions
  useEffect(() => {
    if (typeof window !== 'undefined') {
      (window as any).analytics = {
        trackRestaurantView,
        trackSearch,
        trackFilter,
        trackMapInteraction,
        trackAddToFavorites,
        trackShare,
        trackPhoneCall,
        trackWebsiteVisit,
        trackDirections,
        trackPerformance,
        trackError,
      };
    }

    return () => {
      if (typeof window !== 'undefined') {
        delete (window as any).analytics;
      }
    };
  }, []);

  // Track page performance metrics
  useEffect(() => {
    if (typeof window !== 'undefined' && 'performance' in window) {
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (entry.entryType === 'navigation') {
            const navEntry = entry as PerformanceNavigationTiming;
            trackPerformance('page_load_time', navEntry.loadEventEnd - navEntry.loadEventStart);
            trackPerformance('dom_content_loaded', navEntry.domContentLoadedEventEnd - navEntry.domContentLoadedEventStart);
            trackPerformance('first_paint', navEntry.responseStart - navEntry.fetchStart);
          }
        }
      });

      observer.observe({ entryTypes: ['navigation'] });

      return () => observer.disconnect();
    }
  }, []);

  // Track Core Web Vitals
  useEffect(() => {
    if (typeof window !== 'undefined' && 'performance' in window) {
      import('web-vitals').then((webVitals) => {
        webVitals.onCLS((metric) => trackPerformance('CLS', metric.value));
        webVitals.onINP((metric) => trackPerformance('INP', metric.value));
        webVitals.onFCP((metric) => trackPerformance('FCP', metric.value));
        webVitals.onLCP((metric) => trackPerformance('LCP', metric.value));
        webVitals.onTTFB((metric) => trackPerformance('TTFB', metric.value));
      }).catch((error) => {
        console.warn('Failed to load web-vitals:', error);
      });
    }
  }, []);

  // Error boundary tracking
  useEffect(() => {
    const handleError = (event: ErrorEvent) => {
      trackError(event.error, {
        error_type: 'javascript_error',
        error_filename: event.filename,
        error_lineno: event.lineno,
        error_colno: event.colno,
      });
    };

    const handleUnhandledRejection = (event: PromiseRejectionEvent) => {
      trackError(new Error(event.reason), {
        error_type: 'unhandled_promise_rejection',
      });
    };

    window.addEventListener('error', handleError);
    window.addEventListener('unhandledrejection', handleUnhandledRejection);

    return () => {
      window.removeEventListener('error', handleError);
      window.removeEventListener('unhandledrejection', handleUnhandledRejection);
    };
  }, []);

  // Return null since this is a utility component
  return null;
}

// Global type declarations
declare global {
  interface Window {
    gtag?: (...args: any[]) => void;
    trackAnalyticsEvent?: (eventName: string, properties?: Record<string, any>) => void;
    analytics?: {
      trackRestaurantView: (restaurantId: number, restaurantName: string) => void;
      trackSearch: (query: string, resultsCount: number) => void;
      trackFilter: (filterType: string, filterValue: string) => void;
      trackMapInteraction: (interactionType: string, properties?: Record<string, any>) => void;
      trackAddToFavorites: (restaurantId: number, restaurantName: string) => void;
      trackShare: (restaurantId: number, shareMethod: string) => void;
      trackPhoneCall: (restaurantId: number, restaurantName: string) => void;
      trackWebsiteVisit: (restaurantId: number, restaurantName: string) => void;
      trackDirections: (restaurantId: number, restaurantName: string) => void;
      trackPerformance: (metric: string, value: number) => void;
      trackError: (error: Error, context?: Record<string, any>) => void;
    };
  }
} 