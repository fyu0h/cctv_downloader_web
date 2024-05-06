# GetVideo.py
# -*- coding:utf-8 -*-
import requests
import subprocess
import re
import os
import ffmpeg
def download_video(url):
    # 从用户获取原始链接
    input_url = url
    # 从输入的URL中提取GUID
    guid_match = re.search(r'guid=([0-9a-fA-F\-]+)', input_url)
    if not guid_match:
        print("未找到有效的GUID，请确认链接是否正确")
        return {"error": "未找到有效的GUID，请确认链接是否正确"}

    guid = guid_match.group(1)
    # 构造获取视频信息的API URL
    api_url = f'https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={guid}'

    # 从API URL获取JSON数据
    response = requests.get(api_url)
    if response.status_code != 200:
        print("无法获取视频信息。")
        return {"error": "无法获取视频信息。"}

    video_info = response.json()
    if 'hls_url' not in video_info:
        return {"error": "无有效的视频下载链接。"}

    # 从JSON数据中获取视频标题和m3u8下载链接
    title = video_info['title']
    hls_url = video_info['hls_url']
    orgin_url = url

    # 视频标题用于命名输出文件
    output_file = f"{title}.mp4"

    # 下载目录
    download_dir = "download"

    # 确保下载目录存在，如果不存在则创建
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # 如果输出文件已存在于下载目录中，则删除它
    output_path = os.path.join(download_dir, output_file)
    if os.path.exists(output_path):
        os.remove(output_path)

    # 使用ffmpeg下载并转换视频
    command = f'ffmpeg -i "{hls_url}" -c copy -bsf:a aac_adtstoasc "{output_path}"'

    # 执行命令
    subprocess.run(command, shell=True)
    # 输出下载链接
    download_link = f"https://cntv.iinin.me:6688/download/{title}.mp4"
    print(f"下载链接：{download_link}")

    print(f"视频已保存为 {output_file}")
    # 返回视频标题、源网站和文件下载链接
    return {"title": video_info['title'], "url": input_url, "hls_url": video_info['hls_url'], "file": download_link}
