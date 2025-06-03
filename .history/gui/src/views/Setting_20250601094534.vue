<template>
  <div style="height: 100%;">
    <Loading ref="loadingRef"/>
    <TipTab ref="tipRef" /> 
    <h1  class="light_nav" id="nav"  style="border-radius: 3px;line-height: 3em;text-indent: 1em;font-size: 24px;font-family: -apple-system;font-weight: 600;margin-bottom: 15px;">设置</h1>
    <el-tabs type="border-card" class="my-tabs" style="font-family:-apple-system;">
      <el-tab-pane label="基础设置">
        <div class="container light_nav" style="font-family: --apple-system;box-shadow: none;">
          <el-form :model="formData" label-width="150px" style="width: 90%;margin:0 auto; padding:20px;font-family: --apple-system;">
            <el-form-item label="* 工作文件夹位置:" class="dark-font">
              <el-input v-model="formData.workFolder"></el-input>
            </el-form-item>
            <el-form-item label="* 剪映草稿位置:" style="position: relative;">
                <el-input v-model="formData.draftFolder"></el-input>
                <el-button style="position: absolute;right: 0;" color="#6777ef" plain @click="handleGetJYPath">自动获取</el-button>
            </el-form-item>
            <el-form-item label="* 素材网用户名:">
              <el-input v-model="formData.username"></el-input>
            </el-form-item>
            <el-form-item label="* 素材网密码:">
              <el-input v-model="formData.password" type="password"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitSettings" color="#6777ef" style="display: block;width: 70%;font-size: 18px;" plain>确 定</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-tab-pane>
      <el-tab-pane label="常见问题" style="overflow-y: auto;height: calc(100vh - 220px);">
        <div class="container light_nav">
          <h2 class="question">&nbsp;&nbsp;&nbsp;&nbsp;Q:初次使用，如何设置</h2>
          <p class="answer">&nbsp;&nbsp;&nbsp;&nbsp;A:购买软件后，按下图设置:
            <img src="../assets/teach.png" width="70%" style="display: block;" alt="教程">
          </p>
          <h2 class="question">&nbsp;&nbsp;&nbsp;&nbsp;Q:获取剪映草稿目录失败怎么办</h2>
          <p class="answer">&nbsp;&nbsp;&nbsp;&nbsp;A:可能是电脑上没安装剪映。如果确定安装了剪映，可手动获取剪映草稿位置：<br/>
              打开剪映点设置-全局设置-复制草稿位置-粘贴到软件设置
            <img src="../assets/teach1.png" width="60%" style="display: block;" alt="教程1">
            <img src="../assets/teach2.png" width="60%" style="display: block;" alt="教程2">
            <img src="../assets/teach3.png" width="60%" style="display: block;" alt="教程3">
          </p>
          <template v-for="item in QandA">
            <h2 class="question">&nbsp;&nbsp;&nbsp;&nbsp;Q:{{ item.Q }}</h2>
            <p class="answer">&nbsp;&nbsp;&nbsp;&nbsp;A:{{ item.A }}</p>
          </template>
        </div>
      </el-tab-pane>
      <el-tab-pane label="更新日志"  style="overflow-y: auto;height: calc(100vh - 220px);">
        <div class="container light_nav" style="box-shadow: none;">
          <h2 class="question" style="font-weight: 400;">&nbsp;&nbsp;v1.2.0</h2>
          <ul class="answer" style="font-family: '微软雅黑 light';font-size: 16px;">
            <li>增加了素材多样性</li>
            <li>和圆梦素材网联动</li>
          </ul>
          <h2 class="question" style="font-weight: 400;">&nbsp;&nbsp;v1.1.4</h2>
          <ul class="answer" style="font-family: '微软雅黑 light';font-size: 16px;">
            <li>添加“古代人物”模块</li>
            <li>修复字幕与音频长度不对应问题</li>
          </ul>
          <h2 class="question" style="font-weight: 400;">&nbsp;&nbsp;v1.1.3</h2>
          <ul class="answer" style="font-family: '微软雅黑 light';font-size: 16px;">
            <li>修复有时候表格高度无法自适应的bug</li>
          </ul>
          <h2 class="question" style="font-weight: 400;">&nbsp;&nbsp;v1.1.2</h2>
          <ul class="answer" style="font-family: '微软雅黑 light';font-size: 16px;">
            <li>修复部分兼容性bug</li>
          </ul>
          <h2 class="question" style="font-weight: 400;">&nbsp;&nbsp;v1.1.1</h2>
          <ul class="answer" style="font-family: '微软雅黑 light';font-size: 16px;">
            <li>加入了软件本地在线更新</li>
            <li>素材栏目添加：人物-同人系列、人物-怪兽异兽</li>
            <li>编辑草稿页面: 添加了图片快捷收藏</li>
            <li>添加了自动获取剪映草稿目录功能</li>
            <li>设置页面添加了常见问题、更新日志栏目</li>
            <li>优化了黑夜主题样式</li>
          </ul>

        </div>

      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script >

