/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./static/src/**/*.{html,js}",
    "./templates/**/*.{html,js}",
    'node_modules/preline/dist/*.js'
  ],
  theme: {
    colors: {
      "white":"#FFFFFF",
      "black":{
        5:"#E9E9EA",
        25:"#BABFC2",
        50:"#818A91",
        75:"#47545F",
        100:"#0D1F2D"
      },
      "blue":"#3842FA",
      "green":{
        light:"#A7F3D0",
        dark:"#047857"
      },
      "yellow":{
        light:"#FEF08A",
        dark:"#CA8A04"
      },
      "red":{
        light:"#FECDD3",
        dark:"#BE123C"
      }
    },
    fontFamily:{
      inter: ['Inter', 'sans-serif']
    },
    extend: {},
  },
  plugins: [require('preline/plugin'), require('@tailwindcss/forms'), require('@tailwindcss/forms')],
}