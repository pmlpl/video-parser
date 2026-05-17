import time
import requests
from bs4 import BeautifulSoup
from DrissionPage import *

EDGE_SET = ChromiumOptions() #创建配置浏览器
# 尝试常见的 Chrome 和 Edge 安装路径，增加代码的兼容性
import os
common_paths = [
    # Google Chrome 常见路径
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files(x86)\Google\Chrome\Application\chrome.exe",
    os.path.join(os.environ.get('LOCALAPPDATA', ''), r"Google\Chrome\Application\chrome.exe"),
    # Microsoft Edge 常见路径
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
else:
    print("警告：未找到 Chrome 浏览器默认安装路径，将尝试使用系统默认路径或 DrissionPage 自动检测。")
url = 'https://www.daga.cc/'

res = requests.get(url).text
# print(res)
html = BeautifulSoup(res, 'html.parser')


vip_url = [option['value'] for option in html.select('option')][2]
vip_url = 'https:' + vip_url
print(f"解析接口: {vip_url}")

while True:
    movie= input('请输入电影地址：')
    EDGE = ChromiumPage(EDGE_SET)

    parse_url = vip_url + movie
    print(f"正在访问：{parse_url}")
    EDGE.get(parse_url)
    print("等待页面加载...")
    EDGE.wait.load_start(timeout=10)
    time.sleep(5)
    current_url = EDGE.url
    print(f"当前页面: {current_url}")
    print("解析完成！如果页面没有自动播放，请检查浏览器窗口。")
    print("=" * 50)

# https://v.qq.com/x/cover/mzc002009g0nh88/w4102d4f4ur.html

# https://www.bilibili.com/bangumi/play/ep1231584?spm_id_from=333.337.0.0