import { ElPopover, ElButton,ElLoading   } from 'element-plus';
import { QuestionFilled,Edit,Folder,Delete,UploadFilled,Refresh  } from '@element-plus/icons-vue'    // 图标
import api from '../api/index'
import TipTab from '../components/TipTab.vue';
import Loading from '../components/Loading.vue';



export default {
  inject: ['globalDark'],  // 声明式注入 
  watch:{
    // 监视 count 属性
    globalDark(newVal, oldVal) {
      if(newVal){
          // 调为暗黑
          this.toggleDarkTheme('dark');
      }else{
          // 调为光
          this.toggleDarkTheme('light');
      }
    }
  },
  data() {
    return {
      formData: {
        workFolder: '',
        draftFolder: '',
        username: '',
        password: ''
      },
      QandA:[
        {
          'Q':'为什么我打开软件显示空白',
          'A':'电脑上缺少WebView2驱动，按照以下教程下载即可:\nhttps://blog.csdn.net/ywd1992/article/details/142463008'
        },
                {
          'Q':'删除收藏的图片后，草稿中一些图片会失效？',
          'A':'为节约空间，编辑草稿时加入的收藏栏图片，都直接引用收藏图片的位置。因此，删除收藏图片后会导致草稿中的该图片失效。\n补救方法：再收藏这张图片即可（注意名称和原来一致）\n同时建议大家作品发布后再删除收藏的图片'
        },
        {
          'Q':'手动重命名草稿文件夹后，草稿所有图片失效？',
          'A':'手动重命名草稿文件夹会导致图片位置找不到，不要轻易尝试。\n如需重命名草稿一定要用软件内的重命名按钮。'
        }
      ]
    };
  },
  components:{
    TipTab,
    Loading
  },
  methods: {
    async handleGetJYPath(){
      // 获取剪映目录
      const path =  await window.pywebview.api.get_jianying_draft_path();
      if(path){
        this.formData.draftFolder = path.replace(/\\/g,'/');
        this.$refs.tipRef.showSuccessTip('自动获取目录成功！');
      }else{
        this.$refs.tipRef.showFailTip('自动获取目录失败！请手动填入！');
      }
    },
    toggleDarkTheme(theme) {
      // 对导航进行处理
      const nav = window.document.querySelector('#nav');
      if(nav) {
          nav.className = `${theme}_nav`;
          const bodys = window.document.querySelectorAll('.container');
          for(let i = 0;i<bodys.length;i++){
            let body = bodys[i];
            body.className = `container ${theme}_nav`
          }
          const tabs = window.document.querySelector('.my-tabs');
          if(this.globalDark){
            tabs.classList.add('dark_nav');
            tabs.classList.remove('light_nav');
          }else{
            tabs.classList.add('light_nav');
            tabs.classList.remove('dark_nav');
          }
      }
    },
    async submitSettings() {
      /* 
        0. 保存json文件
        1. 设置工作文件夹和草稿文件夹（接口）
            (1) 判断地址存在，不存在返回false  ->  提示地址不存在，直接返回
            (2) 创建draft文件夹，以及一系列文件夹
       * 2. 验证账号密码是否正确(用登录接口)
            已完成
      */
      this.$refs.loadingRef.startLoading();
      const workFolder = this.formData.workFolder;
      const draftFolder = this.formData.draftFolder;
      const username = this.formData.username;
      const password = this.formData.password;
      await window.pywebview.api.saveSetting({
        "draftPath": workFolder,
        "jyFilePath":draftFolder,
        "username": username,
        "password": password
      });
      const b = await window.pywebview.api.createWorkdir();
      if(!await window.pywebview.api.veritySetting()){
        this.$refs.loadingRef.endLoading();
        this.$refs.tipRef.showFailTip('路径不存在！请检查路径再试！');
        return;
      }
      api.login(username,password).then(loginResponse=>{
         this.$refs.loadingRef.endLoading();
         const newToken = loginResponse.data.token;
          if (newToken === undefined){
            // 显示登录失败，账号或者密码不匹配，或设备不匹配
            console.log('登录失败，账号或者密码不匹配，或设备不匹配');
            this.$refs.tipRef.showFailTip('登录失败，检查账号密码!');
            localStorage.setItem('token', ''); // 更新 token
            return;
          }
          localStorage.setItem('token', newToken); // 更新 token
          this.$loginStatue = true;
          this.$refs.tipRef.showSuccessTip('登录成功!');
      });
    },
    async init(){
      const ans = await window.pywebview.api.getAllConfig();
      if(!ans){
        this.$refs.showFailTip('配置文件出错！');
        return;
      }
      this.formData.workFolder = ans.draftPath;
      this.formData.draftFolder = ans.jyFilePath;
      this.formData.username = ans.username;
      this.formData.password = ans.password;
    }
  },
  mounted(){
    this.init();
    if(this.globalDark){
      // 调为暗黑
      this.toggleDarkTheme('dark');
    }else{
      // 调为光
      this.toggleDarkTheme('light');
    }
  }
};
</script>

