<template>
    <div style="height: 100%;">
        <TipTab ref="tipRef" /> 
        <!-- 收藏图片对话框 -->
        <el-dialog v-model="FavDialog" width="600" top="5%" title="收藏图片">
          <selectFavImage2 ref="selectFavImageRef" @closeDialog="FavDialog=false"  @favorSuccess="favorSuccess" :url = 'FavCard.url' :name="FavCard.name"/>
        </el-dialog>
        <!-- 主要内容 -->
         <div class="light_nav" id="nav"  style="border:none;border-radius: 3px;margin-bottom: 15px;">
            <h1 class="light_nav" id="nav-h1" style="line-height: 3em;text-indent: 1em;font-size: 24px;font-family: -apple-system;font-weight: 600;">
                <el-button size="24px" style="border: none;border-radius:5px;box-shadow: none" class="back-btn light_nav" @click="backCreate">
                    <el-icon size="20px" style="padding: 5px;">
                        <svg stroke-width="100" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 1024 1024"><path fill="currentColor" d="M224 480h640a32 32 0 1 1 0 64H224a32 32 0 0 1 0-64"/><path fill="currentColor" d="m237.248 512l265.408 265.344a32 32 0 0 1-45.312 45.312l-288-288a32 32 0 0 1 0-45.312l288-288a32 32 0 1 1 45.312 45.312z"/></svg>
                    </el-icon>
                </el-button>  创作 - <span style="font-size: 20px;font-weight: 300;">{{ draft_name }}</span>
            </h1>
        </div>
        <el-dialog v-model="dialogVisible" center width="80%">
          <div class="image-container">
            <img :src="dialogImageUrl" alt="图片预览" />
          </div>
        </el-dialog>
        <div id="app1" style="width: 100%;box-shadow: 0 4px 8px rgba(0, 0, 0, 0.03);border-radius: 3px;">
            <!-- 按钮 -->
            <el-button-group style="margin-left: 2.5%;">
              <el-button type="primary" color="#626aef" @click="exportClip">导出剪映</el-button>
              <el-button type="primary" color="#626aef" @click="drawerVisable2=true">收藏列表</el-button>
            </el-button-group>
            <!-- 表格 -->
            <vxe-table
              ref="tableRef"
              :data="draft"
              :height="tableHeight"
              style="width: 95%; margin: 0 auto; font-family: 'SansHans-medium';"
              :cell-style="{ padding: '8px', 'font-family': '--apple-system' }"
              :header-cell-style="{ background: '#eff0fd', fontSize: '17px', color: 'black', fontWeight: '700' }"
              :row-config="{ useKey: 'id' ,rowHeight:216,isHover: true,resizable:true }"
              :scroll-y="{ enabled: true, immediate:true,oSize:0 }"

              >
              <!-- 编号列 -->
              <vxe-column type="seq" title="编号" width="80" class-name="custom-index-column"></vxe-column>
              <!-- 字幕列 -->
              <vxe-column title="字幕" width="300">
                <template #default="{ row, rowIndex }">
                  <div style="margin-top:10px;">
                    <el-button 
                      @click="upMerge(rowIndex)" 
                      v-show="rowIndex !== 0" 
                      plain size="small" 
                      class="ch-button"  
                      style="display: block;margin-bottom: 10px;font-size: 14px;">
                      向上合并
                    </el-button>
                    <el-tag 
                      color="#2e2e2e" 
                      effect="dark" 
                      size="large"
                      style="cursor: text; user-select: text; font-family: '--apple-system'; color:#dadbdc; line-height: 1.5em; padding:0.6em 0.8em; height:auto; white-space: normal; word-wrap: break-word; border: 0; font-size: 16px; margin-bottom: 10px; margin-right:30px;"
                      v-for="(item, index) in row.text" :key="index">
                      {{ item }}
                    </el-tag>
                    <el-button 
                      @click="downSplit(rowIndex)" 
                      v-show="row.text.length > 1" 
                      plain size="small"
                      class="ch-button"
                      style="display: block;font-size: 14px;">
                      向下拆分
                    </el-button>
                  </div>  
                </template>
              </vxe-column>
              <!-- 素材列 -->
              <vxe-column title="素材">
                <template #default="{ row, rowIndex }">
                  <el-scrollbar>
                    <div style="display: flex;">  
                      <el-upload
                        v-model:file-list="row.image"
                        list-type="picture-card"
                        :auto-upload="true"
                        :http-request="(request) => customUpload(request, rowIndex)"
                        :before-upload="beforeUpload"
                        @dragover.prevent
                        drag
                      >
                        <template #default>
                          <div @click="selectAsset(rowIndex)" class="centered-container"  @dragenter="handleDragEnter" @dragover.prevent @drop="handleDrop2($event, rowIndex)">
                            <el-icon size="medium"><Plus color="#409eff" /></el-icon>
                            <span style="color:#409eff;font-family: --apple-system;font-size: medium;">选择素材</span>
                          </div>
                        </template>
                        <template #file="{ file, index }">
                          <div
                            draggable="true" 
                            @dragover.prevent 
                            @drop="handleDrop($event, rowIndex, index)" 
                            @dragstart="handleDragStart($event, rowIndex, index)"
                            @dragend="handleDragEnd"
                            >
                            <img :src="file.url" class="el-upload-list__item-thumbnail" draggable="false"/>
                            <div class="el-upload-list__item-actions">
                              <el-icon @click="handlePictureCardPreview(file)" class="eicon el-icon--check el-icon--upload-success el-icon--check">
                                <ZoomIn />
                              </el-icon>
                              <el-icon v-show="!file.url.includes('http://localhost:6500/images/myImage/')" style="margin-left: 10px;" 
                               class="eicon el-icon--upload-success el-icon--check" @click="handleFavImage(file,rowIndex, index)"><Star /></el-icon>
                              <el-icon v-show="file.url.includes('http://localhost:6500/images/myImage/')" style="margin-left: 10px;color: #ffb802;"
                               size="25px" class="eicon el-icon--upload-success el-icon--check" @click="$refs.tipRef.showSuccessTip('请勿重复收藏');"><StarFilled /></el-icon>
                              <el-icon @click="handleRemove(rowIndex, index)"
                                style="margin-left: 10px;" class="eicon el-icon--upload-success el-icon--check">
                                <Delete />
                              </el-icon>
                            </div>
                          </div>
                        </template>
                      </el-upload>                      
                    </div>
                  </el-scrollbar>
                </template>
              </vxe-column>
            </vxe-table>
        </div>
        <!-- 主要内容结束 -->
         <!-- 抽屉开始 -->
        <el-drawer v-model="drawerVisable" title="选择素材"  size="75%" class="mydrawer" @open="handleDrawerOpen">
          <el-tabs class="tabs" style="height: 100%;" v-model="select" >
            <!-- 选项卡1 -->
            <el-tab-pane label="官方素材" name="1">
              <NetworkAsset ref="NetworkAssetRef" :draft_name="draft_name" :selectIndex="selectIndex" @addAsset="addAsset" />
            </el-tab-pane>
            <!-- 选项卡2 -->
            <el-tab-pane label="收藏图片" name="2">
              <FavorImage ref="FavorImageRef" v-if="drawerVisable" :selectIndex="selectIndex" @cancel="drawerVisable = false" @addFavImages="addFavImages"/>
            </el-tab-pane>
            <!-- 选项卡3 -->
            <el-tab-pane label="收藏Psd" name="3">
              <PresetPsd ref="PresetPsdRef" v-if="drawerVisable" :selectIndex="selectIndex" :draft_name="draft_name"  @addAsset="addAsset"/>
            </el-tab-pane>
          </el-tabs>
        </el-drawer>
         <!-- 抽屉结束 -->
          <!-- 抽屉2开始 -->
        <el-drawer v-model="drawerVisable2" title="收藏列表"  size="67%" class="mydrawer" @open="handleDrawerOpen">
          <el-tabs class="tabs" style="height: 100%;" v-model="select2" >
            <!-- 选项卡2 -->
            <el-tab-pane label="收藏图片" name="1">
              <FavorImage2 ref="FavorImageRef" v-if="drawerVisable2" :selectIndex="selectIndex"/>
            </el-tab-pane>
            <!-- 选项卡3 -->
            <el-tab-pane label="收藏Psd" name="2">
              <PresetPsd2 ref="PresetPsdRef" v-if="drawerVisable2" :selectIndex="selectIndex"/>
            </el-tab-pane>
          </el-tabs>
        </el-drawer>
         <!-- 抽屉2结束 -->
    </div>
