<template>
  <div>
    <el-dialog v-model="renameVisible" title="重命名" width="500">
            <el-input v-model="newName" placeholder="输入要更换的名字"/>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="renameVisible = false">取消</el-button>
            <el-button type="primary" @click="confirmRename" :disabled="newName==''">确定</el-button>
          </div>
        </template>
      </el-dialog>
    <el-dialog v-model="dialogVisible" center width="1000" style="background-color: #fff;">
        <template #header>
            <h2 style="text-align: left;font-weight: 400;font-family: -apple-system;margin: 5px auto;font-size: 20px;">psd预览</h2>
        </template>
        <psdPreview ref="viewRef" v-if="dialogVisible" @addAsset="addAsset" :name="target_name" :url="target_url" :add_bool="false" :fav_bool="false"/>
    </el-dialog>
    <TipTab ref="tipRef" /> 
    <el-popover ref="popover" placement="bottom" v-model:visible="popoverVisible" trigger="click" width="300">
            <template #reference>
              <el-button type="primary" size="medium">新增分类</el-button>
            </template>
            <template #default>
              <span>新建分类</span>
              <el-input v-model="newKindName" placeholder="请输入收藏分类名称" style="margin: 10px 0px;"></el-input>
              <el-button type="danger" @click="popoverVisible=false" size="medium">取消</el-button>
              <el-button type="success" @click="addKind" size="medium" :disabled="newKindName?false:true">确认</el-button>
            </template>
    </el-popover>
    <el-upload
            :auto-upload="false"
            v-model:file-list="fileList"
            accept=".psd"
            multiple
            :limit="20"
            :on-change="handleChange"
            :show-file-list="false" 
            style="display: inline-block;margin-left:15px;"
          >
              <el-button size="medium" type="primary">上传psd</el-button>
    </el-upload>
    <div class="search-area" style="margin-top: 10px;">
      <el-select v-model="selectedKind" placeholder="请选择分类" @change="getCardlist"  style="width: 30%;">
        <el-option v-for="item in kinds" :key="item.value" :label="item.label" :value="item.value">
            <span style="float: left">{{ item.label }}</span>
            <span style="float: right;color: red;font-size: 10px;" @click="deleteKind(item.value)">
              删除
            </span>
        </el-option>
      </el-select>
      <el-input v-model="searchName" placeholder="请输入收藏图片名称"  style="width: 40%;margin-left: 3%;"></el-input>
      <el-button size="medium" type="primary" @click="search" style="margin-left: 2%;">搜索</el-button>
      <el-button size="medium" @click="reset">刷新</el-button>
    </div>
    <div class="materials" style="height: calc(100vh - 300px);overflow-y:auto;">
        <el-empty :image-size="200" v-if="cardList.length==0" style="margin: 0 auto;" description="空空如也~"/>
        <el-card class="card black-border" v-for="item in cardList.slice((currentPage - 1) * pageSize, currentPage * pageSize)" :key="item.id" @click="handleClickCard(item)">
            <div class="info">
                
                <el-image :src="item.url" style="width: 100%" class="cardimg" @error="handleImageError(item)" >
                  <template #error>
                    <div style="width: 100%;font-family: -apple-system;font-size: 16px;color: red;">
                      <p>缓存失效...</p>
                      <p>点击重新加载</p>
                    </div>
                  </template>
                </el-image>
                <p class="title">{{ item.name }}</p>
            </div>
                            <!-- 遮罩层 -->
            <div class="image-overlay">
              <!-- <el-button type="primary" @click="handleMenuClick">菜单按钮</el-button> -->
              <div style="display: flex;gap:10px;position: relative;bottom: 0px;">
                <el-icon color="white" size="large" @click="handlePreview($event,item)"><Search /></el-icon>
                <el-icon color="white" size="large" @click="handleRename($event,item)"><Edit /></el-icon>
                <el-icon color="white" size="large" @click="handleDelete($event,item)"><Delete /></el-icon>
              </div>
            </div>
        </el-card>
        <div style="height: 20px;width: 100%;"></div>
    </div>
    
    <div style="width: 100%;position: fixed;bottom: 10px;">
      <el-pagination
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-size="pageSize"
        layout="total, prev, pager, next"
        :total="cardList.length"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import TipTab from '../components/TipTab.vue';
