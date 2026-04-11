/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        dark: {
          950: '#050505',
          900: '#0A0A0A',
          800: '#141414',
          700: '#1E1E1E',
          600: '#2A2A2A',
          500: '#3A3A3A',
        },
        gold: {
          400: '#D4A853',
          500: '#C49A3C',
          600: '#A67C2E',
        },
        warm: {
          50: '#FAF8F5',
          100: '#F5F0E8',
          200: '#E8DFD0',
        },
      },
      fontFamily: {
        heading: ['Poppins', 'sans-serif'],
        body: ['Poppins', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
