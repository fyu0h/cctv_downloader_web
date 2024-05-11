# app.py
# -*- coding:utf-8 -*-
from flask import Flask, request, jsonify, render_template, send_file
from GetVideo import fetch_api
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 从环境变量获取值
PORT = os.getenv('PORT', 5000)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']
    result = fetch_api(video_url)
    if "error" in result:
        return jsonify(result)  # 将错误信息返回给前端
    # 返回视频信息
    return jsonify({
        "title": result['title'],
        "url": result['url'],
        "progress": "下载中...",
        "download_url": result['file'],
    })

@app.route('/download/<path:filename>')
def download_file(filename):
    # 文件路径
    file_path = f'download/{filename}'
    # 发送文件
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(PORT), debug=True)  # 确保端口是整数
