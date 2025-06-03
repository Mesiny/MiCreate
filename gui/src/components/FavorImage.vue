<template>
  <div>
    <TipTab ref="tipRef" /> 
      <el-dialog v-model="renameVisible" title="重命名" width="500">
          <el-input v-model="newName" placeholder="输入要更换的名字"/>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="renameVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmRename" :disabled="newName==''">确定</el-button>
        </div>
      </template>
    </el-dialog>
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
            accept="image/jpeg,image/png"
            multiple
            :limit="20"
            :on-change="handleChange"
            :show-file-list="false" 
            style="display: inline-block;margin-left:15px;"
          >
              <el-button size="medium" type="primary">上传图片</el-button>
          </el-upload>
    <div class="search-area" style="margin-top: 10px;">
      <el-select v-model="selectedKind" placeholder="请选择分类" @change="getCardlist"  style="width: 30%;">
        <el-option v-for="item in kinds" :key="item.value" :label="item.label" :value="item.value"></el-option>
      </el-select>
      <el-input v-model="searchName" placeholder="请输入收藏图片名称"  style="width: 40%;margin-left: 3%;"></el-input>
      <el-button size="medium" type="primary" @click="search" style="margin-left: 2%;">搜索</el-button>
      <el-button size="medium" @click="reset">刷新</el-button>
    </div>
    <div class="materials" style="height: calc(100vh - 300px);overflow-y:auto;">
        <el-empty :image-size="200" v-if="cardList.length==0" style="margin: 0 auto;" description="空空如也~"/>
        <el-card :class="`card ${item.choosed?'green-border':'black-border'}`" v-for="(item, index) in cardList.slice((currentPage - 1) * pageSize, currentPage * pageSize)" :key="item.id" @click="handleClickCard(item)">
            <div class="info">
                <img :src="item.url" style="width: 100%" class="cardimg" />
                <p class="title">{{ item.name }}</p>
            </div>
              <div class="image-overlay">
              <!-- <el-button type="primary" @click="handleMenuClick">菜单按钮</el-button> -->
              <div style="display: flex;gap:10px;position: relative;bottom: 0px;">
                <el-icon color="white" size="22px" @click="handlePreview($event,index)"><Search /></el-icon>
                <el-icon color="white" size="22px" @click="handleRename($event,item)"><Edit /></el-icon>
                <el-popover placement="bottom" trigger="click" ref="myPopover">
                    <template #reference>
                      <el-icon color="white" size="22px" @click="$event.stopPropagation();"><Delete /></el-icon>
                    </template>
                    <p><el-icon><QuestionFilled color="rgb(255,153,0)" /></el-icon>确定删除吗?</p>
                    <div style="text-align: right; margin: 0; display: flex; flex-direction: row;">
                      <el-button size="small" text @click="cancelDelete">取消</el-button>
                      <el-button size="small" type="primary" @click="handleDelete($event,item)">确认</el-button>
                    </div>
                  </el-popover>
              </div>
            </div>
        </el-card>
        <div style="height: 20px;width: 100%;"></div>
    </div>
    <!-- 图片预览 -->
    <el-image-viewer
      v-if="showPreview"
      :url-list="previewList"
      :initial-index="initialIndex"
      @close="showPreview = false"
    />
    <div style="width: 100%;position: fixed;bottom: 10px;display: flex;">
      <el-pagination
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-size="pageSize"
        layout="total, prev, pager, next"
        :total="cardList.length"
      >
      </el-pagination>
      <div style="margin-left:300px ;">
        <el-button @click="confirmAdd" type="primary">添加素材</el-button>
        <el-button @click="this.$emit('cancel')">取消</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import TipTab from '../components/TipTab.vue';
import { Search,Edit,Delete } from '@element-plus/icons-vue' 


