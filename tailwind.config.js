/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Primary JewGo Brand Colors
        jewgo: {
          50: '#f0fdf4',   // Very light mint
          100: '#dcfce7',  // Light mint
          200: '#bbf7d0',  // Lighter mint
          300: '#86efac',  // Light mint
          400: '#4ade80',  // Primary mint green
          500: '#22c55e',  // Medium mint
          600: '#16a34a',  // Darker mint
          700: '#15803d',  // Dark mint
          800: '#166534',  // Very dark mint
          900: '#14532d',  // Darkest mint
          950: '#052e16',  // Near black mint
        },
        
        // Secondary/Neutral Colors
        neutral: {
          50: '#fafafa',
          100: '#f5f5f5',
          200: '#e5e5e5',
          300: '#d4d4d4',
          400: '#a3a3a3',
          500: '#737373',
          600: '#525252',
          700: '#404040',
          800: '#262626',
          900: '#171717',
          950: '#0a0a0a',
        },
        
        // Accent Colors
        accent: {
          blue: '#3B82F6',    // Primary blue
          'blue-dark': '#2563EB',
          green: '#10B981',   // Success green
          'green-dark': '#059669',
          yellow: '#F59E0B',  // Warning yellow
          'yellow-dark': '#D97706',
          purple: '#8B5CF6',  // Purple accent
          'purple-dark': '#7C3AED',
          orange: '#F97316',  // Orange accent
          'orange-dark': '#EA580C',
        },
        
        // Kosher Category Colors (Semantic)
        kosher: {
          meat: '#ef4444',      // Red for meat
          'meat-light': '#fef2f2',
          'meat-dark': '#dc2626',
          dairy: '#3b82f6',     // Blue for dairy
          'dairy-light': '#eff6ff',
          'dairy-dark': '#2563eb',
          pareve: '#f59e0b',    // Yellow for pareve
          'pareve-light': '#fffbeb',
          'pareve-dark': '#d97706',
          unknown: '#6b7280',   // Gray for unknown
          'unknown-light': '#f9fafb',
          'unknown-dark': '#374151',
        },
        
        // Certification Agency Colors
        agency: {
          orb: '#1e40af',       // ORB blue
          'orb-light': '#dbeafe',
          km: '#10b981',        // KM green
          'km-light': '#d1fae5',
          kdm: '#f59e0b',       // KDM yellow
          'kdm-light': '#fef3c7',
          'diamond-k': '#8b5cf6', // Diamond K purple
          'diamond-k-light': '#ede9fe',
        },
        
        // Status Colors
        status: {
          success: '#10b981',
          'success-light': '#d1fae5',
          warning: '#f59e0b',
          'warning-light': '#fef3c7',
          error: '#ef4444',
          'error-light': '#fef2f2',
          info: '#3b82f6',
          'info-light': '#dbeafe',
        },
        
        // Legacy aliases for backward compatibility
        'mint-green': '#A8E6CF',
        primary: '#4ade80',
        secondary: '#374151',
      },
      
      // Extended spacing for better consistency
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      
      // Extended border radius
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
      },
      
      // Extended shadows
      boxShadow: {
        'soft': '0 2px 8px rgba(0, 0, 0, 0.08)',
        'medium': '0 4px 12px rgba(0, 0, 0, 0.12)',
        'strong': '0 8px 25px rgba(0, 0, 0, 0.15)',
        'glow': '0 0 20px rgba(74, 222, 128, 0.3)',
      },
      
      // Extended gradients
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'gradient-jewgo': 'linear-gradient(135deg, #4ade80 0%, #22c55e 100%)',
        'gradient-jewgo-reverse': 'linear-gradient(135deg, #22c55e 0%, #4ade80 100%)',
      },
      
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Inter', 'system-ui', 'sans-serif'],
      },
      
      // Extended animation
      animation: {
        'fade-in-up': 'fadeInUp 0.5s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'filter-pulse': 'filterPulse 0.3s ease-in-out',
        'bounce-gentle': 'bounce 1s ease-in-out infinite',
        'pulse-gentle': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [],
}; 