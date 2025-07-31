'use client'

export default function RefreshButton() {
  return (
    <button 
      onClick={() => window.location.reload()}
      className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
    >
      Refresh Status
    </button>
  )
} 