'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import BottomNavigation from '@/components/BottomNavigation';
import { safeFilter } from '@/utils/validation';

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState([
    {
      id: 1,
      type: 'special',
      title: 'New Special Available!',
      message: 'Kosher Deli & Grill has a new Shabbat special - 20% off complete meals',
      time: '2 hours ago',
      read: false,
      icon: '🎉'
    },
    {
      id: 2,
      type: 'restaurant',
      title: 'New Restaurant Added',
      message: 'Diamond K Ice Cream has been added to our directory',
      time: '1 day ago',
      read: false,
      icon: '🏪'
    },
    {
      id: 3,
      type: 'update',
      title: 'Menu Updated',
      message: 'Miami Kosher Market has updated their menu with new items',
      time: '2 days ago',
      read: true,
      icon: '📝'
    },
    {
      id: 4,
      type: 'reminder',
      title: 'Shabbat Reminder',
      message: 'Don\'t forget to order your Shabbat meals by Thursday!',
      time: '3 days ago',
      read: true,
      icon: '🕯️'
    },
    {
      id: 5,
      type: 'certification',
      title: 'Certification Update',
      message: 'Kosher Pizza Place has renewed their ORB certification',
      time: '1 week ago',
      read: true,
      icon: '✅'
    },
    {
      id: 6,
      type: 'system',
      title: 'Welcome to Jewgo!',
      message: 'Thank you for joining our kosher restaurant directory',
      time: '1 week ago',
      read: true,
      icon: '👋'
    }
  ]);

  const [activeFilter, setActiveFilter] = useState('all');

  const markAsRead = (id: number) => {
    setNotifications(prev => 
      prev.map(notification => 
        notification.id === id ? { ...notification, read: true } : notification
      )
    );
  };

  const markAllAsRead = () => {
    setNotifications(prev => 
      prev.map(notification => ({ ...notification, read: true }))
    );
  };

  const deleteNotification = (id: number) => {
    setNotifications(prev => safeFilter(prev, (notification: any) => notification.id !== id));
  };

  const filteredNotifications = activeFilter === 'all' 
    ? notifications 
    : safeFilter(notifications, (notification: any) => notification.type === activeFilter);

  const unreadCount = safeFilter(notifications, (n: any) => !n.read).length;

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'special': return 'bg-red-100 text-red-800';
      case 'restaurant': return 'bg-blue-100 text-blue-800';
      case 'update': return 'bg-green-100 text-green-800';
      case 'reminder': return 'bg-yellow-100 text-yellow-800';
      case 'certification': return 'bg-purple-100 text-purple-800';
      case 'system': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
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
            <div className="text-4xl mb-4">🔔</div>
            <h1 className="text-2xl font-bold text-gray-800 mb-2">Notifications</h1>
            <p className="text-gray-600">Stay updated with kosher community news</p>
          </div>

          {/* Notification Stats */}
          <div className="bg-white rounded-lg shadow-md p-4 mb-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-jewgo-primary">{notifications.length}</div>
                  <div className="text-sm text-gray-600">Total</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-500">{unreadCount}</div>
                  <div className="text-sm text-gray-600">Unread</div>
                </div>
              </div>
              {unreadCount > 0 && (
                <button
                  onClick={markAllAsRead}
                  className="text-jewgo-primary hover:text-jewgo-primary-dark text-sm font-medium"
                >
                  Mark all as read
                </button>
              )}
            </div>
          </div>

          {/* Filter Tabs */}
          <div className="mb-6">
            <div className="flex space-x-2 overflow-x-auto pb-2 scrollbar-hide">
              {[
                { id: 'all', name: 'All', count: notifications.length },
                { id: 'special', name: 'Specials', count: safeFilter(notifications, (n: any) => n.type === 'special').length },
                { id: 'restaurant', name: 'Restaurants', count: safeFilter(notifications, (n: any) => n.type === 'restaurant').length },
                { id: 'update', name: 'Updates', count: safeFilter(notifications, (n: any) => n.type === 'update').length },
                { id: 'reminder', name: 'Reminders', count: safeFilter(notifications, (n: any) => n.type === 'reminder').length }
              ].map((filter) => (
                <button
                  key={filter.id}
                  onClick={() => setActiveFilter(filter.id)}
                  className={`flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                    activeFilter === filter.id
                      ? 'bg-jewgo-primary text-white'
                      : 'bg-white text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  {filter.name} ({filter.count})
                </button>
              ))}
            </div>
          </div>

          {/* Notifications List */}
          {filteredNotifications.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">📭</div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">No Notifications</h3>
              <p className="text-gray-600">You&apos;re all caught up!</p>
            </div>
          ) : (
            <div className="space-y-3">
              {filteredNotifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`bg-white rounded-lg shadow-md p-4 transition-colors ${
                    !notification.read ? 'border-l-4 border-jewgo-primary' : ''
                  }`}
                >
                  <div className="flex items-start space-x-3">
                    {/* Notification Icon */}
                    <div className="text-2xl">{notification.icon}</div>

                    {/* Notification Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-1">
                            <h3 className="font-semibold text-gray-800">{notification.title}</h3>
                            <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getTypeColor(notification.type)}`}>
                              {notification.type}
                            </span>
                          </div>
                          <p className="text-gray-600 text-sm mb-2">{notification.message}</p>
                          <p className="text-gray-500 text-xs">{notification.time}</p>
                        </div>

                        {/* Action Buttons */}
                        <div className="flex items-center space-x-2">
                          {!notification.read && (
                            <button
                              onClick={() => markAsRead(notification.id)}
                              className="text-jewgo-primary hover:text-jewgo-primary-dark p-1"
                              title="Mark as read"
                            >
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                              </svg>
                            </button>
                          )}
                          <button
                            onClick={() => deleteNotification(notification.id)}
                            className="text-red-500 hover:text-red-700 p-1"
                            title="Delete notification"
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Notification Settings */}
          <div className="mt-8 bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Notification Settings</h3>
            <div className="space-y-3">
              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  defaultChecked
                  className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                />
                <span className="text-sm text-gray-700">Special offers and deals</span>
              </label>
              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  defaultChecked
                  className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                />
                <span className="text-sm text-gray-700">New restaurant additions</span>
              </label>
              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  defaultChecked
                  className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                />
                <span className="text-sm text-gray-700">Menu updates</span>
              </label>
              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                />
                <span className="text-sm text-gray-700">Shabbat reminders</span>
              </label>
              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  className="w-4 h-4 text-jewgo-primary border-gray-300 rounded focus:ring-jewgo-primary"
                />
                <span className="text-sm text-gray-700">Certification updates</span>
              </label>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Navigation */}
      <BottomNavigation />
    </div>
  );
} 