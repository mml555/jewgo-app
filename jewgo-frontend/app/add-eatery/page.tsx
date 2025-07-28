'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import BottomNavigation from '@/components/BottomNavigation';

export default function AddEateryPage() {
  const [userType, setUserType] = useState<'owner' | 'community' | ''>('');
  const [formData, setFormData] = useState({
    name: '',
    address: '',
    city: '',
    state: '',
    zipCode: '',
    phone: '',
    website: '',
    certifyingAgency: '',
    kosherType: '',
    kosherCategory: '',
    description: '',
    ownerName: '',
    ownerEmail: '',
    ownerPhone: ''
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!userType) {
      alert('Please select whether you own this establishment or are adding it to the community.');
      return;
    }
    
    setIsSubmitting(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    setIsSubmitting(false);
    
    if (userType === 'owner') {
      alert('Thank you! Your establishment has been submitted for review. We will contact you soon to verify your ownership and complete the listing process.');
    } else {
      alert('Thank you! Your submission has been received and will be reviewed by our team. We will verify the information before adding it to the directory.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Header />
      
      {/* Content */}
      <div className="px-4 py-6 pb-24">
        <div className="max-w-2xl mx-auto">
          {/* Page Header */}
          <div className="text-center mb-8">
            <div className="text-4xl mb-4">🏪</div>
            <h1 className="text-2xl font-bold text-gray-800 mb-2">Add a New Eatery</h1>
            <p className="text-gray-600">Help the community by adding a kosher establishment</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-6 space-y-6">
            {/* User Type Selection */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Who are you?</h3>
              <div className="space-y-3">
                <label className="flex items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                  <input
                    type="radio"
                    name="userType"
                    value="owner"
                    checked={userType === 'owner'}
                    onChange={(e) => setUserType(e.target.value as 'owner')}
                    className="mr-3 text-jewgo-primary focus:ring-jewgo-primary"
                  />
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">👨‍💼</span>
                      <div>
                        <div className="font-medium text-gray-900">I own this establishment</div>
                        <div className="text-sm text-gray-600">I'm the owner or manager and want to list my business</div>
                      </div>
                    </div>
                  </div>
                </label>

                <label className="flex items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                  <input
                    type="radio"
                    name="userType"
                    value="community"
                    checked={userType === 'community'}
                    onChange={(e) => setUserType(e.target.value as 'community')}
                    className="mr-3 text-jewgo-primary focus:ring-jewgo-primary"
                  />
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">🤝</span>
                      <div>
                        <div className="font-medium text-gray-900">I want to add it to the community</div>
                        <div className="text-sm text-gray-600">I found a kosher establishment that should be listed</div>
                      </div>
                    </div>
                  </div>
                </label>
              </div>
              
              {userType && (
                <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                  <div className="flex items-start space-x-2">
                    <span className="text-blue-500 mt-0.5">ℹ️</span>
                    <div className="text-sm text-blue-800">
                      {userType === 'owner' ? (
                        <>
                          <strong>Owner submission:</strong> We'll contact you to verify ownership and help you set up your listing with additional features like menu updates and special announcements.
                        </>
                      ) : (
                        <>
                          <strong>Community submission:</strong> We'll review and verify the information before adding it to our directory. Thank you for helping the community!
                        </>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Owner Information (only show if user is owner) */}
            {userType === 'owner' && (
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Owner Information</h3>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Your Name *
                      </label>
                      <input
                        type="text"
                        name="ownerName"
                        value={formData.ownerName}
                        onChange={handleInputChange}
                        required
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                        placeholder="Your full name"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Your Email *
                      </label>
                      <input
                        type="email"
                        name="ownerEmail"
                        value={formData.ownerEmail}
                        onChange={handleInputChange}
                        required
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                        placeholder="your@email.com"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Your Phone Number *
                    </label>
                    <input
                      type="tel"
                      name="ownerPhone"
                      value={formData.ownerPhone}
                      onChange={handleInputChange}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                      placeholder="(555) 123-4567"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Basic Information */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Establishment Information</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Restaurant Name *
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                    placeholder="Enter restaurant name"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Address *
                  </label>
                  <input
                    type="text"
                    name="address"
                    value={formData.address}
                    onChange={handleInputChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                    placeholder="Street address"
                  />
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">City *</label>
                    <input
                      type="text"
                      name="city"
                      value={formData.city}
                      onChange={handleInputChange}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                      placeholder="City"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">State *</label>
                    <input
                      type="text"
                      name="state"
                      value={formData.state}
                      onChange={handleInputChange}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                      placeholder="State"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">ZIP Code *</label>
                    <input
                      type="text"
                      name="zipCode"
                      value={formData.zipCode}
                      onChange={handleInputChange}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                      placeholder="ZIP"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                    <input
                      type="tel"
                      name="phone"
                      value={formData.phone}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                      placeholder="(555) 123-4567"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Website</label>
                    <input
                      type="url"
                      name="website"
                      value={formData.website}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                      placeholder="https://example.com"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Kosher Information */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Kosher Information</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Certifying Agency *
                  </label>
                  <select
                    name="certifyingAgency"
                    value={formData.certifyingAgency}
                    onChange={handleInputChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                  >
                    <option value="">Select certifying agency</option>
                    <option value="ORB">ORB</option>
                    <option value="KM">KM (Cholov Yisroel)</option>
                    <option value="KDM">KDM (Mixed)</option>
                    <option value="Diamond K">Diamond K</option>
                    <option value="OU">OU</option>
                    <option value="Other">Other</option>
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Kosher Type</label>
                    <select
                      name="kosherType"
                      value={formData.kosherType}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                    >
                      <option value="">Select type</option>
                      <option value="restaurant">Restaurant</option>
                      <option value="bakery">Bakery</option>
                      <option value="catering">Catering</option>
                      <option value="grocery">Grocery</option>
                      <option value="ice_cream">Ice Cream</option>
                      <option value="cafe">Cafe</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Dietary Category</label>
                    <select
                      name="kosherCategory"
                      value={formData.kosherCategory}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                    >
                      <option value="">Select category</option>
                      <option value="meat">Meat</option>
                      <option value="dairy">Dairy</option>
                      <option value="pareve">Pareve</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    rows={4}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                    placeholder="Tell us about this establishment..."
                  />
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <div className="pt-4">
              <button
                type="submit"
                disabled={isSubmitting || !userType}
                className="w-full bg-jewgo-primary text-white py-3 px-6 rounded-lg font-medium hover:bg-jewgo-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    <span>Submitting...</span>
                  </div>
                ) : (
                  userType === 'owner' ? 'Submit as Owner' : 'Submit for Review'
                )}
              </button>
            </div>

            {/* Note */}
            <div className="text-center text-sm text-gray-500">
              <p>
                {userType === 'owner' 
                  ? 'As an owner, you\'ll receive priority review and additional listing features.'
                  : 'All community submissions are reviewed before being added to the directory.'
                }
              </p>
            </div>
          </form>
        </div>
      </div>

      {/* Bottom Navigation */}
      <BottomNavigation />
    </div>
  );
} 