<style scoped>
.question {
  border-bottom: 2px solid #ccc;
  padding-bottom: 10px;
}
.answer {
  white-space: pre-line;
  line-height: 1.5em;
  font-size: 20px;
  margin-bottom: 40px;
}

::v-deep .el-tabs__nav-scroll .el-tabs__nav .el-tabs__item {
  font-family: '微软雅黑';
  font-size: large;

}
::v-deep .el-tabs__nav-scroll .el-tabs__nav .el-tabs__item.is-active  {
  color: #6777ef !important;
}
::v-deep .my-tabs .el-tabs__nav-scroll .el-tabs__nav .el-tabs__item:hover  {
  color: #6777ef !important;
}
::v-deep .my-tabs.dark_nav .el-tabs__nav-scroll .el-tabs__nav .el-tabs__item {
  color: white;
  background-color: rgba(18, 18, 29,0.8);
}
::v-deep .my-tabs.dark_nav .el-tabs__nav-scroll .el-tabs__nav .el-tabs__item.is-active  {
  color: #6777ef !important;
  background-color: rgba(28, 28, 39);
  border-left: 1px solid #555;
  border-right: 1px solid #555;
}
::v-deep .my-tabs.dark_nav  .el-tabs__header .el-tabs__nav-wrap .el-tabs__nav-scroll{
  background-color: rgba(28, 28, 39);
}
/* 修改标签栏背景色 */
.el-tabs__header {
  background: #f5f5f5;
}
::v-deep .el-form-item__label{
  font-size: 16px;     /* 字号调整 */
  font-family: '微软雅黑 light';
  color: black;
}
::v-deep .dark_nav .el-form-item__label{
  color: white;      /* 红色字体 */
}
</style>