</template>


<script>
import { ElPopover, ElButton,ElLoading,ElTableV2, timeSelectProps   } from 'element-plus'; 
import { QuestionFilled,Edit,Folder,Delete,UploadFilled,Refresh,Plus,ZoomIn,Back,StarFilled,Star   } from '@element-plus/icons-vue'    // 图标
import NetworkAsset from '../components/NetworkAsset.vue';
import FavorImage from '../components/FavorImage.vue';
import PresetPsd from '../components/PresetPsd.vue';
import TipTab from '../components/TipTab.vue';
import FavorImage2 from '../components/FavorImage2.vue';
import PresetPsd2 from '../components/PresetPsd2.vue';
import selectFavImage2 from '../components/selectFavImage2.vue';
import VXETable from 'vxe-table'

export default {
  inject: ['globalDark'],  // 声明式注入 
  components: {
    ElPopover,
    ElButton,
    QuestionFilled,
    Edit,
    Folder,
    Delete,
    UploadFilled,
    Refresh,
    Plus,
    ZoomIn,
    Back,
    ElTableV2,
    NetworkAsset,
    FavorImage,
    PresetPsd,
    TipTab,
    FavorImage2,
    PresetPsd2,
    StarFilled,
    Star,
    selectFavImage2
  },
  data() {
    return {
      FavIndex1:0,
      FavIndex2:0,
      FavCard:{},
      FavDialog:false,
      select2:'1',
      drawerVisable2:false,
      baseUrl:'http://localhost:6500',
      draft_name:'',
      project:[
      ],
      fileList :[
      ],
      draft:[],
      operateSuccess:false,
      operateFail:false,
      successTip:'操作成功!',
      failTip:'操作失败！',
      tableHeight:window.innerHeight- 180,
      dialogVisible:false,
      isDark:false,
      dialogImageUrl:'',
      draggingIndex1: null, // 存储正在拖拽的图片的索引
      draggingIndex2: null,  // 存储正在拖拽的文件信息
      id_total:1,
      isExternal: true,  // 标志位，判断是否是外部文件
      drawerVisable:false,
      selectIndex:0,
      select:'1'
    };
  },
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
  methods: {
    favorSuccess(url){
      this.$refs.tipRef.showSuccessTip('收藏成功!');
      this.FavCard.url = url;
      this.FavDialog=false;
      // 还需要更改工程文件，然后保存才行。应该参考保存外来的图片
      // 同步修改project  需获取index1和index2
      const project_img = this.project[this.FavIndex1].image;
      window.pywebview.api.url2path(url).then(res=>{
        // project_img.push(res);
        project_img[this.FavIndex2] = res;
        window.pywebview.api.saveProject(this.draft_name,this.project);
      });
    },
    handleFavImage(file,index1,index2){
      // @click="handleFavImage"
      this.FavDialog = true;
      this.FavCard = file;
      // 保存index1和index2
      this.FavIndex1 = index1;
      this.FavIndex2 = index2;
    },
    handleDrawerOpen(){
      console.log(this.globalDark);
      if(this.globalDark){
        // 添加暗黑样式
        const drawers = window.document.querySelectorAll('.mydrawer');
        for(let i=0;i<drawers.length;i++){
          const drawer = drawers[i];
          drawer.classList.add('dark_nav');
        }
      }
    },
    async addFavImages(list){

      const index = this.selectIndex;
      const image = this.draft[index].image
      // 对url内容依次添加进project和draft，然后保存
      for(let i=0;i<list.length;i++){
        image.push({
          "name": '添加本地收藏图片',
          "url": list[i],
          "uid": Date.now(),
          "status": "success"
        });
      }
      // 同步修改project
      const project_img = this.project[index].image;
      for(let i=0;i<list.length;i++){
        const res = await window.pywebview.api.url2path(list[i])
        project_img.push(res);
      }
      window.pywebview.api.saveProject(this.draft_name,this.project);
      this.drawerVisable = false;
      this.$refs.tipRef.showSuccessTip('添加成功！');
      },
    toggleDarkTheme(theme) {
      // 对表格进行处理
      VXETable.setConfig({ 
        theme: theme // 强制切换为暗黑模式 
      });
      // // 对导航进行处理
      const nav = window.document.querySelector('#nav');
      if(nav) {
        nav.className = `${theme}_nav`;
        // 对导航按钮进行处理
        const back = nav.querySelector('.back-btn');
        back.className = `back-btn ${theme}_nav`;
        const h1 = nav.querySelector('#nav-h1');
        h1.className = `${theme}_nav`;
      }
    },
    async addAsset(url){
      // 修改project和draft
      const index = this.selectIndex;  // 被选中的序号
      const image = this.draft[index].image;
      // 为image添加一个元素
      console.log('为image添加一个元素',image);
      let name = "添加网络素材图片";
      name = await window.pywebview.api.get_name_from_url(url); 
      // 这里要换一个名字，name从url中提取即可!
      image.push({
          "name": name,
          "url": url,
          "uid": Date.now(),
          "status": "success"
      });
      // image[image.length-1].url = url;
      // 同步修改project
      const project_img = this.project[index].image;
      window.pywebview.api.url2path(url).then(res=>{
        console.log('url2path',res);
        project_img.push(res);
        window.pywebview.api.saveProject(this.draft_name,this.project);
        this.drawerVisable = false;
        this.$refs.tipRef.showSuccessTip('添加成功！');
      });

    },
    backCreate(){
        this.$router.push({ name: 'Create' });
    },
    handleChange(){
      console.log('handleChange');
    },
    // 捕获拖拽开始事件
    handleDragStart(event, index1, index2) {
      this.isExternal = false;
      console.log('拖拽开始');
      // 存储被拖拽的元素的索引和文件信息
      this.draggingIndex1 = index1;
      this.draggingIndex2 = index2;
      // 可以在这里设置拖拽元素的一些样式或动作
      // event.dataTransfer.setData("text/plain", file.name); // 可以在拖拽时存储其他自定义数据
    },
    // 捕获拖拽结束事件
    handleDragEnd(){
      console.log('拖拽结束');
      this.isExternal = true;
    },
    handleDrop(event,index1,index2){
      if(this.draggingIndex1 == null) return;
      let asset = this.draft[index1].image; // asset是列表
      /* 判断行号是否相同
       *   -相同：asset中的draggingIndex2和index2交换顺序
       *   -不同：在asset中的index2之前插入原来的url
       */
      if(this.draggingIndex1 === index1){
        [asset[this.draggingIndex2], asset[index2]] = [asset[index2], asset[this.draggingIndex2]];
      }else{
        asset.splice(index2, 0, this.draft[this.draggingIndex1].image[this.draggingIndex2]);
      }
      // 同步更新project
      asset = this.project[index1].image;
      if(this.draggingIndex1 === index1){
        [asset[this.draggingIndex2], asset[index2]] = [asset[index2], asset[this.draggingIndex2]];
      }else{
        asset.splice(index2, 0, this.project[this.draggingIndex1].image[this.draggingIndex2]);
      }
      console.log(asset);
      // 保存json
      window.pywebview.api.saveProject(this.draft_name,this.project);
    },
    handleDrop2($event, index1){
      // 重写逻辑：外部文件直接跳过
      if(this.isExternal) return;
      // if(index1 === this.draggingIndex1) return;
      console.log('触发handleDrop2');
      // 在当前image的尾部添加Start的元素
      if(this.draggingIndex1 == null) return;
      let asset = this.draft[index1].image; // asset是列表
      asset.push(this.draft[this.draggingIndex1].image[this.draggingIndex2]);
      //  同步更新project 
      asset = this.project[index1].image;
      asset.push(this.project[this.draggingIndex1].image[this.draggingIndex2]);
      console.log(asset);
      // 保存json
      window.pywebview.api.saveProject(this.draft_name,this.project);
    },
    beforeUpload(file){
      const isImage = file.type.startsWith("image/");
      return isImage; // 返回 false 会阻止文件上传
    },
    selectAsset(index){
      event.stopPropagation(); // 阻止事件冒泡
      this.selectIndex = index;
      this.drawerVisable = true;
    },
    customUpload(request,index){
      // 自定义上传行为
      /* 1. 获取file对象，对象名 + 修改日期 以及数据
       * 2. 保存file为.png格式，返回url
       * 3. 修改url
      */ 
      console.log('customUpload');
      const file = request.file;
      const reader = new FileReader();
      const that = this;
      reader.onloadend = () => {
        // 获取图片的二进制数据
        const fileData = reader.result;
        // 调用 pywebview API 将图片数据传递给后端
        window.pywebview.api.saveAsset(fileData, file.name, file.size,that.draft_name).then(response => {
            if(response.status == 'success'){
              // 计算url,并且指定url
              const name = response.name;
              const url = that.baseUrl + '/images/jbh/' + that.draft_name + '/' + name;
              const image = that.draft[index].image;
              image[image.length-1].url = url;
              // console.log(image);
              // 同步修改project
              const project_img = that.project[index].image;
              window.pywebview.api.url2path(url).then(res=>{
                console.log('url2path',res);
                project_img.push(res);
                window.pywebview.api.saveProject(this.draft_name,this.project);
              })
            }
        });
      };
      // 读取文件为数据URL
      reader.readAsDataURL(file);
      console.log('customUpload',request,index);
    },
    upMerge(index) { 
      if(index-1 < 0) return;
      let last_frame = this.draft[index-1];
      let now_frame = this.draft[index];
      if(last_frame === undefined || now_frame === undefined) return;
      last_frame.text.push(...now_frame.text);
      last_frame.time.push(...now_frame.time);
      this.draft.splice(index,1);
      // 对project进行同步修改
      // console.log('upMerge同步修改');
      last_frame = this.project[index-1];
      now_frame = this.project[index];
      if(last_frame === undefined || now_frame === undefined) return;
      last_frame.text.push(...now_frame.text);
      last_frame.time.push(...now_frame.time);
      this.project.splice(index,1);
      console.log('同步后project:',this.project);
      // 调用接口保存json文件
      window.pywebview.api.saveProject(this.draft_name,this.project);
    },
    downSplit(index) {
      // 向下拆分，只修改draft
      /* 1.draft在当前元素之后插入一个元素，该元素的text为当前元素text最后一个元素，time元素也如此
         2.删除当前元素的text和time元素的最后一个
      */ 
      let now_frame = this.draft[index];
      if(now_frame === undefined) return;
      this.draft.splice(index+1,0,{
          "id": this.id_total,
          "time": [
            now_frame.time[now_frame.time.length-1]
          ],
          "text": [
            now_frame.text[now_frame.text.length-1]
          ],
          "image": [
          ]
      });
      now_frame.text.splice(now_frame.text.length-1,1);
      now_frame.time.splice(now_frame.time.length-1,1);
      // 对project执行同样操作
      // console.log('downSplit同步修改');
      now_frame = this.project[index];
      if(now_frame === undefined) return;
      this.project.splice(index+1,0,{
          "id": this.id_total,
          "time": [
            now_frame.time[now_frame.time.length-1]
          ],
          "text": [
            now_frame.text[now_frame.text.length-1]
          ],
          "image": [
          ]
      });
      now_frame.text.splice(now_frame.text.length-1,1);
      now_frame.time.splice(now_frame.time.length-1,1);
      console.log('同步后project:',this.project);
      this.id_total = this.id_total + 1;
      // 调用接口保存json文件
      window.pywebview.api.saveProject(this.draft_name,this.project);
    },
    calcHeight(){
      this.tableHeight = window.innerHeight-180;
    },
    handleRemove(index1, index2){
      console.log(index1, index2);
      let asset = this.draft[index1];
      asset.image.splice(index2,1);
      // 对project同步修改
      asset = this.project[index1];
      asset.image.splice(index2,1);
      window.pywebview.api.saveProject(this.draft_name,this.project);
    },
    handlePictureCardPreview(uploadFile){
      console.log(uploadFile.url);
      this.dialogImageUrl = uploadFile.url;
      this.dialogVisible = true;
    },
    // 转换images到fileList
    images2filelist(images){
      const fileList = [];
      images.forEach(image => {
        // 正则匹配相对地址
        // project文件中的地址必须都是反斜杠！
        console.log(image);
        const regex = /(?<=\\draft)(\\jbh(?:\\.*))/;
        const match = image.match(regex);
        if (match) {
          const rePath = match[0].replace(/\\/g, "/");
          const fileName = rePath.split("/").pop();
          fileList.push({
            'name':fileName,
            'url':this.baseUrl + '/images'  + rePath
          });
        }else{
          const regex2 = /(?<=\\draft)(\\myImage(?:\\.*))/;
          console.log('image match2');
          const match2 = image.match(regex2);
          if(match2){
            const rePath = match2[0].replace(/\\/g, "/");
            const fileName = rePath.split("/").pop();
            fileList.push({
              'name':fileName,
              'url':this.baseUrl + '/images'  + rePath
            });
            }
        }
      })
      return fileList;
    },
    // project到draft
    project2draft(project){
      // 将每个对象的'images'替换为fileList(name和url)，同时将url的格式转换一下即可
      const draft = JSON.parse(JSON.stringify(project));
      draft.forEach(element => {
        element.image = this.images2filelist(element.image);
      });
      return draft
    },
    exportClip() {
      console.log('执行导出剪辑操作');
      /* 调用makeJY(project,name):
       * 提示成功
      */ 
      window.pywebview.api.makeJY(this.project,this.draft_name);
      this.$refs.tipRef.showSuccessTip('导出成功！');
      
    },
    selectFavorite(index) {
      console.log(`对第${index + 1}条记录执行选择收藏操作`);
    },
    selectMaterial(index) {
      console.log(`对第${index + 1}条记录执行选择素材操作`);
    },
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
    startLoading() {
      const loading = ElLoading.service({
        lock: true,
        text: "加载中...",
        customClass:'custom-loading',
        background: "rgba(0, 0, 0, 0.7)"
      });
      return loading;
    },
    endLoading(loading) {
      loading.close();
    },
  },
  mounted(){
    window.addEventListener('resize', this.calcHeight);
    if(this.globalDark){
      // 调为暗黑
      this.toggleDarkTheme('dark');
    }else{
      // 调为光
      this.toggleDarkTheme('light');
    }
    // 更新this.draft
    // 通过 this.$route.query.param 获取传递的参数并解析
    let param = this.$route.query.param;
    if (param) {
      param = JSON.parse(param);  // 解析回对象
      this.project = param.project;
      this.draft = this.project2draft(this.project);
      this.id_total = this.project.length;
      this.draft_name = param.name;
    }
    // this.$refs.tableRef.reloadData(this.draft);
  }
};
</script>

