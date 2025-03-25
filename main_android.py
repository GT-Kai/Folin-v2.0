#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import signal
import threading
import time
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.clock import Clock
from kivy.utils import platform

# 导入茯苓核心组件
try:
    from src.application import Application
    from src.utils.logging_config import setup_logging
except ImportError:
    # 在Android上可能需要调整路径
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    from src.application import Application
    from src.utils.logging_config import setup_logging

# 设置日志
logger = logging.getLogger("FulingAndroid")
setup_logging()

# Android权限请求
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.RECORD_AUDIO,
        Permission.INTERNET,
        Permission.WAKE_LOCK
    ])

# Kivy UI定义
KV = '''
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        
        Image:
            source: 'assets/logo.png'
            size_hint_y: 0.3
        
        Label:
            text: '茯苓语音助手'
            font_size: '24sp'
            size_hint_y: 0.1
        
        Label:
            id: status_label
            text: root.status_text
            font_size: '18sp'
            size_hint_y: 0.1
        
        Button:
            text: '启用唤醒词' if not root.is_listening else '停用唤醒词'
            size_hint_y: 0.15
            on_press: root.toggle_wake_word()
        
        Button:
            text: '设置'
            size_hint_y: 0.15
            on_press: root.open_settings()
        
        Button:
            text: '关于'
            size_hint_y: 0.15
            on_press: root.manager.current = 'about'

<AboutScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        
        Label:
            text: '茯苓语音助手 v1.0'
            font_size: '22sp'
            size_hint_y: 0.2
            
        Label:
            text: '一个智能语音交互系统\\n支持唤醒词功能和自然语言交互'
            halign: 'center'
            size_hint_y: 0.4
            
        Button:
            text: '返回'
            size_hint_y: 0.15
            on_press: root.manager.current = 'home'
'''

class HomeScreen(Screen):
    status_text = StringProperty("准备就绪")
    is_listening = BooleanProperty(False)
    sensitivity = NumericProperty(0.5)
    
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.app_instance = None
        self.wake_word_thread = None
        
        # 初始化茯苓应用实例
        try:
            self.app_instance = Application.get_instance()
            logger.info("茯苓核心已初始化")
        except Exception as e:
            logger.error(f"初始化茯苓核心失败: {e}", exc_info=True)
            self.status_text = "初始化失败"
    
    def toggle_wake_word(self):
        if self.is_listening:
            self.stop_wake_word()
        else:
            self.start_wake_word()
    
    def start_wake_word(self):
        retry_count = 0
        max_retries = 3
        while retry_count < max_retries:
            try:
                if self.app_instance:
                    try:
                        # 启动唤醒词线程
                        self.wake_word_thread = threading.Thread(
                            target=self._run_wake_word_service,
                            daemon=True
                        )
                        self.wake_word_thread.start()
                        
                        self.is_listening = True
                        self.status_text = "正在监听唤醒词..."
                        logger.info("唤醒词服务已启动")
                        break
                    except Exception as e:
                        logger.error(f"启动唤醒词服务失败: {e}", exc_info=True)
                        self.status_text = "启动监听失败"
            except Exception as e:
                retry_count += 1
                logger.warning(f"启动失败，尝试重试 {retry_count}/{max_retries}")
                time.sleep(1)
    
    def stop_wake_word(self):
        if self.app_instance:
            try:
                # 停止唤醒词服务
                self.app_instance.shutdown_wake_word()
                self.is_listening = False
                self.status_text = "唤醒词监听已停止"
                logger.info("唤醒词服务已停止")
            except Exception as e:
                logger.error(f"停止唤醒词服务失败: {e}", exc_info=True)
    
    def _run_wake_word_service(self):
        try:
            # 配置参数
            config = {
                'mode': 'service',
                'wake_word_enabled': True,
                'wake_word_sensitivity': self.sensitivity,
                'on_wake_word': self.on_wake_word_detected
            }
            
            # 运行唤醒词服务
            self.app_instance.run_wake_word_service(**config)
        except Exception as e:
            logger.error(f"唤醒词服务运行错误: {e}", exc_info=True)
            Clock.schedule_once(lambda dt: self._update_status("服务出错"), 0)
    
    def on_wake_word_detected(self):
        # 唤醒词被触发后的回调
        logger.info("检测到唤醒词！")
        Clock.schedule_once(lambda dt: self._update_status("检测到唤醒词!"), 0)
        
        # 播放提示音（可选）
        self._play_notification()
        
        # 短暂等待后恢复状态
        Clock.schedule_once(lambda dt: self._update_status("正在监听唤醒词..."), 3)
    
    def _update_status(self, text):
        self.status_text = text
    
    def _play_notification(self):
        # 唤醒提示音实现（可选）
        pass
    
    def open_settings(self):
        self.manager.current = 'settings'

class AboutScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass


class FulingAndroidApp(App):
    def build(self):
        # 加载UI
        Builder.load_string(KV)
        
        # 创建屏幕管理器
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AboutScreen(name='about'))
        
        # 注册Android生命周期回调
        if platform == 'android':
            from android import activity
            activity.bind(on_pause=self.on_pause)
            activity.bind(on_resume=self.on_resume)
            activity.bind(on_stop=self.on_stop)
        
        # 注册退出处理
        signal.signal(signal.SIGINT, self.signal_handler)
        
        return sm
    
    def build_settings(self, settings):
        # 应用设置
        settings.add_json_panel('茯苓设置', self.config, data='''
        [
            {
                "type": "bool",
                "title": "开机自启",
                "desc": "应用启动时自动开始监听",
                "section": "general",
                "key": "auto_start"
            },
            {
                "type": "numeric",
                "title": "唤醒词敏感度",
                "desc": "值越高越容易被唤醒",
                "section": "wake_word",
                "key": "sensitivity",
                "min": 0.1,
                "max": 1.0
            },
            {
                "type": "options",
                "title": "省电模式",
                "desc": "调整功耗与性能平衡",
                "section": "performance",
                "key": "power_mode",
                "options": ["低耗电", "平衡", "高性能"]
            }
        ]
        ''')
    
    def get_application_config(self):
        if platform == 'android':
            return super(FulingAndroidApp, self).get_application_config('~/.%(appname)s.ini')
        return super(FulingAndroidApp, self).get_application_config()
    
    def on_config_change(self, config, section, key, value):
        # 处理设置变更
        logger.info(f"设置已更改: [{section}] {key} = {value}")
        
        if section == 'wake_word' and key == 'sensitivity':
            home_screen = self.root.get_screen('home')
            home_screen.sensitivity = float(value)
    
    def on_pause(self):
        # Android应用进入后台
        logger.info("应用进入后台")
        return True  # 允许继续在后台运行
    
    def on_resume(self):
        # Android应用恢复前台
        logger.info("应用恢复前台")
    
    def on_stop(self):
        # Android应用停止
        logger.info("应用停止运行")
        self.cleanup()
    
    def signal_handler(self, sig, frame):
        # 处理信号
        logger.info("接收到中断信号，正在关闭...")
        self.stop()
    
    def on_start(self):
        # 应用启动后检查自启动设置
        if self.config.getboolean('general', 'auto_start'):
            Clock.schedule_once(lambda dt: self._auto_start(), 2)
    
    def _auto_start(self):
        home_screen = self.root.get_screen('home')
        home_screen.start_wake_word()
    
    def cleanup(self):
        # 清理资源
        try:
            home_screen = self.root.get_screen('home')
            if home_screen.is_listening:
                home_screen.stop_wake_word()
            
            app = Application.get_instance()
            app.shutdown()
        except Exception as e:
            logger.error(f"清理资源时发生错误: {e}", exc_info=True)

    def build_config(self, config):
        config.setdefaults('general', {
            'auto_start': False
        })
        config.setdefaults('wake_word', {
            'sensitivity': 0.5
        })
        config.setdefaults('performance', {
            'power_mode': '平衡'
        })

    def create_foreground_service(self):
        if platform == 'android':
            from jnius import autoclass
            Service = autoclass('org.kivy.android.PythonService')
            service = Service.mService
            # 创建通知并转为前台服务


if __name__ == "__main__":
    try:
        # 创建应用实例并运行
        app = FulingAndroidApp()
        app.run()
    except Exception as e:
        logger.error(f"应用运行失败: {e}", exc_info=True) 