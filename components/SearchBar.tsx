'use client';

import { useState, useEffect, useRef } from 'react';

interface SearchBarProps {
  onSearch: (query: string) => void;
  placeholder?: string;
}

export default function SearchBar({ onSearch, placeholder = "Search restaurants, agencies, or dietary preferences..." }: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const searchTimeoutRef = useRef<NodeJS.Timeout>();
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // Clear existing timeout
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }

    // Set new timeout for debounced search
    searchTimeoutRef.current = setTimeout(() => {
      onSearch(query);
    }, 300);

    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, [query]); // Removed onSearch dependency

  const handleClear = () => {
    setQuery('');
    onSearch('');
    inputRef.current?.focus();
  };

  const handleSuggestionClick = (suggestion: string) => {
    setQuery(suggestion);
    onSearch(suggestion);
    setShowSuggestions(false);
    inputRef.current?.focus();
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    setShowSuggestions(value.length > 0);
  };

  const handleFocus = () => {
    setIsFocused(true);
    if (query.length > 0) {
      setShowSuggestions(true);
    }
  };

  const handleBlur = () => {
    setIsFocused(false);
    // Delay hiding suggestions to allow for clicks
    setTimeout(() => setShowSuggestions(false), 200);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      setShowSuggestions(false);
      inputRef.current?.blur();
    }
  };

  const searchSuggestions = [
    { label: 'ORB Certified', value: 'ORB', icon: '✓', color: 'bg-blue-500' },
    { label: 'KM Certified', value: 'KM', icon: '🥛', color: 'bg-green-500' },
    { label: 'KDM Certified', value: 'KDM', icon: '🍽️', color: 'bg-yellow-500' },
    { label: 'Diamond K', value: 'Diamond K', icon: '💎', color: 'bg-purple-500' },
    { label: 'Meat Restaurants', value: 'meat', icon: '🥩', color: 'bg-red-500' },
    { label: 'Dairy Restaurants', value: 'dairy', icon: '🥛', color: 'bg-blue-500' },
    { label: 'Pareve Restaurants', value: 'pareve', icon: '🥬', color: 'bg-green-500' },
    { label: 'Miami Beach', value: 'Miami Beach', icon: '🏖️', color: 'bg-blue-500' },
    { label: 'Hollywood FL', value: 'Hollywood', icon: '🎬', color: 'bg-orange-500' },
    { label: 'Boca Raton', value: 'Boca', icon: '🌴', color: 'bg-green-500' }
  ];

  const filteredSuggestions = searchSuggestions.filter(suggestion =>
    suggestion.label.toLowerCase().includes(query.toLowerCase()) ||
    suggestion.value.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="relative">
      <form onSubmit={(e) => e.preventDefault()}>
        <div className="relative">
          {/* Search Icon */}
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <svg className={`h-5 w-5 transition-colors duration-200 ${isFocused ? 'text-jewgo-primary' : 'text-gray-400'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
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
            className="search-bar pl-12 pr-12 transition-all duration-200 focus:shadow-lg"
            autoComplete="off"
          />

          {/* Right Side Actions */}
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
            {query && (
              <button
                type="button"
                onClick={handleClear}
                className="p-1 text-gray-400 hover:text-jewgo-primary transition-colors duration-200 mr-2"
                title="Clear search"
              >
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            )}
            
            {/* Search Button */}
            <button
              type="submit"
              className="p-1 text-gray-400 hover:text-jewgo-primary transition-colors duration-200"
              title="Search"
            >
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </button>
          </div>
        </div>
      </form>

      {/* Enhanced Search Suggestions */}
      {showSuggestions && (query.length > 0 || isFocused) && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-xl shadow-strong z-50 animate-fade-in-up max-h-80 overflow-y-auto">
          <div className="p-2">
            {query.length > 0 && (
              <div className="text-xs text-gray-500 px-3 py-1 border-b border-gray-100 mb-2">
                Search suggestions for "{query}"
              </div>
            )}
            
            {filteredSuggestions.length > 0 ? (
              <div className="space-y-1">
                {filteredSuggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => handleSuggestionClick(suggestion.value)}
                    className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition-colors duration-200 flex items-center space-x-3"
                  >
                    <span className={`w-2 h-2 ${suggestion.color} rounded-full flex-shrink-0`}></span>
                    <span className="text-sm">{suggestion.icon}</span>
                    <span className="flex-1">{suggestion.label}</span>
                  </button>
                ))}
              </div>
            ) : query.length > 0 ? (
              <div className="px-3 py-2 text-sm text-gray-500">
                No suggestions found for "{query}"
              </div>
            ) : (
              <div className="space-y-1">
                <div className="text-xs text-gray-500 px-3 py-1">Popular searches</div>
                {searchSuggestions.slice(0, 5).map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => handleSuggestionClick(suggestion.value)}
                    className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition-colors duration-200 flex items-center space-x-3"
                  >
                    <span className={`w-2 h-2 ${suggestion.color} rounded-full flex-shrink-0`}></span>
                    <span className="text-sm">{suggestion.icon}</span>
                    <span className="flex-1">{suggestion.label}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
} 