export default {
  data() {
    return {
      renameUrl:'',
      renameVisible:false,
      newName:'',
      initialIndex:0,
      previewList:[],
      showPreview:false,
      currentPage:1,
      pageSize:9,
      newKindName:'',
      popoverVisible:false,
      selectedKind: {},
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
    Search,
    Edit,
    Delete
  },
  methods: {
    cancelDelete(){
      document.body.click();
    },
    handleDelete(e,item){
      e.stopPropagation();
      console.log('handleDelete');
      // 不提示，直接删除
      window.pywebview.api.deleteFile(item.url).then(()=>{
        this.getCardlist();
        this.$refs.tipRef.showSuccessTip('删除成功！');
      })
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
    handlePreview(e,index){
      e.stopPropagation();
      console.log('handlePreview');
      this.initialIndex = index;
      this.showPreview = true;
      const previewList = [];
      let cards = this.cardList.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize);
      for(let i = 0;i < cards.length; i++)  previewList.push(cards[i].url);
      this.previewList = previewList;
    },
    confirmRename(){
      const url = this.renameUrl;
      if(!url){
        this.$refs.tipRef.showFailTip('图片地址不存在！');
        return;
      }
      // newname不带后缀
      window.pywebview.api.renameFile(this.newName,url).then(()=>{
        setTimeout(()=>{
          this.getCardlist();
        },300);
        this.$refs.tipRef.showSuccessTip('重命名成功！');
        this.renameUrl = '';
        this.newName = '';
        this.renameVisible = false;
      })
    },
    confirmAdd(){
      // 将选中的都添加
      const list = this.cardList;
      if(!list.length){
        this.$refs.tipRef.showFailTip('添加数目为0！');
        return;
      }
      const list2 = [];
      for(let i=0;i<list.length;i++){
        const card = list[i];
        if(card.choosed) {
          list2.push(card.url);
        }
      }
      if(!list2.length) {
        this.$refs.tipRef.showFailTip('未选择任何图片！');
        return;
      }
      this.$emit('addFavImages',list2);
    },
    // 点击卡片
    handleClickCard(item){
      console.log('handleClickCard');
      item.choosed = ! item.choosed;
      // 原版本为打开图片预览，不需要
      // this.initialIndex = index;
      // this.showPreview = true;
      // const previewList = [];
      // let cards = this.cardList.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize);
      // for(let i = 0;i < cards.length; i++)  previewList.push(cards[i].url);
      // this.previewList = previewList;
    },
    handleChange(file){
      // 检查文件类型
      if (!file.raw.type.startsWith('image/')) {
        this.$refs.tipRef.showFailTip('只能上传图片文件！');
        return;
      }
      // 使用 FileReader 读取文件
      const reader = new FileReader();
      reader.onloadend = () => {
          const fileData = reader.result;
          // 文件数据是fileData
          window.pywebview.api.saveFavorImage(fileData,file.raw.name,this.selectedKind).then(response=>{
            console.log(response);
            if(response.status == 'success'){
              // 计算url,并且指定url
              const name = response.name;
              const url =  'http://localhost:6500' + '/images/myImage/' + this.selectedKind + '/' + name;
              this.cardList.push({
                  id:Date.now(),
                  name:name.replace(/\.[^/.]+$/, ''),
                  url:url,
                  choosed:false
              });
            }
          });
        
      };
      reader.readAsDataURL(file.raw);
    },
    addKind(){
      if(!this.newKindName) return;
      // 添加文件夹，kinds对象push一类
      const path = 'myImage/' + this.newKindName;
      window.pywebview.api.createDir(path).then((res)=>{
        if(res){
          this.refreshKinds();
          this.popoverVisible = false;
          this.selectKind = this.newKindName;
          this.getCardlist();
          this.$refs.tipRef.showSuccessTip('操作成功！');
        }
        else{
          this.$refs.tipRef.showFailTip('操作失败！收藏夹已经存在！');
        }
      });
    },
    beforeUpload(file) {
      // 上传前处理逻辑，例如文件类型、大小校验等
      return true;
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
      const list = await window.pywebview.api.getFavImage(kind);
      const new_list = [];
      for(let i=0;i<list.length;i++){
        new_list.push({
          id:Date.now(),
          name:list[i].replace(/\.[^/.]+$/, ''),
          url:'http://localhost:6500'+ '/images/myImage/' + kind + '/' + list[i],
          choosed:false
        });
      }
      this.cardList = new_list;
      this.allCardList = new_list;
    },
    async refreshKinds(){
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
/* 覆盖 el-image-viewer 的默认样式 */
::v-deep .el-image-viewer__wrapper {
  max-width: 80vw; /* 设置图片最大宽度为视口宽度的 80% */
  max-height: 80vh; /* 设置图片最大高度为视口高度的 80% */
  object-fit: contain; /* 保持图片比例 */
  margin: 10vh auto;
}
.image-overlay {
  position: absolute;
  bottom: 0px;
  left: 0;
  width: 100%;
  height: 30%;
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
  border: 3px  solid rgba(64, 158, 255, 0.637);
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
  gap: 10px; /* 设置元素之间的间距 */
}

.custom-style .el-segmented {
    --el-segmented-item-selected-color: white;
    --el-segmented-item-selected-bg-color: #6777ef;
    --el-border-radius-base: 16px;
    display: flex;

}

.custom-style {
    width: fit-content;
    padding: 20px;
}

/* card */
/* From Uiverse.io by Yaya12085 */
.card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border-radius: 0.75rem;
    background-color: white;
    width: 215px;
    max-height: 180px;
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
    margin:0 auto;
    color: rgb(38 50 56);
    font-family: -apple-system;
    font-weight: 100;
    letter-spacing: 0;
    line-height: 1.375;
    font-size: 1.15rem;
    margin-bottom: 1rem;
    max-width: 150px;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
}

</style>