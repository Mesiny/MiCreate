import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { viteObfuscateFile } from 'vite-plugin-obfuscator';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    viteObfuscateFile({
      include: ['src/**/*.js'], // 指定需要混淆的文件路径
      exclude: ['node_modules/**'], // 排除无需混淆的文件
      obfuscatorOptions: {
        compact: true, // 压缩代码
        controlFlowFlattening: true, // 控制流平坦化
        deadCodeInjection: true, // 插入假代码
        debugProtection: true, // 防止调试
        disableConsoleOutput: true, // 禁用 console 输出
        identifierNamesGenerator: 'hexadecimal', // 混淆变量名
        renameGlobals: true, // 混淆全局变量
        selfDefending: true, // 保护混淆后的代码
        stringArrayEncoding: ['rc4'], // 字符串加密
        unicodeEscapeSequence: false // 不使用 Unicode 转义
      }
    })
  ],
  // 配置跨域
  server: {
    proxy: {
      '/character': {
        target: 'https://mxjbh.cn',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/character/, '/character')
      },
      '/static': {
        target: 'https://mxjbh.cn',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/static/, '/static')
      },
      '/assets': {
        target: 'https://mxjbh.cn',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/static/, '/assets')
      }

    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },

  build: {
    sourcemap: false,
    chunkSizeWarningLimit: 1500, // 块大小警告的限制（以 kbs 为单位）
    rollupOptions: {
      output: {
        // 分解块，将大块分解成更小的块
        manualChunks(id) {
          if (id.includes('node_modules')) {
            return id.toString().split('node_modules/')[1].split('/')[0].toString()
          }
        },
        // 将不同的文件放在不同的文件下
        chunkFileNames: (chunkInfo) => {
          const facadeModuleId = chunkInfo.facadeModuleId ? chunkInfo.facadeModuleId.split('/') : []
          const fileName = facadeModuleId[facadeModuleId.length - 2] || '[name]'
          return `js/${fileName}/[name].[hash].js`
        }
      }
    }
  }
})
