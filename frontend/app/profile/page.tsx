'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import BottomNavigation from '@/components/BottomNavigation';
import NavTabs from '@/components/NavTabs';
import ConfirmModal from '@/components/ui/ConfirmModal';
import PasswordChangeModal from '@/components/ui/PasswordChangeModal';
import { showToast } from '@/components/ui/Toast';
import { mockExportUserData, mockDeleteAccount } from '@/lib/api/mock';
import { getFavorites } from '@/utils/favorites';

export default function ProfilePage() {
  const [activeFilters, setActiveFilters] = useState<{
    agency?: string;
    dietary?: string;
    openNow?: boolean;
    category?: string;
    nearMe?: boolean;
    distanceRadius?: number;
  }>({});
  const [userProfile, setUserProfile] = useState({
    name: 'Sarah Cohen',
    email: 'sarah.cohen@email.com',
    phone: '(305) 555-0123',
    location: 'Miami, FL',
    dietaryPreferences: ['dairy', 'pareve'],
    favoriteCertifications: ['ORB', 'KM'],
    notifications: {
      specials: true,
      newRestaurants: true,
      menuUpdates: true,
      shabbatReminders: false,
      certificationUpdates: false
    }
  });

  const [activeTab, setActiveTab] = useState('profile');
  const [profileTab, setProfileTab] = useState('profile');
  
  // ✅ Phase 1: Add router and state management
  const router = useRouter();
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [showDeleteConfirmation, setShowDeleteConfirmation] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const updateProfile = (field: string, value: any) => {
    setUserProfile(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const updateNotification = (type: string, value: boolean) => {
    setUserProfile(prev => ({
      ...prev,
      notifications: {
        ...prev.notifications,
        [type]: value
      }
    }));
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

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
  };

  // ✅ Phase 1: Implement handler functions
  const handleChangePassword = () => {
    setShowPasswordModal(true);
  };

  const handlePrivacySettings = () => {
    router.push('/profile/privacy');
  };

  const handleExportData = async () => {
    setIsExporting(true);
    try {
      const userData = await mockExportUserData();
      
      const blob = new Blob([JSON.stringify(userData, null, 2)], { 
        type: 'application/json' 
      });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `jewgo-data-${new Date().toISOString().split('T')[0]}.json`;
      link.click();
      
      showToast('Data exported successfully!', 'success');
    } catch (error) {
      console.error('Export failed:', error);
      showToast('Failed to export data. Please try again.', 'error');
    } finally {
      setIsExporting(false);
    }
  };

  const handleDeleteAccount = () => {
    setShowDeleteConfirmation(true);
  };

  const handleConfirmDeleteAccount = async () => {
    setIsDeleting(true);
    try {
      await mockDeleteAccount('password123'); // In real app, get from form
      showToast('Account deleted successfully.', 'success');
      // Redirect to home page after deletion
      setTimeout(() => router.push('/'), 2000);
    } catch (error) {
      console.error('Delete failed:', error);
      showToast('Failed to delete account. Please try again.', 'error');
    } finally {
      setIsDeleting(false);
      setShowDeleteConfirmation(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Header />

      {/* Navigation Tabs */}
      <NavTabs activeTab={activeTab} onTabChange={handleTabChange} />
      
      {/* Content */}
      <div className="px-4 py-6 pb-24">
        <div className="max-w-2xl mx-auto">
          {/* Page Header */}
          <div className="text-center mb-8">
            <div className="text-4xl mb-4">👤</div>
            <h1 className="text-2xl font-bold text-gray-800 mb-2">My Profile</h1>
            <p className="text-gray-600">Manage your account and preferences</p>
          </div>



          {/* Profile Tabs */}
          <div className="mb-6">
            <div className="flex space-x-2 overflow-x-auto pb-2 scrollbar-hide">
              {[
                { id: 'profile', name: 'Profile', icon: '👤' },
                { id: 'preferences', name: 'Preferences', icon: '⚙️' },
                { id: 'notifications', name: 'Notifications', icon: '🔔' },
                { id: 'activity', name: 'Activity', icon: '📊' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setProfileTab(tab.id)}
                  className={`flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                    profileTab === tab.id
                      ? 'bg-jewgo-primary text-white'
                      : 'bg-white text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <span className="mr-2">{tab.icon}</span>
                  {tab.name}
                </button>
              ))}
            </div>
          </div>

          {/* Tab Content */}
          <div className="bg-white rounded-lg shadow-md p-6">
            {profileTab === 'profile' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Personal Information</h3>
                
                {/* Profile Picture */}
                <div className="text-center">
                  <div className="w-24 h-24 bg-gradient-to-br from-jewgo-primary/20 to-jewgo-primary/40 rounded-full mx-auto mb-4 flex items-center justify-center">
                    <span className="text-3xl">👤</span>
                  </div>
                  <button className="text-jewgo-primary hover:text-jewgo-primary-dark text-sm font-medium">
                    Change Photo
                  </button>
                </div>

                {/* Form Fields */}
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                    <input
                      type="text"
                      value={userProfile.name}
                      onChange={(e) => updateProfile('name', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
                    <input
                      type="email"
                      value={userProfile.email}
                      onChange={(e) => updateProfile('email', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                    <input
                      type="tel"
                      value={userProfile.phone}
                      onChange={(e) => updateProfile('phone', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
                    <input
                      type="text"
                      value={userProfile.location}
                      onChange={(e) => updateProfile('location', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                    />
                  </div>
                </div>

                <div className="pt-4">
                  <button className="w-full bg-jewgo-primary text-white py-3 px-6 rounded-lg font-medium hover:bg-jewgo-primary-dark transition-colors">
                    Save Changes
                  </button>
                </div>
              </div>
            )}

            {activeTab === 'preferences' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Dietary Preferences</h3>
                
                <div className="space-y-3">
                  {['meat', 'dairy', 'pareve'].map((preference) => (
                    <label key={preference} className="flex items-center space-x-3">
                      <input
                        type="checkbox"
                        checked={userProfile.dietaryPreferences.includes(preference)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            updateProfile('dietaryPreferences', [...userProfile.dietaryPreferences, preference]);
                          } else {
                            updateProfile('dietaryPreferences', userProfile.dietaryPreferences.filter(p => p !== preference));
                          }
                        }}
                        className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                      />
                      <span className="text-sm text-gray-700 capitalize">{preference}</span>
                    </label>
                  ))}
                </div>

                <h3 className="text-lg font-semibold text-gray-800 mb-4">Preferred Certifications</h3>
                
                <div className="space-y-3">
                  {['ORB', 'KM', 'KDM', 'Diamond K', 'OU'].map((certification) => (
                    <label key={certification} className="flex items-center space-x-3">
                      <input
                        type="checkbox"
                        checked={userProfile.favoriteCertifications.includes(certification)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            updateProfile('favoriteCertifications', [...userProfile.favoriteCertifications, certification]);
                          } else {
                            updateProfile('favoriteCertifications', userProfile.favoriteCertifications.filter(c => c !== certification));
                          }
                        }}
                        className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                      />
                      <span className="text-sm text-gray-700">{certification}</span>
                    </label>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'notifications' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Notification Preferences</h3>
                
                <div className="space-y-4">
                  {Object.entries(userProfile.notifications).map(([key, value]) => (
                    <label key={key} className="flex items-center justify-between">
                      <div>
                        <span className="text-sm font-medium text-gray-700">
                          {key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                        </span>
                        <p className="text-xs text-gray-500">
                          {key === 'specials' && 'Get notified about special offers and deals'}
                          {key === 'newRestaurants' && 'Be informed when new restaurants are added'}
                          {key === 'menuUpdates' && 'Receive updates when menus change'}
                          {key === 'shabbatReminders' && 'Get reminders for Shabbat meal planning'}
                          {key === 'certificationUpdates' && 'Stay updated on certification changes'}
                        </p>
                      </div>
                      <input
                        type="checkbox"
                        checked={value}
                        onChange={(e) => updateNotification(key, e.target.checked)}
                        className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                      />
                    </label>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'activity' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Activity Summary</h3>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-50 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-jewgo-primary">12</div>
                    <div className="text-sm text-gray-600">Restaurants Visited</div>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-jewgo-primary">8</div>
                    <div className="text-sm text-gray-600">Reviews Written</div>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-jewgo-primary">15</div>
                    <div className="text-sm text-gray-600">Favorites Saved</div>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-jewgo-primary">5</div>
                    <div className="text-sm text-gray-600">Deals Claimed</div>
                  </div>
                </div>

                <div className="space-y-3">
                  <h4 className="font-medium text-gray-800">Recent Activity</h4>
                  <div className="space-y-2">
                    <div className="flex items-center space-x-3 text-sm">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span className="text-gray-600">Added "Kosher Deli" to favorites</span>
                      <span className="text-gray-400">2 hours ago</span>
                    </div>
                    <div className="flex items-center space-x-3 text-sm">
                      <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                      <span className="text-gray-600">Wrote a review for "Miami Kosher Market"</span>
                      <span className="text-gray-400">1 day ago</span>
                    </div>
                    <div className="flex items-center space-x-3 text-sm">
                      <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                      <span className="text-gray-600">Claimed "Shabbat Special" deal</span>
                      <span className="text-gray-400">3 days ago</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Account Actions */}
          <div className="mt-6 bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Account Actions</h3>
            <div className="space-y-3">
              {/* ✅ Phase 1: Updated button elements with onClick handlers */}
              <button 
                onClick={handleChangePassword}
                className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">Change Password</span>
                  <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </button>
              <button 
                onClick={handlePrivacySettings}
                className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">Privacy Settings</span>
                  <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </button>
              <button 
                onClick={handleExportData}
                disabled={isExporting}
                className="w-full text-left px-4 py-3 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">
                    {isExporting ? 'Exporting...' : 'Export Data'}
                  </span>
                  <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </button>
              <button 
                onClick={handleDeleteAccount}
                className="w-full text-left px-4 py-3 rounded-lg hover:bg-red-50 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <span className="text-red-600">Delete Account</span>
                  <svg className="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Navigation */}
      <BottomNavigation />
      
      {/* ✅ Phase 1: Add modal components */}
      {showDeleteConfirmation && (
        <ConfirmModal
          isOpen={showDeleteConfirmation}
          onClose={() => setShowDeleteConfirmation(false)}
          onConfirm={handleConfirmDeleteAccount}
          title="Delete Account"
          message="Are you sure you want to delete your account? This action cannot be undone and all your data will be permanently removed."
          confirmText="Delete Account"
          confirmColor="red"
          isLoading={isDeleting}
        />
      )}
      
      {/* ✅ Phase 2: Add password change modal */}
      <PasswordChangeModal
        isOpen={showPasswordModal}
        onClose={() => setShowPasswordModal(false)}
        onSuccess={() => {
          showToast('Password changed successfully!', 'success');
        }}
      />
    </div>
  );
} 