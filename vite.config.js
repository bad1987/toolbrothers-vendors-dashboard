import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    // https: {
    //   key: path.resolve(__dirname, 'certificates/vendors.toolbrothers.com-selfsigned.key'),
    //   cert: path.resolve(__dirname, 'certificates/vendors.toolbrothers.com-selfsigned.crt')
    // }
  }
})
