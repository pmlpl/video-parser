#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""视频解析工具 — Rich 彩色终端界面。"""

import os
import sys
import time

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.rule import Rule
from rich.text import Text

from parser_core import fetch_parse_interface, parse_video_url

console = Console(force_terminal=True)


def setup_console_encoding() -> None:
    if sys.platform == "win32":
        os.system("chcp 65001 >nul 2>&1")


def log_info(message: str) -> None:
    ts = time.strftime("%H:%M:%S")
    console.print(f"[dim][{ts}][/dim] [cyan]{message}[/cyan]")


def log_success(message: str) -> None:
    ts = time.strftime("%H:%M:%S")
    console.print(f"[dim][{ts}][/dim] [green]{message}[/green]")


def log_warning(message: str) -> None:
    ts = time.strftime("%H:%M:%S")
    console.print(f"[dim][{ts}][/dim] [yellow]{message}[/yellow]")


def log_error(message: str) -> None:
    ts = time.strftime("%H:%M:%S")
    console.print(f"[dim][{ts}][/dim] [bold red]{message}[/bold red]")


def show_banner() -> None:
    console.clear()
    body = Text.from_markup(
        "通过第三方解析接口，在本地 Chrome/Edge 中播放视频。\n"
        "[dim]支持腾讯视频、哔哩哔哩等主流平台 · 请在 Windows Terminal 中运行以获得最佳彩色效果[/dim]"
    )
    console.print(
        Panel(
            body,
            title="[bold magenta]视频解析工具[/bold magenta]",
            border_style="bright_blue",
            padding=(1, 2),
        )
    )
    console.print()


def show_interface_panel(vip_url: str) -> None:
    console.print(
        Panel(
            vip_url,
            title="[bold]当前解析接口[/bold]",
            border_style="green",
        )
    )
    console.print()


def load_parse_interface() -> str | None:
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("正在获取解析接口...", total=None)
        try:
            vip_url = fetch_parse_interface()
            progress.update(task, description="解析接口获取成功")
            return vip_url
        except Exception as exc:
            progress.update(task, description="获取失败")
            log_error(f"获取解析接口失败：{exc}")
            return None


def run_parse(vip_url: str) -> None:
    video_url = Prompt.ask(
        "[bold cyan]请输入视频链接[/bold cyan]",
        default="",
    ).strip()
    if not video_url:
        log_warning("链接为空，已取消")
        return

    console.print()
    log_info(f"开始解析：{video_url}")
    console.print()

    try:
        with console.status("[bold cyan]正在解析，请稍候...[/bold cyan]", spinner="dots"):
            current_url = parse_video_url(
                video_url,
                vip_url,
                on_status=log_info,
            )
        log_success("解析完成！")
        console.print(
            Panel(
                current_url,
                title="[bold green]当前页面[/bold green]",
                border_style="green",
            )
        )
        log_info("若未自动播放，请查看浏览器窗口")
    except Exception as exc:
        log_error(f"解析失败：{exc}")

    console.print(Rule(style="dim"))


def show_menu() -> str:
    console.print("[bold]主菜单[/bold]")
    console.print("  [cyan][1][/cyan] 解析视频")
    console.print("  [cyan][2][/cyan] 刷新解析接口")
    console.print("  [cyan][q][/cyan] 退出")
    console.print()
    choice = Prompt.ask(
        "请选择",
        choices=["1", "2", "q"],
        default="1",
        show_choices=False,
    )
    return choice.strip().lower()


def main() -> None:
    setup_console_encoding()
    show_banner()

    vip_url = load_parse_interface()
    if not vip_url:
        console.print("[yellow]无法继续：请先检查网络后重新运行程序。[/yellow]")
        sys.exit(1)

    log_success("解析接口获取成功")
    show_interface_panel(vip_url)

    while True:
        choice = show_menu()

        if choice == "q":
            log_info("再见！")
            break
        if choice == "2":
            console.print()
            new_url = load_parse_interface()
            if new_url:
                vip_url = new_url
                log_success("解析接口已刷新")
                show_interface_panel(vip_url)
            else:
                log_warning("刷新失败，仍使用原接口")
            continue
        if choice == "1":
            console.print()
            run_parse(vip_url)
            console.print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[dim]已中断[/dim]")
        sys.exit(0)
