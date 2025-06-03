import os
from jysdk.tools import *
import time

class JianYing:
    # 初始化
    def __init__(self, path, name,jhb_path):
        self.save_path = os.path.join(path,name)
        self.name = name
        self.content_template , self.meta_template = get_template()
        self.time_length = 0
        self.caption_num = 0
        # 初始化两个模版
        self.content_template['id'] = generate_id()  # 给模版ID设置唯一id
        self.tracks = self.content_template['tracks']  # 列表引用-轨道
        tk = track('caption', 'text')  # 字幕轨道
        self.tracks.append(tk)
        self.text_style= self.content_template['materials']['texts']  # 列表引用-字体样式
        self.material_animations = self.content_template['materials']['material_animations']  # 列表引用-动画效果
        self.meta_template['id'] = generate_id()
        self.meta_template['draft_root_path'] = path  # 剪映的草稿路劲 如：D:\\\\software\\\\剪映\\\\JianyingPro Drafts
        self.meta_template['tm_draft_create'] = int(time.time() * 1000)  # draft_meta_info.json创建时间，时间戳
        self.meta_template['tm_draft_modified'] = generate_16_digit_timestamp()  # 13或16位毫秒级时间戳
        self.meta_template['draft_removable_storage_device'] = get_drive_from_path(path)  # 磁盘的驱动器 如"D:"
        self.meta_template['draft_fold_path'] = self.save_path.replace('\\','/')  # 剪映安装路劲加上草稿名字 如： D:/software/剪映/JianyingPro Drafts/六合八荒唯我独尊
        self.meta_template['draft_name'] = self.name  # 草稿名字 如："六合八荒唯我独尊"
        draft_materials = os.path.join(jhb_path,name)  # 添加图片资源夹 如：‘D:\YJtest\draft\jbh\你明明是高考满分的三好学生’
        self.meta_template['draft_materials'].append(draft_materials)

    # 将最底层的track移动到tracks的最上层
    def turnCaptionTop(self):
        self.tracks.append(self.tracks[0])
        del self.tracks[0]
        return

    # 加字幕
    def addCaption(self,start,duration,text,tk=None):  # track为None时，自动创建轨道 strat、duration单位是s
        if tk == None:
            tk = track('caption','text')   # 单轨道默认新建轨道
            self.tracks.append(tk)
        # 配置字体样式、字体动作，写segment
        index = self.caption_num
        text_style = texts_items(text)
        material_animations = material_animations_items()
        sg = segments_font(index,start*1000000,duration*1000000)
        sg['extra_material_refs'].append(material_animations['id'])
        sg['material_id']= text_style['id']
        tk['segments'].append(sg)
        self.text_style.append(text_style)
        self.material_animations.append(material_animations)
        self.caption_num += 1
        self.time_length = max(self.time_length,(start+duration)*1000000)
        return


    # 添加一张图片到track轨迹中
    def addImageToTrack(self,start,duration,img,track):
        # 修改tracks下的segments
        # 生成id
        canvases_id = generate_id()
        sound_channel_mappings_id = generate_id()
        speeds_id = generate_id()
        videos_id = generate_id()
        vocal_separations_id = generate_id()
        # 修改canvases
        canvase = canvases_items()
        canvase['id'] = canvases_id
        self.content_template['materials']['canvases'].append(canvase)

        # 修改sound_channel_mappings
        sound = sound_items()
        sound['id'] = sound_channel_mappings_id
        sound['type'] = "none"
        self.content_template['materials']['sound_channel_mappings'].append(sound)

        # 修改speeds
        speeds = speeds_items()
        speeds['id'] = speeds_id
        self.content_template['materials']['speeds'].append(speeds)

        # 修改vocal_separations
        vocal_separation = vocal()
        vocal_separation['id'] = vocal_separations_id
        self.content_template['materials']['vocal_separations'].append(vocal_separation)

        # 修改video
        video = videos_items(os.path.basename(img),img)
        video['id'] = videos_id
        self.content_template['materials']['videos'].append(video)
        segment = segment_video()
        segment['extra_material_refs'] = [speeds_id, canvases_id, sound_channel_mappings_id, vocal_separations_id]
        segment['material_id'] = videos_id
        segment['source_timerange']['duration'] = duration*1000000
        segment['target_timerange']['duration'] = duration*1000000
        segment['target_timerange']['start'] = start*1000000  # 时间不含当前图片
        track['segments'].append(segment)



    # 添加很多图片到轨道中
    def addImages(self,start,duration,imgs,tracks=None):
        if tracks == None:  # 检查视频轨道数量，不够自动创建视频轨道
            tracks = self.tracks  # 从self中获取轨道tracks,从第0层开始for循环添加图片，若索引超出则新建picture#图层添加
        for index,img in enumerate(imgs):
            if index < len(tracks):
                self.addImageToTrack(start,duration,img,tracks[index])
            else:
                # 创建新轨道
                tk = track(f'picture{len(tracks)}', 'video')
                self.tracks.append(tk)
                self.addImageToTrack(start,duration,img,tk)
        return

    # 保存文件
    def save(self):
        self.content_template['duration'] = self.time_length
        self.meta_template['tm_duration'] = self.time_length  # 写入tm_duration 不确定有没有用
        # 创建文件夹
        os.makedirs(self.save_path,exist_ok=True)
        # 创建 draft_meta_info.json
        meta_info_path = os.path.join(self.save_path,'draft_meta_info.json')
        content_path = os.path.join(self.save_path,'draft_content.json')
        with open(meta_info_path, 'w', encoding='utf-8') as meta_info_file:
            json.dump(self.meta_template, meta_info_file, indent=4, ensure_ascii=False)
        # 创建 draft_content.json
        with open(content_path, 'w', encoding='utf-8') as content_file:
            json.dump(self.content_template, content_file, indent=4, ensure_ascii=False)
        print('生成剪印文件成功！')



