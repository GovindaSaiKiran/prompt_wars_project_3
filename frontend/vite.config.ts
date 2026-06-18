// purpose: Frontend build config | enforces: Efficiency-first
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      thresholds: {
        lines: 98,
        functions: 98,
        branches: 98,
        statements: 98
      }
    }
  }
})
