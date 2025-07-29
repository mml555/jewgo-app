'use client';

import { useState, useEffect } from 'react';

export default function TestPage() {
  const [testData, setTestData] = useState([
    {
      id: 1,
      name: "Test Restaurant 1",
      address: "123 Test St",
      city: "Test City",
      kosher_category: "dairy",
      short_description: "Test description 1"
    },
    {
      id: 2,
      name: "Test Restaurant 2",
      address: "456 Test Ave",
      city: "Test City",
      kosher_category: "meat",
      short_description: "Test description 2"
    }
  ]);

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    console.log('Test page loaded');
    console.log('Test data:', testData);
  }, [testData]);

  return (
    <div className="min-h-screen bg-white p-4">
      <h1 className="text-2xl font-bold mb-4">Test Page</h1>
      
      <div className="mb-4">
        <p>Loading state: {loading ? 'Loading...' : 'Not loading'}</p>
        <p>Test data count: {testData.length}</p>
      </div>

      <div className="space-y-4">
        {testData.map((restaurant) => (
          <div key={restaurant.id} className="border p-4 rounded-lg">
            <h2 className="text-lg font-semibold">{restaurant.name}</h2>
            <p className="text-gray-600">{restaurant.address}, {restaurant.city}</p>
            <p className="text-sm text-blue-600">Kosher: {restaurant.kosher_category}</p>
            <p className="text-sm text-gray-500">{restaurant.short_description}</p>
          </div>
        ))}
      </div>

      <button 
        onClick={() => setLoading(!loading)}
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
      >
        Toggle Loading
      </button>
    </div>
  );
} 