<style scoped>
html,body {
  font-family: --apple-system,
}
::v-deep .el-scrollbar__bar.is-horizontal{
  display: block !important; /* 隐藏横向滚动条 */
}
::v-deep .el-scrollbar__bar .el-scrollbar__thumb{
  background-color: #e09de8;  /* 设置背景色 */
  height: 10px;
  border-radius:5px ;
  display: block;
}
::v-deep .vxe-table--body-wrapper {
  background:none;
  overflow-x:hidden ;
}

::v-deep  .el-tag {
  transition: none !important; /* 禁用所有过渡动画 */
}
::v-deep .el-tabs__item {
  font-size: 16px; /* 可根据需求调整字体大小 */
}
/* 关闭所有动画，包括显示和删除时的动画 */
.back-btn:hover {
  background-color: #6777ef;  /* 设置背景色 */
  color: white;               /* 设置文字颜色 */
}
/* 强制图片卡片横向排列 */
::v-deep  .el-upload-list {
  display: flex;
  flex-wrap: nowrap;
  height: 200;
}
/* 如果需要让每个图片卡片保持一个固定的宽度和高度 */
::v-deep .el-upload-list .el-upload-list__item {

  border: 1px solid #ddd;
  margin-left: 6px;
}
::v-deep .el-upload-list .el-upload--picture-card{

  margin-left: 6px;
}
::v-deep .el-upload-list .el-upload-list__item .el-upload-list__item-thumbnail{
  object-fit: cover; /* 确保图片覆盖整个框 */
}
.ch-button:hover {
  color: #6777ef;
  border-color: #6777ef;
}
/* 隐藏右上角的对号 */
::v-deep .el-upload-list .el-upload-list__item .el-upload-list__item-status-label {
  display: none;
}

