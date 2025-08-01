'use client';

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import SearchBar from '@/components/SearchBar';
import BottomNavigation from '@/components/BottomNavigation';
import { RestaurantSpecial } from '@/types/restaurant';
import { showToast } from '@/components/ui/Toast';
import { fetchSpecials, claimDeal, getMockSpecials } from '@/lib/api/specials';
import { safeFilter } from '@/utils/validation';

interface Special {
  id: number;
  title: string;
  restaurant: string;
  description: string;
  discount: string;
  validUntil: string;
  category: string;
  image: string;
  restaurant_id?: number;
}

export default function SpecialsPageClient() {
  const router = useRouter();
  const [specials, setSpecials] = useState<Special[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [categoryTab, setCategoryTab] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [claimingDeals, setClaimingDeals] = useState<Set<number>>(new Set());
  const [mounted, setMounted] = useState(false);

  // Initialize component
  useEffect(() => {
    setMounted(true);
  }, []);

  // Fetch specials data
  useEffect(() => {
    if (mounted) {
      fetchSpecialsData();
    }
  }, [mounted]);

  const fetchSpecialsData = async () => {
    try {
      setLoading(true);
      setError(null);

      const specialsData = await fetchSpecials();
      setSpecials(specialsData);
    } catch (error) {
      console.error('Error fetching specials:', error);
      setError('Failed to load specials');
      // Fallback to mock data
      setSpecials(getMockSpecials());
    } finally {
      setLoading(false);
    }
  };



  // Memoized categories and filtered specials
  const categories = useMemo(() => [
    { id: 'all', name: 'All Specials', count: specials.length },
    { id: 'shabbat', name: 'Shabbat', count: safeFilter(specials, s => s.category === 'shabbat').length },
    { id: 'lunch', name: 'Lunch', count: safeFilter(specials, s => s.category === 'lunch').length },
    { id: 'dinner', name: 'Dinner', count: safeFilter(specials, s => s.category === 'dinner').length },
    { id: 'breakfast', name: 'Breakfast', count: safeFilter(specials, s => s.category === 'breakfast').length },
    { id: 'dessert', name: 'Dessert', count: safeFilter(specials, s => s.category === 'dessert').length },
    { id: 'catering', name: 'Catering', count: safeFilter(specials, s => s.category === 'catering').length },
    { id: 'promotion', name: 'Promotions', count: safeFilter(specials, s => s.category === 'promotion').length },
    { id: 'discount', name: 'Discounts', count: safeFilter(specials, s => s.category === 'discount').length },
    { id: 'event', name: 'Events', count: safeFilter(specials, s => s.category === 'event').length }
  ], [specials]);

  const filteredSpecials = useMemo(() => {
    try {
      // First filter by category
      let filtered = safeFilter(specials, special => 
        categoryTab === 'all' || special.category === categoryTab
      );
      
      // Then filter by search query
      filtered = safeFilter(filtered, special => 
        !searchQuery.trim() || 
        special.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        special.restaurant.toLowerCase().includes(searchQuery.toLowerCase()) ||
        special.description.toLowerCase().includes(searchQuery.toLowerCase())
      );
      
      return filtered;
    } catch (error) {
      console.error('Error in filteredSpecials useMemo:', error);
      return [];
    }
  }, [specials, categoryTab, searchQuery]);

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      });
    } catch (error) {
      return 'Valid until further notice';
    }
  };

  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query);
  }, []);

  const handleClaimDeal = async (specialId: number) => {
    setClaimingDeals(prev => new Set(prev).add(specialId));
    
    try {
      const result = await claimDeal(specialId);
      showToast(result.message, 'success');
    } catch (error) {
      console.error('Failed to claim deal:', error);
      showToast('Failed to claim deal. Please try again.', 'error');
    } finally {
      setClaimingDeals(prev => {
        const newSet = new Set(prev);
        newSet.delete(specialId);
        return newSet;
      });
    }
  };

  const handleViewRestaurant = (restaurantName: string) => {
    const searchQuery = encodeURIComponent(restaurantName);
    router.push(`/?search=${searchQuery}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-neutral-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-jewgo-primary"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Header */}
      <Header />

      {/* Search Bar */}
      <div className="px-4 py-4">
        <SearchBar onSearch={handleSearch} />
      </div>

      {/* Back Navigation */}
      <div className="px-4 py-2 bg-white border-b border-gray-100">
        <div className="flex space-x-2 overflow-x-auto pb-2 scrollbar-hide">
          <button
            onClick={() => router.push('/')}
            className="flex items-center justify-center gap-2 px-4 py-2 rounded-full text-sm font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Eatery
          </button>
        </div>
      </div>
      
      {/* Content */}
      <div className="px-4 py-6 pb-24">
        <div className="max-w-4xl mx-auto">
          {/* Page Header */}
          <div className="text-center mb-8">
            <div className="text-4xl mb-4">🎉</div>
            <h1 className="text-2xl font-bold text-neutral-800 mb-2">Kosher Specials</h1>
            <p className="text-neutral-600">Exclusive deals and promotions from kosher establishments</p>
          </div>

          {/* Error Display */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          )}

          {/* Category Tabs */}
          <div className="mb-6">
            <div className="flex space-x-2 overflow-x-auto pb-2 scrollbar-hide">
              {categories.map((category) => (
                <button
                  key={category.id}
                  onClick={() => setCategoryTab(category.id)}
                  className={`flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                    categoryTab === category.id
                      ? 'bg-gradient-jewgo text-white'
                      : 'bg-white text-neutral-700 hover:bg-neutral-50'
                  }`}
                >
                  {category.name} ({category.count})
                </button>
              ))}
            </div>
          </div>

          {/* Specials Grid */}
          {filteredSpecials.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">😔</div>
              <h3 className="text-xl font-semibold text-neutral-800 mb-2">No Specials Available</h3>
              <p className="text-neutral-600">Check back later for new deals and promotions!</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {filteredSpecials.map((special) => (
                <div key={special.id} className="bg-white rounded-lg shadow-md overflow-hidden">
                  {/* Special Image */}
                  <div className="h-48 bg-gradient-to-br from-jewgo-400/20 to-jewgo-400/40 relative">
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-6xl">🍽️</span>
                    </div>
                    {/* Discount Badge */}
                    <div className="absolute top-3 right-3">
                      <span className="bg-red-500 text-white px-3 py-1 rounded-full text-sm font-bold">
                        {special.discount}
                      </span>
                    </div>
                  </div>

                  {/* Special Content */}
                  <div className="p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-neutral-800 text-lg">{special.title}</h3>
                    </div>
                    
                    <p className="text-neutral-600 text-sm mb-2">{special.restaurant}</p>
                    <p className="text-neutral-700 mb-3">{special.description}</p>
                    
                    {/* Valid Until */}
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-1 text-sm text-neutral-500">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        <span>Valid until {formatDate(special.validUntil)}</span>
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex space-x-2">
                      <button 
                        onClick={() => handleClaimDeal(special.id)}
                        disabled={claimingDeals.has(special.id)}
                        className="flex-1 bg-gradient-jewgo text-white py-2 px-4 rounded-lg text-sm font-medium hover:bg-jewgo-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {claimingDeals.has(special.id) ? (
                          <div className="flex items-center justify-center space-x-2">
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                            <span>Claiming...</span>
                          </div>
                        ) : (
                          'Claim Deal'
                        )}
                      </button>
                      <button 
                        onClick={() => handleViewRestaurant(special.restaurant)}
                        className="flex-1 bg-neutral-100 text-neutral-700 py-2 px-4 rounded-lg text-sm font-medium hover:bg-neutral-200 transition-colors"
                      >
                        View Restaurant
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Newsletter Signup */}
          <div className="mt-8 bg-white rounded-lg shadow-md p-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold text-neutral-800 mb-2">Get Special Deals First!</h3>
              <p className="text-neutral-600 mb-4">Subscribe to receive exclusive kosher specials and promotions</p>
              <div className="flex max-w-md mx-auto space-x-2">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="flex-1 px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-jewgo-400 focus:border-transparent"
                />
                <button className="bg-gradient-jewgo text-white px-4 py-2 rounded-lg font-medium hover:bg-jewgo-600 transition-colors">
                  Subscribe
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Navigation */}
      <BottomNavigation />
    </div>
  );
} 