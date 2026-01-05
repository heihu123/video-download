# 技术栈文档：YT-DLP 桌面视频下载器

- **项目名称**：YT-DLP 桌面视频下载器  
- **版本**：v1.0  
- **目标平台**：Windows（可扩展至 macOS / Linux）  
- **许可证**：MIT（基于开源组件）

---

## 1. 架构概览

本项目是一个**本地 GUI 桌面应用**，通过图形界面封装 `yt-dlp` 命令行工具，实现用户友好的视频下载体验。整体采用 **单进程 + 多线程** 模型，避免界面卡死。[ 用户界面 (Tkinter) ]
↓
[ 业务逻辑 (Python) ]
↓
[ 调用外部工具: yt-dlp.exe + ffmpeg.exe ]
↓
[ 本地文件系统 (downloads/) ]

## 2. 技术栈明细

| 类别 | 技术/工具 | 说明 |
|------|----------|------|
| **语言** | Python 3.7+ | 主开发语言，跨平台兼容性好 |
| **GUI 框架** | Tkinter | Python 标准库，无需额外依赖，轻量高效 |
| **核心下载引擎** | [yt-dlp](https://github.com/yt-dlp/yt-dlp) | 开源命令行工具，支持 1000+ 网站 |
| **音视频处理** | [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) | 用于合并分段音视频流（如 YouTube 的 DASH 格式） |
| **打包工具** | PyInstaller | 将 Python 脚本打包为独立 `.exe` 可执行文件 |
| **并发模型** | `threading` | 后台线程执行下载任务，防止 GUI 冻结 |

---

## 3. 项目结构

```bash
yt-gui-downloader/
├── main.py                 # 主程序入口（GUI + 业务逻辑）
├── yt-dlp.exe              # yt-dlp 可执行文件（Windows 版）
├── ffmpeg.exe              # FFmpeg 可执行文件（用于音视频合并）
├── downloads/              # 默认视频输出目录（自动创建）
└── dist/                   # （打包后生成）独立 EXE 程序目录