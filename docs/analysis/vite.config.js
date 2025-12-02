import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/5d/docs/analysis/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  }
})
