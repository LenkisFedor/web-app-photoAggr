/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,sjs,ts,jsx,tsx}', './components/*'],
  theme: {
    extend: {      
      transitionProperty: {
      'width':'width',
      'position':'position',
      'translate':'translate'
    }
    }
  },
  plugins: []
}
