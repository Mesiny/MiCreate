<template>
  <div>
    <TipTab ref="tipRef" /> 
    <el-dialog v-model="isSelect" width="600" top="5%" :title="'收藏'+(isSelectImg?'图片':'Psd')">
      <selectFavImage ref="selectFavImageRef" @favorSuccess="favorSuccess" @closeDialog="isSelect=false" v-if="isSelectImg" :name="name" :base64="base64_url"/>
      <selectFavPsd ref="selectFavPsdRef" @favorSuccess2="favorSuccess" @closeDialog="isSelect=false" v-if="!isSelectImg" :name="name" :img="img" :psdUrl="url"/>
    </el-dialog>
  </div>
  <div style="min-height:400px;" class="dialog-content">
    <Loading ref="loadingRef"/>
    <!-- <input type="file" @change="handleFileUpload" accept=".psd" class="ipt"> -->
    <div class="left" style="position: relative;;height:384px;width: 550px;display: inline-block;border: 1px solid black;overflow: hidden;">
      <canvas class="xxx" width="1920" height="1080" style="margin-left:-10px ;transform: scale(0.3);transform-origin: top left;background-color: transparent;"></canvas>
      <el-row style="position: absolute;width: 350px;;bottom:-20px;;display: flex;justify-content: space-around;left: 50%;transform:translate(-50%, 0);padding-bottom: 30px;">
        <el-button type="success" plain v-if="add_bool" @click="addAsset">加入素材</el-button>  
        <el-button color="#f18cb9" plain @click="handleFavImg" >收藏图片</el-button>
        <el-button color="#db6a21" plain @click="handleFavPsd" :disabled="!fav_bool">收藏psd</el-button>
      </el-row>
    </div>
    <div class="right" style="width: 350px;display: inline-block;border: 1px solid #ccc;margin-left:0px ;">
      <el-input
        v-model="filterText"
        style="width: 100%"
        placeholder="搜索"
      />
      <el-tree
        ref="treeRef"
        style="max-width: 600px"
        class="filter-tree"
        :data="data"
        :props="defaultProps"
        node-key="id"
        accordion
        :filter-node-method="filterNode"
      >
          <template #default="{ node, data }">
            <span class="custom-tree-node">
              <span style="font-size: medium;">{{ node.label }}</span>&ensp;
              <el-switch
                style="--el-switch-on-color: #13ce66;"
                size="medium"
                v-model="data.visable"
                @change="handleSwitchChange(data)"
              ></el-switch>
              <el-popover
                placement="right-start"
                :width="200"
                trigger="hover"
                content=""
              >
                <template #reference>
                  <img v-if="(!data.children)&&data.name!='背景'&&data.base64" :src="data.base64" style="margin-left: 5px;height: 25px;width: 25px;">
                </template>
                <template #default>
                  <img v-if="(!data.children)&&data.name!='背景'" :src="data.base64" style="width: 100%;">
                </template>
              </el-popover>
            </span>
          </template>
      </el-tree>
    </div>
  </div>
</template>
<style scoped>
.dialog-content {
  flex: 1;
  overflow-y: auto; /* 内容超出时显示滚动条 */
  padding: 20px;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}
  .aa {
    float: left;
  }
  .ipt {
    display: block;
  }
  .right {
    float: right;
    width: 300px;
    margin-left: 20px;
  }
  .diving-suit {
  padding: 20px;
  border-radius: 8px;
  max-width: 300px;
  margin: 0 auto;
}

.el-tree {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
}

.el-tree-node__content {
  padding: 2px 0;
}

.el-tree-node__label {
  font-size: 14px;
  color: #333;
}
.showimg {
  position: relative;
}
</style>
<script>
import { readPsd  } from 'ag-psd';
import Loading from '../components/Loading.vue';
import selectFavImage from './selectFavImage.vue';
import selectFavPsd from './selectFavPsd.vue';
import TipTab from '../components/TipTab.vue';

