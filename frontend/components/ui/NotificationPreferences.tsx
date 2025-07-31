'use client';

import { useState } from 'react';
import { showToast } from './Toast';

interface NotificationPreference {
  id: string;
  title: string;
  description: string;
  email: boolean;
  push: boolean;
  sms: boolean;
  category: 'marketing' | 'updates' | 'security' | 'social';
}

interface NotificationPreferencesProps {
  preferences: NotificationPreference[];
  onSave: (preferences: NotificationPreference[]) => Promise<void>;
  className?: string;
}

export default function NotificationPreferences({ 
  preferences: initialPreferences, 
  onSave, 
  className = '' 
}: NotificationPreferencesProps) {
  const [preferences, setPreferences] = useState<NotificationPreference[]>(initialPreferences);
  const [isSaving, setIsSaving] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);

  const updatePreference = (id: string, channel: 'email' | 'push' | 'sms', value: boolean) => {
    setPreferences(prev => 
      prev.map(pref => 
        pref.id === id ? { ...pref, [channel]: value } : pref
      )
    );
    setHasChanges(true);
  };

  const toggleCategory = (category: string, enabled: boolean) => {
    setPreferences(prev => 
      prev.map(pref => 
        pref.category === category 
          ? { ...pref, email: enabled, push: enabled, sms: enabled }
          : pref
      )
    );
    setHasChanges(true);
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      await onSave(preferences);
      setHasChanges(false);
      showToast('Notification preferences saved!', 'success');
    } catch (error) {
      showToast('Failed to save preferences. Please try again.', 'error');
    } finally {
      setIsSaving(false);
    }
  };

  const handleReset = () => {
    setPreferences(initialPreferences);
    setHasChanges(false);
    showToast('Preferences reset to defaults', 'info');
  };

  const getCategoryPreferences = (category: string) => {
    return preferences.filter(pref => pref.category === category);
  };

  const isCategoryEnabled = (category: string) => {
    const categoryPrefs = getCategoryPreferences(category);
    return categoryPrefs.some(pref => pref.email || pref.push || pref.sms);
  };

  const categories = [
    { 
      key: 'marketing', 
      title: 'Marketing & Promotions', 
      description: 'Special offers, deals, and promotional content',
      icon: '🎯'
    },
    { 
      key: 'updates', 
      title: 'App Updates', 
      description: 'New features, improvements, and app news',
      icon: '🆕'
    },
    { 
      key: 'security', 
      title: 'Security & Account', 
      description: 'Login alerts, password changes, and security updates',
      icon: '🔒'
    },
    { 
      key: 'social', 
      title: 'Social & Community', 
      description: 'Friend activity, reviews, and community updates',
      icon: '👥'
    }
  ];

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Notification Preferences</h2>
        <p className="text-gray-600">Choose how you'd like to receive notifications</p>
      </div>

      {/* Categories */}
      {categories.map(category => {
        const categoryPrefs = getCategoryPreferences(category.key);
        const isEnabled = isCategoryEnabled(category.key);

        return (
          <div key={category.key} className="bg-white rounded-lg shadow-md p-6">
            {/* Category Header */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <span className="text-2xl">{category.icon}</span>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{category.title}</h3>
                  <p className="text-sm text-gray-600">{category.description}</p>
                </div>
              </div>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={isEnabled}
                  onChange={(e) => toggleCategory(category.key, e.target.checked)}
                  className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <span className="ml-2 text-sm font-medium text-gray-700">All</span>
              </label>
            </div>

            {/* Individual Preferences */}
            {categoryPrefs.length > 0 && (
              <div className="space-y-3 pl-8">
                {categoryPrefs.map(pref => (
                  <div key={pref.id} className="border-l-2 border-gray-200 pl-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium text-gray-900">{pref.title}</span>
                    </div>
                    <p className="text-sm text-gray-600 mb-3">{pref.description}</p>
                    
                    {/* Notification Channels */}
                    <div className="flex space-x-6">
                      <label className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          checked={pref.email}
                          onChange={(e) => updatePreference(pref.id, 'email', e.target.checked)}
                          className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <span className="text-sm text-gray-700">Email</span>
                      </label>
                      <label className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          checked={pref.push}
                          onChange={(e) => updatePreference(pref.id, 'push', e.target.checked)}
                          className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <span className="text-sm text-gray-700">Push</span>
                      </label>
                      <label className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          checked={pref.sms}
                          onChange={(e) => updatePreference(pref.id, 'sms', e.target.checked)}
                          className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                        />
                        <span className="text-sm text-gray-700">SMS</span>
                      </label>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        );
      })}

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={() => {
              setPreferences(prev => 
                prev.map(pref => ({ ...pref, email: true, push: true, sms: true }))
              );
              setHasChanges(true);
            }}
            className="p-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-left"
          >
            <div className="font-medium text-gray-900">Enable All</div>
            <div className="text-sm text-gray-600">Turn on all notifications</div>
          </button>
          <button
            onClick={() => {
              setPreferences(prev => 
                prev.map(pref => ({ ...pref, email: false, push: false, sms: false }))
              );
              setHasChanges(true);
            }}
            className="p-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-left"
          >
            <div className="font-medium text-gray-900">Disable All</div>
            <div className="text-sm text-gray-600">Turn off all notifications</div>
          </button>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex space-x-3">
        <button
          onClick={handleReset}
          disabled={!hasChanges}
          className="flex-1 px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Reset
        </button>
        <button
          onClick={handleSave}
          disabled={!hasChanges || isSaving}
          className="flex-1 px-4 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isSaving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>

      {/* Summary */}
      <div className="bg-blue-50 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <svg className="w-5 h-5 text-blue-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <h4 className="font-medium text-blue-900">Notification Summary</h4>
            <p className="text-sm text-blue-700 mt-1">
              You have {preferences.filter(p => p.email || p.push || p.sms).length} active notification types.
              {preferences.filter(p => p.email).length > 0 && ` ${preferences.filter(p => p.email).length} via email,`}
              {preferences.filter(p => p.push).length > 0 && ` ${preferences.filter(p => p.push).length} via push,`}
              {preferences.filter(p => p.sms).length > 0 && ` ${preferences.filter(p => p.sms).length} via SMS`}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
} 