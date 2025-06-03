import { pa } from "element-plus/es/locale/index.mjs";
import axios from "../utils/request"; //注意引用路径
import base64js from 'base64-js';
import querystring from "querystring"


function decodeBase64(base64String) {
    // 将 Base64 字符串解码为 Uint8Array
    const byteArray = base64js.toByteArray(base64String);

    // 使用 TextDecoder 将 Uint8Array 解码为 UTF-8 字符串
    const decoder = new TextDecoder('utf-8');
    return decoder.decode(byteArray);
}

// 从type1到网址的转换
let kind_dict = {
    'rw': 'sddhrwsc/',
    'bj': 'sddh/bjt/',
    'dj': 'sddh/djgl/',
    'tx': 'sddh/tx/'
}


// 从type1到网址的转换
let type_dict = {
    '都市角色': 'a235cc8f-cfde-44a1-a335-a5f597d1486c',
    '古代角色': 'fa7f5811-6ec8-43c6-ad23-ff004eb1cb21',
    '修仙角色': '6f1c8423-3e91-43ec-b4aa-1e55f192c76a',
    '网游角色': 'bd4a7625-8e8b-4ef5-aa9a-d8d24451c54e',
    '同人角色': 'afe3c6bf-b0db-4678-85d5-e75016824089',
    '诡异角色': '6560ad1f-a1ca-4840-8256-7f5c9aa2f44f',
    '女频角色': '55bea5e0-d254-48ef-9e55-1bc949b5f110',
    '场景': 'f4399dd6-98f7-449d-8a6c-d026dab4bd54',
    '怪兽': '369e3b8a-5fe3-4f49-906d-4f64dda17219',
    '特效': '62320f96-edd2-402b-9439-86a805c42355',
    '道具': '06e2e52c-1b5d-4a7f-9c43-f18392063474'
}
let PsdProp = {
    'rw': 'sddhRwsc',
    'bj': 'sddhBjt',
    'dj': 'sddhDjgl',
    'tx': 'sddhTx'
}

// api接口写在这里 后面调用api即可
const api = {
    // 获取素材列表 page页码,limit每页个数,type1大类(‘人物、背景、道具、特效’的小写首字母),
    // tpye2小类型(每个大类不同) 可为空,key搜索关键字(搜索时用)  可为空
    // 如getList(1, 20, 'tx','ddtx', '鬼手').then(res=>{ console.log(res.data) });
    // 第[1]页的[20]个[特效]类的[打斗特效],且包含关键字['鬼手']的素材
    // 1.获取素材列表
    async getList(page, limit, type1, type2 = '', key = '') {
        if (kind_dict[type1] == undefined) {
            console.log('搜索大类错误'); return null;
        }
        const res = await axios({
            url: `https://mxjbh.cn/mxjbh/${kind_dict[type1]}web/page?page=${page}&limit=${limit}${type2 == 'a' ? '' : '&type='}${type2 == 'a' ? '' : type2}&filename=${key}`,
            method: 'get'
        });

        if (!res) return;
        const data = res.data.page;
        const pages = [];

        for (let i = 0; i < data.list.length; i++) {
            pages.push({
                // atob(res.data.page.list[i].photoPath)
                "id": data.list[i].id,
                "fileName": data.list[i].fileName,
                "photoPath": `https://mxjbh.oss-cn-beijing.aliyuncs.com/${decodeBase64(res.data.page.list[i].photoPath)}?x-oss-process=image/resize,l_400`,
                "type1": type1,
                "type2": data.list[i].type,
                "createTime": data.list[i].createTime,
            });
            // console.log(pages[i].photoPath);
        }
        data.list = pages;
        return data;
    },
    // 2.获取素材的Psd
    async getPsd(id, type1) {
        if (kind_dict[type1] == undefined) {
            console.log('大类错误'); return null;
        }
        console.log(`https://mxjbh.cn/mxjbh/${kind_dict[type1]}info/${id}`);
        const res = await axios({
            url: `https://mxjbh.cn/mxjbh/${kind_dict[type1]}info/${id}`,
            method: 'get'
        });
        const data = res.data;
        if (data === undefined) return '';
        const address = data[PsdProp[type1]].filePath;
        const psd_url = `http://mxjbh.oss-cn-beijing.aliyuncs.com/${decodeBase64(address)}`;
        return psd_url;
    },
    // 3.登录接口
    async login(username, password) {
        const mac_address = await window.pywebview.api.get_mac_address();
        if (!mac_address) return { 'code': 499, 'message': '识别机器码失败！' };
        const res = await axios.post(
            `http://www.95manhua.com/api/auth/login`,
            {
                username: username,  // 键名无需引号（合法标识符）
                password: password,
                device_id: mac_address
            },
            {  // 第三个参数是配置对象（包含请求头）
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );
        if (res == undefined) {
            return {
                'code': 499, "data": {
                    "token": ''
                }, 'message': '登录失败！'
            };
        }
        console.log(res.request.response);
        const res2 = JSON.parse(res.request.response);
        res2.data = {
            "token": (res2.result == null) ? '' : res2.result.token
        }
        console.log(res2);
        return res2;
    },
    // 4. v2 获取素材列表
    async getList2(page, limit, type = '', key = '') {
        if (type == undefined || type == '') {
            console.log('类型为空');
            return;
        }

        const res = await axios({
            url: `https://mxjbh.cn/mxjbh/${kind_dict[type1]}web/page?page=${page}&limit=${limit}${type2 == 'a' ? '' : '&type='}${type2 == 'a' ? '' : type2}&filename=${key}`,
            method: 'get'
        });

        if (!res) return;
        const data = res.data.page;
        const pages = [];

        for (let i = 0; i < data.list.length; i++) {
            pages.push({
                // atob(res.data.page.list[i].photoPath)
                "id": data.list[i].id,
                "fileName": data.list[i].fileName,
                "photoPath": `https://mxjbh.oss-cn-beijing.aliyuncs.com/${decodeBase64(res.data.page.list[i].photoPath)}?x-oss-process=image/resize,l_400`,
                "type1": type1,
                "type2": data.list[i].type,
                "createTime": data.list[i].createTime,
            });
            // console.log(pages[i].photoPath);
        }
        data.list = pages;
        return data;
    },
}

export default api