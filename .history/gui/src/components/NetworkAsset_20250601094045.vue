<template>
    <div>
        <Loading ref="loadingRef"/>
        <TipTab ref="tipRef" /> 
        <el-dialog v-model="dialogVisible" center width="1000" style="background-color: #fff;">
            <template #header>
              <h2 style="text-align: left;font-weight: 400;font-family: -apple-system;margin: 5px auto;font-size: 20px;">编辑素材</h2>
            </template>
            <psdPreview ref="viewRef" v-if="dialogVisible" @addAsset="addAsset" :name="target_name" :img="target_img" :url="target_url" :draft_name="draft_name" :add_bool="selectIndex > -1"/>
          </el-dialog>
        <div class="container" >
            <div style="display: flex;justify-content: space-between;">
                <div style="width: 70%;">
                    <el-input v-model="search_input" style="max-width: 1200px;padding: 20px;" placeholder="搜索">
                        <template #append>
                            <el-button @click="search(1)" style="width: 40px;">
                                <el-icon size="20px" style="margin-left: -8px;margin-top: -2px;"><Search /></el-icon>
                            </el-button>
                        </template>
                    </el-input>
                </div>
            </div>
            <div class="custom-style" style="padding-top: 0px !important;">
                <el-segmented v-model="seg_value" :options="typeList" @change="handleCommand" block>
                    <template #default="scope">
                        <div style="text-align: center;padding-right: 9px;font-size: 14px;">{{ scope.item }}</div>
                    </template>
                </el-segmented>
            </div>
            <div class="materials">
                <el-empty :image-size="200" v-if="cardList.length==0" style="margin-left: calc(50% - 100px);" description="空空如也~"/>
                <div class="card" v-for="item in cardList" :key="item.id" @click="handleClickCard(item)">
                    <div class="info">
                        <p class="title">{{ item.fileName }}</p>
                        <img :src="item.photoPath" style="width: 100%" class="cardimg" />
                    </div>
                </div>
            </div>
            <!-- 图片预览 -->
            <el-image-viewer v-if="showImagePreview" :zoom-rate="1.2" :hide-on-click-modal="true" @close="closePreview"
                :url-list="imgPreviewList" />
            <div style="height: 50px;"></div>
            <div style="display: flex;justify-content: center;">
                <el-pagination background layout="prev, pager, next" :page-count="totalpage" :total="totalcount"
                    v-model:current-page="curpage" @current-change="handleCurrentChange" />
            </div>
            <div style="height: 50px;"></div>
        </div>
    </div>
</template>
<style scoped>

.container {
    height: 80vh;
    overflow-y: scroll;
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
    width: 225px;
    min-height: 225px;
    border: 0.5px solid rgba(118, 176, 214, 0.637);

}
.card:hover {
    box-shadow: 0 4px 6px 0px rgba(0, 0, 0, .1),
        0 2px 4px -1px rgba(0, 0, 0, .1);
    transform: scale(1.02);
    transition: transform 0.2s ease-in-out;
}

.info {
    border: none;
    padding: 1.5rem;
    text-align: center;
}

.title {
    color: rgb(38 50 56);
    letter-spacing: 0;
    line-height: 1.375;
    font-weight: 600;
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
}

.footer {
    padding: 0.75rem;
    border: 1px solid rgb(236 239 241);
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: 0.75rem;
    background-color: rgba(0, 140, 255, 0.082);
}

.tag {
    font-weight: 300;

    display: block;
}

.action {
    -webkit-user-select: none;
    -moz-user-select: none;
    user-select: none;
    border: none;
    outline: none;
    box-shadow: 0 4px 6px -1px rgba(33, 150, 243, .4), 0 2px 4px -2px rgba(33, 150, 243, .4);
    color: rgb(255 255 255);
    text-transform: uppercase;
    font-weight: 700;
    font-size: .75rem;
    padding: 0.75rem 1.5rem;
    background-color: rgb(33 150 243);
    border-radius: 0.5rem;

}

.action2 {
    -webkit-user-select: none;
    -moz-user-select: none;
    user-select: none;
    border: none;
    outline: none;
    box-shadow: 0 4px 6px -1px rgba(33, 150, 243, .4), 0 2px 4px -2px rgba(33, 150, 243, .4);
    color: rgb(255 255 255);
    text-transform: uppercase;
    font-weight: 700;
    font-size: .75rem;
    padding: 0.75rem 1.5rem;
    background-color: rgb(49, 136, 14);
    border-radius: 0.5rem;
}
</style>

<script>
import api from '../api/index'
import { ElMessage } from 'element-plus'
import axios from 'axios';
import { ArrowDownBold } from '@element-plus/icons-vue'
import { Search } from '@element-plus/icons-vue' 
import Loading from '../components/Loading.vue';
import psdPreview from '../components/psdPreview.vue'
import TipTab from '../components/TipTab.vue';

