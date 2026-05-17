"""视频解析核心逻辑（与 UI 解耦）。"""

import os
import time
from collections.abc import Callable
from typing import Optional

import requests
from bs4 import BeautifulSoup
from DrissionPage import ChromiumOptions, ChromiumPage

PARSE_SITE_URL = "https://www.daga.cc/"

COMMON_BROWSER_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files(x86)\Google\Chrome\Application\chrome.exe",
    os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        r"Google\Chrome\Application\chrome.exe",
    ),
    r"C:\Program Files(x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        r"Microsoft\Edge\Application\msedge.exe",
    ),
]


def find_browser_path() -> Optional[str]:
    for path in COMMON_BROWSER_PATHS:
        if path and os.path.exists(path):
            return path
    return None


def build_chromium_options() -> ChromiumOptions:
    options = ChromiumOptions()
    browser_path = find_browser_path()
    if browser_path:
        options.set_browser_path(browser_path)
    return options


def fetch_parse_interface(timeout: int = 10) -> str:
    """从解析站获取 VIP 接口基址。"""
    res = requests.get(PARSE_SITE_URL, timeout=timeout)
    res.raise_for_status()
    html = BeautifulSoup(res.text, "html.parser")
    options = html.select("option")
    if len(options) <= 2:
        raise RuntimeError("解析站页面结构已变化，未找到可用接口")
    value = options[2].get("value")
    if not value:
        raise RuntimeError("解析接口 option 缺少 value 属性")
    if value.startswith("//"):
        return "https:" + value
    if value.startswith("http"):
        return value
    return "https:" + value


def parse_video_url(
    video_url: str,
    vip_url: str,
    on_status: Optional[Callable[[str], None]] = None,
    load_wait_seconds: int = 5,
) -> str:
    """
    使用 DrissionPage 打开解析页，返回最终页面 URL。
    on_status: 可选状态回调，供 UI 层输出日志。
    """
    def status(msg: str) -> None:
        if on_status:
            on_status(msg)

    parse_url = vip_url + video_url
    status(f"解析地址：{parse_url}")

    options = build_chromium_options()
    browser_path = find_browser_path()
    if browser_path:
        status(f"使用浏览器：{browser_path}")
    else:
        status("警告：未找到 Chrome/Edge，将使用 DrissionPage 默认路径")

    page = ChromiumPage(options)
    try:
        status("正在访问解析页面...")
        page.get(parse_url)
        status("等待页面加载...")
        page.wait.load_start(timeout=10)
        time.sleep(load_wait_seconds)
        return page.url
    finally:
        try:
            page.quit()
        except Exception:
            pass
