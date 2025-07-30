// Performance monitoring and analytics system

interface PerformanceMetrics {
  // Core Web Vitals
  lcp?: number; // Largest Contentful Paint
  fid?: number; // First Input Delay
  cls?: number; // Cumulative Layout Shift
  ttfb?: number; // Time to First Byte
  fcp?: number; // First Contentful Paint
  
  // Custom metrics
  pageLoadTime?: number;
  apiResponseTime?: number;
  componentRenderTime?: number;
  errorCount?: number;
  userInteractions?: number;
}

interface PerformanceEvent {
  name: string;
  value: number;
  category: 'navigation' | 'paint' | 'layout' | 'api' | 'component' | 'error';
  timestamp: number;
  metadata?: Record<string, any>;
}

class PerformanceMonitor {
  private events: PerformanceEvent[] = [];
  private observers: Map<string, PerformanceObserver> = new Map();
  private isInitialized = false;

  constructor() {
    if (typeof window !== 'undefined') {
      this.initialize();
    }
  }

  private initialize() {
    if (this.isInitialized) return;
    
    this.setupCoreWebVitals();
    this.setupCustomMetrics();
    this.setupErrorTracking();
    
    this.isInitialized = true;
  }

  private setupCoreWebVitals() {
    // Largest Contentful Paint
    if ('PerformanceObserver' in window) {
      try {
        const lcpObserver = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lastEntry = entries[entries.length - 1];
          this.recordEvent('LCP', lastEntry.startTime, 'paint', {
            element: lastEntry.element?.tagName,
            url: lastEntry.url
          });
        });
        lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
        this.observers.set('lcp', lcpObserver);
      } catch (error) {
        console.warn('LCP observer failed:', error);
      }

