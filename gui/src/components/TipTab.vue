<template>
    <div style="display: block;min-width: 100px;margin: 0 auto;position: fixed;top: 10px;left: 50%;transform: translateX(-50%);">
        <transition name="slide-fade">
          <el-alert :title="successTip" type="success" center show-icon :closable="false" v-if="operateSuccess"/>
        </transition>
        <transition name="slide-fade">
          <el-alert :title="failTip" type="error" center show-icon :closable="false" v-if="operateFail"/>
        </transition>
      </div>
</template>
<style scoped>
/* 定义提示框进入和离开的动画 */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s ease-in;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}
</style>
<script>
export default {
  data() {
    return {
        operateSuccess:false,
        operateFail:false,
        successTip:'操作成功!',
        failTip:'操作失败！',
    };
  },
  methods: {
    showSuccessTip(tipWord){
      /* 1.使得op..Success = true,op..Success = false
       * 2.3s后使得op..Success = false
      */
      if(arguments.length != 0 ){
        this.successTip = tipWord;
      }
      this.operateSuccess = true;this.operateFail = false;
      setTimeout(()=>{
        this.operateSuccess = false;
        this.successTip = '操作成功!'
      },2000);
    },
    showFailTip(tipWord){
      if(arguments.length != 0 ){
        this.failTip = tipWord;
      }
      this.operateFail = true;this.operateSuccess = false;
      setTimeout(()=>{
        this.operateFail = false;
        this.failTip = '操作失败!'
      },2000);
    },
  }
}
</script>