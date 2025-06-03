import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from "axios"


const app = createApp(App)

// 将axios挂载到全局
app.config.globalProperties.$axios = axios
app.config.globalProperties.$loginStatue = false;


// 组件库 ElementPlus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'  // element-plus的所有样式
import 'element-plus/theme-chalk/dark/css-vars.css';// 暗黑模式

app.use(ElementPlus, { size: 'large', zIndex: 3000 })
app.use(router)

import VXETable from 'vxe-table';
import 'vxe-table/lib/style.css';
import XEUtils from 'xe-utils';
import VxeUI from 'vxe-pc-ui'
import 'vxe-pc-ui/lib/style.css'

app.use(VXETable);


// 图标库 ElementPlus
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(`ele-${key}`, component)
}

// 自定义图标库
import SvgIcon from '@/components/SvgIcon/index.vue'
app.component('SvgIcon', SvgIcon)

// 自定义样式
import '@/assets/main.scss'

app.mount('#app')
