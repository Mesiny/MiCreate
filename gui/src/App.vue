<template>
  <div class="">
        <BtnUpdate></BtnUpdate>
        <div id="app" style="display: flex;width: 100%;">
        <!-- 垂直导航栏 -->
        <el-menu ref="menuRef" default-active="1" :class="`el-menu-vertical-demo text-space ${dark?'my-dark-menu':''}` " :collapse="isCollapse" 
        @mouseenter="openCollapse" @mouseleave="closeCollapse" @select="handleSelect"
          active-text-color="#6777ef" style="z-index: 1;height: 100vh;float: left;font-weight: 400;font-family: --apple-system;position: relative;">
            <el-menu-item class="el-menu-item-custom-size" index="1">
              <el-icon size="150px"><HomeFilled /></el-icon>
              <template #title style="width: 100%;display: flex;justify-content: center;">主页</template>
            </el-menu-item>
            <el-menu-item class="el-menu-item-custom-size" index="2">
              <el-icon size="150px"><icon-menu /></el-icon>
              <template #title>创作</template>
            </el-menu-item>
            <el-menu-item class="el-menu-item-custom-size" index="3">
             <el-icon size="150px">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 1024 1024"><path fill="currentColor" d="M764.416 254.72a351.7 351.7 0 0 1 86.336 149.184H960v192.064H850.752a351.7 351.7 0 0 1-86.336 149.312l54.72 94.72l-166.272 96l-54.592-94.72a352.64 352.64 0 0 1-172.48 0L371.136 936l-166.272-96l54.72-94.72a351.7 351.7 0 0 1-86.336-149.312H64v-192h109.248a351.7 351.7 0 0 1 86.336-149.312L204.8 160l166.208-96h.192l54.656 94.592a352.64 352.64 0 0 1 172.48 0L652.8 64h.128L819.2 160l-54.72 94.72zM704 499.968a192 192 0 1 0-384 0a192 192 0 0 0 384 0"/></svg>
              </el-icon>
              <template #title>设置</template>
            </el-menu-item>
            <!-- <el-menu-item class="el-menu-item-custom-size" index="4">
            <el-icon size="150px"><HelpFilled /></el-icon>
            <template #title>购买软件</template>
            </el-menu-item> -->
            <el-menu-item class="el-menu-item-custom-size" index="5" style="width: 100%;;position: absolute;bottom: 0px;" @click="turnDark">
            <el-icon size="150px"><Sunny v-if="!dark" /><Moon v-else /></el-icon>
            <template #title>主题</template>
            </el-menu-item>
            <div class="indicator" :style="movebar">
                <div class="movebar"></div>
            </div>
        </el-menu>
        <!-- 垂直导航栏结束 -->
        <!-- 路由页面 -->
        <nav id="bg" style="height: 80px;width: 100%;position: absolute;top: 0;left: 0;z-index: 0;"></nav>
        <div  style="float: right;flex: 1;margin-left: 2%;margin-right: 2%;z-index: 1;">
            <transition name="page-transition">
                <router-view style="margin-top: 40px;"></router-view>
            </transition>
        </div>
        <!-- 路由页面结束 -->
    </div>
  </div>
</template>

<script setup>
import { RouterLink, useRouter } from 'vue-router';
import { onMounted,provide  } from 'vue';
const router = useRouter();
import HelloWorld from './components/HelloWorld.vue'
import api from './api/index'
import BtnUpdate from './components/BtnUpdate.vue'

import { ref,computed,watch} from 'vue'
import {
  House,
  Menu as IconMenu,
  Help,
  Setting,
  HomeFilled,
  HelpFilled,
  Sunny,
  Moon
} from '@element-plus/icons-vue'    // 图标

/*
 *导航栏部分
 */
const dark = ref(false);
const globalDark = ref(false) // 使用ref保持响应式
provide('globalDark', globalDark) // 提供变量（建议用Symbol定义唯一key）


