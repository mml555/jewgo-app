import React, { useState, useEffect, useCallback } from 'react';

// Test component to verify our infinite loop fix
function TestSearchComponent() {
  const [query, setQuery] = useState('');
  const [searchCount, setSearchCount] = useState(0);

  // This should be stable with useCallback
  const handleSearch = useCallback((query: string) => {
    console.log('=== handleSearch called - setting currentPage to 1 ===');
    setSearchCount(prev => prev + 1);
  }, []);

  // Simulate the EnhancedSearch component's useEffect
  useEffect(() => {
    if (query.trim()) {
      const timeout = setTimeout(() => {
        handleSearch(query);
      }, 500);
      return () => clearTimeout(timeout);
    }
  }, [query]); // Removed handleSearch from dependencies

  return (
    <div>
      <h2>Test Infinite Loop Fix</h2>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Type to test search..."
      />
      <p>Search count: {searchCount}</p>
      <p>Query: {query}</p>
    </div>
  );
}

export default TestSearchComponent; 