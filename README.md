# 视频解析工具 (video-parser)

Windows 桌面工具：通过第三方解析接口，在本地 Chrome/Edge 中打开腾讯视频、哔哩哔哩等平台的视频链接。

## 功能

- 自动从解析站获取可用接口
- 图形界面（Tkinter）与命令行两种入口
- 支持 PyInstaller 打包为 exe

## 环境要求

- Windows
- Python 3.10+
- 已安装 Google Chrome 或 Microsoft Edge

## 安装

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python create_icon.py
```

## 运行

```powershell
# GUI 版（推荐）
python lookingVideo_gui.py

# 命令行版
python lookingVideo.py
```

## 打包

```powershell
.\build_gui.bat
```

生成目录：`dist\视频解析工具\视频解析工具.exe`

## 依赖说明

- [DrissionPage](https://github.com/g1879/DrissionPage) — 浏览器自动化
- requests、beautifulsoup4 — 获取解析接口

## 免责声明

本工具仅供学习交流。请遵守各视频平台服务条款与相关法律法规，勿用于侵犯版权或商业用途。