/* 确保图片在对话框中自适应 */
.image-container img {
  max-width: 100%; /* 图片的最大宽度为对话框的宽度 */
  height: auto; /* 高度根据宽度自适应 */
  display: block; /* 去掉图片下方的默认间距 */
  margin: 0 auto; /* 居中图片 */
}
::v-deep .el-upload-list .el-upload-list__item .el-icon--close-tip {
  display: none !important;
}
/* 去掉图片被选中时的边框 */
::v-deep .el-upload-list .focusing {
  outline: none !important;
  border-color: transparent !important;
  box-shadow: none !important;
}
::v-deep .centered-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;  /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  gap: 8px; /* 可以调整图标和文本之间的间距 */
}
::v-deep .el-upload--picture-card .el-upload-dragger {
  padding: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;  /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  gap: 8px; /* 可以调整图标和文本之间的间距 */
}
.eicon {
  cursor: pointer;
}
::v-deep .el-overlay .el-drawer .el-drawer__header {
  margin-bottom: 5px;
}
::v-deep .el-drawer .el-drawer__header span{
  color: rgb(48, 49, 51);
  text-indent: 0.5em;
  font-family: --apple-system;
  font-size: 18px;
}
::v-deep .el-overlay .el-drawer .el-drawer__body{
  border-top: 1px solid #eee;
  margin-top: 15px;
  padding-top: 10px;
}
::v-deep .dark_nav .el-tabs__item {
  color:white;
}
::v-deep .dark_nav.el-drawer .el-drawer__header span{
  color: #fff;
}

/* 鼠标悬停样式 */
::v-deep .el-tabs__item:hover {
  color: #409eff;
}
 
/* 选中状态样式 */
::v-deep .el-tabs__item.is-active  {
  color: #409eff !important;
}
::v-deep .vxe-body--row .vxe-cell{

  height: auto !important;

}
</style>