'use client';

export default function SimpleMapPage() {
  return (
    <div className="min-h-screen bg-white">
      <div className="relative h-[calc(100vh-120px)]">
        <div className="w-full h-full bg-gradient-to-br from-blue-100 to-green-100 flex items-center justify-center">
          <div className="text-center">
            <div className="text-6xl mb-4">🗺️</div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Simple Map Test</h2>
            <p className="text-gray-600 mb-4">This is a simple map test page</p>
            <div className="bg-white rounded-lg p-4 shadow-lg max-w-md mx-auto">
              <p className="text-sm text-gray-500">
                If you can see this, the page is working correctly.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 