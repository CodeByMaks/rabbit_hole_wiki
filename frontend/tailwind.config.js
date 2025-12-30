/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'rabbit-primary': '#8b5cf6',
        'rabbit-secondary': '#10b981',
        'rabbit-accent': '#f59e0b',
        'graph-node': '#6366f1',
        'graph-link': '#8b5cf6',
      },
      animation: {
        'graph-pulse': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'slide-in': 'slideIn 0.3s ease-out',
      },
    },
  },
  plugins: [],
}