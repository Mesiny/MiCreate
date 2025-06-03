import json
import uuid
import time
import os

# 加载json文件
def open_json(filePath):
    # 打开JSON文件
    with open(filePath, 'r', encoding='utf-8') as file:
        # 将JSON文件内容解析为Python字典
        data = json.load(file)
    # 现在data变量包含了JSON文件中的数据
    return data

# 将字幕时间格式（HH:MM:SS,MMM）转换为秒数。
def convert_to_seconds(time_str):
    """
    将字幕时间格式（HH:MM:SS,MMM）转换为秒数。
    """
    hours, minutes, seconds = time_str.split(':')
    sec, milliseconds = seconds.split(',')
    total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(sec) + int(milliseconds) / 1000
    return total_seconds

# 解析 SRT 字幕文件，返回每个字幕的开始时间、结束时间和文本内容。
def parse_srt(file_path):
    """
    解析 SRT 字幕文件，返回每个字幕的开始时间、结束时间和文本内容。
    """
    subtitles = []
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()
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
    print(subtitles)
    return subtitles

# 生成uuid(大写)
def generate_id():
    """
    生成uuid(大写)
    """
    return str(uuid.uuid4()).upper()

# 时间格式（00:00:00,000 --> 00:00:01,808）转为时间段
def get_duration(time):
    if ' --> ' in time:
        start, end = time.split(' --> ')
        return convert_to_seconds(end) - convert_to_seconds(start)
    print('Get duration wrong')
    return 0


# 获取模版
def get_template():
    content_path = './_internal/static/assets/draft/draft_content_data.json'
    meta_path = './_internal/static/assets/draft/draft_meta_data.json'
    return open_json(content_path),open_json(meta_path)

# 创建track的json对象,需要轨道名字和类型
def track(name,type):
    return {
        "attribute": 0,
        "flag": 1 if type == 'text' else 0,
        "id": generate_id(),
        "is_default_name": True,
        "name": name,
        "segments": [],
        "type": type
    }

def segment_video():
    return {
        "cartoon": False,
        "clip": {
            "alpha": 1.0,
            "flip": {
                "horizontal": False,
                "vertical": False
            },
            "rotation": 0.0,
            "scale": {
                "x": 1.0,
                "y": 1.0
            },
            "transform": {
                "x": 0.0,
                "y": 0.0
            }
        },
        "common_keyframes": [],
        "enable_adjust": True,
        "enable_color_curves": True,
        "enable_color_match_adjust": False,
        "enable_color_wheels": True,
        "enable_lut": True,
        "enable_smart_color_adjust": False,
        "extra_material_refs": [],
        "group_id": "",
        "hdr_settings": {
            "intensity": 1.0,
            "mode": 1,
            "nits": 1000
        },
        "id": generate_id(),
        "intensifies_audio": False,
        "is_placeholder": False,
        "is_tone_modify": False,
        "keyframe_refs": [],
        "last_nonzero_volume": 1.0,
        "material_id": "",
        "render_index": 0,
        "responsive_layout": {
            "enable": False,
            "horizontal_pos_layout": 0,
            "size_layout": 0,
            "target_follow": "",
            "vertical_pos_layout": 0
        },
        "reverse": False,
        "source_timerange": {
            "duration": 5000000,  # 默认持续5s 可以改
            "start": 0
        },
        "speed": 1.0,
        "target_timerange": {
            "duration": 5000000,
            "start": 0
        },
        "template_id": "",
        "template_scene": "default",
        "track_attribute": 0,
        "track_render_index": 0,
        "uniform_scale": {
            "on": True,
            "value": 1.0
        },
        "visible": True,
        "volume": 1.0
    }


