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
        const res = await axios.post(`http://www.95manhua.com/api/auth/login`, {
            'username': username,
            'password': password,
            'device_id': mac_address
        });
        if (res == undefined) {
            return {
                'code': 499, "data": {
                    "token": ''
                }, 'message': '登录失败！'
            };
        }
        res.data = {
            "token": (res.result == null) ? '' : res.result.token
        }
        console.log(res);
        return res;
    },
}

export default api