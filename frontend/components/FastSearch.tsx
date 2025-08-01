'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { Search, MapPin, Clock, Star, Filter, X } from 'lucide-react';

interface FastSearchProps {
  onSearch: (query: string) => void;
  placeholder?: string;
  className?: string;
  showAdvancedFilters?: boolean;
}

interface SearchSuggestion {
  id: string;
  type: 'category' | 'agency' | 'location' | 'popular';
  title: string;
  subtitle?: string;
  icon: string;
  color: string;
  action: () => void;
}

export default function FastSearch({
  onSearch,
  placeholder = "Search for kosher restaurants, agencies, or locations...",
  className = "",
  showAdvancedFilters = true
}: FastSearchProps) {
  const [query, setQuery] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [suggestions, setSuggestions] = useState<SearchSuggestion[]>([]);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const [showFilters, setShowFilters] = useState(false);
  const [recentSearches, setRecentSearches] = useState<string[]>([]);
  
  const [popularSearches] = useState([
    { text: 'Kosher restaurants near me', icon: '🍽️', color: 'bg-green-500' },
    { text: 'ORB certified', icon: '✓', color: 'bg-blue-500' },
    { text: 'Dairy restaurants', icon: '🥛', color: 'bg-blue-400' },
    { text: 'Meat restaurants', icon: '🥩', color: 'bg-red-500' },
    { text: 'Miami Beach', icon: '🏖️', color: 'bg-yellow-500' },
    { text: 'Boca Raton', icon: '🌴', color: 'bg-green-400' }
  ]);

  const inputRef = useRef<HTMLInputElement>(null);
  const searchTimeoutRef = useRef<NodeJS.Timeout>();

  // Load recent searches from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('jewgo-recent-searches');
    if (saved) {
      try {
        setRecentSearches(JSON.parse(saved));
      } catch (error) {
        console.error('Error loading recent searches:', error);
      }
    }
  }, []);

  // Save recent searches to localStorage
  const saveRecentSearch = useCallback((search: string) => {
    const updated = [search, ...recentSearches.filter(s => s !== search)].slice(0, 5);
    setRecentSearches(updated);
    localStorage.setItem('jewgo-recent-searches', JSON.stringify(updated));
  }, [recentSearches]);

  // Generate search suggestions (fast, local only)
  const generateSuggestions = useCallback((searchQuery: string) => {
    const allSuggestions: SearchSuggestion[] = [];

    // Category suggestions
    const categorySuggestions: SearchSuggestion[] = [
      { text: 'ORB', icon: '✓', color: 'bg-blue-600' },
      { text: 'KM', icon: '🥛', color: 'bg-blue-500' },
      { text: 'Star-K', icon: '⭐', color: 'bg-yellow-500' },
      { text: 'OU', icon: '🕎', color: 'bg-purple-500' },
      { text: 'dairy', icon: '🥛', color: 'bg-blue-400' },
      { text: 'meat', icon: '🥩', color: 'bg-red-500' },
      { text: 'pareve', icon: '🥬', color: 'bg-green-500' },
      { text: 'restaurant', icon: '🍽️', color: 'bg-orange-500' },
      { text: 'bakery', icon: '🥖', color: 'bg-yellow-400' },
      { text: 'catering', icon: '🎉', color: 'bg-purple-400' }
    ]
    .filter(cat => cat.text.toLowerCase().includes(searchQuery.toLowerCase()))
    .map(cat => ({
      id: `category-${cat.text}`,
      type: 'category' as const,
      title: `${cat.text} restaurants`,
      subtitle: `Find ${cat.text} certified establishments`,
      icon: cat.icon,
      color: cat.color,
      action: () => handleSuggestionSelect(cat.text)
    }));

    allSuggestions.push(...categorySuggestions);

    // Agency suggestions
    const agencySuggestions: SearchSuggestion[] = [
      { text: 'ORB', name: 'Orthodox Rabbinical Board', icon: '✓', color: 'bg-blue-600' },
      { text: 'KM', name: 'Kosher Miami', icon: '🥛', color: 'bg-blue-500' },
      { text: 'Star-K', name: 'Star-K Kosher', icon: '⭐', color: 'bg-yellow-500' },
      { text: 'OU', name: 'Orthodox Union', icon: '🕎', color: 'bg-purple-500' },
      { text: 'CRC', name: 'Chicago Rabbinical Council', icon: '🏛️', color: 'bg-gray-600' },
      { text: 'Kof-K', name: 'KOF-K Kosher', icon: '🔒', color: 'bg-green-600' }
    ]
    .filter(agency => agency.text.toLowerCase().includes(searchQuery.toLowerCase()) || agency.name.toLowerCase().includes(searchQuery.toLowerCase()))
    .map(agency => ({
      id: `agency-${agency.text}`,
      type: 'agency' as const,
      title: `${agency.text} certified`,
      subtitle: agency.name,
      icon: agency.icon,
      color: agency.color,
      action: () => handleSuggestionSelect(agency.text)
    }));

    allSuggestions.push(...agencySuggestions);

    // Location suggestions (local)
    if (searchQuery.length > 2) {
      const locationSuggestions: SearchSuggestion[] = [
        { text: 'Miami Beach', state: 'FL', icon: '🏖️', color: 'bg-yellow-500' },
        { text: 'Boca Raton', state: 'FL', icon: '🌴', color: 'bg-green-400' },
        { text: 'Hollywood', state: 'FL', icon: '🎬', color: 'bg-orange-500' },
        { text: 'Aventura', state: 'FL', icon: '🏢', color: 'bg-blue-500' },
        { text: 'Sunny Isles', state: 'FL', icon: '🌅', color: 'bg-pink-500' },
        { text: 'North Miami Beach', state: 'FL', icon: '🏖️', color: 'bg-cyan-500' }
      ]
      .filter(loc => loc.text.toLowerCase().includes(searchQuery.toLowerCase()))
      .map(loc => ({
        id: `location-${loc.text}`,
        type: 'location' as const,
        title: loc.text,
        subtitle: `${loc.state}`,
        icon: loc.icon,
        color: loc.color,
        action: () => handleSuggestionSelect(loc.text)
      }));

      allSuggestions.push(...locationSuggestions);
    }

    return allSuggestions;
  }, []);

  // Handle input change with fast debouncing
  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    setSelectedIndex(-1);

    // Clear existing timeout
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }

    if (value.trim()) {
      searchTimeoutRef.current = setTimeout(() => {
        const newSuggestions = generateSuggestions(value);
        setSuggestions(newSuggestions);
      }, 100); // Very fast - only 100ms delay
    } else {
      setSuggestions([]);
    }
  }, [generateSuggestions]);

  // Handle suggestion selection
  const handleSuggestionSelect = useCallback((suggestion: string) => {
    setQuery(suggestion);
    setShowSuggestions(false);
    saveRecentSearch(suggestion);
    onSearch(suggestion);
  }, [onSearch, saveRecentSearch]);

  // Handle keyboard navigation
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex(prev => Math.min(prev + 1, suggestions.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex(prev => Math.max(prev - 1, -1));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedIndex >= 0 && suggestions[selectedIndex]) {
        suggestions[selectedIndex].action();
      } else if (query.trim()) {
        handleSuggestionSelect(query);
      }
    } else if (e.key === 'Escape') {
      setShowSuggestions(false);
      inputRef.current?.blur();
    }
  }, [suggestions, selectedIndex, query, handleSuggestionSelect]);

  // Handle focus
  const handleFocus = useCallback(() => {
    setIsFocused(true);
    setShowSuggestions(true);
  }, []);

  // Handle blur
  const handleBlur = useCallback(() => {
    setTimeout(() => {
      setIsFocused(false);
      setShowSuggestions(false);
    }, 100);
  }, []);

  // Handle clear
  const handleClear = useCallback(() => {
    setQuery('');
    setSuggestions([]);
    setSelectedIndex(-1);
    inputRef.current?.focus();
  }, []);

  // Handle search submission
  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      handleSuggestionSelect(query);
    }
  }, [query, handleSuggestionSelect]);

  return (
    <div className={`relative ${className}`}>
      <form onSubmit={handleSubmit}>
        <div className="relative">
          {/* Search Icon */}
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <Search className={`h-5 w-5 transition-colors duration-200 ${isFocused ? 'text-blue-500' : 'text-gray-400'}`} />
          </div>

          {/* Search Input */}
          <input
            ref={inputRef}
            type="text"
            placeholder={placeholder}
            value={query}
            onChange={handleInputChange}
            onFocus={handleFocus}
            onBlur={handleBlur}
            onKeyDown={handleKeyDown}
            className="w-full pl-12 pr-20 py-4 bg-white border border-gray-200 rounded-full text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 shadow-sm hover:shadow-md text-base"
            autoComplete="off"
          />

          {/* Right Side Actions */}
          <div className="absolute inset-y-0 right-0 pr-4 flex items-center space-x-2">
            {showAdvancedFilters && (
              <button
                type="button"
                onClick={() => setShowFilters(!showFilters)}
                className={`p-2 rounded-full transition-all duration-200 ${
                  showFilters 
                    ? 'bg-blue-100 text-blue-600' 
                    : 'text-gray-400 hover:text-gray-600 hover:bg-gray-50'
                }`}
                title="Advanced filters"
              >
                <Filter className="w-4 h-4" />
              </button>
            )}
            
            {query && (
              <button
                type="button"
                onClick={handleClear}
                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-full transition-all duration-200"
                title="Clear search"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      </form>

      {/* Fast Suggestions Panel */}
      {showSuggestions && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-xl shadow-xl z-50 max-h-80 overflow-y-auto">
          <div className="p-4">
            {/* Search Results */}
            {query.length > 0 && suggestions.length > 0 && (
              <div className="mb-4">
                <div className="text-xs text-gray-500 px-2 py-1 mb-2 font-medium">
                  Search results for "{query}"
                </div>
                <div className="space-y-1">
                  {suggestions.map((suggestion, index) => (
                    <button
                      key={suggestion.id}
                      onClick={suggestion.action}
                      className={`w-full text-left px-3 py-3 rounded-lg transition-all duration-200 flex items-center space-x-3 ${
                        index === selectedIndex 
                          ? 'bg-blue-50 border border-blue-200' 
                          : 'hover:bg-gray-50'
                      }`}
                    >
                      <div className={`w-8 h-8 rounded-full ${suggestion.color} flex items-center justify-center text-white text-sm flex-shrink-0`}>
                        {suggestion.icon}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="font-medium text-gray-900 truncate">
                          {suggestion.title}
                        </div>
                        {suggestion.subtitle && (
                          <div className="text-sm text-gray-500 truncate">
                            {suggestion.subtitle}
                          </div>
                        )}
                      </div>
                      {suggestion.type === 'location' && (
                        <MapPin className="w-4 h-4 text-gray-400 flex-shrink-0" />
                      )}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Recent Searches */}
            {!query && recentSearches.length > 0 && (
              <div className="mb-4">
                <div className="text-xs text-gray-500 px-2 py-1 mb-2 font-medium flex items-center">
                  <Clock className="w-3 h-3 mr-1" />
                  Recent searches
                </div>
                <div className="space-y-1">
                  {recentSearches.map((search, index) => (
                    <button
                      key={index}
                      onClick={() => handleSuggestionSelect(search)}
                      className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-50 transition-all duration-200 flex items-center space-x-3"
                    >
                      <div className="w-6 h-6 rounded-full bg-gray-100 flex items-center justify-center text-gray-600 text-xs flex-shrink-0">
                        <Clock className="w-3 h-3" />
                      </div>
                      <span className="text-sm text-gray-700 truncate">{search}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Popular Searches */}
            {!query && (
              <div>
                <div className="text-xs text-gray-500 px-2 py-1 mb-2 font-medium flex items-center">
                  <Star className="w-3 h-3 mr-1" />
                  Popular searches
                </div>
                <div className="space-y-1">
                  {popularSearches.map((search, index) => (
                    <button
                      key={index}
                      onClick={() => handleSuggestionSelect(search.text)}
                      className="w-full text-left px-3 py-2 rounded-lg hover:bg-gray-50 transition-all duration-200 flex items-center space-x-3"
                    >
                      <div className={`w-6 h-6 rounded-full ${search.color} flex items-center justify-center text-white text-xs flex-shrink-0`}>
                        {search.icon}
                      </div>
                      <span className="text-sm text-gray-700 truncate">{search.text}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* No Results */}
            {query.length > 0 && suggestions.length === 0 && (
              <div className="text-center py-8">
                <div className="text-gray-500 text-sm mb-2">No results found for "{query}"</div>
                <div className="text-gray-400 text-xs">Try a different search term</div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Advanced Filters Panel */}
      {showFilters && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-xl shadow-xl z-50 p-4">
          <div className="mb-4">
            <h3 className="text-sm font-medium text-gray-900 mb-3">Advanced Filters</h3>
            <div className="grid grid-cols-2 gap-2">
              {[
                { label: 'Open Now', icon: '🕐', color: 'bg-green-500' },
                { label: 'High Rating', icon: '⭐', color: 'bg-yellow-500' },
                { label: 'Near Me', icon: '📍', color: 'bg-blue-500' },
                { label: 'Delivery', icon: '🚚', color: 'bg-purple-500' }
              ].map((filter, index) => (
                <button
                  key={index}
                  className="flex items-center space-x-2 px-3 py-2 rounded-lg border border-gray-200 hover:border-blue-300 hover:bg-blue-50 transition-all duration-200"
                >
                  <div className={`w-4 h-4 rounded-full ${filter.color} flex items-center justify-center text-white text-xs`}>
                    {filter.icon}
                  </div>
                  <span className="text-sm text-gray-700">{filter.label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 