/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1e3a5f',
        'primary-light': '#2a4f7f',
        secondary: '#f47920',
        'secondary-dark': '#d96810',
      },
    },
  },
  plugins: [],
}
