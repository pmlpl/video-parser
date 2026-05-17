import time
import requests
from bs4 import BeautifulSoup
from DrissionPage import ChromiumPage, ChromiumOptions
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
import os

class VideoParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("视频解析工具")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        
        # 设置窗口图标
        try:
            if os.path.exists('logo.ico'):
                self.root.iconbitmap('logo.ico')
        except:
            pass
        
        # 配置样式
        self.setup_style()
        
        # 初始化变量
        self.vip_url = ""
        self.is_parsing = False
        
        # 创建界面
        self.create_widgets()
        
        # 获取解析接口
        self.get_parse_interface()
    
    def setup_style(self):
        """设置现代化样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置按钮样式
        style.configure('Custom.TButton', 
                       font=('Microsoft YaHei UI', 11),
                       padding=(20, 10))
        
        # 配置标签样式
        style.configure('Title.TLabel', 
                       font=('Microsoft YaHei UI', 16, 'bold'),
                       foreground='#2c3e50')
        
        style.configure('Info.TLabel', 
                       font=('Microsoft YaHei UI', 9),
                       foreground='#7f8c8d')
        
        # 配置输入框样式
        style.configure('Custom.TEntry', 
                       font=('Microsoft YaHei UI', 11),
                       padding=5)
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title_label = ttk.Label(main_frame, text="🎬 视频解析工具", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 接口信息框架
        interface_frame = ttk.LabelFrame(main_frame, text="解析接口", padding="10")
        interface_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.interface_var = tk.StringVar(value="正在加载...")
        interface_label = ttk.Label(interface_frame, textvariable=self.interface_var, 
                                   style='Info.TLabel', wraplength=600)
        interface_label.grid(row=0, column=0, sticky=tk.W)
        
        # URL输入框架
        url_frame = ttk.LabelFrame(main_frame, text="视频地址", padding="10")
        url_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(url_frame, text="请输入视频链接：", font=('Microsoft YaHei UI', 10)).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.url_entry = ttk.Entry(url_frame, width=60, font=('Microsoft YaHei UI', 10))
        self.url_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 添加示例链接
        example_frame = ttk.Frame(url_frame)
        example_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W)
        
        ttk.Label(example_frame, text="示例：", font=('Microsoft YaHei UI', 9), 
                 foreground='#95a5a6').grid(row=0, column=0, sticky=tk.W)
        
        example_links = [
            "https://v.qq.com/x/cover/xxx.html",
            "https://www.bilibili.com/bangumi/play/epxxx"
        ]
        
        for i, link in enumerate(example_links):
            ttk.Label(example_frame, text=link, font=('Microsoft YaHei UI', 8), 
                     foreground='#3498db').grid(row=i+1, column=0, sticky=tk.W, padx=(20, 0))
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        self.parse_button = ttk.Button(button_frame, text="🚀 开始解析", 
                                       command=self.start_parsing, 
                                       style='Custom.TButton')
        self.parse_button.grid(row=0, column=0, padx=5)
        
        clear_button = ttk.Button(button_frame, text="🗑️ 清空", 
                                 command=self.clear_input, 
                                 style='Custom.TButton')
        clear_button.grid(row=0, column=1, padx=5)
        
        # 状态显示框架
        status_frame = ttk.LabelFrame(main_frame, text="状态信息", padding="10")
        status_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_text = tk.Text(status_frame, height=8, width=70, 
                                  font=('Consolas', 9),
                                  bg='#f8f9fa',
                                  fg='#2c3e50',
                                  relief=tk.FLAT,
                                  state=tk.DISABLED)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # 底部说明
        note_label = ttk.Label(main_frame, 
                              text="💡 提示：支持腾讯视频、哔哩哔哩等主流视频平台",
                              style='Info.TLabel')
        note_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        # 配置网格权重
        main_frame.columnconfigure(0, weight=1)
        url_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(0, weight=1)
    
    def log_message(self, message):
        """在状态区域显示消息"""
        self.status_text.config(state=tk.NORMAL)
        timestamp = time.strftime("%H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def get_parse_interface(self):
        """获取解析接口"""
        try:
            self.log_message("正在获取解析接口...")
            url = 'https://www.daga.cc/'
            res = requests.get(url, timeout=10).text
            html = BeautifulSoup(res, 'html.parser')
            
            options = html.select('option')
            if len(options) > 2:
                vip_url = 'https:' + options[2]['value']
                self.vip_url = vip_url
                self.interface_var.set(f"当前接口：{vip_url}")
                self.log_message(f"✓ 解析接口获取成功")
                self.log_message(f"接口地址：{vip_url}")
            else:
                self.log_message("✗ 未找到可用的解析接口")
                messagebox.showwarning("警告", "未找到可用的解析接口，请检查网络连接")
        except Exception as e:
            self.log_message(f"✗ 获取接口失败：{str(e)}")
            messagebox.showerror("错误", f"获取解析接口失败：\n{str(e)}")
    
    def start_parsing(self):
        """开始解析（在新线程中执行）"""
        if self.is_parsing:
            messagebox.showwarning("提示", "正在解析中，请稍候...")
            return
        
        video_url = self.url_entry.get().strip()
        if not video_url:
            messagebox.showwarning("提示", "请输入视频地址！")
            return
        
        if not self.vip_url:
            messagebox.showwarning("提示", "解析接口未就绪，请稍后重试")
            return
        
        # 在新线程中执行解析
        self.is_parsing = True
        self.parse_button.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self.parse_video, args=(video_url,))
        thread.daemon = True
        thread.start()
    
    def parse_video(self, video_url):
        """解析视频"""
        try:
            self.log_message("=" * 50)
            self.log_message(f"开始解析：{video_url}")
            
            parse_url = self.vip_url + video_url
            self.log_message(f"解析地址：{parse_url}")
            self.log_message("正在启动浏览器...")
            
            # 配置浏览器
            EDGE_SET = ChromiumOptions()
            
            # 尝试常见的浏览器路径
            common_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files(x86)\Google\Chrome\Application\chrome.exe",
                os.path.join(os.environ.get('LOCALAPPDATA', ''), r"Google\Chrome\Application\chrome.exe"),
                r"C:\Program Files(x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                os.path.join(os.environ.get('LOCALAPPDATA', ''), r"Microsoft\Edge\Application\msedge.exe")
            ]
            
            browser_path = None
            for path in common_paths:
                if os.path.exists(path):
                    browser_path = path
                    break
            
            if browser_path:
                EDGE_SET.set_browser_path(browser_path)
                self.log_message(f"使用浏览器：{browser_path}")
            else:
                self.log_message("警告：未找到浏览器，将使用默认路径")
            
            # 打开浏览器并访问解析页面
            EDGE = ChromiumPage(EDGE_SET)
            self.log_message("正在访问解析页面...")
            EDGE.get(parse_url)
            
            self.log_message("等待页面加载...")
            EDGE.wait.load_start(timeout=10)
            time.sleep(5)
            
            current_url = EDGE.url
            self.log_message(f"✓ 解析完成！")
            self.log_message(f"当前页面：{current_url}")
            self.log_message("如果页面没有自动播放，请检查浏览器窗口")
            self.log_message("=" * 50)
            
            messagebox.showinfo("成功", "视频解析完成！\n请查看浏览器窗口")
            
        except Exception as e:
            error_msg = f"解析失败：{str(e)}"
            self.log_message(f"✗ {error_msg}")
            messagebox.showerror("错误", error_msg)
        finally:
            self.is_parsing = False
            self.parse_button.config(state=tk.NORMAL)
    
    def clear_input(self):
        """清空输入"""
        self.url_entry.delete(0, tk.END)
        self.log_message("已清空输入")

def main():
    root = tk.Tk()
    app = VideoParserApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
