'use client';

interface CategoryNavProps {
  selectedFilters: {
    agency?: string;
    dietary?: string;
    openNow?: boolean;
    category?: string;
    nearMe?: boolean;
    distanceRadius?: number;
  };
  onFilterChange: (key: string, value: any) => void;
  onToggleFilter?: (filterType: 'openNow' | 'nearMe', value: boolean) => void;
  onDistanceChange?: (distance: number) => void;
  onClearAll: () => void;
}

export default function CategoryNav({ selectedFilters, onFilterChange, onToggleFilter, onDistanceChange, onClearAll }: CategoryNavProps) {
  const agencyFilters = [
    { value: 'all', label: 'All Agencies', icon: '🏢' },
    { value: 'ORB', label: 'ORB', icon: '✓', tooltip: 'Orthodox Union Rabbinical Board' },
    { value: 'KM', label: 'KM', icon: '🥛', tooltip: 'Cholov Yisroel only' },
    { value: 'KDM', label: 'KDM', icon: '🍽️', tooltip: 'Not exclusively Cholov Yisroel' },
    { value: 'Diamond K', label: 'Diamond K', icon: '💎', tooltip: 'ORB subsidiary, not Cholov Yisroel' }
  ];

  const dietaryFilters = [
    { value: 'all', label: 'All Types', icon: '🍽️' },
    { value: 'meat', label: 'Meat', icon: '🥩' },
    { value: 'dairy', label: 'Dairy', icon: '🥛' },
    { value: 'pareve', label: 'Pareve', icon: '🥬' }
  ];

  const categoryFilters = [
    { value: 'all', label: 'All Categories', icon: '🏪' },
    { value: 'restaurant', label: 'Restaurants', icon: '🍽️' },
    { value: 'bakery', label: 'Bakeries', icon: '🥖' },
    { value: 'grocery', label: 'Grocery', icon: '🛒' },
    { value: 'catering', label: 'Catering', icon: '🎉' }
  ];

  const hasActiveFilters = selectedFilters.agency || selectedFilters.dietary || selectedFilters.category || selectedFilters.openNow || selectedFilters.distanceRadius;

  const handleFilterClick = (filterType: 'agency' | 'dietary' | 'category', value: string) => {
    const currentValue = selectedFilters[filterType];
    
    // If clicking the same filter that's already selected, remove it (set to 'all')
    if (currentValue === value) {
      onFilterChange(filterType, 'all');
    } else {
      // Otherwise, set the new filter
      onFilterChange(filterType, value);
    }
  };

  const isFilterActive = (filterType: 'agency' | 'dietary' | 'category', value: string) => {
    return selectedFilters[filterType] === value;
  };

  return (
    <div className="bg-white rounded-xl shadow-soft border border-gray-200 p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
        {hasActiveFilters && (
          <button
            onClick={onClearAll}
            className="text-sm text-jewgo-primary hover:text-jewgo-primary/80 font-medium transition-colors duration-200"
          >
            Clear All
          </button>
        )}
      </div>

      <div className="space-y-6">
        {/* Agency Filters */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <svg className="w-4 h-4 mr-2 text-jewgo-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            Certifying Agencies
            <span className="text-xs text-gray-400 ml-2">(click to toggle)</span>
          </h4>
          <div className="grid grid-cols-3 sm:grid-cols-5 gap-2">
            {agencyFilters.map((filter) => (
              <button
                key={filter.value}
                onClick={() => handleFilterClick('agency', filter.value)}
                className={`filter-button w-full ${isFilterActive('agency', filter.value) ? 'active' : ''}`}
                title={filter.tooltip}
              >
                <span className="text-sm">{filter.icon}</span>
                <span className="text-xs sm:text-sm">{filter.label}</span>
              </button>
            ))}
          </div>
          <p className="text-xs text-gray-500 mt-2">
            KM: Cholov Yisroel only • KDM: Not exclusively Cholov Yisroel • Diamond K: ORB subsidiary
          </p>
        </div>

        {/* Dietary Filters */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <svg className="w-4 h-4 mr-2 text-jewgo-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
            </svg>
            Dietary Preferences
            <span className="text-xs text-gray-400 ml-2">(click to toggle)</span>
          </h4>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            {dietaryFilters.map((filter) => (
              <button
                key={filter.value}
                onClick={() => handleFilterClick('dietary', filter.value)}
                className={`filter-button w-full ${isFilterActive('dietary', filter.value) ? 'active' : ''}`}
              >
                <span className="text-sm">{filter.icon}</span>
                <span className="text-xs sm:text-sm">{filter.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Category Filters */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <svg className="w-4 h-4 mr-2 text-jewgo-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            Categories
            <span className="text-xs text-gray-400 ml-2">(click to toggle)</span>
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {categoryFilters.map((filter) => (
              <button
                key={filter.value}
                onClick={() => handleFilterClick('category', filter.value)}
                className={`filter-button w-full ${isFilterActive('category', filter.value) ? 'active' : ''}`}
              >
                <span className="text-sm">{filter.icon}</span>
                <span className="text-xs sm:text-sm">{filter.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Active Filters Summary */}
        {hasActiveFilters && (
          <div className="pt-4 border-t border-gray-100">
            <div className="flex flex-wrap gap-2">
              {selectedFilters.agency && selectedFilters.agency !== 'all' && (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-jewgo-primary/10 text-jewgo-primary">
                  {agencyFilters.find(f => f.value === selectedFilters.agency)?.label}
                  <button
                    onClick={() => onFilterChange('agency', 'all')}
                    className="ml-2 hover:bg-jewgo-primary/20 rounded-full p-0.5"
                  >
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                  </button>
                </span>
              )}
              {selectedFilters.dietary && (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-jewgo-primary/10 text-jewgo-primary">
                  {dietaryFilters.find(f => f.value === selectedFilters.dietary)?.label}
                  <button
                    onClick={() => onFilterChange('dietary', 'all')}
                    className="ml-2 hover:bg-jewgo-primary/20 rounded-full p-0.5"
                  >
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                  </button>
                </span>
              )}
              {selectedFilters.category && selectedFilters.category !== 'all' && (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-jewgo-primary/10 text-jewgo-primary">
                  {categoryFilters.find(f => f.value === selectedFilters.category)?.label}
                  <button
                    onClick={() => onFilterChange('category', 'all')}
                    className="ml-2 hover:bg-jewgo-primary/20 rounded-full p-0.5"
                  >
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                  </button>
                </span>
              )}
              {selectedFilters.openNow && (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-jewgo-primary/10 text-jewgo-primary">
                  Open Now
                  <button
                    onClick={() => onToggleFilter?.('openNow', false)}
                    className="ml-2 hover:bg-jewgo-primary/20 rounded-full p-0.5"
                  >
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                  </button>
                </span>
              )}
              {selectedFilters.distanceRadius && (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-jewgo-primary/10 text-jewgo-primary">
                  {selectedFilters.distanceRadius} miles
                  <button
                    onClick={() => onDistanceChange?.(0)}
                    className="ml-2 hover:bg-jewgo-primary/20 rounded-full p-0.5"
                  >
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                  </button>
                </span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 