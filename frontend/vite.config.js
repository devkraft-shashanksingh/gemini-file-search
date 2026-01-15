import { defineConfig } from 'vite'

export default defineConfig({
    build: {
        outDir: 'dist',
    },
    server: {
        proxy: {
            '/upload-doc': 'http://localhost:8000',
            '/search': 'http://localhost:8000',
        }
    }
})