      // First Input Delay
      try {
        const fidObserver = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          entries.forEach(entry => {
            this.recordEvent('FID', entry.processingStart - entry.startTime, 'navigation', {
              name: entry.name,
              type: entry.entryType
            });
          });
        });
        fidObserver.observe({ entryTypes: ['first-input'] });
        this.observers.set('fid', fidObserver);
      } catch (error) {
        console.warn('FID observer failed:', error);
      }

      // Cumulative Layout Shift
      try {
        const clsObserver = new PerformanceObserver((list) => {
          let clsValue = 0;
          const entries = list.getEntries();
          entries.forEach(entry => {
            if (!entry.hadRecentInput) {
              clsValue += (entry as any).value;
            }
          });
          this.recordEvent('CLS', clsValue, 'layout');
        });
        clsObserver.observe({ entryTypes: ['layout-shift'] });
        this.observers.set('cls', clsObserver);
      } catch (error) {
        console.warn('CLS observer failed:', error);
      }
    }
  }

  private setupCustomMetrics() {
    // Page load time
    if (typeof window !== 'undefined') {
      window.addEventListener('load', () => {
        const loadTime = performance.now();
        this.recordEvent('PageLoad', loadTime, 'navigation');
      });

      // Navigation timing
      if ('performance' in window && 'getEntriesByType' in performance) {
        const navigationEntries = performance.getEntriesByType('navigation');
        if (navigationEntries.length > 0) {
          const navEntry = navigationEntries[0] as PerformanceNavigationTiming;
          this.recordEvent('TTFB', navEntry.responseStart - navEntry.requestStart, 'navigation');
          this.recordEvent('DOMContentLoaded', navEntry.domContentLoadedEventEnd - navEntry.domContentLoadedEventStart, 'navigation');
        }
      }
    }
  }

  private setupErrorTracking() {
    if (typeof window !== 'undefined') {
      // JavaScript errors
      window.addEventListener('error', (event) => {
        this.recordEvent('JavaScriptError', 0, 'error', {
          message: event.message,
          filename: event.filename,
          lineno: event.lineno,
          colno: event.colno
        });
      });

      // Promise rejections
      window.addEventListener('unhandledrejection', (event) => {
        this.recordEvent('UnhandledRejection', 0, 'error', {
          reason: event.reason?.toString()
        });
      });
    }
  }

  recordEvent(name: string, value: number, category: PerformanceEvent['category'], metadata?: Record<string, any>) {
    const event: PerformanceEvent = {
      name,
      value,
      category,
      timestamp: Date.now(),
      metadata
    };

    this.events.push(event);
    this.sendToAnalytics(event);
  }

  measureComponentRender(componentName: string, renderFn: () => void) {
    const startTime = performance.now();
    renderFn();
    const endTime = performance.now();
    
    this.recordEvent('ComponentRender', endTime - startTime, 'component', {
      component: componentName
    });
  }

  measureApiCall(apiName: string, apiCall: () => Promise<any>) {
    const startTime = performance.now();
    return apiCall().finally(() => {
      const endTime = performance.now();
      this.recordEvent('ApiCall', endTime - startTime, 'api', {
        api: apiName
      });
    });
  }

  trackUserInteraction(interactionName: string, metadata?: Record<string, any>) {
    this.recordEvent('UserInteraction', 0, 'navigation', {
      interaction: interactionName,
      ...metadata
    });
  }

  private sendToAnalytics(event: PerformanceEvent) {
    // Send to your analytics service (Google Analytics, Mixpanel, etc.)
    if (typeof window !== 'undefined' && (window as any).gtag) {
      (window as any).gtag('event', 'performance', {
        event_category: event.category,
        event_label: event.name,
        value: Math.round(event.value),
        custom_parameters: event.metadata
      });
    }

    // Log to console in development
    if (process.env.NODE_ENV === 'development') {
      console.log('Performance Event:', event);
    }

    // Store locally for debugging
    this.storeLocally(event);
  }

  private storeLocally(event: PerformanceEvent) {
    try {
      const stored = localStorage.getItem('jewgo_performance_events');
      const events = stored ? JSON.parse(stored) : [];
      events.push(event);
      
      // Keep only last 100 events
      if (events.length > 100) {
        events.splice(0, events.length - 100);
      }
      
      localStorage.setItem('jewgo_performance_events', JSON.stringify(events));
    } catch (error) {
      console.warn('Failed to store performance event locally:', error);
    }
  }

  getMetrics(): PerformanceMetrics {
    const metrics: PerformanceMetrics = {};
    
    // Calculate averages from events
    const lcpEvents = this.events.filter(e => e.name === 'LCP');
    const fidEvents = this.events.filter(e => e.name === 'FID');
    const clsEvents = this.events.filter(e => e.name === 'CLS');
    const apiEvents = this.events.filter(e => e.name === 'ApiCall');
    const errorEvents = this.events.filter(e => e.category === 'error');

    if (lcpEvents.length > 0) {
      metrics.lcp = lcpEvents[lcpEvents.length - 1].value; // Use latest LCP
    }
    if (fidEvents.length > 0) {
      metrics.fid = Math.min(...fidEvents.map(e => e.value)); // Use best FID
    }
    if (clsEvents.length > 0) {
      metrics.cls = clsEvents[clsEvents.length - 1].value; // Use latest CLS
    }
    if (apiEvents.length > 0) {
      metrics.apiResponseTime = apiEvents.reduce((sum, e) => sum + e.value, 0) / apiEvents.length;
    }
    metrics.errorCount = errorEvents.length;

    return metrics;
  }

  getEvents(category?: string): PerformanceEvent[] {
    if (category) {
      return this.events.filter(e => e.category === category);
    }
    return [...this.events];
  }

  clearEvents() {
    this.events = [];
    localStorage.removeItem('jewgo_performance_events');
  }

  disconnect() {
    this.observers.forEach(observer => observer.disconnect());
    this.observers.clear();
  }
}

// Singleton instance
export const performanceMonitor = new PerformanceMonitor();

// Utility functions
export const measureRender = (componentName: string) => {
  return (renderFn: () => void) => {
    performanceMonitor.measureComponentRender(componentName, renderFn);
  };
};

export const measureApi = (apiName: string) => {
  return <T>(apiCall: () => Promise<T>): Promise<T> => {
    return performanceMonitor.measureApiCall(apiName, apiCall);
  };
};

export const trackInteraction = (interactionName: string, metadata?: Record<string, any>) => {
  performanceMonitor.trackUserInteraction(interactionName, metadata);
};

// React hook for measuring component performance
export const usePerformanceTracking = (componentName: string) => {
  const trackRender = () => {
    performanceMonitor.recordEvent('ComponentRender', 0, 'component', {
      component: componentName,
      timestamp: Date.now()
    });
  };

  return { trackRender };
}; 