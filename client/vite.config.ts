import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, path.resolve(__dirname, '..'), '')
  const serverPort = env.PORT ?? process.env.PORT ?? 8082

  return {
    plugins: [react(), tailwindcss()],
    base: process.env.VITE_BASE ?? '/',
    envDir: path.resolve(__dirname, '..'),
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    server: {
      port: 5173,
      proxy: {
        '/v1': `http://localhost:${serverPort}`,
        '/dashboard': `http://localhost:${serverPort}`,
      },
    },
  }
})
