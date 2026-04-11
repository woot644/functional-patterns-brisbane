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
        accent: {
          400: '#6BB8E8',
          500: '#4A9FD9',
          600: '#2D7BB8',
        },
        warm: {
          50: '#F8FAFB',
          100: '#EEF4F8',
          200: '#D8E8F0',
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
