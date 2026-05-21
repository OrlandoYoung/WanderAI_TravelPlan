module.exports = {
  purge: [
    './public/**/*.html',
    './src/**/*.vue'
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#6366f1'
      },
      borderRadius: {
        'button': '1.5rem'
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