def segment_audio():
    return {
        "cartoon": False,
        "clip": None,
        "common_keyframes": [],
        "enable_adjust": False,
        "enable_color_curves": True,
        "enable_color_match_adjust": False,
        "enable_color_wheels": True,
        "enable_lut": False,
        "enable_smart_color_adjust": False,
        "extra_material_refs": [],
        "group_id": "",
        "hdr_settings": None,
        "id": generate_id(),
        "intensifies_audio": False,
        "is_placeholder": False,
        "is_tone_modify": False,
        "keyframe_refs": [],
        "last_nonzero_volume": 1.0,
        "material_id": "",
        "render_index": 0,
        "responsive_layout": {
            "enable": False,
            "horizontal_pos_layout": 0,
            "size_layout": 0,
            "target_follow": "",
            "vertical_pos_layout": 0
        },
        "reverse": False,
        "source_timerange": {
            "duration": 0,
            "start": 0
        },
        "speed": 1.0,
        "target_timerange": {
            "duration": 0,
            "start": 0
        },
        "template_id": "",
        "template_scene": "default",
        "track_attribute": 0,
        "track_render_index": 0,
        "uniform_scale": None,
        "visible": True,
        "volume": 1.0
    }

# 字幕segment
def segments_font(index, start_time, duration):
    return {
        "caption_info": None,
        "cartoon": False,
        "clip": {
            "alpha": 1.0,
            "flip": {
                "horizontal": False,
                "vertical": False
            },
            "rotation": 0.0,
            "scale": {
                "x": 1.0,
                "y": 1.0
            },
            "transform": {
                "x": 0.0,
                "y": 0
            }
        },
        "common_keyframes": [],
        "enable_adjust": True,
        "enable_color_curves": True,
        "enable_color_match_adjust": False,
        "enable_color_wheels": True,
        "enable_lut": True,
        "enable_smart_color_adjust": False,
        "extra_material_refs": [],   # 这里要加入相关的material的id
        "group_id": "",
        "hdr_settings": {
            "intensity": 1,
            "mode": 1,
            "nits": 1000
          },
        "id": generate_id(),
        "intensifies_audio": False,
        "is_placeholder": False,
        "is_tone_modify": False,
        "keyframe_refs": [],
        "last_nonzero_volume": 1.0,
        "material_id": "",    # 这里好像要添加东西
        "render_index": 14000 + index,
        "responsive_layout": {
            "enable": False,
            "horizontal_pos_layout": 0,
            "size_layout": 0,
            "target_follow": "",
            "vertical_pos_layout": 0
        },
        "reverse": False,
        "source_timerange": None,
        "speed": 1.0,
        "target_timerange": {
            "duration": duration,  # 真持续时间  需要改
            "start": start_time  # 真开始时间
        },
        "template_id": "",
        "template_scene": "default",
        "track_attribute": 0,
        "track_render_index": 0,
        "uniform_scale": {
            "on": True,
            "value": 1.0
        },
        "visible": True,
        "volume": 1.0

    }

