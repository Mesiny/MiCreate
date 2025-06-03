<template>
    <div>
      <TipTab ref="tipRef" /> 
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
        <el-input v-model="psdName" placeholder="请输入收藏psd名称"></el-input>
        <div style="margin: 10px;">
          <el-button type="primary" @click="confirm" :disabled="(selectKind&&psdName)?false:true">确认</el-button>
          <el-button @click="cancel">取消</el-button>
        </div>

      </div>
    </div>
</template>

<script >
import TipTab from '../components/TipTab.vue';

export default {
  props: {
      psdUrl: {
        type: String,
        required: true,
        default: ""
      },
      img:{
        type: String,
        required: false,
        default: ""
      },
      name:{
        type: String,
        required: false,
        default: ""
      }
  },
  components: {
    TipTab
  },
  data(){
    return {
      selectKind:'',
      psdName :'',
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
      const path = 'myPsd/' + this.newKindName;
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
      const path =  'myPsd/' + kind;
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
      if(!this.psdUrl){
        this.$refs.tipRef.showFailTip('psd文件出错！请重试.');
        return;
      }
      window.pywebview.api.saveFavorPsd(this.psdUrl,this.psdName+'.psd',this.selectKind).then(()=>{
        this.$emit("favorSuccess2");
      });
      if(this.img) window.pywebview.api.saveFavorPsdCache(this.img,this.psdName+'.png',this.selectKind);
    },
    async init(){
      const list = await window.pywebview.api.getFavorPsdKinds();
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
    }
  },
  mounted(){
    /* 0. 初始化：获取kinds
    *  1.
    *  2.
    */ 
    this.psdName = this.name;
    this.init();
    
  }
}
</script>