//  css样式 控制movebar块
const indicatorPosition = ref(0);  // 初始位置为 0px
const movebar = computed(() => ({
  transition: 'transform 0.3s ease', // 添加平滑过渡效果
  transform: `translateY(${indicatorPosition.value}px)`,
}));
const turnDark = () => {
  dark.value = !dark.value
  globalDark.value = dark.value;
}
const handleSelect = (key, keyPath) => {
    let index = Number(key);
    if(index==5) return;
    if(index==1)    router.push('/#/'); 
    if(index==2)    router.push('/create'); 
    if(index==3)    router.push('/setting'); 
    if(index==4)    router.push('/help'); 
    indicatorPosition.value = (index-1)*71;
    // 改变选中状态
}
//  导航栏是否展开
const isCollapse = ref(true);
const openCollapse = (event)=>{
    isCollapse.value = false
}
const closeCollapse =(event)=>{
    isCollapse.value = true
}
watch(dark, (newValue, oldValue) => {
  const html = document.documentElement;
  const body = document.body;
  const bgnav = document.querySelector('#bg');
  if (newValue) {
    html.style.backgroundColor = 'rgb(8,8,8)';
    body.style.backgroundColor = 'rgb(8,8,8)';
    bgnav.style.backgroundColor = 'rgb(8,8,8)';
    window.pywebview.api.set_dark(true);
  } else {
    html.style.backgroundColor = 'white';
    body.style.backgroundColor = 'white';
    bgnav.style.backgroundColor = '#6777ef'
    window.pywebview.api.set_dark(false);
  }
});

// 使用 onMounted 生命周期钩子
onMounted(() => {
  // 在这里可以执行 DOM 操作或其他初始化逻辑
  // 打开app自动登录
  localStorage.setItem('token', ''); // 更新 token
  console.log('token已清空');
  window.addEventListener('pywebviewready', () => {
    window.pywebview.api.get_software_setting().then(dark=>{
      // 设置全局变量为dark
      if(dark){
        // 点击切换黑夜白天
        handleSelect(5, '');
        turnDark();
      }
    });
    window.pywebview.api.getUserInfo().then(user=>{
    api.login(user.username,user.password).then(loginResponse=>{
          console.log(loginResponse);
          const newToken = loginResponse.data.token;
          if(newToken){
            localStorage.setItem('token', newToken); // 更新 token
            console.log('登录成功');
          }else{
            localStorage.setItem('token', ''); // 更新 token
          }
        });
    });
  });
  });



</script>

<style>
#bg {
    background-color: #6777ef;
}
/* 覆盖 Element Plus 的 CSS 变量 */
.my-dark-menu {
  --el-menu-bg-color: #1b1b1c; /* 背景颜色 */
  --el-menu-text-color: #ffffff; /* 文字颜色 */
  --el-menu-hover-bg-color: #2c3137; /* 鼠标悬停背景颜色 */
  --el-menu-active-color: #ffffff; /* 激活状态文字颜色 */
  --el-menu-border-color: #3a3f46; /* 边框颜色 */
}
.el-menu-item {
  font-family: 'SansHans-medium';
  font-weight: 700;
  font-size: medium;
}
/* 滑动动画 */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.5s ease;
}

.slide-enter-from {
  transform: translateX(100%);
}

.slide-leave-to {
  transform: translateX(-100%);
}
/* 定义进入动画开始时的样式，页面组件初始隐藏时的状态 */
.page-transition-enter-from {
  opacity: 0;
  transform: translateY(30%);
}

/* 进入动画执行时的样式，让页面组件逐渐显示并移动到正确位置 */
.page-transition-enter-active {
  transition: all 0.5s ease;
}

/* 进入动画结束时的样式，页面组件完全显示的状态 */
.page-transition-enter-to {
  opacity: 1;
  transform: translateY(0);
}

/* 离开动画开始时的样式，页面组件完全显示时的状态 */
.page-transition-leave-from {
  opacity: 1;
  transform: translateY(0);
}

/* 离开动画执行时的样式，让页面组件逐渐隐藏并移出屏幕 */
.page-transition-leave-active {
  transition: all 0.3s ease;
}

/* 离开动画结束时的样式，页面组件完全隐藏的状态 */
.page-transition-leave-to {
  opacity: 0;
  transform: translateY(30%);
}
.text-space{
    letter-spacing: 2px;
}
.el-menu{
    position: relative;
}
.el-menu-vertical-demo {
    height: 800px;
      /* border-top-right-radius: 10px 10px; */
    overflow: hidden;
}
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 150px;

}
.el-menu-vertical-demo li {
  text-indent: 1.5em;
  height: 70px;
}
.indicator{
    display: flex;
    justify-content: center; /* 水平居中 */
    align-items: center; /* 垂直居中 */
    position: absolute;
    top: 8px;
    left: 5px;
    width: 5px; /* 根据实际需求调整宽度 */
    height: 55px; /* 根据实际需求调整高度 */
}
.indicator .movebar{
    width: 80%;
    height: 60%;
    background-color: #6777ef;
    border-radius: 30%;
}

</style>
