# 视频解析工具 (video-parser)

Windows 终端工具：通过第三方解析接口，在本地 Chrome/Edge 中打开腾讯视频、哔哩哔哩等平台的视频链接。

仓库地址：<https://github.com/pmlpl/video-parser>

## 功能

- Rich 彩色终端界面（面板、菜单、进度与分级日志）
- 自动从解析站获取可用接口
- 支持 PyInstaller 打包为控制台 exe

## 环境要求

- Windows
- Python 3.10+
- 已安装 Google Chrome 或 Microsoft Edge
- 建议使用 **Windows Terminal** 或支持 ANSI 的 PowerShell，以正确显示彩色界面

## 安装

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python create_icon.py
```

## 运行

```powershell
python lookingVideo.py
```

主菜单：`1` 解析视频 · `2` 刷新解析接口 · `q` 退出

## 打包

```powershell
.\build.bat
```

生成目录：`dist\视频解析工具\视频解析工具.exe`（控制台程序，会显示终端窗口）

## 项目结构

| 文件 | 说明 |
|------|------|
| `lookingVideo.py` | Rich 终端入口 |
| `parser_core.py` | 解析接口获取与浏览器解析逻辑 |
| `create_icon.py` | 生成 `logo.ico` |
| `build.bat` | PyInstaller 打包脚本 |

## 依赖说明

- [Rich](https://github.com/Textualize/rich) — 终端彩色 UI
- [DrissionPage](https://github.com/g1879/DrissionPage) — 浏览器自动化
- requests、beautifulsoup4 — 获取解析接口

## 免责声明

本工具仅供学习交流。请遵守各视频平台服务条款与相关法律法规，勿用于侵犯版权或商业用途。
