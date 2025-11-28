import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f5f9ff',
          100: '#e0edff',
          200: '#bfd8ff',
          300: '#8eb8ff',
          400: '#5890ff',
          500: '#2f6afe',
          600: '#1f4dda',
          700: '#1a3eb0',
          800: '#19358b',
          900: '#1a326f',
        },
        success: '#3cc987',
        warning: '#ffb347',
        danger: '#ff6b6b',
      },
      boxShadow: {
        card: '0 10px 45px rgba(15, 23, 42, 0.08)',
      },
    },
  },
  plugins: [],
}

export default config
