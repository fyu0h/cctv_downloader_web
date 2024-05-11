# -*- coding:utf-8 -*-
import requests
import subprocess
import re
import os
from dotenv import load_dotenv

#加载环境变量
load_dotenv()

# 从环境变量获取值
DOWNLOAD_BASE_URL = os.getenv('DOWNLOAD_URL')
PORT = os.getenv('PORT')

# 从用户链接导出GUID
def extract_guid(url): 
    pattern = r"guid=([a-zA-Z0-9]+)" 
    match = re.search(pattern, url) 
    if match: 
        print(match.group(1))
        return match.group(1) 
    return None 
 
# 从用户链接导出VID
def extract_vid(url): 
    pattern = r"VID([a-zA-Z0-9]+)" 
    match = re.search(pattern, url) 
    if match: 
        print(match.group(0))
        return match.group(0) 
        print ("match")
    return None 
 
# 下载合并m3u8并转码为mp4
def download_and_merge(hls_url, title, input_url): 
    output_dir = f'download'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, f"{title}.mp4")
    if os.path.exists(output_path):
        os.remove(output_path)
    subprocess.run(['ffmpeg', '-i', hls_url, '-c', 'copy', '-bsf:a', 'aac_adtstoasc', output_path]) 
    download_link =  f"https://{DOWNLOAD_BASE_URL}/{output_dir}/{title}.mp4"
    print(f"下载链接：https://{DOWNLOAD_BASE_URL}/{output_dir}/{title}.mp4")
     # 返回视频标题、源网站和文件下载链接
    return {"title": title, "url": input_url, "file": download_link}

def fetch_api(url):
    if "VID" in url:
        vid = extract_vid(url)
        if vid:
            api_url = f"https://api.cntv.cn/Article/newContentInfo?serviceId=tvcctv&id={vid}&cb=abcde{vid}"
            response = requests.get(api_url)
            if response.status_code == 200:
                start_index = response.text.find('"guid":') + len('"guid":')
                end_index = response.text.find(',', start_index)
                if start_index != -1 and end_index != -1:
                    guid = response.text[start_index:end_index].strip('"')
                    if guid:
                        api_url = f"https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={guid}"
                        json_data = requests.get(api_url).json()
                        if json_data:
                            hls_url = json_data.get("hls_url")
                            title = json_data.get("title")
                            if hls_url and title:
                                return download_and_merge(hls_url, title, url)
                            else:
                                print("Failed to extract HLS URL or title from JSON data.")
                        else:
                            print("Failed to retrieve JSON data from API.")
                    else:
                        print("GUID not found in response data.")
                else:
                    print("Failed to retrieve data from API. Status code:", response.status_code)
            else:
                print("Failed to extract VID from URL.")
    else:
        guid = extract_guid(url)
        if guid:
            api_url = f"https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={guid}"
            json_data = requests.get(api_url).json()
            if json_data:
                hls_url = json_data.get("hls_url")
                title = json_data.get("title")
                if hls_url and title:
                    return download_and_merge(hls_url, title, url)
                else:
                    print("Failed to extract HLS URL or title from JSON data.")
            else:
                print("Failed to retrieve JSON data from API.")
        else:
            print("Failed to extract GUID from URL.")
