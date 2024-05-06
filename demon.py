# -*- coding:utf-8 -*-
import os
import subprocess
import time

def run_app():
    print("启动 app.py ...")
    # 启动 app.py
    subprocess.Popen(["python", "app.py"])

def clear_download_directory(download_dir):
    try:
        # 检查下载目录是否存在
        if not os.path.exists(download_dir):
            print(f"下载目录 {download_dir} 不存在。")
            return

        # 清空下载目录
        for file_name in os.listdir(download_dir):
            file_path = os.path.join(download_dir, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

        print("下载目录已清空。")
    except Exception as e:
        print(f"清空下载目录时发生错误：{e}")

def main():
    # 下载目录路径
    download_dir = "/root/web/download"

    while True:
        # 运行 app.py
        run_app()

        # 每隔一小时清理一次下载目录
        time.sleep(3600)
        clear_download_directory(download_dir)

if __name__ == "__main__":
    main()
