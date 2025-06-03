<template>
  <div style="height: 100%;">
    <el-dialog v-model="renameVisible" title="重命名" width="500">
      <el-input v-model="newName" placeholder="输入要更换的名字"/>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="renameVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmRename" :disabled="newName==''">确定</el-button>
        </div>
      </template>
    </el-dialog>
    <h1 class="light_nav" id="nav" style="border-radius: 3px;line-height: 3em;text-indent: 1em;font-size: 24px;font-family: -apple-system;font-weight: 600;margin-bottom: 15px;">创作</h1>
    <div>
    <!-- 弹出框 -->
    <el-dialog
      title="上传字幕文件"
      v-model="dialogVisible"
      width="40%"
    >
      <!-- 子页面内容 -->
      <el-upload
        class="upload-demo"
        drag
        :auto-upload="false"
        :on-change="handleSrtUpload"
        :show-file-list="false"
        accept=".srt"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          将字幕文件拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            上传srt文件
          </div>
        </template>
      </el-upload>
            <!-- 底部按钮 -->
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false" size="default">取消</el-button>
        </span>
      </template>
    </el-dialog>
      <TipTab ref="tipRef" /> 
      <div class="container light_nav">
        <div style="width: 95%;margin: 0 auto;height: 60px;line-height: 60px;padding-top: 10px;">
          <el-button style="margin-bottom: 10px;font-family: --apple-system;font-weight: 400;font-size: medium;" color="#626aef" plain :dark="isDark" @click="beginCreate">开始创作</el-button>
          <el-tooltip  content="刷新列表" placement="bottom" effect="dark" :show-after='800'>
            <el-button style="float:right;margin-right: 20px;margin-top: 10px;" circle color="#626aef" @click="refreshList" size="default"><el-icon size="medium"><Refresh /></el-icon></el-button>
          </el-tooltip>
        </div>
        <el-table class="my-table" :cell-style="{padding: '8px','font-famliy':'微软雅黑'}" :header-cell-style="{background:'#eff0fd',fontSize: '18px',color:'black'}" 
        :data="drafts" :height='tableHeight' style="background-color: transparent;box-shadow: 0 4px 8px rgba(0, 0, 0, 0.03);border-radius: 3px;width: 95%; margin:0 auto;font-size: 15px;font-family: --apple-system;">
          <el-table-column prop="name" label="草稿名称" show-overflow-tooltip/>
          <el-table-column prop="createTime" label="创建时间" />
          <el-table-column fixed="right">
            <template #default="scope">
              <el-tooltip content="编辑" placement="bottom" effect="dark" :show-after='800'>
                <el-button  type="success" size="default"  color="#626aef"  plain @click="openDraft(scope.$index)">
                  <el-icon style="vertical-align: middle;"><Edit /></el-icon>
                </el-button>
              </el-tooltip>
              <el-tooltip content="打开目录" placement="bottom" effect="dark" :show-after='800'>
                <el-button type="success" size="default"  color="#626aef"  plain @click="siteDraft(scope.$index)">
                  <el-icon style="vertical-align: middle;"><Folder /></el-icon>
                </el-button>
              </el-tooltip>
              <el-tooltip content="重命名" placement="bottom" effect="dark" :show-after='800'>
                <el-button  type="success" size="default"  color="#626aef"  plain @click="reName(scope.$index)">
                  <el-icon style="vertical-align: middle;"><FolderRemove /></el-icon>
                </el-button>
              </el-tooltip>
              <el-tooltip content="删除" placement="bottom" effect="dark" :show-after='800'>
                <div style="display: inline-block;margin-left: 12px;">
                  <el-popover placement="bottom" trigger="click" ref="myPopover">
                    <template #reference>
                        <el-button type="danger" size="default"  plain>
                          <el-icon style="vertical-align: middle;"><Delete /></el-icon>
                        </el-button>
                    </template>
                    <p><el-icon><QuestionFilled color="rgb(255,153,0)" /></el-icon>确定删除吗?</p>
                    <div style="text-align: right; margin: 0; display: flex; flex-direction: row;">
                      <el-button size="small" text @click="cancelDelete">取消</el-button>
                      <el-button size="small" type="primary" @click="deleteDraft(scope.$index)">确认</el-button>
                    </div>
                  </el-popover>
                </div>
              </el-tooltip>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>

</template>

