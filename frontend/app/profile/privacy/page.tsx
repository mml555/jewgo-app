'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import BottomNavigation from '@/components/BottomNavigation';
import { showToast } from '@/components/ui/Toast';
import { LoadingButton } from '@/components/ui/LoadingStates';

interface PrivacySettings {
  profileVisibility: 'public' | 'private' | 'friends';
  locationSharing: boolean;
  searchHistory: boolean;
  personalizedAds: boolean;
  emailNotifications: boolean;
  pushNotifications: boolean;
  dataAnalytics: boolean;
  thirdPartySharing: boolean;
}

export default function PrivacySettingsPage() {
  const router = useRouter();
  const [settings, setSettings] = useState<PrivacySettings>({
    profileVisibility: 'public',
    locationSharing: true,
    searchHistory: true,
    personalizedAds: false,
    emailNotifications: true,
    pushNotifications: true,
    dataAnalytics: true,
    thirdPartySharing: false
  });

  const [isSaving, setIsSaving] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);

  const updateSetting = (key: keyof PrivacySettings, value: any) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
    setHasChanges(true);
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      // Mock API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      showToast('Privacy settings saved successfully!', 'success');
      setHasChanges(false);
    } catch (error) {
      showToast('Failed to save settings. Please try again.', 'error');
    } finally {
      setIsSaving(false);
    }
  };

  const handleReset = () => {
    setSettings({
      profileVisibility: 'public',
      locationSharing: true,
      searchHistory: true,
      personalizedAds: false,
      emailNotifications: true,
      pushNotifications: true,
      dataAnalytics: true,
      thirdPartySharing: false
    });
    setHasChanges(false);
    showToast('Settings reset to defaults', 'info');
  };

  const handleExportData = async () => {
    try {
      const data = {
        privacySettings: settings,
        exportDate: new Date().toISOString(),
        dataTypes: ['profile', 'preferences', 'activity']
      };

      const blob = new Blob([JSON.stringify(data, null, 2)], {
        type: 'application/json'
      });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `jewgo-privacy-data-${new Date().toISOString().split('T')[0]}.json`;
      link.click();

      showToast('Privacy data exported successfully!', 'success');
    } catch (error) {
      showToast('Failed to export data. Please try again.', 'error');
    }
  };

  const handleDeleteData = async () => {
    if (confirm('Are you sure you want to delete all your data? This action cannot be undone.')) {
      try {
        // Mock API call
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        showToast('All data deleted successfully', 'success');
        router.push('/');
      } catch (error) {
        showToast('Failed to delete data. Please try again.', 'error');
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <div className="bg-white shadow-soft border-b border-neutral-200 sticky top-0 z-50">
        <div className="px-4 py-3 sm:px-6 sm:py-4">
          <div className="flex items-center space-x-3">
            <button
              onClick={() => router.back()}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <h1 className="text-lg font-semibold text-gray-900">Privacy Settings</h1>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 p-4 space-y-6">
        {/* Profile Visibility */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Profile Visibility</h3>
          <div className="space-y-3">
            <label className="flex items-center space-x-3">
              <input
                type="radio"
                name="profileVisibility"
                value="public"
                checked={settings.profileVisibility === 'public'}
                onChange={(e) => updateSetting('profileVisibility', e.target.value)}
                className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
              />
              <div>
                <span className="font-medium text-gray-900">Public</span>
                <p className="text-sm text-gray-600">Anyone can see your profile and activity</p>
              </div>
            </label>
            <label className="flex items-center space-x-3">
              <input
                type="radio"
                name="profileVisibility"
                value="friends"
                checked={settings.profileVisibility === 'friends'}
                onChange={(e) => updateSetting('profileVisibility', e.target.value)}
                className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
              />
              <div>
                <span className="font-medium text-gray-900">Friends Only</span>
                <p className="text-sm text-gray-600">Only your friends can see your profile</p>
              </div>
            </label>
            <label className="flex items-center space-x-3">
              <input
                type="radio"
                name="profileVisibility"
                value="private"
                checked={settings.profileVisibility === 'private'}
                onChange={(e) => updateSetting('profileVisibility', e.target.value)}
                className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
              />
              <div>
                <span className="font-medium text-gray-900">Private</span>
                <p className="text-sm text-gray-600">Only you can see your profile</p>
              </div>
            </label>
          </div>
        </div>

        {/* Location & Data */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Location & Data</h3>
          <div className="space-y-4">
            <label className="flex items-center justify-between">
              <div>
                <span className="font-medium text-gray-900">Location Sharing</span>
                <p className="text-sm text-gray-600">Allow JewGo to access your location for nearby recommendations</p>
              </div>
              <input
                type="checkbox"
                checked={settings.locationSharing}
                onChange={(e) => updateSetting('locationSharing', e.target.checked)}
                className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
            </label>
            <label className="flex items-center justify-between">
              <div>
                <span className="font-medium text-gray-900">Search History</span>
                <p className="text-sm text-gray-600">Save your search history for personalized recommendations</p>
              </div>
              <input
                type="checkbox"
                checked={settings.searchHistory}
                onChange={(e) => updateSetting('searchHistory', e.target.checked)}
                className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
            </label>
            <label className="flex items-center justify-between">
              <div>
                <span className="font-medium text-gray-900">Data Analytics</span>
                <p className="text-sm text-gray-600">Help us improve by sharing anonymous usage data</p>
              </div>
              <input
                type="checkbox"
                checked={settings.dataAnalytics}
                onChange={(e) => updateSetting('dataAnalytics', e.target.checked)}
                className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
            </label>
          </div>
        </div>

        {/* Notifications */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Notifications</h3>
          <div className="space-y-4">
            <label className="flex items-center justify-between">
              <div>
                <span className="font-medium text-gray-900">Email Notifications</span>
                <p className="text-sm text-gray-600">Receive updates and special offers via email</p>
              </div>
              <input
                type="checkbox"
                checked={settings.emailNotifications}
                onChange={(e) => updateSetting('emailNotifications', e.target.checked)}
                className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
            </label>
            <label className="flex items-center justify-between">
              <div>
                <span className="font-medium text-gray-900">Push Notifications</span>
                <p className="text-sm text-gray-600">Receive notifications on your device</p>
              </div>
              <input
                type="checkbox"
                checked={settings.pushNotifications}
                onChange={(e) => updateSetting('pushNotifications', e.target.checked)}
                className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
            </label>
          </div>
        </div>

        {/* Advertising & Third Party */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Advertising & Third Party</h3>
          <div className="space-y-4">
            <label className="flex items-center justify-between">
              <div>
                <span className="font-medium text-gray-900">Personalized Ads</span>
                <p className="text-sm text-gray-600">Show ads based on your interests and activity</p>
              </div>
              <input
                type="checkbox"
                checked={settings.personalizedAds}
                onChange={(e) => updateSetting('personalizedAds', e.target.checked)}
                className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
            </label>
            <label className="flex items-center justify-between">
              <div>
                <span className="font-medium text-gray-900">Third Party Sharing</span>
                <p className="text-sm text-gray-600">Allow sharing data with trusted third-party services</p>
              </div>
              <input
                type="checkbox"
                checked={settings.thirdPartySharing}
                onChange={(e) => updateSetting('thirdPartySharing', e.target.checked)}
                className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
            </label>
          </div>
        </div>

        {/* Data Management */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Data Management</h3>
          <div className="space-y-4">
            <button
              onClick={handleExportData}
              className="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center justify-between">
                <div>
                  <span className="font-medium text-gray-900">Export My Data</span>
                  <p className="text-sm text-gray-600">Download a copy of all your data</p>
                </div>
                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
            </button>
            <button
              onClick={handleDeleteData}
              className="w-full text-left p-4 border border-red-200 rounded-lg hover:bg-red-50 transition-colors"
            >
              <div className="flex items-center justify-between">
                <div>
                  <span className="font-medium text-red-600">Delete All Data</span>
                  <p className="text-sm text-red-500">Permanently delete all your data and account</p>
                </div>
                <svg className="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </div>
            </button>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-3">
          <button
            onClick={handleReset}
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          >
            Reset to Defaults
          </button>
          <LoadingButton
            onClick={handleSave}
            loading={isSaving}
            disabled={!hasChanges}
            className="flex-1"
            loadingText="Saving..."
          >
            Save Changes
          </LoadingButton>
        </div>
      </div>

      {/* Bottom Navigation */}
      <BottomNavigation />
    </div>
  );
} 