# 文本 dict['materials']['texts']
def texts_items(txt, size=8.0):  # 需要传入文本参数
    return {
        "add_type": 2,
        "alignment": 1,
        "background_alpha": 1.0,
        "background_color": "",
        "background_height": 0.14,
        "background_horizontal_offset": 0.0,
        "background_round_radius": 0.0,
        "background_style": 0,
        "background_vertical_offset": 0.0,
        "background_width": 0.14,
        "bold_width": 0.0,
        "border_alpha": 1.0,
        "border_color": "",
        "border_width": 0.08,
        "check_flag": 7,
        "combo_info": {
            "text_templates": []
        },
        "content": '''{\"styles\":[{\"fill\":{\"alpha\":1.0,\"content\":{\"render_type\":\"solid\",\"solid\":\
{\"alpha\":1.0,\"color\":[1.0,1.0,1.0]}}},\"font\":{\"id\":\"\",\"path\"\
:\"\"},\"range\":[0,%d],\"size\":%.1f}],\"text\":\"%s\"}''' % (len(txt), size, txt),
        "fixed_height": -1.0,
        "fixed_width": -1.0,
        "font_category_id": "",
        "font_category_name": "",
        "font_id": "",
        "font_name": "",
        "font_path": "",  # 剪映自动补齐
        "font_resource_id": "",
        "font_size": size,
        "font_source_platform": 0,
        "font_team_id": "",
        "font_title": "none",
        "font_url": "",
        "fonts": [],
        "force_apply_line_max_width": False,
        "global_alpha": 1.0,
        "group_id": "",
        "has_shadow": False,
        "id": generate_id(),   # 需要传入
        "initial_scale": 1.0,
        "is_rich_text": False,
        "italic_degree": 0,
        "ktv_color": "",
        "language": "",
        "layer_weight": 1,
        "letter_spacing": 0.0,
        "line_feed": 1,
        "line_spacing": 0.02,
        "name": "",
        "original_size": [],
        "preset_category": "",
        "preset_category_id": "",
        "preset_has_set_alignment": False,
        "preset_id": "",
        "preset_index": 0,
        "preset_name": "",
        "recognize_task_id": "",
        "recognize_type": 0,
        "relevance_segment": [],
        "shadow_alpha": 0.8,
        "shadow_angle": -45.0,
        "shadow_color": "",
        "shadow_distance": 8.0,
        "shadow_point": {
            "x": 1.0182337649086284,  # 固定值
            "y": -1.0182337649086284  # 固定值
        },
        "shadow_smoothing": 1.0,
        "shape_clip_x": False,
        "shape_clip_y": False,
        "style_name": "",
        "sub_type": 0,
        "subtitle_keywords": None,
        "text_alpha": 1.0,
        "text_color": "#FFFFFF",
        "text_curve": None,
        "text_preset_resource_id": "",
        "text_size": 30,
        "text_to_audio_ids": [],
        "tts_auto_update": False,
        "type": "subtitle",
        "typesetting": 0,
        "underline": False,
        "underline_offset": 0.22,
        "underline_width": 0.05,
        "use_effect_default_color": True,
        "words": {
            "end_time": [],
            "start_time": [],
            "text": []
        }
    }

# dict['materials']['material_animations'] 存储与材料（如文本、贴纸、图像等）相关的动画效果
def material_animations_items():
    return {
        "animations": [],
        "id": generate_id(),
        "multi_language_current": "none",
        "type": "sticker_animation"
    }

def generate_16_digit_timestamp():
    try:
        a = (str(time.time()).replace('.', ''))[0:16]
        return int(a)
    except:
        # 失败随便返回一个数
        return 1706750401233751

def get_drive_from_path(base_path):
    try:
        return (os.path.splitdrive(base_path))[0]
    except Exception as e:
        print(f"文件路径 {base_path} 获取磁盘时错误：{e}")
        return None

# Dict[‘materials’][‘canvases’]  # 画板材料
def canvases_items():
    return {
        "album_image": "",
        "blur": 0.0,
        "color": "",
        "id": generate_id(),
        "image": "",
        "image_id": "",
        "image_name": "",
        "source_platform": 0,
        "team_id": "",
        "type": "canvas_color"
    }

# dict['materials']['videos']  # 视频材料
def videos_items(name,path):
    return {
        "aigc_type": "none",
        "audio_fade": None,
        "cartoon_path": "",
        "category_id": "",
        "category_name": "local",
        "check_flag": 63487,
        "crop": {
            "lower_left_x": 0.0,
            "lower_left_y": 1.0,
            "lower_right_x": 1.0,
            "lower_right_y": 1.0,
            "upper_left_x": 0.0,
            "upper_left_y": 0.0,
            "upper_right_x": 1.0,
            "upper_right_y": 0.0
        },
        "crop_ratio": "free",
        "crop_scale": 1.0,
        "duration": 10800000000,
        "extra_type_option": 0,
        "formula_id": "",
        "freeze": None,
        "gameplay": None,
        "has_audio": False,
        "height": 1080,
        "id": generate_id(),
        "intensifies_audio_path": "",
        "intensifies_path": "",
        "is_ai_generate_content": False,
        "is_unified_beauty_mode": False,
        "local_id": "",
        "local_material_id": "",
        "material_id": "",
        "material_name": name,
        "material_url": "",
        "matting": {
            "flag": 0,
            "has_use_quick_brush": False,
            "has_use_quick_eraser": False,
            "interactiveTime": [],
            "path": "",
            "strokes": []
        },
        "media_path": "",
        "object_locked": None,
        "origin_material_id": "",
        "path": path,
        "picture_from": "none",
        "picture_set_category_id": "",
        "picture_set_category_name": "",
        "request_id": "",
        "reverse_intensifies_path": "",
        "reverse_path": "",
        "smart_motion": None,
        "source": 0,
        "source_platform": 0,
        "stable": {
            "matrix_path": "",
            "stable_level": 0,
            "time_range": {
                "duration": 0,
                "start": 0
            }
        },
        "team_id": "",
        "type": "photo",
        "video_algorithm": {
            "algorithms": [],
            "deflicker": None,
            "motion_blur_config": None,
            "noise_reduction": None,
            "path": "",
            "quality_enhance": None,
            "time_range": None
        },
        "width": 1920
    }

