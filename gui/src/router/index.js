// 路由的配置文件
import { createRouter, createWebHashHistory } from 'vue-router';
import Home from '../views/Home.vue'
import Create from '../views/Create.vue'
import Help from '../views/Help.vue'
import Setting from '../views/Setting.vue'
import Create2 from '../views/Create2.vue';

// 配置页面相关配置
const routes = [
    {
        path: '/',
        component: Home
    },
    {
        path: '/create',
        name: 'Create',
        component: Create
    },
    {
        path: '/setting',
        component: Setting
    },
    {
        path: '/help',
        component: Help
    },
    {
        path: '/create/detail',
        name: 'Create2',
        component: Create2
    },

]



const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router