export default {
  data() {
    return {
      psd: {},
      data: [],
      filterText: '',
      defaultProps: {
        children: 'children',
        label: 'name',
      },
      isSelectImg:true,
      base64_url:"",
      isSelect:false
    };
  },
  components: {
      Loading,
      selectFavImage,
      selectFavPsd,
      TipTab
  },
  props: {
    url: {
      type: String,
      required: true,
      default: ""
    },
    add_bool:{
      type: Boolean,
      required: false,
      default: true
    },
    fav_bool:{
      type: Boolean,
      required: false,
      default: true
    },
    img:{
      type: String,
      required: false,
      default: ''
    },
    name:{
      type: String,
      required: false,
      default: ''
    },
    draft_name:{
      type: String,
      required: false,
      default: ''
    },
  },
  watch: {
    filterText(val) {
      console.log(val);
      if (this.$refs.treeRef) {
        this.$refs.treeRef.filter(val);
      }
    },
  },
  methods: {
    async addAsset(){
      /* 0.导出图片，保存图片到素材库 saveAsset(self,file_data,filename,size,draft_path) 命名为name+.png
      *  1.返回新名字filename，组合成url
      *  2.使父元素触发事件addAsset成功
      *  3.使爷爷元素触发事件addAsset成功，添加到草稿文件中
      */ 
      const cns = document.querySelector('.xxx');
      const file_data = cns.toDataURL('image/png');
      if(!this.draft_name) return;
      const response =  await window.pywebview.api.saveAsset(file_data,this.name+'.png',0,this.draft_name);
      if(response.status == 'success'){
          // 计算url,并且指定url
          const name = response.name;
          const url = 'http://localhost:6500' + '/images/jbh/' + this.draft_name + '/' + name;
          this.$emit("addAsset",url);
      }else{
        return;
      }


    },
    favorSuccess(){
      console.log('收藏成功');
      this.isSelect = false;
      this.$refs.tipRef.showSuccessTip('操作成功！');
    },
    async handleFavImg(){
      if((!await window.pywebview.api.veritySetting())||(!localStorage.getItem('token'))){
        this.$refs.tipRef.showFailTip('操作失败！请检查设置！');
        return;
      }
      console.log('收藏图片启动');
      // 设置prop属性
      this.$refs.loadingRef.startLoading();
      const cns = document.querySelector('.xxx');
      this.base64_url = cns.toDataURL('image/png');
      this.$refs.loadingRef.endLoading();
      this.isSelect = true;
      this.isSelectImg = true;
    },
    async handleFavPsd(){
      if((!await window.pywebview.api.veritySetting())||(!localStorage.getItem('token'))){
        this.$refs.tipRef.showFailTip('操作失败！请检查设置！');
        return;
      }
      console.log('收藏PSD启动');
      this.isSelect = true;
      this.isSelectImg = false;
    },
    // psd格式转换函数
    transformData(data) {
      // 查找data中是否有背景，有的话默认关闭
      // 如果 data 是数组，遍历数组中的每个对象
      if (Array.isArray(data)) {
        return data.map(item => this.transformData(item));
      }
      // 如果 data 是对象，处理其属性
      if (typeof data === 'object' && data !== null) {
        const newData = { ...data };

        // 如果对象有 hidden 属性，将其转换为 visable
        if ('hidden' in newData) {
          newData.visable = !newData.hidden; // 将 hidden 的值取反并赋值给 visable
          delete newData.hidden; // 删除原来的 hidden 属性
          // 如果名字为背景，则newData.visable = false
          if(newData.name == '背景') newData.visable = false;
        }

        // 递归处理子节点
        if (newData.children && Array.isArray(newData.children)) {
          newData.children = this.transformData(newData.children);
        }else{
          // console.log(newData.name);
          // 对newData进行修改
          if(newData.canvas)
            newData.base64 = newData.canvas.toDataURL();
          else
            newData.base64 = ''
        }

        return newData;
      }

      // 如果 data 不是对象或数组，直接返回
      return data;
    },
    // Switch状态改变->重新渲染
    handleSwitchChange() {
      // 渲染到画板中
      setTimeout(() => {
        const cns = document.querySelector('.xxx');
        this.drawPsd(cns, this.psd);  // 注意参数是psd文件，要保证psd文件实时更新
      }, 100);
    },
    // 过滤节点
    filterNode(value, data) {
      if (!value) return true;
      return data.name.includes(value);
    },
    // 画图片
    drawPsd(canvas, psd) {
      console.log(psd);
      const ctx = canvas.getContext('2d');
      // 清空画布
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      // canvas.width= psd.width
      // canvas.height = psd.height
      // 递归绘制图层
      const size = {
        width: psd.width,
        height: psd.height,
      };
      psd.children.forEach((child) => {
        this.drawLayer(ctx, child, canvas, size);
      });
    },
    // 画图层
    drawLayer(ctx, layer, canvas, size) {
      // console.log(layer);
      if (!layer.visable) return; // 如果图层不可见，跳过
      // 如果当前图层有 canvas 数据，直接绘制
      if (layer.canvas) {
        const left = Math.round(layer.left / size.width * canvas.width);
        const top = Math.round(layer.top / size.height * canvas.height);
        const right = Math.round(layer.right / size.width * canvas.width);
        const bottom = Math.round(layer.bottom / size.height * canvas.height);
        ctx.drawImage(layer.canvas, left, top, right-left, bottom-top);
      }
      // 如果当前图层有子图层，递归绘制
      if (layer.children) {
        layer.children.forEach((child) => this.drawLayer(ctx, child, canvas, size));
      }
    },
    // 绑定上传文件事件
    async handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = async (e) => {
          try {
            // 读取文件内容 e.target.result即为arrayBuffer格式
            const arrayBuffer = e.target.result;
            // 使用 ag-psd 的 readPsd 函数解析文件
            this.psd = await readPsd(arrayBuffer);
            this.psd = this.transformData(this.psd);
            this.data = this.psd.children;
            const cns = document.querySelector('.xxx');
            this.drawPsd(cns, this.psd);  // 注意参数是psd文件，要保证psd文件实时更新
          } catch (error) {
            console.error('Error parsing PSD file:', error);
          }
        };
        reader.readAsArrayBuffer(file);
      }
    },
    async loadPsd(){
      this.$refs.loadingRef.startLoading();
      const res = await fetch(this.url);
      if(res.ok){
        this.$refs.loadingRef.endLoading();
        console.log(res);
        const arrayBuffer = await res.arrayBuffer();
        const psd = readPsd(arrayBuffer);
        console.log(psd);
        this.psd = psd;
        // 根据psd长宽设置画板长宽
        const cns = window.document.querySelector('.xxx');
        cns.width = psd.width;
        cns.height = psd.height;
        // 修改left
        const left = window.document.querySelector('.left');
        left.style.width = `${Math.floor(psd.width/1920*550)}px`;
        left.style.height = `${Math.floor(psd.height/1080*384)}px`;
        console.log(cns);
        this.psd = this.transformData(this.psd);
        this.data = this.psd.children;
        this.drawPsd(cns, this.psd);  // 注意参数是psd文件，要保证psd文件实时更新
        this.downloadImage();
      }else{
        console.log('数据错误!');
        this.$refs.loadingRef.endLoading();
      }
      
    },
    // 下载图片
    downloadImage(){
      const cns = document.querySelector('.xxx');
      const base64 = cns.toDataURL('image/png');
      // window.pywebview.api.saveAsset(base64,'111.png',222,'111');
    }
  },
  mounted(){
    console.log('mounted触发');
    this.loadPsd();
    
  }
};
</script>