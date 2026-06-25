# -*- coding: utf-8 -*-
"""
点击器模型模块 - 管理点击器状态和业务逻辑
"""
import sys
import time
import threading
from typing import Optional


class ClickThread(threading.Thread):
    """后台点击线程"""
    
    def __init__(self, interval: int, button: str = 'left'):
        """初始化点击线程
        
        Args:
            interval: 点击间隔（毫秒）
            button: 鼠标按钮类型（'left' 或 'right'）
        """
        super().__init__()
        self.interval = interval / 1000.0
        self.button = button
        self.running = False
        self.daemon = False
    
    def run(self) -> None:
        """运行点击线程"""
        import pyautogui
        pyautogui.FAILSAFE = False
        self.running = True
        while self.running:
            try:
                pyautogui.click(button=self.button)
                time.sleep(self.interval)
            except Exception:
                pass
    
    def stop(self) -> None:
        """停止点击线程"""
        self.running = False


class ClickerModel:
    """点击器模型 - 管理点击器状态"""
    
    def __init__(self):
        """初始化点击器模型"""
        self.click_thread: Optional[ClickThread] = None
        self.is_running: bool = False
        self.interval: int = 500
        self.button: str = 'left'
    
    def start_clicking(self, interval: int, button: str = 'left') -> None:
        """开始点击
        
        Args:
            interval: 点击间隔（毫秒）
            button: 鼠标按钮类型
        """
        if self.is_running:
            return
        
        self.interval = interval
        self.button = button
        self.click_thread = ClickThread(interval, button)
        self.click_thread.start()
        self.is_running = True
    
    def stop_clicking(self) -> None:
        """停止点击"""
        self.is_running = False
        
        if self.click_thread:
            self.click_thread.stop()
            self.click_thread.join(timeout=1.0)
            self.click_thread = None