import { readPsd  } from 'ag-psd';
import psdPreview from './psdPreview.vue';
import { Search,Edit,Delete } from '@element-plus/icons-vue' 

export default {
  data() {
    return {
      renameUrl:'',
      newName:'',
      renameVisible:false,
      target_url:'',
      target_name:'',
      dialogVisible:false,
      currentPage:1,
      pageSize:9,
      newKindName:'',
      popoverVisible:false,
      selectedKind: '',
      searchName: '',
      cardList: [],
      currentPage: 1,
      pageSize: 9,
      total: 0,
      kinds:[],
      fileList:[], //上传文件
      allCardList:[]
    };
  },
  props:{
    selectIndex:{
      type: Number,
      required: false,
      default: -1
    }
  },
  components: {
    TipTab,
    psdPreview,
    Search,
    Edit,
    Delete
  },
  methods: {
    
    confirmRename(){
      let url = this.renameUrl;
      if(!url){
        this.$refs.tipRef.showFailTip('图片地址不存在！');
        return;
      }
      // newname不带后缀
      window.pywebview.api.renameFile(this.newName,url).then(()=>{
        url = url.replace('cache','myPsd').replace('.png','.psd');
        window.pywebview.api.renameFile(this.newName,url);
        setTimeout(()=>{
          this.getCardlist();
        },300);
        this.$refs.tipRef.showSuccessTip('重命名成功！');
        this.renameUrl = '';
        this.newName = '';
        this.renameVisible = false;
      })
    },
    handlePreview(e,item){
      e.stopPropagation();
      console.log('handlePreview');
      // 设置好target_url和target_name
      this.target_url = item.url.replace('cache','myPsd').replace('.png','.psd')
      this.target_name = item.name;
      this.dialogVisible = true;
    },
    handleRename(e,item){
      e.stopPropagation();
      console.log('handleRename');
      /* 弹出
       * 
      */ 
      // 重命名
      // 对item.url
      this.renameUrl = item.url;
      this.renameVisible = true;
    },
    handleDelete(e,item){
      e.stopPropagation();
      console.log('handleDelete');
      // 不提示，直接删除
      window.pywebview.api.deleteFile(item.url).then(()=>{
        const url = item.url.replace('cache','myPsd').replace('.png','.psd');
        window.pywebview.api.deleteFile(url);
        setTimeout(()=>{
          this.getCardlist();
        },300);
        this.$refs.tipRef.showSuccessTip('删除成功！');
      })
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
    async handleImageError(item){
      console.log(item);
      const url = 'http://localhost:6500' + '/images/myPsd/' + this.selectedKind + '/' + item.name + '.psd';
      console.log('handleImageError-url',url);
      const res = await fetch(url);
      console.log(res);
      if(res.ok){
        const arrayBuffer = await res.arrayBuffer();
        const psd = readPsd(arrayBuffer);
        const base_64 = psd.canvas.toDataURL();
        await window.pywebview.api.makeFavorPsdCache(base_64,item.name+'.png',this.selectedKind);
        // console.log(item.url);
        // 重新刷新
        setTimeout(()=>{
          this.getCardlist();
        },1000);
      }else{
        console.log('数据错误!');
      }
    },
    handleChange(file){
      // 检查文件类型
      console.log(file.raw.name); // 22ac918fc58f4681b568d57074318c07.psd
      if (!file.raw.name.includes('.psd')) {
        this.$refs.tipRef.showFailTip('只能上传psd文件！');
        return;
      }
      // 使用 FileReader 读取文件
      const reader = new FileReader();
      reader.onload  = (event) => {
          const arrayBuffer  = event.target.result;
          const uint8Array = new Uint8Array(arrayBuffer);
          console.log(event);
          // 文件数据是fileData
          // 然后写.psd文件即可
          window.pywebview.api.saveFavorPsdFromUs(Array.from(uint8Array),file.raw.name,this.selectedKind).then(()=>{
              // 计算url,并且指定url
              const name = file.raw.name;
              const url =  'http://localhost:6500' + '/images/cache/' + this.selectedKind + '/' + name.replace('.psd', '.png');
              const card = {
                  id:Date.now(),
                  name:name.replace(/\.[^/.]+$/, ''),
                  url:url
              }
              // this.handleImageError(card).then(()=>{
              //   this.cardList.push(card);
              // })
          });
        
      };
      reader.readAsArrayBuffer(file.raw)
    },
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
    handleSuccess(response, file) {
      // 上传成功处理逻辑，例如更新图片列表
      this.imageList.push({
        url: URL.createObjectURL(file.raw),
        name: file.name
      });
    },
    handleRemove(file, fileList) {
      // 删除图片处理逻辑
      // 这里简单地从列表中移除图片
      const index = this.imageList.findIndex(image => image.name === file.name);
      if (index!== -1) {
        this.imageList.splice(index, 1);
      }
    },
    search() {
      // 搜索逻辑，这里只是模拟，实际应发送请求到后端获取数据
      // 假设返回的数据格式为 {data: [], total: 0}
      const files = this.allCardList;
      const keyword = this.searchName;
      let new_files = files.filter((file) =>
        file.name.toLowerCase().includes(keyword.toLowerCase())
      );
      this.cardList = new_files;
    },
    reset() {
      this.refreshKinds();
      this.getCardlist();
      this.$refs.tipRef.showSuccessTip('刷新成功！');
    },
    handleCurrentChange(page) {
      this.currentPage = page;
    },
    async getCardlist(){
      // 获取CardList
      const kind = this.selectedKind;
      const list = await window.pywebview.api.getFavPsd(kind);
      console.log('const list',list);
      const new_list = [];
      for(let i=0;i<list.length;i++){
        new_list.push({
          id:Date.now(),
          name:list[i].replace(/\.[^/.]+$/, ''),
          url:'http://localhost:6500'+ '/images/cache/' + kind + '/' + list[i].replace('.psd', '.png')
        });
      }
      this.cardList = new_list;
      console.log(new_list);
      this.allCardList = new_list;
    },
    async refreshKinds(){
      const list = await window.pywebview.api.getFavorPsdKinds();
      if(!list) return;
      const kindList = [];
      for(let i=0;i<list.length;i++){
        kindList.push({
          'value':list[i],
          'label':list[i]
        })
      }
      this.kinds = kindList;
      // 默认选中第一类，然后再初始化第一类中得结果
    },
    async init(){
      await this.refreshKinds();
      if(this.kinds[0]){
        this.selectedKind = this.kinds[0].value;
        this.getCardlist();
      }
    }
  },
  mounted(){
    this.init();
  } 
};
</script>

<style scoped>
/* 调整所有按钮的外边距 */
::v-deep .el-pagination {
  display: flex;
  gap: 5px !important;  /* 整体按钮间距 */
}
/* 页码数字之间的间距 */
::v-deep .el-pagination .el-pager li.number  {
  margin: 0 5px !important;
}
.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* 半透明黑色背景 */
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s;
}
.card:hover .image-overlay {
  opacity: 1;
}
.black-border {
  border: 0.5px solid #ccc;
}
.green-border {
  
  border: 0.5px solid rgba(14, 209, 104, 0.637);
}
.upload-demo {
  margin-bottom: 20px;
}

.search-area {
  margin-bottom: 20px;
}
.materials {
  display: flex;
  flex-wrap: wrap; /* 让元素换行排列 */
  gap: 5px; /* 设置元素之间的间距 */
}

.custom-style .el-segmented {
    --el-segmented-item-selected-color: white;
    --el-segmented-item-selected-bg-color: #6777ef;
    --el-border-radius-base: 16px;
    display: flex;

}

.custom-style {
    width: fit-content;
    padding: 10px;
}

/* card */
/* From Uiverse.io by Yaya12085 */
.card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border-radius: 0.75rem;
    background-color: white;
    width: 225px;
    max-height: 225px;
    position: relative;
}
::v-deep .el-card__body{
  padding: 0;
}

.card:hover {
    box-shadow: 0 4px 6px 0px rgba(0, 0, 0, .1), 0 2px 4px -1px rgba(0, 0, 0, .1);
    transform: scale(1.02);
    transition: transform 0.2s ease-in-out;
    cursor: pointer;
}

.info {
    border: none;
    padding: 0.5rem;
    text-align: center;
}

.title {
    color: rgb(38 50 56);
    letter-spacing: 0;
    line-height: 1.375;
    font-weight: 500;
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
    max-width: 225px;
    overflow: hidden;
}

</style>