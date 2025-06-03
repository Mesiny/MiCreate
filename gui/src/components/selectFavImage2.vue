<template>
    <div>
      <TipTab ref="tipRef" /> 
      <!-- {{ url }} -->
        <el-popover ref="popover" placement="bottom" v-model:visible="popoverVisible" trigger="click" width="300">
            <template #reference>
              <el-button type="primary">新增分类</el-button>
            </template>
            <template #default>
              <span>新建分类</span>
              <el-input v-model="newKindName" placeholder="请输入收藏分类名称" style="margin: 10px 0px;"></el-input>
              <el-button type="danger" @click="popoverVisible=false" size="medium">取消</el-button>
              <el-button type="success" @click="addKind" size="medium" :disabled="newKindName?false:true">确认</el-button>
            </template>
        </el-popover>
        <div style="margin: 15px 0px;width: 100%;">
        <el-select v-model="selectKind" placeholder="请选择分类">
          <el-option v-for="item in kinds" :key="item.value" :label="item.label" :value="item.value">
            <span style="float: left">{{ item.label }}</span>
            <span style="float: right;color: red;font-size: 13px;" @click="deleteKind(item.value)">
              删除
            </span>
          </el-option>
        </el-select>
        <el-input v-model="imageName" placeholder="请输入收藏图片名称"></el-input>
        <div style="margin: 10px;">
          <el-button type="primary" @click="confirm" :disabled="(selectKind&&imageName)?false:true">确认</el-button>
          <el-button @click="cancel">取消</el-button>
        </div>

      </div>
    </div>
</template>

<script >
import TipTab from './TipTab.vue';

export default {
  props: {
      url: {
        type: String,
        required: true,
        default: ""
      },
      name: {
        type: String,
        required: false,
        default: ""
      }
  },
  components: {
    TipTab
  },
  watch:{
    name(newVal){
      if(newVal&&(newVal!='添加网络素材图片')){
        this.imageName = newVal.replace(/\.png/g,  '');
      }else{
        this.imageName = '';
      }
    }
  },
  data(){
    return {
      selectKind:'',
      imageName :'',
      kinds:[
      ],
      popoverVisible:false,
      newKindName:''
    }
  },
  methods:{
    addKind(){
      if(!this.newKindName) return;
      // 添加文件夹，kinds对象push一类
      const path = 'myImage/' + this.newKindName;
      console.log('添加文件夹',path);
      window.pywebview.api.createDir(path).then((res)=>{
        if(res){
          this.init();
          this.popoverVisible = false;
          this.selectKind = this.newKindName;
          this.$refs.tipRef.showSuccessTip('操作成功！');
        }
        else{
          this.$refs.tipRef.showFailTip('操作失败！收藏夹已经存在！');
        }
      });
    },
    deleteKind(kind){
      const path =  'myImage/' + kind;
      console.log(path);
      window.pywebview.api.deleteDir(path).then((res)=>{
        if(res){
          this.init();
          this.selectKind = '';
          this.$refs.tipRef.showSuccessTip('操作成功！');
        }
        else{
          this.$refs.tipRef.showFailTip('操作失败！收藏夹不存在！');
        }
      });
    },
    cancel(){
      this.$emit("closeDialog"); 
    },
    confirm(){
      // 重新写确认逻辑：再写一个通过url保存的接口即可
      if(!this.url){
        this.$refs.tipRef.showFailTip('图片出错！请重试.');
        return;
      }
      window.pywebview.api.saveFavorImage2(this.url,this.imageName+'.png',this.selectKind.value).then((res)=>{
        console.log(res);
        if(res&&(res.status == 'success')){
          const url = 'http://localhost:6500'+ '/images/myImage/' + this.selectKind.value + '/' + res.name;
          console.log('收藏成功',url);
          this.$emit("favorSuccess",url);
          return;
        }
        this.$refs.tipRef.showFailTip('收藏失败！');
      });
    },
    async init(){
      const list = await window.pywebview.api.getFavorImageKinds();
      if(!list) return;
      const kindList = [];
      for(let i=0;i<list.length;i++){
        console.log(list[i]);
        kindList.push({
          'value':list[i],
          'label':list[i]
        })
      }
      this.kinds = kindList;
      this.selectKind = kindList[0];
    }
  },
  mounted(){
    /* 0. 初始化：获取kinds
    *  1.
    *  2.
    */ 
    if(this.name&&(this.name!='添加网络素材图片')){
      this.imageName = this.name.replace(/\.png/g,  '');
    }else{
      this.imageName = '';
    }
    this.init();
  }
}
</script>