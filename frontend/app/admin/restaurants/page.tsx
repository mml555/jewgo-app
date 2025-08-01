'use client';

import { useState, useEffect } from 'react';
import Header from '@/components/Header';
import BottomNavigation from '@/components/BottomNavigation';
import { Restaurant } from '@/types/restaurant';
import { safeFilter } from '@/utils/validation';
import { showToast } from '@/components/ui/Toast';

interface PendingRestaurant {
  id: number;
  name: string;
  short_description: string;
  certifying_agency: string;
  kosher_category: string;
  phone: string;
  address: string;
  status: string;
  created_at: string;
  user_type: 'owner' | 'community';
  owner_info?: {
    name: string;
    email: string;
    phone: string;
  };
}

export default function AdminRestaurantsPage() {
  const [pendingRestaurants, setPendingRestaurants] = useState<PendingRestaurant[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedRestaurant, setSelectedRestaurant] = useState<PendingRestaurant | null>(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchPendingRestaurants();
  }, []);

  const fetchPendingRestaurants = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/restaurants?status=pending_approval');
      const data = await response.json();
      
      if (data.success) {
        setPendingRestaurants(data.data || []);
      } else {
        setError('Failed to fetch pending restaurants');
      }
    } catch (error) {
      console.error('Error fetching pending restaurants:', error);
      setError('Failed to fetch pending restaurants');
    } finally {
      setLoading(false);
    }
  };

  const approveRestaurant = (restaurantId: number) => {
    setPendingRestaurants(prev => safeFilter(prev, r => r.id !== restaurantId));
    showToast('Restaurant approved successfully!', 'success');
  };

  const rejectRestaurant = (restaurantId: number) => {
    setPendingRestaurants(prev => safeFilter(prev, r => r.id !== restaurantId));
    showToast('Restaurant rejected', 'info');
  };

  const openRestaurantDetails = (restaurant: PendingRestaurant) => {
    setSelectedRestaurant(restaurant);
    setShowModal(true);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="flex items-center justify-center min-h-screen">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-jewgo-primary"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="px-4 py-6 pb-24">
        <div className="max-w-4xl mx-auto">
          {/* Page Header */}
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-gray-800 mb-2">Restaurant Submissions</h1>
            <p className="text-gray-600">Review and approve pending restaurant submissions</p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-white rounded-lg shadow p-4">
              <div className="text-2xl font-bold text-blue-600">{pendingRestaurants.length}</div>
              <div className="text-sm text-gray-600">Pending Review</div>
            </div>
            <div className="bg-white rounded-lg shadow p-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-jewgo-primary">{safeFilter(pendingRestaurants, (r: PendingRestaurant) => r.user_type === 'owner').length}</div>
                <div className="text-sm text-gray-600">Owner Submissions</div>
              </div>
            </div>
            <div className="bg-white rounded-lg shadow p-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-jewgo-primary">{safeFilter(pendingRestaurants, (r: PendingRestaurant) => r.user_type === 'community').length}</div>
                <div className="text-sm text-gray-600">Community Submissions</div>
              </div>
            </div>
          </div>

          {/* Restaurant List */}
          {pendingRestaurants.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-8 text-center">
              <div className="text-4xl mb-4">🎉</div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">No Pending Submissions</h3>
              <p className="text-gray-600">All restaurant submissions have been reviewed!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {pendingRestaurants.map((restaurant) => (
                <div key={restaurant.id} className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-lg font-semibold text-gray-800">{restaurant.name}</h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          restaurant.user_type === 'owner' 
                            ? 'bg-blue-100 text-blue-800' 
                            : 'bg-purple-100 text-purple-800'
                        }`}>
                          {restaurant.user_type === 'owner' ? 'Owner' : 'Community'}
                        </span>
                      </div>
                      
                      <p className="text-gray-600 mb-2">{restaurant.short_description}</p>
                      
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div>
                          <span className="font-medium text-gray-700">Agency:</span>
                          <span className="ml-1 text-gray-600">{restaurant.certifying_agency}</span>
                        </div>
                        <div>
                          <span className="font-medium text-gray-700">Category:</span>
                          <span className="ml-1 text-gray-600 capitalize">{restaurant.kosher_category}</span>
                        </div>
                        <div>
                          <span className="font-medium text-gray-700">Phone:</span>
                          <span className="ml-1 text-gray-600">{restaurant.phone}</span>
                        </div>
                        <div>
                          <span className="font-medium text-gray-700">Submitted:</span>
                          <span className="ml-1 text-gray-600">{formatDate(restaurant.created_at)}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex space-x-2 ml-4">
                      <button
                        onClick={() => openRestaurantDetails(restaurant)}
                        className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition-colors"
                      >
                        View Details
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Modal for restaurant details */}
      {showModal && selectedRestaurant && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-gray-800">{selectedRestaurant.name}</h2>
                <button
                  onClick={() => setShowModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ×
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <h3 className="font-medium text-gray-700 mb-2">Basic Information</h3>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="font-medium">Description:</span>
                      <p className="text-gray-600">{selectedRestaurant.short_description}</p>
                    </div>
                    <div>
                      <span className="font-medium">Address:</span>
                      <p className="text-gray-600">{selectedRestaurant.address}</p>
                    </div>
                    <div>
                      <span className="font-medium">Phone:</span>
                      <p className="text-gray-600">{selectedRestaurant.phone}</p>
                    </div>
                    <div>
                      <span className="font-medium">Agency:</span>
                      <p className="text-gray-600">{selectedRestaurant.certifying_agency}</p>
                    </div>
                  </div>
                </div>

                {selectedRestaurant.owner_info && (
                  <div>
                    <h3 className="font-medium text-gray-700 mb-2">Owner Information</h3>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="font-medium">Name:</span>
                        <p className="text-gray-600">{selectedRestaurant.owner_info.name}</p>
                      </div>
                      <div>
                        <span className="font-medium">Email:</span>
                        <p className="text-gray-600">{selectedRestaurant.owner_info.email}</p>
                      </div>
                      <div>
                        <span className="font-medium">Phone:</span>
                        <p className="text-gray-600">{selectedRestaurant.owner_info.phone}</p>
                      </div>
                    </div>
                  </div>
                )}

                <div className="flex space-x-3 pt-4">
                  <button
                    onClick={() => approveRestaurant(selectedRestaurant.id)}
                    className="flex-1 bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition-colors"
                  >
                    Approve
                  </button>
                  <button
                    onClick={() => rejectRestaurant(selectedRestaurant.id)}
                    className="flex-1 bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-700 transition-colors"
                  >
                    Reject
                  </button>
                  <button
                    onClick={() => setShowModal(false)}
                    className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-400 transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      <BottomNavigation />
    </div>
  );
} 