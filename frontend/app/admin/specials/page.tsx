'use client';

import React from 'react';

import { useState, useEffect } from 'react';
import { RestaurantSpecial } from '@/types/restaurant';
import { safeFilter } from '@/utils/validation';

export default function SpecialsManagementPage() {
  const [specials, setSpecials] = useState<RestaurantSpecial[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSpecial, setSelectedSpecial] = useState<RestaurantSpecial | null>(null);
  const [showPaymentModal, setShowPaymentModal] = useState(false);

  useEffect(() => {
    fetchSpecials();
  }, []);

  const fetchSpecials = async () => {
    try {
      setLoading(true);
      
      // Use mock data since admin specials endpoints don't exist on backend yet
      const mockSpecials: RestaurantSpecial[] = [
        {
          id: 1,
          restaurant_id: 1,
          title: "Shabbat Special",
          description: "Complete Shabbat meal with soup, main course, and dessert",
          discount_percent: 20,
          start_date: "2024-01-01",
          end_date: "2024-12-31",
          is_paid: true,
          payment_status: "paid",
          special_type: "discount",
          priority: 1,
          is_active: true,
          created_date: "2024-01-01T00:00:00Z",
          updated_date: "2024-01-01T00:00:00Z"
        },
        {
          id: 2,
          restaurant_id: 2,
          title: "Summer Promotion",
          description: "Buy one get one free on all ice cream flavors",
          discount_percent: 50,
          start_date: "2024-06-01",
          end_date: "2024-08-31",
          is_paid: false,
          payment_status: "unpaid",
          special_type: "promotion",
          priority: 2,
          is_active: true,
          created_date: "2024-06-01T00:00:00Z",
          updated_date: "2024-06-01T00:00:00Z"
        },
        {
          id: 3,
          restaurant_id: 3,
          title: "Holiday Event",
          description: "Special holiday menu with traditional dishes",
          discount_percent: 15,
          start_date: "2024-09-01",
          end_date: "2024-10-31",
          is_paid: true,
          payment_status: "paid",
          special_type: "event",
          priority: 3,
          is_active: true,
          created_date: "2024-09-01T00:00:00Z",
          updated_date: "2024-09-01T00:00:00Z"
        }
      ];
      
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setSpecials(mockSpecials);
    } catch (error) {
      console.error('Error fetching specials:', error);
      setError('Failed to load specials');
    } finally {
      setLoading(false);
    }
  };

  const handlePayment = async (specialId: number) => {
    if (!selectedSpecial) {
      console.error('No special selected for payment');
      return;
    }
    
    try {
      // Update local state directly since we're using mock data
      setSpecials(prev => prev.map(special => 
        special.id === specialId 
          ? { ...special, is_paid: !selectedSpecial.is_paid, payment_status: !selectedSpecial.is_paid ? 'paid' : 'unpaid' }
          : special
      ));
      setShowPaymentModal(false);
      setSelectedSpecial(null);
      
      // Show success message
      console.log(`Payment status updated for special ${specialId}`);
    } catch (error) {
      console.error('Error updating payment status:', error);
    }
  };

  const getStatusBadge = (special: RestaurantSpecial) => {
    if (special.is_paid) {
      return (
        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
          Paid
        </span>
      );
    } else {
      return (
        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
          Unpaid
        </span>
      );
    }
  };

  const getTypeBadge = (special: RestaurantSpecial) => {
    const colors = {
      discount: 'bg-blue-100 text-blue-800',
      promotion: 'bg-purple-100 text-purple-800',
      event: 'bg-orange-100 text-orange-800'
    };
    
    return (
      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${colors[special.special_type] || colors.discount}`}>
        {special.special_type.charAt(0).toUpperCase() + special.special_type.slice(1)}
      </span>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-jewgo-primary"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="flex items-center justify-between mb-6">
              <h1 className="text-2xl font-bold text-gray-900">Restaurant Specials Management</h1>
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-500">
                  Total Specials: {specials.length}
                </span>
                <span className="text-sm text-gray-500">
                  Paid: {safeFilter(specials, (s: RestaurantSpecial) => s.is_paid).length}
                </span>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Restaurant
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Special
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Type
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {specials.map((special) => (
                    <tr key={special.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        Restaurant #{special.restaurant_id}
                      </td>
                      <td className="px-6 py-4">
                        <div>
                          <div className="text-sm font-medium text-gray-900">{special.title}</div>
                          {special.description && (
                            <div className="text-sm text-gray-500">{special.description}</div>
                          )}
                          {special.discount_percent && (
                            <div className="text-sm text-green-600 font-medium">
                              {special.discount_percent}% OFF
                            </div>
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {getTypeBadge(special)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {getStatusBadge(special)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button
                          onClick={() => {
                            setSelectedSpecial(special);
                            setShowPaymentModal(true);
                          }}
                          className="text-jewgo-primary hover:text-jewgo-accent mr-4"
                        >
                          {special.is_paid ? 'Mark Unpaid' : 'Mark Paid'}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {specials.length === 0 && (
              <div className="text-center py-12">
                <div className="text-gray-500 mb-4">
                  <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
                  </svg>
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">No specials found</h3>
                <p className="text-gray-500">Restaurant specials will appear here once they are created.</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Payment Modal */}
      {showPaymentModal && selectedSpecial && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3 text-center">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Update Payment Status
              </h3>
              <div className="mb-4 text-sm text-gray-600">
                <p><strong>Special:</strong> {selectedSpecial.title}</p>
                <p><strong>Current Status:</strong> {selectedSpecial.is_paid ? 'Paid' : 'Unpaid'}</p>
              </div>
              <div className="flex justify-center space-x-4">
                <button
                  onClick={() => handlePayment(selectedSpecial.id)}
                  className={`px-4 py-2 rounded-md text-sm font-medium ${
                    selectedSpecial.is_paid
                      ? 'bg-red-600 text-white hover:bg-red-700'
                      : 'bg-green-600 text-white hover:bg-green-700'
                  }`}
                >
                  {selectedSpecial.is_paid ? 'Mark as Unpaid' : 'Mark as Paid'}
                </button>
                <button
                  onClick={() => {
                    setShowPaymentModal(false);
                    setSelectedSpecial(null);
                  }}
                  className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md text-sm font-medium hover:bg-gray-400"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 