# class JianYin:
#     # base_path 草稿路径 如：D:\\study\\Datawhale\\jianyin\\草稿文件\\JianyingPro Drafts
#     # folder_path 剪映安装路劲加上草稿名字 如： D:/study/Datawhale/jianyin/草稿文件/JianyingPro Drafts/2月1日
#     # novel_name 草稿名字  如：2月1日
#     def __init__(self, base_path, folder_path, novel_name):
#         # 写入操作时维护time_length的长度
#         self.time_length = 0
#         # 默认字体大小
#         self.size = 8.0
#         # 字幕编号
#         self.font_index = 1
#         self.base_path = base_path
#         self.folder_path = folder_path
#         self.novel_name = novel_name
#         self.meta_info_path = os.path.join(self.folder_path, 'draft_meta_info.json')
#         self.content_path = os.path.join(self.folder_path, 'draft_content.json')
#         # base_path 草稿路径 如：D:\\study\\Datawhale\\jianyin\\草稿文件\\JianyingPro Drafts
#         # folder_path 剪映安装路劲加上草稿名字 如： D:/study/Datawhale/jianyin/草稿文件/JianyingPro Drafts/2月1日
#         # novel_name 草稿名字  如：2月1日
#         """
#         初始化数据
#         """
#         self.template_meta_info_path, self.template_meta_content_path = template_path()  # 返回两个模版的完整路劲
#         print(template_path())
#         self.draft_content_template = read_json(self.template_meta_content_path)  # 模版1
#         self.draft_meta_template = read_json(self.template_meta_info_path)  # 模版2
#
#         self.draft_content_template['id'] = generate_id()  # 给模版ID设置唯一id
#         tracks_video_data = tracks()  # 创建tracks用于存放图片信息
#         tracks_video_data['type'] = 'video'  # 类型
#         self.draft_content_template['tracks'].append(tracks_video_data)  # 添加到模板里
#
#         # 需创建用于字幕信息的轨道
#         tracks_font_data = tracks()  # 创建tracks用于存放字幕信息
#         tracks_font_data['type'] = 'text'  # 类型
#         tracks_font_data['flag'] = 1  # 字母 flag为1
#         self.draft_content_template['tracks'].append(tracks_font_data)  # 添加到模板里
#
#         tracks_audio_data = tracks()  # 创建tracks用于存放音频信息
#         tracks_audio_data['type'] = 'audio'  # 类型
#         self.draft_content_template['tracks'].append(tracks_audio_data)  # 添加到模板里
#
#         material_animations = material_animations_items()
#         material_animations['id'] = generate_id()
#         self.draft_content_template['materials']['material_animations'].append(material_animations)
#
#         self.draft_meta_template['draft_id'] = generate_id()  # 给模版ID设置唯一id
#         self.draft_meta_template[
#             'draft_root_path'] = self.base_path  # 剪映的草稿路劲 如：D:\\\\software\\\\剪映\\\\JianyingPro Drafts
#         self.draft_meta_template['tm_draft_create'] = int(time.time() * 1000)  # draft_meta_info.json创建时间，时间戳
#         self.draft_meta_template['tm_draft_modified'] = generate_16_digit_timestamp()  # 13或16位毫秒级时间戳
#         self.draft_meta_template['draft_removable_storage_device'] = get_drive_from_path(self.base_path)  # 磁盘的驱动器 如"D:"
#         self.draft_meta_template['draft_fold_path'] = self.folder_path.replace('\\',
#                                                                                '/')  # 剪映安装路劲加上草稿名字 如： D:/software/剪映/JianyingPro Drafts/六合八荒唯我独尊
#         self.draft_meta_template['draft_name'] = self.novel_name  # 草稿名字 如："D:/software/剪映/JianyingPro Drafts/六合八荒唯我独尊"
#
#         draft_materials = draft_materials_out()  # 添加图片资源夹
#         self.draft_meta_template['draft_materials'].append(draft_materials)