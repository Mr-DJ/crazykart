/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        'lol-gold': '#C8AA6E',
        'lol-gold-dark': '#785A28',
        'lol-blue': '#0AC8B9',
        'lol-blue-dark': '#005A82',
        'lol-grey': '#A09B8C',
        'lol-grey-dark': '#463714',
        'lol-black': '#010A13',
        'lol-black-blue': '#0A1428',
        'lol-red': '#EE2D23'
      },
      fontFamily: {
        'heading': ['Cinzel', 'serif'],
        'body': ['system-ui', 'sans-serif']  // Using system font for body text
       }
    },
  },
  plugins: [],
}
