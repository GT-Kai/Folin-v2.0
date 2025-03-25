import argparse
import logging
import sys
import signal
from src.application import Application
from src.utils.logging_config import setup_logging

# 可选的Windows界面框架
# PyQt/PySide
from PySide6 import QtWidgets, QtCore

# 或 tkinter (内置)
import tkinter as tk

# 或 wxPython
import wx

# 或 自定义系统托盘应用
import pystray
from PIL import Image

# Windows特定功能示例
import win32api
import win32con
import win32gui
import winreg

# 音频录制和处理
import pyaudio
import numpy as np
import wave

# VAD (Voice Activity Detection)
import webrtcvad

# 多线程处理
import threading

logger = logging.getLogger("Main")
# 配置日志

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='茯苓')
    
    # 添加界面模式参数
    parser.add_argument(
        '--mode', 
        choices=['gui', 'cli'],
        default='gui',
        help='运行模式：gui(图形界面) 或 cli(命令行)'
    )
    
    # 添加协议选择参数
    parser.add_argument(
        '--protocol', 
        choices=['mqtt', 'websocket'], 
        default='websocket',
        help='通信协议：mqtt 或 websocket'
    )
    
    # 添加唤醒词功能参数
    parser.add_argument(
        '--wake-word',
        action='store_true',
        help='启用唤醒词功能'
    )
    
    # 添加唤醒词敏感度参数
    parser.add_argument(
        '--sensitivity',
        type=float,
        default=0.5,
        help='唤醒词检测敏感度 (0.0-1.0)'
    )
    
    # 添加自定义唤醒词参数
    parser.add_argument(
        '--custom-wake-word',
        type=str,
        default='',
        help='设置自定义唤醒词，多个词用逗号分隔'
    )
    
    return parser.parse_args()

def signal_handler(sig, frame):
    """处理Ctrl+C信号"""
    logger.info("接收到中断信号，正在关闭...")
    app = Application.get_instance()
    app.shutdown()
    sys.exit(0)

def set_autostart(autostart=True):
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0, winreg.KEY_SET_VALUE
    )
    if autostart:
        winreg.SetValueEx(key, "茯苓助手", 0, winreg.REG_SZ, sys.executable)
    else:
        try:
            winreg.DeleteValue(key, "茯苓助手")
        except:
            pass

def create_tray_app():
    icon = pystray.Icon('茯苓助手')
    icon.icon = Image.open('assets/icon.png')
    
    # def on_exit(icon, item):
    #     icon.stop()
    #     shutdown_app()
    
    # def on_settings(icon, item):
    #     show_settings_window()
    
    def on_toggle(icon, item):
        global wake_word_enabled
        wake_word_enabled = not wake_word_enabled
        # 更新菜单
        icon.update_menu()
    
    # 创建动态菜单
    def get_menu():
        return pystray.Menu(
            pystray.MenuItem(
                '启用唤醒词' if not wake_word_enabled else '禁用唤醒词', 
                on_toggle
            ),
            pystray.MenuItem('设置', on_settings),
            pystray.MenuItem('退出', on_exit)
        )
    
    icon.menu = get_menu
    return icon

def main():
    """程序入口点"""
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    # 解析命令行参数
    args = parse_args()
    try:
        # 日志
        setup_logging()
        # 创建并运行应用程序
        app = Application.get_instance()

        logger.info("应用程序已启动，按Ctrl+C退出")

        # 启动应用，传入参数
        app.run(
            mode=args.mode,
            protocol=args.protocol,
            wake_word_enabled=args.wake_word,
            wake_word_sensitivity=args.sensitivity,
            custom_wake_word=args.custom_wake_word
        )

    except Exception as e:
        logger.error(f"程序发生错误: {e}", exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())