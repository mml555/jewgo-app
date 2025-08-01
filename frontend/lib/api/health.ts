const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL 
  ? process.env.NEXT_PUBLIC_BACKEND_URL
  : process.env.NODE_ENV === 'production'
  ? 'https://jewgo.onrender.com'
  : 'http://127.0.0.1:8081';

interface HealthCheckResponse {
  status: string;
  database: string;
  restaurants_count?: number;
  version?: string;
  error?: string;
}

interface HealthCheckResult {
  isHealthy: boolean;
  response?: HealthCheckResponse;
  error?: string;
  responseTime: number;
}

export class HealthAPI {
  static async checkHealth(timeout: number = 10000): Promise<HealthCheckResult> {
    const startTime = Date.now();
    
    try {
      // Create AbortController for timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeout);
      
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      const responseTime = Date.now() - startTime;
      
      if (!response.ok) {
        return {
          isHealthy: false,
          error: `HTTP ${response.status}: ${response.statusText}`,
          responseTime
        };
      }
      
      const data: HealthCheckResponse = await response.json();
      
      return {
        isHealthy: data.status === 'healthy',
        response: data,
        responseTime
      };
      
    } catch (error) {
      const responseTime = Date.now() - startTime;
      
      if (error instanceof Error && error.name === 'AbortError') {
        return {
          isHealthy: false,
          error: `Request timed out after ${timeout}ms - backend server may be down or overloaded`,
          responseTime
        };
      }
      
      return {
        isHealthy: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        responseTime
      };
    }
  }
  
  static async checkApiEndpoints(): Promise<{
    health: HealthCheckResult;
    restaurants: { success: boolean; error?: string; responseTime: number };
  }> {
    const health = await this.checkHealth();
    
    // Test restaurants endpoint
    const restaurantsStartTime = Date.now();
    let restaurantsSuccess = false;
    let restaurantsError: string | undefined;
    
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 15000);
      
      const response = await fetch(`${API_BASE_URL}/api/restaurants?limit=1`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (response.ok) {
        const data = await response.json();
        restaurantsSuccess = data && (Array.isArray(data) || (data.restaurants && Array.isArray(data.restaurants)));
      } else {
        restaurantsError = `HTTP ${response.status}: ${response.statusText}`;
      }
    } catch (error) {
      if (error instanceof Error && error.name === 'AbortError') {
        restaurantsError = 'Request timed out';
      } else {
        restaurantsError = error instanceof Error ? error.message : 'Unknown error';
      }
    }
    
    const restaurantsResponseTime = Date.now() - restaurantsStartTime;
    
    return {
      health,
      restaurants: {
        success: restaurantsSuccess,
        error: restaurantsError,
        responseTime: restaurantsResponseTime
      }
    };
  }
}

export const checkHealth = () => HealthAPI.checkHealth();
export const checkApiEndpoints = () => HealthAPI.checkApiEndpoints(); 