/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx,jsx,js}"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui"],
      },
      colors: {
        brand: {
          DEFAULT: "#38b2ac",
          foreground: "#0f172a"
        },
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
