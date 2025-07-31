'use client';

import { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import BottomNavigation from '@/components/BottomNavigation';
import SearchBar from '@/components/SearchBar';
import { showToast } from '@/components/ui/Toast';
import { mockClaimDeal } from '@/lib/api/mock';

export default function SpecialsPage() {
  const [categoryTab, setCategoryTab] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [activeFilters, setActiveFilters] = useState<{
    agency?: string;
    dietary?: string;
    openNow?: boolean;
    category?: string;
    nearMe?: boolean;
    distanceRadius?: number;
  }>({});
  
  // ✅ Phase 1: Add router and state management
  const router = useRouter();
  const [claimingDeals, setClaimingDeals] = useState<Set<number>>(new Set());

  const specials = [
    {
      id: 1,
      title: 'Shabbat Special',
      restaurant: 'Kosher Deli & Grill',
      description: 'Complete Shabbat meal for 4 people - $89.99',
      discount: '20% OFF',
      validUntil: '2024-01-31',
      category: 'shabbat',
      image: '/images/placeholder-restaurant.jpg'
    },
    {
      id: 2,
      title: 'Lunch Combo Deal',
      restaurant: 'Miami Kosher Market',
      description: 'Sandwich + Soup + Drink - $12.99',
      discount: '15% OFF',
      validUntil: '2024-02-15',
      category: 'lunch',
      image: '/images/placeholder-restaurant.jpg'
    },
    {
      id: 3,
      title: 'Ice Cream Happy Hour',
      restaurant: 'Diamond K Ice Cream',
      description: 'Buy 1 Get 1 Free on all ice cream',
      discount: '50% OFF',
      validUntil: '2024-01-25',
      category: 'dessert',
      image: '/images/placeholder-restaurant.jpg'
    },
    {
      id: 4,
      title: 'Family Dinner Package',
      restaurant: 'Kosher Pizza Place',
      description: 'Large Pizza + 2 Sides + 2 Drinks - $34.99',
      discount: '25% OFF',
      validUntil: '2024-02-10',
      category: 'dinner',
      image: '/images/placeholder-restaurant.jpg'
    },
    {
      id: 5,
      title: 'Breakfast Special',
      restaurant: 'Kosher Cafe',
      description: 'Bagel + Coffee + Fruit - $8.99',
      discount: '10% OFF',
      validUntil: '2024-01-30',
      category: 'breakfast',
      image: '/images/placeholder-restaurant.jpg'
    },
    {
      id: 6,
      title: 'Catering Discount',
      restaurant: 'Kosher Catering Co.',
      description: '20% off all catering orders over $200',
      discount: '20% OFF',
      validUntil: '2024-03-01',
      category: 'catering',
      image: '/images/placeholder-restaurant.jpg'
    }
  ];

  const categories = [
    { id: 'all', name: 'All Specials', count: specials.length },
    { id: 'shabbat', name: 'Shabbat', count: specials.filter(s => s.category === 'shabbat').length },
    { id: 'lunch', name: 'Lunch', count: specials.filter(s => s.category === 'lunch').length },
    { id: 'dinner', name: 'Dinner', count: specials.filter(s => s.category === 'dinner').length },
    { id: 'breakfast', name: 'Breakfast', count: specials.filter(s => s.category === 'breakfast').length },
    { id: 'dessert', name: 'Dessert', count: specials.filter(s => s.category === 'dessert').length },
    { id: 'catering', name: 'Catering', count: specials.filter(s => s.category === 'catering').length }
  ];

  const filteredSpecials = specials
    .filter(special => categoryTab === 'all' || special.category === categoryTab)
    .filter(special => 
      !searchQuery.trim() || 
      special.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      special.restaurant.toLowerCase().includes(searchQuery.toLowerCase()) ||
      special.description.toLowerCase().includes(searchQuery.toLowerCase())
    );

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  const handleFilterChange = (key: string, value: any) => {
    setActiveFilters(prev => ({
      ...prev,
      [key]: value === 'all' ? undefined : value
    }));
  };

  const handleToggleFilter = (key: string, value: boolean) => {
    setActiveFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleDistanceChange = (distance: number) => {
    setActiveFilters(prev => ({
      ...prev,
      distanceRadius: distance
    }));
  };

  const handleClearAll = () => {
    setActiveFilters({});
  };



  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query);
  }, []);

  // ✅ Phase 1: Implement handler functions
  const handleClaimDeal = async (specialId: number) => {
    setClaimingDeals(prev => new Set(prev).add(specialId));
    
    try {
      const result = await mockClaimDeal(specialId);
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
    // Navigate to restaurant search or detail page
    const searchQuery = encodeURIComponent(restaurantName);
    router.push(`/?search=${searchQuery}`);
  };

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Header */}
      <Header />

      {/* Search Bar */}
      <div className="px-4 py-4">
        <SearchBar onSearch={handleSearch} />
      </div>

      {/* Simple Back Navigation */}
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

                    {/* ✅ Phase 1: Updated action buttons with onClick handlers */}
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