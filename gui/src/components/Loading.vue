<template>

</template>
<style scoped>
/* 在你的样式文件中，例如 styles.css 或组件的 <style> 标签中 */
::v-deep .custom-loading .el-loading-spinner .path {
  stroke: #29a43f; /* 将加载动画的颜色改为绿色 */
}
</style>
<script>
import {ElLoading} from 'element-plus';
export default {
    data(){
        return {

        };
    },
    methods:{
        startLoading() {
        const loading = ElLoading.service({
            lock: true,
            text: "加载中...",
            customClass:'custom-loading',
            background: "rgba(0, 0, 0, 0.3)"
        });
        return loading;
        },
        endLoading() {
            const loading = this.startLoading();
            loading.close();
        },
    }
}
</script>