# vocal_separations = dict['materials']['vocal_separations']  # 声音片段(可以不加？)
def vocal_separations():
    return {
        "choice": 0,
        "id": generate_id(),
        "production_path": "",
        "time_range": None,
        "type": "vocal_separation"
    }


# 视频片段
def segment_video():
    return {
        "caption_info": None,
        "cartoon": False,
        "clip": {
            "alpha": 1.0,
            "flip": {
                "horizontal": False,
                "vertical": False
            },
            "rotation": 0.0,
            "scale": {
                "x": 1.0,
                "y": 1.0
            },
            "transform": {
                "x": 0.0,
                "y": 0.0
            }
        },
        "common_keyframes": [],
        "enable_adjust": True,
        "enable_color_curves": True,
        "enable_color_match_adjust": False,
        "enable_color_wheels": True,
        "enable_lut": True,
        "enable_smart_color_adjust": False,
        "extra_material_refs": [],   # 画板、声音的id
        "group_id": "",
        "hdr_settings": {
            "intensity": 1.0,
            "mode": 1,
            "nits": 1000
        },
        "id": generate_id(),
        "intensifies_audio": False,
        "is_placeholder": False,
        "is_tone_modify": False,
        "keyframe_refs": [],
        "last_nonzero_volume": 1.0,
        "material_id": "",  # 视频id
        "render_index": 0,
        "responsive_layout": {
            "enable": False,
            "horizontal_pos_layout": 0,
            "size_layout": 0,
            "target_follow": "",
            "vertical_pos_layout": 0
        },
        "reverse": False,
        "source_timerange": {
            "duration": 5000000,  # 默认持续5s 可以改
            "start": 0
        },
        "speed": 1.0,
        "target_timerange": {
            "duration": 5000000,
            "start": 0
        },
        "template_id": "",
        "template_scene": "default",
        "track_attribute": 0,
        "track_render_index": 0,
        "uniform_scale": {
            "on": True,
            "value": 1.0
        },
        "visible": True,
        "volume": 1.0
    }

# 响声
def sound_items():
    return {
        "audio_channel_mapping": 0,
        "id": "",
        "is_config_open": False,
        "type": ""
    }

# 声乐
def vocal():
    return {
        "choice": 0,
        "id": "",
        "production_path": "",
        "time_range": None,
        "type": "vocal_separation"
    }

# 速度
def speeds_items():
    return {
        "curve_speed": None,  # 注意空是None
        "id": "",
        "mode": 0,
        "speed": 1.0,
        "type": "speed"
    }


def draft_materials_items():
    return {
        "create_time": int(time.time()),
        "duration": 0,
        "extra_info": "",
        "file_Path": "",
        "height": 0,
        "id": generate_id(),
        "import_time": int(time.time()),
        "import_time_ms": int(time.time()) * 10 ** 3,
        "item_source": 1,
        "md5": "",
        "metetype": "0",
        "roughcut_time_range": {
            "duration": -1,
            "start": -1
        },
        "sub_time_range": {
            "duration": -1,
            "start": -1
        },
        "type": 0,
        "width": 0
    }