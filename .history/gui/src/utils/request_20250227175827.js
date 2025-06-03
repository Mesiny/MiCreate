import axios from "axios"
import { el } from "element-plus/es/locale/index.mjs";
import querystring from "querystring"
import api from "../api";

const errrHandle = (status, info) => {
    switch (status) {
        case 400:
            console.log("语义有误"); break;
        case 401:
            console.log("服务器认证失败"); break;
        case 403:
            console.log("服务器拒绝访问"); break;
        case 404:
            console.log("地址错误"); break;
        case 500:
            console.log("服务器遇到意外"); break;
        case 502:
            console.log("服务器无响应"); break;
        default:
            console.log(info); break;
    }
}


const instance = axios.create({

    // 网络请求的公共配置
    timeout: 5000
});


const refreshToken = async (originalConfig) => {
    const user = await window.pywebview.api.getUserInfo();
    const loginResponse = await api.login(user.username, user.password)
    const newToken = loginResponse.data.token;
    if (newToken === undefined) {
        localStorage.setItem('token', ''); // 更新 token
        return;
    }
    localStorage.setItem('token', newToken); // 更新 token
    // // 重新发送原始请求
    // response.config.headers['token'] = `${newToken}`;
    return instance(originalConfig);
}


instance.interceptors.request.use(
    config => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['token'] = `${token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
)


instance.interceptors.response.use(
    response => {
        if (response.status === 200) {
            if (response.data.code === 401) { // 401 表示未授权，通常意味着 token 无效或过期
                try {

                    return refreshToken(response.config);
                } catch (loginError) {
                    // 登录失败，处理错误
                    console.error('登录失败：', loginError);
                    return Promise.reject(error);
                }
            }

            return response;
        } else {
            throw new Error(response.statusText);
        }
    },
    error => {
        const { response } = error;
        errrHandle(response)
    }
)

export default instance;