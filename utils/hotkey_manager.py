# utils/hotkey_manager.py
# -*- coding: utf-8 -*-
"""
快捷键管理器模块 - 管理全局快捷键
"""
from PyQt5.QtCore import pyqtSignal, QObject
from typing import Optional, Callable


class HotkeyManager(QObject):
    """快捷键管理器"""
    
    hotkey_pressed = pyqtSignal()
    
    def __init__(self):
        """初始化快捷键管理器"""
        super().__init__()
        self.current_hotkey: Optional[str] = None
    
    def set_hotkey(self, hotkey_str: str) -> bool:
        """设置快捷键
        
        Args:
            hotkey_str: 快捷键字符串
            
        Returns:
            bool: 是否设置成功
        """
        import keyboard
        
        try:
            if self.current_hotkey:
                keyboard.remove_hotkey(self.current_hotkey)
            
            self.current_hotkey = keyboard.add_hotkey(hotkey_str, self.hotkey_pressed.emit)
            return True
        except ValueError:
            return False
    
    def remove_hotkey(self) -> None:
        """移除快捷键"""
        if self.current_hotkey:
            try:
                import keyboard
                keyboard.remove_hotkey(self.current_hotkey)
                self.current_hotkey = None
            except Exception:
                pass
