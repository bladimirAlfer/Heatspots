/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/templates/**/*.html',  // Indica dónde buscar las clases de Tailwind en tus archivos HTML.
    './src/static/js/**/*.js',     // También puedes agregar archivos JS si usas clases dinámicas.
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