<script >
import { ElPopover, ElButton,ElLoading   } from 'element-plus';
import { QuestionFilled,Edit,Folder,Delete,UploadFilled,Refresh,FolderRemove  } from '@element-plus/icons-vue'    // 图标
import TipTab from '../components/TipTab.vue';

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
  components: {
    ElPopover,
    ElButton,
    QuestionFilled,
    Edit,
    Folder,
    Delete,
    UploadFilled,
    Refresh,
    TipTab,
    FolderRemove
  },
  data() {
    return {
      old_name:'-',
      renameVisible:false,
      newName:'',
      drafts: [
      ],
      tableHeight:window.innerHeight - 210,
      dialogVisible:false,
      isDark:false
    };
  },
  methods: {
    toggleDarkTheme(theme) {
      // 对导航进行处理
      const nav = window.document.querySelector('#nav');
      console.log(nav);
      if(nav) {
          nav.className = `${theme}_nav`;
          const body = window.document.querySelector('.container');
          body.className = `container ${theme}_nav`
      }
    },
    confirmRename(){
      // newname不带后缀
      window.pywebview.api.renameDir(this.old_name,this.newName).then((res)=>{
        if(res == -1){
          this.$refs.tipRef.showFailTip('重命名失败，草稿已存在！');
          this.old_name = '-';
          this.newName = '';
          this.renameVisible = false;
          return;
        }
        if(res){
          this.$refs.tipRef.showSuccessTip('重命名成功！');
          this.getdrafts();
          this.old_name = '-';
          this.newName = '';
          this.renameVisible = false;
        }

      })
    },
    async beginCreate(){
      if((!await window.pywebview.api.veritySetting())||(!localStorage.getItem('token'))){
        this.$refs.tipRef.showFailTip('操作失败！请重新登录！');
        return;
      }
      this.dialogVisible = true;
    },
    calcHeight(){
      this.tableHeight = window.innerHeight - 210;
    },
    cancelDelete(){
      document.body.click();
    },
    async handleSrtUpload(file) {
      if((!await window.pywebview.api.veritySetting())||(!localStorage.getItem('token'))){
        this.$refs.tipRef.showFailTip('操作失败！请检查设置或重新登录！');
        return;
      }
      this.dialogVisible = false;
      this.startLoading();
      file = file.raw;
      // 这里可以添加开始创作的逻辑，比如跳转到创作页面等
      if (file) {
        const name = file.name.replace(/\.srt$/, "");
        const reader = new FileReader();
        reader.onload = async (e) => {
          try {
            // 读取文件内容 e.target.result即为arrayBuffer格式
            const srt = e.target.result;
            const that = this;
            window.pywebview.api.parseSrt(srt).then(project=>{
                console.log(project);
                window.pywebview.api.createDraftDocument(name,project,srt).then((basename)=>{
                  that.endLoading(this.startLoading());
                  that.getdrafts();
                  const params = {
                    'project':project,
                    'name':basename
                  }
                  // 自动传递project，跳转至创作页面
                  this.$router.push({ name: 'Create2', query: { param: JSON.stringify(params) } });
                });

                /*
                  需补充完整
                */ 
            })
          } catch (error) {
            console.error('Error parsing SRT file:', error);
          }
        };
        reader.readAsText(file, 'UTF-8');
      }
      console.log('开始创作');

    },
    refreshList(){
      this.getdrafts();
      this.$refs.tipRef.showSuccessTip('刷新成功!');
    },
    getdrafts(){
      // 从目录获取草稿列表 需要name和createTime
      console.log('获取草稿列表');
      window.pywebview.api.getDrafts().then(res=>{
        this.drafts = res;
      });
    },
    async reName(index) {
      this.renameVisible = true;
      this.old_name = this.drafts[index].name;
    },
    async openDraft(index) {
      // 打开草稿的逻辑，比如获取草稿内容并展示
      /*
        1.读取草稿project
        2.传递project,跳转
      */ 
      if((!await window.pywebview.api.veritySetting())||(!localStorage.getItem('token'))){
        this.$refs.tipRef.showFailTip('操作失败！请检查设置或重新登录！');
        return;
      }
      const name = this.drafts[index].name;
      const that = this;
      window.pywebview.api.getProject(name).then(project=>{
        if(project){
          // 传递project到下一个页面，跳转
          console.log('页面跳转');
          const params = {
            'project':project,
            'name':name
          }
                // 自动传递project，跳转至创作页面
          this.$router.push({ name: 'Create2', query: { param: JSON.stringify(params) } });

        }else{
          that.showFailTip('草稿不存在,请重试!');
          that.getdrafts();
        }
      });
      // refs.tipRef.showFailTip();
      console.log(`打开草稿 ${index}`);
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
    deleteDraft(index){
      document.body.click();
      const name = this.drafts[index].name;
      window.pywebview.api.deleteDraft(name).then(res=>{
        if(res){
          // 提示删除成功
          this.$refs.tipRef.showSuccessTip('删除成功!');
          console.log('删除成功');
          this.getdrafts();
        }else{
          console.log(res);
        }
      })
      // 应替换成获取本地drafts
      
    },
    async siteDraft(index){
      if((!await window.pywebview.api.veritySetting())||(!localStorage.getItem('token'))){
        this.$refs.tipRef.showFailTip('操作失败！请检查设置或重新登录！');
        return;
      }
      this.startLoading();
      window.pywebview.api.siteDraft(this.drafts[index].name).then(res=>{
        if(res){
          setTimeout(()=>{
            this.endLoading(this.startLoading());
            this.$refs.tipRef.showSuccessTip('打开目录成功!');
          },500);
        }else{
          refs.tipRef.showFailTip('打开目录失败，请检查路径');
          // 获取本地drafts 
          this.endLoading(this.startLoading());
        }
      })
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
    // 在组件挂载后，监听全局的点击事件
    this.getdrafts();
    window.addEventListener('resize', this.calcHeight);
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
#app1 {
  font-family: --apple-system,'SansHans-medium',Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;

}

table {
  border-collapse: collapse;
  width: 100%;
}
tr {
    border-left: none; /* 隐藏左边框 */
    border-right: none; /* 隐藏右边框 */
    border-top: 2px solid rgb(245,247,250); /* 上边框 */
    border-bottom: 2px solid rgb(245,247,250); /* 下边框 */
}
th,
td {
  text-align: left;
  padding: 8px;
  border: 1px solid #ddd;
}

.open-button {
  background-color: #42b983;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
}

.delete-button {
  background-color: #f56c6c;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
table, td, th {
  border-style: none; /* 隐藏边框 */
}
</style>