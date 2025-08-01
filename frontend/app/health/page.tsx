import { Suspense } from 'react'
import RefreshButton from '@/components/ui/RefreshButton'

// Force dynamic rendering to prevent static generation timeout
export const dynamic = 'force-dynamic'
export const revalidate = 0

interface HealthStatus {
  frontend: 'healthy' | 'degraded' | 'down'
  backend: 'healthy' | 'degraded' | 'down' | 'unknown'
  database: 'healthy' | 'degraded' | 'down' | 'unknown'
  timestamp: string
  version: string
  commit: string
}

async function getHealthStatus(): Promise<HealthStatus> {
  try {
    // Skip health check during static generation
    if (process.env.NODE_ENV === 'production' && typeof window === 'undefined') {
      return {
        frontend: 'healthy',
        backend: 'unknown',
        database: 'unknown',
        timestamp: new Date().toISOString(),
        version: '1.0.0',
        commit: process.env.VERCEL_GIT_COMMIT_SHA || 'unknown'
      };
    }

    const backendResponse = await fetch('https://jewgo.onrender.com/health', {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      cache: 'no-store' // Disable caching for real-time health checks
    })

    if (backendResponse.ok) {
      const backendData = await backendResponse.json()
      return {
        frontend: 'healthy',
        backend: backendData.status === 'healthy' ? 'healthy' : 'degraded',
        database: backendData.database === 'connected' ? 'healthy' : 'degraded',
        timestamp: new Date().toISOString(),
        version: '1.0.0',
        commit: process.env.VERCEL_GIT_COMMIT_SHA || 'unknown'
      }
    } else {
      return {
        frontend: 'healthy',
        backend: 'degraded',
        database: 'unknown',
        timestamp: new Date().toISOString(),
        version: '1.0.0',
        commit: process.env.VERCEL_GIT_COMMIT_SHA || 'unknown'
      }
    }
  } catch (error) {
    return {
      frontend: 'healthy',
      backend: 'down',
      database: 'unknown',
      timestamp: new Date().toISOString(),
      version: '1.0.0',
      commit: process.env.VERCEL_GIT_COMMIT_SHA || 'unknown'
    }
  }
}

function StatusIndicator({ status }: { status: string }) {
  const colors = {
    healthy: 'bg-green-500',
    degraded: 'bg-yellow-500',
    down: 'bg-red-500',
    unknown: 'bg-gray-500'
  }
  
  return (
    <div className="flex items-center space-x-2">
      <div className={`w-3 h-3 rounded-full ${colors[status as keyof typeof colors]}`}></div>
      <span className="capitalize font-medium">{status}</span>
    </div>
  )
}

export default function HealthPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-gray-900">🏥 JewGo System Health</h1>
            <RefreshButton />
          </div>
          
          <Suspense fallback={<div className="text-center py-8">Loading system status...</div>}>
            <HealthStatusDisplay />
          </Suspense>
          
          <div className="mt-8 p-4 bg-gray-50 rounded-lg">
            <h2 className="text-lg font-semibold mb-3">System Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <strong>Environment:</strong> {process.env.NODE_ENV || 'development'}
              </div>
              <div>
                <strong>Build Time:</strong> {new Date().toLocaleString()}
              </div>
              <div>
                <strong>Frontend URL:</strong> https://jewgo-app.vercel.app
              </div>
              <div>
                <strong>Backend URL:</strong> https://jewgo.onrender.com
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

async function HealthStatusDisplay() {
  const status = await getHealthStatus()
  
  const overallStatus = status.backend === 'down' ? 'down' : 
                       status.backend === 'degraded' ? 'degraded' : 'healthy'
  
  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-semibold mb-2">Overall Status</h2>
        <StatusIndicator status={overallStatus} />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 border rounded-lg">
          <h3 className="font-semibold mb-2">Frontend</h3>
          <StatusIndicator status={status.frontend} />
        </div>
        <div className="p-4 border rounded-lg">
          <h3 className="font-semibold mb-2">Backend API</h3>
          <StatusIndicator status={status.backend} />
        </div>
        <div className="p-4 border rounded-lg">
          <h3 className="font-semibold mb-2">Database</h3>
          <StatusIndicator status={status.database} />
        </div>
      </div>
      
      <div className="text-sm text-gray-600">
        <p><strong>Last Updated:</strong> {new Date(status.timestamp).toLocaleString()}</p>
        <p><strong>Version:</strong> {status.version}</p>
        <p><strong>Commit:</strong> {status.commit.substring(0, 8)}</p>
      </div>
    </div>
  )
} 