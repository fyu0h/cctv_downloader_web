# CCTV视频下载器

现在无法下载高清了，推荐使用猫抓
https://chromewebstore.google.com/detail/%E7%8C%AB%E6%8A%93/jfedfbgedapdagkghmgibemcoggfppbb?hl=zh-CN

本项目提供了一个自动化脚本，用于下载央视视频。使用IDM等工具直接下载的视频可能会出现花屏问题，为解决这一问题，本脚本能自动获取未加密的M3U8视频链接，并下载、合并、转码为MP4格式，确保视频质量。

## 支持的链接类型
- 支持通过类似于 `https://app.cctv.com/special/m/livevod/index.html?vtype=2&guid=d94f403668a9458383954b6bafcdd515&vsetId=C10616` 的链接下载视频。
- 也支持 `https://tv.cctv.com/2024/05/06/VIDE2N4S28gtwLfaRTPhb34u240506.shtml?spm=C96370.PPDB2vhvSivD.EGjfbNDqwSOr.1` 类型的链接下载。

## 界面示例
![项目界面示例](https://github.com/fyu0h/cctv_downloader_web/assets/33602841/1b287e57-970c-4439-ad96-39388c77cead)

## 安装步骤
确保系统已安装Python 3和FFmpeg。使用以下命令安装必需的Python库，并启动应用：

```bash
pip install -r requirements.txt
pip install ffmpeg
python3 app.py
```
# 自动清理下载目录

为管理磁盘空间，建议设置定时任务自动清理download目录。以下是一个示例Shell脚本，用于清理超过30天的文件：

```bash
#!/bin/bash
# 清理下载目录中超过30天的文件
find /path/to/your/download/ -type f -mtime +30 -delete
```

# 设置Cron定时任务
在Unix-like系统中，通过cron定时任务自动执行清理脚本。编辑crontab文件：

```bash
crontab -e
```
添加以下行以每天执行清理任务：
```bash
0 2 * * * /path/to/your/cleanup_script.sh
```
此配置使cron在每天凌晨2点执行清理脚本，删除超过30天的文件。
