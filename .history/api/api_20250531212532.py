#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2022-03-21 17:01:39
LastEditTime: 2024-09-08 20:28:48
Description: 业务层API，供前端JS调用
usage: 在Javascript中调用window.pywebview.api.<methodname>(<parameters>)
'''

from api.storage import Storage
from api.system import System
from jysdk.jianying import JianYing
from jysdk.tools import *
from flask import Flask
import shutil
import base64
import subprocess
import uuid
import hashlib
import requests
import re
import glob
import psutil

class API(System, Storage):
    '''业务层API，供前端JS调用'''
    def setWindow(self, window):
        '''获取窗口实例'''
        System._window = window
    
    # 初始化
    def initSoftware(self):
        # 创建./assets文件夹，创建st.json文件（文件夹存在则跳过） 此后获取配置目录更改一下
        if os.path.exists('./assets/st.json'):
            return
        if not os.path.isdir('./assets'):
            # 创建目录
            os.makedirs('./assets')
        # 创建st.json文件
        with open(os.path.join('./assets','st.json'),'w',encoding='utf-8') as f:
            st = {
                "draftPath": "",
                "jyFilePath": "",
                "username": "",
                "password": ""
            }
            json.dump(st, f, indent=2, ensure_ascii=False)
        return

    # 1.获取草稿目录
    def get_draft_path(self):
        '''获取草稿目录'''
        path = open_json('./assets/st.json')['draftPath']
        path = os.path.join(path, 'draft')
        if not os.path.isdir(path):
            os.makedirs(path)
            print(f'{path}文件夹已创建')
        return path

    # 2.获取剪映目录
    def get_jyfile_path(self):
        '''获取JY文件路径'''
        json = open_json('./assets/st.json')
        return json['jyFilePath']

    # 3.制作剪映 
    def makeJY(self, project,name):
        '''根据json制作JY文件到目录'''
        jy = JianYing(self.get_jyfile_path(), name, os.path.join(self.get_draft_path(), 'jbh'))  # 类名
        start = 0
        last_time = 0
        for iindex,segement in enumerate(project):
            start2 = start
            t = segement['time']
            txt = segement['text']
            img = segement['image']  # list类型
            for index, tt in enumerate(t):
                t_ind = get_duration(tt)
                jy.addCaption(start, t_ind, txt[index], tk=jy.tracks[0])  # 加字幕
                # 计算deta_t  convert_to_seconds(time_str)
                if index + 1 < len(t):
                    # index+1是合法的
                    t_next = t[index + 1]
                    s1, e1 = tt.split(' --> ')
                    s2, e2 = t_next.split(' --> ')
                    deta_t = convert_to_seconds(s2)-convert_to_seconds(e1)
                    print(index,iindex,deta_t)
                else:
                    # 当index + 1不合法时，意味着要算到下一个segement的deta_t
                    if iindex + 1 < len(project):
                        t_next = project[iindex + 1]['time'][0]
                        s1, e1 = tt.split(' --> ')
                        s2, e2 = t_next.split(' --> ')
                        deta_t = convert_to_seconds(s2)-convert_to_seconds(e1)
                    else:
                        deta_t = 0                    
                start += t_ind + deta_t
            jy.addImages(start2, start - start2, img, jy.tracks[1:])  # 添加图片
        # 使字幕最顶层
        jy.turnCaptionTop()
        jy.save()  # 保存文件
    
    # 4.创建草稿文件夹 'jbh'目录下
    def createDraftDocument(self,name,project,srt):
        base_path = os.path.join(self.get_draft_path(),'jbh')
        path = os.path.join(base_path,name)
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            # 已经存在，需要重新命名,判断到了副本几
            i = 1
            while True:
                path = os.path.join(base_path,name+f'副本{i}')
                if os.path.exists(path):
                    i += 1
                    continue
                os.makedirs(path)
                break
        # 自此path为文件最终路径路径
        # 创建Project.json和Project.srt
        with open(os.path.join(path,'Project.json'),'w',encoding='utf-8') as f:
            json.dump(project, f, indent=2, ensure_ascii=False)
        with open(os.path.join(path,'Project.srt'),'w',encoding='utf-8') as f:
            f.write(srt)
        return os.path.basename(path)
        
    # 5.转换字幕为project文件
    def parseSrt(self, srt):
        lines = srt.splitlines()
        subtitles = []
        subtitle = None
        for line in lines:
            line = line.rstrip('\n')
            if line.isdigit():
                continue  # 跳过字幕序号
            elif ' --> ' in line:
                start, end = line.split(' --> ')
                subtitle = {'start': start, 'end': end, 'text': ''}
            elif line:
                subtitle['text'] += line
            elif subtitle and subtitle['text']:
                subtitles.append(subtitle)
                subtitle = None

        # 检查最后一行字幕是否被遗漏
        if subtitle and subtitle['text']:
            subtitles.append(subtitle)

        project = []
        i = 1
        for sub in subtitles:
            dict = {
                "id": i,
                "time": [
                    f"{sub['start']} --> {sub['end']}"
                ],
                "text": [
                    sub['text']
                ],
                "image": []
            }
            project.append(dict)
            i += 1
        return project

    # 6*.在本地中打开文件
    def select_file_in_explorer(self,file_path):
        # 将路径转换为绝对路径
        file_path = os.path.abspath(file_path)
        # 使用 explorer /select 命令
        subprocess.run(f'explorer /select,"{file_path}"', shell=True)

    # 7.定位草稿 位置
    def siteDraft(self,name):
        # 计算位置
        jbh_path = os.path.join(self.get_draft_path(),'jbh')
        path = os.path.join(jbh_path,name)
        if not os.path.exists(path):
            return False
        self.select_file_in_explorer(path)
        return True
    
    # 8.删除草稿文件夹
    def deleteDraft(self,name):
        # 计算位置
        jbh_path = os.path.join(self.get_draft_path(),'jbh')
        file_path = os.path.join(jbh_path,name)
        # 删除文件
        try:
            shutil.rmtree(file_path)
            print(f"文件 {file_path} 已删除")
            return 1
        except FileNotFoundError:
            print(f"文件 {file_path} 不存在")
        except PermissionError:
            print(f"没有权限删除文件 {file_path}")
        except Exception as e:
            print(f"删除文件时出错: {e}")
        return 0;

    # 9.获取草稿列表
    def getDrafts(self):
        ''' 从目录中获取draft的name和createTime
            1. 获取draft目录+jbh内的所有文件夹name和createTime
            2. 依次判断文件project.json是否存在,存在则加入ans。最后返回ans
        '''
        folder_path = os.path.join(self.get_draft_path(),'jbh')
        # 确保传入的路径是一个文件夹
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
            return []
        # 获取文件夹中的所有条目
        entries = os.listdir(folder_path)
        print(entries)
        # 遍历条目，筛选出文件夹并获取其创建时间
        folder_info = []
        for entry in entries:
            entry_path = os.path.join(folder_path, entry)
            project_path = os.path.join(entry_path, 'project.json')
            if os.path.isdir(entry_path) and os.path.exists(project_path) :  # 确保是文件夹，且project.json存在
                # 获取创建时间（注意：在 Windows 上是创建时间，在 Unix 系统上是元数据最后改变的时间）
                creation_time = os.path.getctime(entry_path)
                readable_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(creation_time))
                folder_info.append({
                    'name':entry,
                    'createTime':readable_time,
                    'time':os.path.getmtime(entry_path)
                })
        folder_info.sort(key=lambda x: x["time"], reverse=True)
        return folder_info

    # 10.获取草稿project格式文件
    def getProject(self,name):
        # 计算位置
        jbh_path = os.path.join(self.get_draft_path(),'jbh')
        path = os.path.join(jbh_path,name)
        ppath = os.path.join(path,'project.json')
        if not os.path.exists(ppath):
            return False
        # 读取ppath的json文件，并且返回
        return open_json(ppath)

    # 11.保存素材图片
    def saveAsset(self,file_data,filename,size,draft_path):
        # 去掉前缀 'data:image/png;base64,'（如果有的话）
        if file_data.startswith('data:image'):
            file_data = file_data.split(',')[1]

        # 解码图片数据
        image_data = base64.b64decode(file_data)

        # 设置保存路径（根据需要调整）
        base_path = os.path.join(self.get_draft_path(),'jbh',draft_path)
        if not os.path.isdir(base_path):
            os.makedirs(base_path)
        save_path = os.path.join(base_path, filename)
        print(save_path)


        name, extension = os.path.splitext(filename)

        # 如果路径已存在，重复命名，直到save_path路径不存在
        if os.path.isfile(save_path):
            # 如果图片名字和时间戳都相同，则直接返回url
            pysize = os.path.getsize(save_path)
            if pysize == size:
                print('文件已存在，不必保存')
                return {"status": "success", "message": "Image already exists",'name':filename}
            # 循环命名，直到save_path不存在
            i = 1
            while True:
                save_path = os.path.join(base_path,name + f'({i})' + extension)
                if os.path.exists(save_path):
                    i += 1
                    continue
                break

        # 保存图片到本地
        with open(save_path, 'wb') as f:
            f.write(image_data)

        print(f"图片已保存： {save_path}")
        return {"status": "success", "message": "Image uploaded successfully",'name':os.path.basename(save_path)}

    # 12.获取机器码
    def get_mac_address(self):
        # 获取所有网络接口信息
        interfaces = psutil.net_if_addrs()
        
        # 遍历所有接口
        for interface_name, addresses in interfaces.items():
            # 忽略虚拟网卡（根据接口名称过滤）
            if interface_name.startswith(('lo', 'virbr', 'vmnet', 'vboxnet', 'docker', 'wlp')):
                continue
            
            # 查找 MAC 地址
            for address in addresses:
                if address.family == psutil.AF_LINK:  # AF_LINK 表示 MAC 地址
                    mac_address = address.address.replace('-', ':')  # 统一格式
                    print(f"Physical MAC Address: {mac_address}")
                    
                    # 生成特征码
                    feature_code = hashlib.sha256(mac_address.encode()).hexdigest()
                    print(feature_code)
                    return feature_code
        
        # 如果没有找到物理网卡的 MAC 地址
        return '564763'

    # 13.保存json配置文件
    def saveSetting(self,setting):
        with open('./assets/st.json','w',encoding='utf-8') as f:
            json.dump(setting, f, indent = 2 , ensure_ascii = False)
        return

    # 14.创建工作文件夹
    def createWorkdir(self):
        # （0）获取地址
        # （1）判断地址是否存在
        #  (2) 创建draft目录
        draft_path = open_json('./assets/st.json')['draftPath']
        jyfile_path = open_json('./assets/st.json')['jyFilePath']
        if os.path.isdir(draft_path) and os.path.isdir(jyfile_path):
            if not os.path.isdir(os.path.join(draft_path,'draft/jbh')):
                os.makedirs(os.path.join(draft_path,'draft/jbh'))
            if not os.path.isdir(os.path.join(draft_path,'draft/uploadResource')):
                os.makedirs(os.path.join(draft_path,'draft/uploadResource'))
            if not os.path.isdir(os.path.join(draft_path,'draft/myPsd')):
                os.makedirs(os.path.join(draft_path,'draft/myPsd'))
            if not os.path.isdir(os.path.join(draft_path,'draft/myImage')):
                os.makedirs(os.path.join(draft_path,'draft/myImage'))
            if not os.path.isdir(os.path.join(draft_path,'draft/cache')):
                os.makedirs(os.path.join(draft_path,'draft/cache'))
            return True
        else:
            return False
        
    # 15.获取账号密码
    def getUserInfo(self):
        # 读取json文件，获取账号密码
        username = open_json('./assets/st.json')['username']
        password = open_json('./assets/st.json')['password']
        return {
            'username':username,
            'password':password
        }

    # 16.保存project文件
    def saveDraft(self,name,project):
        # 1.根据草稿名name找到草稿文件路径path
        # 2.找到路径后，打开路径，写入新的project
        base_path = os.path.join(self.get_draft_path(),'jbh')
        path = os.path.join(base_path,name)
        if not os.path.exists(path):
            return False
        with open(os.path.join(path,'Project.json'),'w',encoding='utf-8') as f:
            json.dump(project, f, indent=2, ensure_ascii=False)
        return True

    # 17.检测psd文件是否存在，返回url
    def psdIsExist(self,url):
        try:
            part_after_upload = url.split("uploadResource/")[1]
            path = part_after_upload.split('?')[0]
            myPsd_path = os.path.join(self.get_draft_path(),'uploadResource')
            psd_path = os.path.join(myPsd_path,path)
            if not os.path.exists(psd_path):
                return url
            else:
                new_url = 'http://localhost:6500/images/uploadResource/' + path
                return new_url
        except:
            return ''

    # 18.下载psd文件到本地uploadResource
    def downloadPsd(self,url):

        part_after_upload = url.split("uploadResource/")[1]
        path = part_after_upload.split('?')[0]

        myPsd_path = os.path.join(self.get_draft_path(),'uploadResource')
        psd_path = os.path.join(myPsd_path,path)
        dir_path = os.path.dirname(psd_path)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        try:
            # 发送 GET 请求
            response = requests.get(url)
            # 检查请求是否成功
            if response.status_code == 200:
                # 将文件内容保存到本地
                with open(psd_path, 'wb') as file:
                    file.write(response.content)
                print(f"File saved as {psd_path}")
            else:
                print(f"Failed to download file. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")
        
    # 19.保存收藏图片 favorKind不带最后文件 .png
    def saveFavorImage(self,file_data,filename,favorKind):
        # 去掉前缀 'data:image/png;base64,'（如果有的话）
        if file_data.startswith('data:image'):
            file_data = file_data.split(',')[1]

        # 解码图片数据
        image_data = base64.b64decode(file_data)

        # 设置保存路径（根据需要调整）
        base_path = os.path.join(self.get_draft_path(),'myImage',favorKind)
        if not os.path.isdir(base_path):
            os.makedirs(base_path)
        save_path = os.path.join(base_path, filename)
        print(save_path)

        name, extension = os.path.splitext(filename)

        # 如果路径已存在，重复命名，直到save_path路径不存在
        if os.path.isfile(save_path):
            # 循环命名，直到save_path不存在
            i = 1
            while True:
                save_path = os.path.join(base_path,name + f'({i})' + extension)
                if os.path.exists(save_path):
                    i += 1
                    continue
                break

        # 保存图片到本地
        with open(save_path, 'wb') as f:
            f.write(image_data)

        print(f"图片已保存： {save_path}")
        return {"status": "success", "message": "Image uploaded successfully",'name':os.path.basename(save_path)}

    # 20.保存收藏Psd
    def saveFavorPsd(self,url,filename,favor_kind):
        myPsd_path = os.path.join(self.get_draft_path(),'myPsd')
        dir_path = os.path.join(myPsd_path,favor_kind)
        psd_path = os.path.join(dir_path,filename)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        try:
            # 发送 GET 请求
            response = requests.get(url)
            # 检查请求是否成功
            if response.status_code == 200:
                # 将文件内容保存到本地
                with open(psd_path, 'wb') as file:
                    file.write(response.content)
                print(f"File saved as {psd_path}")
            else:
                print(f"Failed to download file. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")

    # 21.创建文件夹(收藏夹)
    def createDir(self,path):
        dir_path = os.path.join(self.get_draft_path(),path)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
            return True
        return False

    # 22.获取图片收藏列表
    def getFavorImageKinds(self):
        favor_img_path = os.path.join(self.get_draft_path(),'myImage')
        if not os.path.isdir(favor_img_path):
            os.makedirs(favor_img_path)
        # 获取当前目录下的所有文件和文件夹
        all_items = os.listdir(favor_img_path)
        # 筛选出文件夹
        folders = [item for item in all_items if os.path.isdir(os.path.join(favor_img_path, item))]
        return folders

    # 23.获取Psd收藏列表
    def getFavorPsdKinds(self):
        favor_psd_path = os.path.join(self.get_draft_path(),'myPsd')
        if not os.path.isdir(favor_psd_path):
            os.makedirs(favor_psd_path)
        # 获取当前目录下的所有文件和文件夹
        all_items = os.listdir(favor_psd_path)
        # 筛选出文件夹
        folders = [item for item in all_items if os.path.isdir(os.path.join(favor_psd_path, item))]
        return folders

    # 24. 删除文件夹
    def deleteDir(self,path):
        dir_path = os.path.join(self.get_draft_path(),path)
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
            return True
        return False

    # 25.下载缓存图片
    def saveFavorPsdCache(self,url,filename,favor_kind):
        myPsd_path = os.path.join(self.get_draft_path(),'cache')
        dir_path = os.path.join(myPsd_path,favor_kind)
        psd_path = os.path.join(dir_path,filename)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        try:
            # 发送 GET 请求
            response = requests.get(url)
            # 检查请求是否成功
            if response.status_code == 200:
                # 将文件内容保存到本地
                with open(psd_path, 'wb') as file:
                    file.write(response.content)
                print(f"File saved as {psd_path}")
            else:
                print(f"Failed to download file. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")

    # 26.保存project文件
    def saveProject(self,draft_name,project):
        path = os.path.join(self.get_draft_path(),'jbh',draft_name)
        if not os.path.isdir(path):
            os.makedirs(path)
        with open(os.path.join(path,'Project.json'),'w',encoding='utf-8') as f:
            json.dump(project, f, indent=2, ensure_ascii=False)
        return

    # 27.url2path
    def url2path(self,url):
        pattern = re.compile(r'http://localhost:\d+/images(.*)')
        match = pattern.search(url)
        if match:
            relativePath = match.group(1).replace('/', '\\')
            path = self.get_draft_path() + relativePath
            return path
        else:
            return ''

    # 28.获取收藏的图片信息（返回total和list）
    def getFavImage(self,kind):
        # 获取kind类中的所有图片
        path = os.path.join(self.get_draft_path(),'myImage',kind)
        if not os.path.exists(path):
            return []
        # 获取path中的所有文件
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff']
        image_files = []
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(path, ext)))
        image_files.sort(key=os.path.getctime, reverse=True)
        image_names = [os.path.basename(image) for image in image_files]
        return image_names

    # 29.获取收藏psd
    def getFavPsd(self,kind):
        # 获取kind类中的所有图片
        path = os.path.join(self.get_draft_path(),'myPsd',kind)
        if not os.path.exists(path):
            return []
                # 获取path中的所有文件
        image_extensions = ['*.psd']
        image_files = []
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(path, ext)))
        # print(image_files)
        image_files.sort(key=os.path.getctime, reverse=True)
        image_names = [os.path.basename(image) for image in image_files]
        return image_names

    # 30.生成缓存图片
    def makeFavorPsdCache(self,file_data,filename,favor_kind):
        myPsd_path = os.path.join(self.get_draft_path(),'cache')
        dir_path = os.path.join(myPsd_path,favor_kind)
        psd_path = os.path.join(dir_path,filename)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        try:
            # 去掉前缀 'data:image/png;base64,'（如果有的话）
            if file_data.startswith('data:image'):
                file_data = file_data.split(',')[1]

            # 解码图片数据
            image_data = base64.b64decode(file_data)

            # 保存图片到本地
            with open(psd_path, 'wb') as f:
                f.write(image_data)
        except Exception as e:
            print(f"An error occurred: {e}")

    # 31.由本地psd加入收藏列表 saveFavorPsdFromUs
    def saveFavorPsdFromUs(self,file_data,filename,favor_kind):
        myPsd_path = os.path.join(self.get_draft_path(),'myPsd')
        dir_path = os.path.join(myPsd_path,favor_kind)
        file_path = os.path.join(dir_path,filename)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        binary_data = bytes(file_data)

        # 将二进制数据写入文件
        with open(file_path, 'wb') as f:
            f.write(binary_data)

    # 32.重命名收藏的图片
    def renameFile(self,new_name,url):
        path = self.url2path(url)
        directory = os.path.dirname(path)
        basename = os.path.basename(path)
        name, extension = os.path.splitext(basename)
        # 构建新的文件路径
        new_path = os.path.join(directory, new_name + extension)
        if not os.path.exists(path):
            return
        try:
        # 重命名文件
            os.rename(path, new_path)
            print(f"文件已成功重命名为 {new_name}")
        except FileNotFoundError:
            print(f"未找到文件: {old_path}")
        except FileExistsError:
            print(f"新文件名 {new_name} 已存在，请选择其他名称。")
        except PermissionError:
            print("没有足够的权限来重命名文件。")
        return

    # 33.删除图片
    def deleteFile(self,url):
        file_path = self.url2path(url)
        try:
            # 尝试删除指定路径的文件
            os.remove(file_path)
            print(f"文件 {file_path} 已成功删除。")
        except FileNotFoundError:
            print(f"未找到文件: {file_path}")
        except PermissionError:
            print("没有足够的权限来删除该文件。")
        except IsADirectoryError:
            print(f"{file_path} 是一个目录，不是文件，请使用合适的方法删除目录。")

    # 34.检查设置是否正确
    def veritySetting(self):
        '''获取草稿目录'''
        try:
            dict1 = open_json('./assets/st.json')
            path1 = dict1['draftPath']
            path2 = dict1['jyFilePath']
            if not os.path.isdir(path1):
                return False
            if not os.path.isdir(path2):
                return False
            if not dict1['username']:
                return False
            if not dict1['password']:
                return False
            return True
        except:
            return False

    # 35.读取所有目录
    def getAllConfig(self):
        try:
            dict1 = open_json('./assets/st.json')
            return dict1
        except:
            return []

    # 36.重命名草稿名
    def renameDir(self,name,new_name):
        if new_name == '':
            return
        path = os.path.join(self.get_draft_path(),'jbh',name)
        new_path = os.path.join(self.get_draft_path(),'jbh',new_name)
        if os.path.isdir(new_path):
            return -1
        if os.path.isdir(path):
            # 先对该目录下的project文件进行地址替换，用正则
            # 读取JSON文件
            file_path = os.path.join(path,'Project.json')
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # 将JSON对象转换为字符串
            json_str = json.dumps(data)

            # 替换字符串
            new_json_str = json_str.replace(f'\\jbh\\{name}\\', f'\\jbh\\{new_name}\\')

            # 将字符串转换回JSON对象
            new_data = json.loads(new_json_str)
            # 将修改后的JSON对象写回文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(new_data, file, ensure_ascii=False, indent=2)
            os.rename(path,new_path)
            return 1
        else:
            return 0

    # 37.通过环境变量获取剪影文件目录

    def get_jianying_draft_path(self):
        import winreg
        try:
            # 定义注册表路径和键名
            root_key = winreg.HKEY_CURRENT_USER
            sub_key = r"Software\ByteDance\JianyingPro\GlobalSettings\History"
            value_name = "currentCustomDraftPath"
            # 打开注册表项
            with winreg.OpenKey(root_key, sub_key) as key:
                # 查询键值
                value_data, value_type = winreg.QueryValueEx(key, value_name)

                # 处理特殊类型数据（如环境变量路径）
                if value_type == winreg.REG_EXPAND_SZ:
                    import os
                    return os.path.expandvars(value_data)
                return value_data
            return ""
        except FileNotFoundError:
            return ""


    # 38.通过url收藏图片（收藏jbh中的图片）,filename带后缀
    def saveFavorImage2(self,url,filename,favorKind):
        # 通过url获取文件地址，找到并移动到收藏目录，然后再直接返回收藏目录url
        rela_path = url.replace('http://localhost:6500/images/','')
        print(rela_path)
        init_path = os.path.join(self.get_draft_path(),rela_path)

        # 设置移动目标路径（根据需要调整）
        base_path = os.path.join(self.get_draft_path(),'myImage',favorKind)
        if not os.path.isdir(base_path):
            os.makedirs(base_path)
        save_path = os.path.join(base_path, filename)
        print(save_path)

        name, extension = os.path.splitext(filename)

        # 如果路径已存在，重复命名，直到save_path路径不存在
        if os.path.isfile(save_path):
            # 循环命名，直到save_path不存在
            i = 1
            while True:
                save_path = os.path.join(base_path,name + f'({i})' + extension)
                if os.path.exists(save_path):
                    i += 1
                    continue
                break
        print('save_path',save_path)
        # 复制文件到save_path
        shutil.copyfile(init_path,  save_path)

        print(f"图片已保存： {save_path}")
        return {"status": "success", "message": "Image uploaded successfully",'name':os.path.basename(save_path)}

    # 39.通过url获取名字
    def get_name_from_url(self,url):
        path = self.url2path(url)
        filename = os.path.basename(path)
        name, extension = os.path.splitext(filename)
        return name

    # 40.获取软件设置
    def get_software_setting(self):
        try:
            dict1 = open_json('./_internal/static/assets/st.json')
            dark = dict1['dark']
            return dark
        except:
            dict1['dark'] = False
            with open(os.path.join('./_internal/static/assets/st.json'),'w',encoding='utf-8') as f:
                json.dump(dict1, f, indent=2, ensure_ascii=False)
            return False

    # 40.设置黑夜白天
    def set_dark(self,dark):
        try:
            dict1 = open_json('./_internal/static/assets/st.json')
            dict1['dark'] = dark
            with open(os.path.join('./_internal/static/assets/st.json'),'w',encoding='utf-8') as f:
                json.dump(dict1, f, indent=2, ensure_ascii=False)
            return
        except:
            dict1['dark'] = False
            with open(os.path.join('./_internal/static/assets/st.json'),'w',encoding='utf-8') as f:
                json.dump(dict1, f, indent=2, ensure_ascii=False)
            return
        