export default {
    props: {
        draft_name:{
            type: String,
            required: false,
            default: ''
        },
        selectIndex:{
            type: Number,
            required: false,
            default: 0
        }
    },
    components: {
        ArrowDownBold,
        Search,
        Loading,
        psdPreview,
        TipTab
    },
    data() {
        return {
            dialogVisible:false,
            flag:false,
            seg_value:'都市角色',
            seg_value1: 'rw',
            seg_value2: 'xhxx',
            cardList: [],
            curpage: 1,
            totalpage: 10,
            totalcount: 0,
            search_input: '',
            imgPreviewList: [],
            showImagePreview: false,
            type:'都市角色',
            type1: 'rw',
            type2: 'xhxx',
            typeList:['都市角色','古代角色','修仙角色','网游角色','同人角色','诡异角色','女频角色','场景','怪兽','特效','道具'],
            type1list: ['rw', 'bj', 'dj', 'tx'],
            type2list:
            {
                'rw': ['xhxx', 'yxwy', 'xdds', 'gyms','trxl','gsys','gdrw'],
                'bj': ['a', 'xhxx', 'jhwx', 'xdds'],
                'dj': ['a', 'xxdl', 'xddj'],
                'tx': ['a', 'ddtx', 'fzfhtx', 'qptx']
            },
            map: {
                'rw': '人物',
                'bj': '背景图',
                'dj': '道具栏',
                'tx': '特效',
                'xhxx': '玄幻修仙',
                'yxwy': '游戏网游',
                'dsrw': '都市人物',
                'gyms': '诡异末世',
                'xdds': '现代都市',
                'jhwx': '江湖武侠',
                'xxdl': '修仙道具',
                'xddj': '现代道具',
                'ddtx': '打斗特效',
                'fzfhtx': '法阵防护特效',
                'qptx': '全屏特效',
                'trxl':'同人系列',
                'gdrw':'古代人物',
                'gsys':'怪兽异兽',
                'a': '全部'
            },
            target_url:'',
            target_img:''
        }
        
    },
    methods: {
        addAsset(url){
            this.dialogVisible = false;
            this.$emit("addAsset",url);
        },
        handleClickCard(item){
            /*
             * 0. 获取token缓存，如果缓存为空，则直接跳出失败：操作失败，请登录后再试！
             * 1. 缓存不为空，尝试获取url
             * 2. 根据url判断文件是否已经下载过，下载过传递本地链接，否则传递网络链接
            */
            const token = localStorage.getItem('token');
            if(!token){
                this.$refs.tipRef.showFailTip('操作失败，请登录后再试！');
                return;
            }
            this.$refs.loadingRef.startLoading();
            // console.log('item',item);
            api.getPsd2(item.id, item.kind).then(url => {
                window.pywebview.api.psdIsExist(url).then(new_url=>{
                    // console.log('new_url', new_url);
                    if(new_url == url) window.pywebview.api.downloadPsd(url);
                    url = new_url;
                    this.$refs.loadingRef.endLoading();
                    url = 'http://localhost:6500/proxy/' + url;
                    this.target_url = url;
                    this.target_img = item.photoPath;
                    this.target_name = item.fileName;
                    this.dialogVisible = true;
                });

            });
        },
        handleCommand(command) {
            console.log('handleCommand');
            // 清空搜索框
            this.search_input = '';
            // 切换类型
            this.type = command;
            this.handleCurrentChange(1);
        },
        handleCommand1(command) {
            console.log('handleCommand1');
            this.type1 = command;
            this.seg_value1 = command;
            this.seg_value2 = this.type2list[command][0];
            if (this.type2list[this.type1].indexOf(command) < 0) {
                this.type2 = this.type2list[this.type1][0]
            }
            this.handleCurrentChange(1);
        },
        handleCommand2(command) {
            console.log('handleCommand2');
            this.type2 = command;
            this.seg_value2 = command;
            this.handleCurrentChange(1);
        },

        search(val=1) {
            api.search(val, 12, this.search_input).then(res => {
                console.log('search',res);
                let cardList = res.list;
                this.totalpage = res.totalPage;
                this.totalcount = res.totalCount;
                for (let i = 0; i < cardList.length; i++) {
                    cardList[i].kind = cardList[i].type;
                    cardList[i].type1 = cardList[i].type;

                    // api.getPsd(u.id, u.type1).then(data => {
                    //      console.log(data);
                    // });
                }
                this.cardList = cardList;
                console.log(cardList);
                const titleElement = document.getElementById('header');
                if (titleElement) {
                    titleElement.scrollIntoView({ behavior: 'smooth' });
                }
                console.log(this.cardList);
                setTimeout(()=>{
                    this.flag = false;
                    if(cardList.length == 0) this.$refs.loadingRef.endLoading();
                },500);
            });
            // 阻止触发页数变化
            this.flag = true;
        },

        handlePreview(url) {
            this.imgPreviewList = [url.replace('/resize,l_400', '/resize,l_1080')];
            this.showImagePreview = true;
        },
        closePreview() {
            this.showImagePreview = false;
            this.imgPreviewList = [];
        },

        handleCurrentChange(val) {
            if(this.search_input){
                this.search(val,12,this.search_input);
            }else{
                this.$refs.loadingRef.startLoading();
                if(this.flag) return;
                console.log(`当前页: ${val}`);
                this.curpage = val;
                console.log('this.type',this.type);
                api.getList2(val, 12, this.type).then(res => {
                    this.$refs.loadingRef.endLoading();
                    let cardList = res.list;
                    this.totalpage = res.totalPage;
                    this.totalcount = res.totalCount;
                    for (let i = 0; i < cardList.length; i++) {
                        cardList[i].kind = cardList[i].type;
                        // api.getPsd(u.id, u.type1).then(data => {
                        //      console.log(data);
                        // });
                    }
                    this.cardList = cardList;
                    const titleElement = document.getElementById('header');
                    if (titleElement) {
                        titleElement.scrollIntoView({ behavior: 'smooth' });
                    }
                    console.log('新的素材列表',this.cardList);
                });
            }

        },
    },
    mounted() {

        //测试接口：对[人物]大类中[玄幻修仙]小类的第[1]页(每页限制[20]个素材)，获取这页中所有素材的Psd地址
        this.handleCurrentChange(1);

    }
}
</script>