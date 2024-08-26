import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'

// https://vitejs.dev/config/
export default defineConfig({
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: '@import "@facade/core_style.scss";'
      }
    }
  },
  plugins: [
    vue(),
    vuetify(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@facade': fileURLToPath(new URL('./trame-facade/trame_facade', import.meta.url)),
    }
  },
  server: {
    hmr: {
      clientPort: 5173
    }
  },
})
