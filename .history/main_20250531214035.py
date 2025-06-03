#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2022-03-23 15:41:46
LastEditTime: 2024-09-08 20:29:41
Description: 生成客户端主程序
usage: 运行前，请确保本机已经搭建Python3开发环境，且已经安装 pywebview 模块。
'''

import argparse
import mimetypes
import os
from flask import Flask,send_from_directory, send_file
import threading
import webview
import sqlalchemy
import sys
from api.api import API
from pyapp.config.config import Config
from pyapp.db.db import DB
from flask_cors import CORS
import requests


cfg = Config()    # 配置
db = DB()    # 数据库类
api = API()    # 本地接口
api.initSoftware()  # 初始化软件


cfg.init()
app2 = Flask(__name__)
CORS(app2)  # 全局启用 CORS

# 定义本地图片目录


@app2.route('/')
def index():
    # 通过 Flask 提供图片文件
    return "helloworld11"

# Flask 路由：根据文件名返回文件url地址
@app2.route('/images/<path:filename>')
def get_image(filename):
    # 通过 Flask 提供图片文件
    # filename从draft开始
    if os.path.exists(os.path.join(api.get_draft_path(), filename)):
        return send_from_directory(api.get_draft_path(), filename)
    else:
        return "File not found", 404

# Flask 路由：阿里云接口转接
@app2.route('/proxy/<path:url>', methods=['GET'])
def proxy(url):
    # 发送GET请求到实际的PSD文件URL
    print('proxy-url',url)
    response = requests.get(url, stream=True)
    # 检查请求是否成功
    if response.status_code == 200:
        # 使用send_file发送文件内容
        return send_file(
            response.raw,
            mimetype='application/octet-stream',  # PSD文件的MIME类型
            as_attachment=True,
            download_name='file.psd'  # 指定下载的文件名
        )
    else:
        # 如果请求失败，返回错误状态码
        return response


def start_flask():
    app2.run(debug=True, use_reloader=False, port=6500)


def on_shown():
    # print('程序启动')
    db.init()    # 初始化数据库


def on_loaded():
    # print('DOM加载完毕')
    pass


def on_closing():
    # print('程序关闭')
    pass


def WebViewApp(ifCef=False):

    # 是否为开发环境
    Config.devEnv = sys.flags.dev_mode

    # 视图层页面URL
    if Config.devEnv:
        # 开发环境
        MAIN_DIR = f'http://localhost:{Config.devPort}/'
        template = os.path.join(MAIN_DIR, "")    # 设置页面，指向远程
    else:
        # 生产环境
        MAIN_DIR = os.path.join(".", "web")
        template = os.path.join(MAIN_DIR, "index.html")    # 设置页面，指向本地

        # 修复某些情况下，打包后软件打开白屏的问题
        mimetypes.add_type('application/javascript', '.js')

    # 系统分辨率
    screens = webview.screens
    screens = screens[0]
    width = screens.width
    height = screens.height
    # 程序窗口大小
    initWidth = int(width * 4 / 5)
    initHeight = int(height * 4 / 5)
    minWidth = int(initWidth*2 / 3)
    minHeight = int(initHeight*2 / 3)
    # background_color 背景色
    # 创建窗口
    window = webview.create_window(background_color='#f9f9f9',title=Config.appTitle, url=template, js_api=api, width=initWidth, height=initHeight, min_size=(minWidth, minHeight))

    # 在单独线程中启动 Flask
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()


    # 获取窗口实例
    api.setWindow(window)

    # 绑定事件
    window.events.shown += on_shown
    window.events.loaded += on_loaded
    window.events.closing += on_closing

    # CEF模式
    guiCEF = 'cef' if ifCef else None

    # 启动窗口
    webview.start(debug=Config.devEnv, http_server=True, gui=guiCEF)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cef", action="store_true", dest="if_cef", help="if_cef")
    args = parser.parse_args()

    ifCef = args.if_cef    # 是否开启cef模式

    WebViewApp(ifCef)
