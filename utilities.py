import os
import random
import string
from pathlib import Path
from datetime import datetime
from pytube import YouTube


# 生成随机的字符串
def random_str(length=16):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


# 生成输出文件包括文件名的完整路径
def get_output_file_path(audio_file_path, output_extension):
    # 获取音频文件的文件基名
    file_basename = Path(audio_file_path).stem
    # 生成输入文件的文件名
    output_file_name = file_basename + "_" + random_str() + output_extension
    # 生成输出文件路径
    output_file_dir = "./outputs/" + datetime.today().strftime('%Y-%m-%d') + "/"
    # 创建输出文件路径
    Path(output_file_dir).mkdir(parents=True, exist_ok=True)

    return output_file_dir, output_file_name


def get_youtube_data(url):
    try:
        youtube_obj = YouTube(url)
        return youtube_obj.thumbnail_url, youtube_obj.title, youtube_obj.description
    except Exception as e:
        print(f"Youtube url: {url} is invalid, get youtube object failed.")
        return "Error"


def get_youtube_audio_file_path(url):
    try:
        youtube_obj = YouTube(url)
        return youtube_obj.streams.get_audio_only().download(filename="youtube_temp.wav")
    except Exception as e:
        print(f"Youtube url: {url} is invalid, get youtube object failed.")
        return "Error"
