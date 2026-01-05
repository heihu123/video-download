import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import subprocess
import os
import re

class VideoDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YT-DLP 桌面视频下载器")
        self.root.geometry("650x420")
        self.root.resizable(False, False)
        
        # 创建下载目录
        self.download_dir = os.path.join(os.getcwd(), "downloads")
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
        
        # 当前下载线程
        self.current_thread = None
        
        # 初始化GUI组件
        self.setup_ui()
    
    def setup_styles(self):
        """配置现代工业风格的样式"""
        style = ttk.Style()
        
        # 配置ttk主题 - 使用现代主题作为基础
        try:
            style.theme_use('clam')
        except:
            style.theme_use('default')
        
        # 现代工业风格配色方案
        colors = {
            'bg_primary': '#1a1a1a',      # 深碳黑
            'bg_secondary': '#2d2d2d',    # 深灰黑
            'bg_tertiary': '#404040',     # 中灰黑
            'accent_primary': '#00d4ff',  # 霓虹蓝
            'accent_secondary': '#0099cc', # 深蓝
            'accent_hover': '#33e0ff',    # 亮蓝
            'text_primary': '#ffffff',    # 纯白
            'text_secondary': '#cccccc',  # 浅灰
            'text_muted': '#999999',      # 中灰
            'border': '#555555',          # 边框灰
            'success': '#00ff88',         # 霓虹绿
            'warning': '#ffaa00',         # 警告橙
            'error': '#ff4444'            # 错误红
        }
        
        # 思源黑体字体配置 - 带回退机制
        font_title = ('Source Han Sans SC', 16, 'bold')  # 思源黑体 粗体
        font_label = ('Source Han Sans SC', 10, 'bold')  # 思源黑体 粗体
        font_regular = ('Source Han Sans SC', 10, 'normal')  # 思源黑体 常规
        font_small = ('Source Han Sans SC', 9, 'normal')  # 思源黑体 小号
        font_status = ('Source Han Sans SC', 8, 'normal')  # 思源黑体 状态
        
        # 字体回退配置
        fallback_fonts = {
            'title': ['Source Han Sans SC', 'Noto Sans CJK SC', 'Microsoft YaHei', 'PingFang SC', 'SimHei', 'Segoe UI', 'Arial', 'sans-serif'],
            'label': ['Source Han Sans SC', 'Noto Sans CJK SC', 'Microsoft YaHei', 'PingFang SC', 'SimHei', 'Segoe UI', 'Arial', 'sans-serif'],
            'regular': ['Source Han Sans SC', 'Noto Sans CJK SC', 'Microsoft YaHei', 'PingFang SC', 'SimHei', 'Segoe UI', 'Arial', 'sans-serif'],
            'small': ['Source Han Sans SC', 'Noto Sans CJK SC', 'Microsoft YaHei', 'PingFang SC', 'SimHei', 'Segoe UI', 'Arial', 'sans-serif'],
            'status': ['Source Han Sans SC', 'Noto Sans CJK SC', 'Microsoft YaHei', 'PingFang SC', 'SimHei', 'Segoe UI', 'Arial', 'sans-serif']
        }
        
        # 配置根背景
        style.configure('.', 
                       background=colors['bg_primary'],
                       foreground=colors['text_primary'],
                       font=font_small)
        
        # 主框架样式
        style.configure('MainFrame.TFrame',
                       background=colors['bg_primary'],
                       relief='flat',
                       borderwidth=0)
        
        # 输入框样式
        style.configure('Modern.TEntry',
                       fieldbackground=colors['bg_secondary'],
                       foreground=colors['text_primary'],
                       bordercolor=colors['border'],
                       lightcolor=colors['accent_primary'],
                       darkcolor=colors['border'],
                       font=font_regular,
                       padding=(12, 8))
        
        # 标签样式
        style.configure('Modern.TLabel',
                       background=colors['bg_primary'],
                       foreground=colors['text_secondary'],
                       font=font_label)
        
        style.configure('Title.TLabel',
                       background=colors['bg_primary'],
                       foreground=colors['text_primary'],
                       font=font_title)
        
        style.configure('Status.TLabel',
                       background=colors['bg_primary'],
                       foreground=colors['text_muted'],
                       font=font_status)
        
        # 按钮样式
        style.configure('Primary.TButton',
                       background=colors['accent_primary'],
                       foreground=colors['bg_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       font=font_label,
                       padding=(20, 12))
        
        style.map('Primary.TButton',
                 background=[('active', colors['accent_hover']),
                           ('pressed', colors['accent_secondary'])])
        
        style.configure('Secondary.TButton',
                       background=colors['bg_secondary'],
                       foreground=colors['text_primary'],
                       bordercolor=colors['border'],
                       lightcolor=colors['border'],
                       darkcolor=colors['border'],
                       focuscolor='none',
                       font=font_small,
                       padding=(12, 8))
        
        style.map('Secondary.TButton',
                 background=[('active', colors['bg_tertiary']),
                           ('pressed', colors['bg_primary'])])
        
        style.configure('Success.TButton',
                       background=colors['success'],
                       foreground=colors['bg_primary'],
                       borderwidth=0,
                       focuscolor='none',
                       font=font_small,
                       padding=(12, 8))
        
        style.map('Success.TButton',
                 background=[('active', '#33ffaa'),
                           ('pressed', '#00cc66')])
        
        # 下拉框样式
        style.configure('Modern.TCombobox',
                       fieldbackground=colors['bg_secondary'],
                       background=colors['bg_tertiary'],
                       foreground=colors['text_primary'],
                       bordercolor=colors['border'],
                       lightcolor=colors['accent_primary'],
                       darkcolor=colors['border'],
                       focuscolor='none',
                       font=font_regular,
                       arrowcolor=colors['accent_primary'],
                       padding=(10, 8))
        
        style.map('Modern.TCombobox',
                 fieldbackground=[('readonly', colors['bg_secondary']),
                                ('active', colors['bg_tertiary'])])
        
        # 进度条样式
        style.configure('Modern.Horizontal.TProgressbar',
                       background=colors['accent_primary'],
                       troughcolor=colors['bg_secondary'],
                       borderwidth=1,
                       lightcolor=colors['accent_primary'],
                       darkcolor=colors['accent_primary'],
                       thickness=8)
        
        return colors
    
    def setup_ui(self):
        # 设置样式
        colors = self.setup_styles()
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, style='MainFrame.TFrame', padding="25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题区域
        title_label = ttk.Label(main_frame, text="⚡ YT-DLP 桌面视频下载器", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 25))
        
        # URL输入区域
        url_label = ttk.Label(main_frame, text="🎬 视频链接:", style='Modern.TLabel')
        url_label.grid(row=1, column=0, sticky=tk.W, pady=8)
        
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=45, style='Modern.TEntry')
        url_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # 质量选择区域
        quality_label = ttk.Label(main_frame, text="🎯 下载质量:", style='Modern.TLabel')
        quality_label.grid(row=2, column=0, sticky=tk.W, pady=8)
        
        self.quality_var = tk.StringVar(value="best")
        quality_combo = ttk.Combobox(main_frame, textvariable=self.quality_var, width=18, 
                                   state="readonly", style='Modern.TCombobox')
        quality_combo['values'] = ("最佳质量", "1080p", "720p", "480p", "360p", "最低质量")
        quality_combo.grid(row=2, column=1, sticky=tk.W, pady=8, padx=(10, 0))
        
        # 保存路径选择
        path_label = ttk.Label(main_frame, text="📁 保存路径:", style='Modern.TLabel')
        path_label.grid(row=3, column=0, sticky=tk.W, pady=8)
        
        self.path_var = tk.StringVar(value=self.download_dir)
        path_entry = ttk.Entry(main_frame, textvariable=self.path_var, width=35, style='Modern.TEntry')
        path_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        browse_btn = ttk.Button(main_frame, text="浏览", command=self.browse_path, style='Secondary.TButton')
        browse_btn.grid(row=3, column=2, sticky=tk.W, pady=8, padx=(8, 0))
        
        # 下载按钮
        download_btn = ttk.Button(main_frame, text="� 开始下载", command=self.start_download, style='Primary.TButton')
        download_btn.grid(row=4, column=0, columnspan=3, pady=20, ipadx=30)
        
        # 进度条
        progress_label = ttk.Label(main_frame, text="📊 下载进度:", style='Modern.TLabel')
        progress_label.grid(row=5, column=0, sticky=tk.W, pady=(15, 5))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, length=500, 
                                          mode="determinate", style='Modern.Horizontal.TProgressbar')
        self.progress_bar.grid(row=6, column=0, columnspan=3, pady=5)
        
        # 状态显示
        self.status_var = tk.StringVar(value="✅ 就绪")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, style='Status.TLabel')
        status_label.grid(row=7, column=0, columnspan=3, pady=5)
        
        # 打开文件夹按钮
        open_folder_btn = ttk.Button(main_frame, text="📂 打开下载文件夹", 
                                   command=self.open_download_folder, style='Success.TButton')
        open_folder_btn.grid(row=8, column=0, columnspan=3, pady=15)
        
        # 配置列权重
        main_frame.columnconfigure(1, weight=1)
        
        # 设置根窗口背景
        self.root.configure(bg=colors['bg_primary'])
    
    def browse_path(self):
        """选择保存路径"""
        path = filedialog.askdirectory(initialdir=self.download_dir)
        if path:
            self.path_var.set(path)
    
    def open_download_folder(self):
        """打开下载文件夹"""
        if os.path.exists(self.download_dir):
            os.startfile(self.download_dir)
        else:
            messagebox.showerror("错误", "下载文件夹不存在")
    
    def start_download(self):
        """开始下载视频"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("错误", "请输入视频链接")
            return
        
        # 验证URL格式
        if not self.is_valid_url(url):
            messagebox.showerror("错误", "无效的视频链接")
            return
        
        # 检查是否正在下载
        if self.current_thread and self.current_thread.is_alive():
            messagebox.showinfo("提示", "当前有下载任务正在进行")
            return
        
        # 重置进度条
        self.progress_var.set(0)
        self.update_status_color("准备下载...")
        
        # 启动下载线程
        self.current_thread = threading.Thread(target=self.download_video, args=(url,))
        self.current_thread.daemon = True
        self.current_thread.start()
    
    def is_valid_url(self, url):
        """验证URL格式"""
        url_pattern = re.compile(r'^(https?://)?(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$')
        return bool(url_pattern.match(url))
    
    def download_video(self, url):
        """下载视频"""
        try:
            # 构建yt-dlp命令
            quality = self.quality_var.get()
            output_path = os.path.join(self.path_var.get(), "%(title)s.%(ext)s")
            
            cmd = [
                "yt-dlp.exe",
                "--no-playlist",
                "--merge-output-format", "mp4",
                "--output", output_path,
                url
            ]
            
            if quality != "best" and quality != "worst":
                cmd.insert(1, f"--format=bestvideo[height<={quality[:-1]}]+bestaudio/best[height<={quality[:-1]}]")
            elif quality == "worst":
                cmd.insert(1, "--format=worst")
            
            # 执行命令
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # 解析输出
            for line in process.stdout:
                self.parse_output(line)
            
            process.wait()
            
            if process.returncode == 0:
                self.update_status_color("下载完成")
                messagebox.showinfo("成功", "视频下载完成")
            else:
                self.update_status_color(f"下载失败: {process.returncode}")
                messagebox.showerror("错误", f"视频下载失败，错误码: {process.returncode}")
                
        except Exception as e:
            self.update_status_color(f"下载错误: {str(e)}")
            messagebox.showerror("错误", f"视频下载失败: {str(e)}")
    
    def parse_output(self, line):
        """解析yt-dlp输出，更新进度"""
        # 进度格式示例: [download]  50.0% of 10.00MiB at  2.00MiB/s ETA 00:02
        progress_pattern = re.compile(r'\[download\]\s+(\d+\.\d+)%\s+of\s+')
        match = progress_pattern.search(line)
        if match:
            progress = float(match.group(1))
            self.progress_var.set(progress)
            self.status_var.set(f"⚡ 下载中... {progress:.1f}%")
    
    def update_status_color(self, status):
        """根据状态更新显示颜色"""
        if "错误" in status or "失败" in status:
            self.status_var.set(f"❌ {status}")
        elif "完成" in status or "成功" in status:
            self.status_var.set(f"✅ {status}")
        elif "下载中" in status:
            self.status_var.set(f"⚡ {status}")
        elif "就绪" in status:
            self.status_var.set(f"✅ {status}")
        else:
            self.status_var.set(f"ℹ️ {status}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloader(root)
    root.mainloop()