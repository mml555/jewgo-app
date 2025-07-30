'use client';

import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error?: Error;
  errorInfo?: ErrorInfo;
}

export default class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    
    this.setState({
      error,
      errorInfo
    });

    // Call the onError callback if provided
    this.props.onError?.(error, errorInfo);

    // Log to external service (e.g., Sentry) in production
    if (process.env.NODE_ENV === 'production') {
      // Add your error reporting service here
      // Example: Sentry.captureException(error, { extra: errorInfo });
    }
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined });
  };

  handleReportError = () => {
    const { error, errorInfo } = this.state;
    if (error) {
      // Create error report
      const errorReport = {
        message: error.message,
        stack: error.stack,
        componentStack: errorInfo?.componentStack,
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent,
        url: window.location.href
      };

      // In a real app, send this to your error reporting service
      console.log('Error Report:', errorReport);
      
      // For now, just show a toast
      if (typeof window !== 'undefined' && (window as any).showToast) {
        (window as any).showToast('Error report sent. Thank you!', 'info');
      }
    }
  };

  render() {
    if (this.state.hasError) {
      // Custom fallback UI
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // Default error UI
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
          <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-6 text-center">
            {/* Error Icon */}
            <div className="mx-auto w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mb-4">
              <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>

            {/* Error Message */}
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              Something went wrong
            </h2>
            <p className="text-gray-600 mb-6">
              We're sorry, but something unexpected happened. Please try again or contact support if the problem persists.
            </p>

            {/* Error Details (Development Only) */}
            {process.env.NODE_ENV === 'development' && this.state.error && (
              <details className="mb-6 text-left">
                <summary className="cursor-pointer text-sm font-medium text-gray-700 mb-2">
                  Error Details (Development)
                </summary>
                <div className="bg-gray-100 rounded p-3 text-xs font-mono text-gray-800 overflow-auto max-h-32">
                  <div className="mb-2">
                    <strong>Error:</strong> {this.state.error.message}
                  </div>
                  {this.state.error.stack && (
                    <div>
                      <strong>Stack:</strong>
                      <pre className="whitespace-pre-wrap mt-1">{this.state.error.stack}</pre>
                    </div>
                  )}
                  {this.state.errorInfo?.componentStack && (
                    <div className="mt-2">
                      <strong>Component Stack:</strong>
                      <pre className="whitespace-pre-wrap mt-1">{this.state.errorInfo.componentStack}</pre>
                    </div>
                  )}
                </div>
              </details>
            )}

            {/* Action Buttons */}
            <div className="flex space-x-3">
              <button
                onClick={this.handleRetry}
                className="flex-1 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
              >
                Try Again
              </button>
              <button
                onClick={this.handleReportError}
                className="flex-1 bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors"
              >
                Report Error
              </button>
            </div>

            {/* Additional Help */}
            <div className="mt-6 pt-6 border-t border-gray-200">
              <p className="text-sm text-gray-500 mb-3">
                Still having trouble?
              </p>
              <div className="flex justify-center space-x-4">
                <button
                  onClick={() => window.location.href = '/'}
                  className="text-blue-500 hover:text-blue-600 text-sm font-medium"
                >
                  Go Home
                </button>
                <button
                  onClick={() => window.location.reload()}
                  className="text-blue-500 hover:text-blue-600 text-sm font-medium"
                >
                  Refresh Page
                </button>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

// Hook for functional components to handle errors
export function useErrorHandler() {
  const handleError = (error: Error, context?: string) => {
    console.error(`Error in ${context || 'component'}:`, error);
    
    // Log to external service in production
    if (process.env.NODE_ENV === 'production') {
      // Add your error reporting service here
      // Example: Sentry.captureException(error, { tags: { context } });
    }

    // Show user-friendly error message
    if (typeof window !== 'undefined' && (window as any).showToast) {
      (window as any).showToast('Something went wrong. Please try again.', 'error');
    }
  };

  return { handleError };
} 