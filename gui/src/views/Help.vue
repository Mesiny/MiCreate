<template>
  <div>
    <h1 class="light_nav" id="nav"  style="border-radius: 3px;line-height: 3em;text-indent: 1em;font-size: 24px;font-family: -apple-system;font-weight: 600;margin-bottom: 15px;">购买软件</h1>
    <div class="light_nav" id="main-body"  style="width: 100%;height: 450px;border-radius: 4px;">
      <div style="height: 10px;"></div>
      <div style="width: 350px;margin: 20px auto;padding: 20px;" class="xx">
        <img src="../assets/QRC.png" style="width: 100%;" alt="购买软件">
      </div>
    </div>
  </div>
</template>

<script>
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
  data () {
    return {
      
    }
  },
  methods:{
    toggleDarkTheme(theme) {
      // 对导航进行处理
      const nav = window.document.querySelector('#nav');
      if(nav) {
          nav.className = `${theme}_nav`;
          const mainbody = window.document.querySelector('#main-body');
          mainbody.className = `${theme}_nav`;
      }
    },
  },
  mounted(){
    if(this.globalDark){
        // 调为暗黑
        this.toggleDarkTheme('dark');
    }else{
        // 调为光
        this.toggleDarkTheme('light');
    }
  }
}
</script>
<style scoped>
.xx {
  border-radius:20px ;
  border: 2px dashed var(--el-border-color);
}
</style>