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
        jewgo: {
          primary: '#4ade80', // Light mint green from logo
          secondary: '#374151', // Dark grey from logo
          accent: '#10b981', // Darker green
          light: '#f0fdf4', // Very light green
        },
        'mint-green': '#A8E6CF', // Exact mint green from logo
        kosher: {
          meat: '#ef4444', // Red for meat
          dairy: '#3b82f6', // Blue for dairy
          pareve: '#f59e0b', // Yellow for pareve
          unknown: '#6b7280', // Grey for unknown
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}; 