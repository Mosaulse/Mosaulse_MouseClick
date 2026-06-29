# -*- coding: utf-8 -*-
"""
设置模型模块 - 管理应用设置
"""
import json
import os
import sys
from typing import Dict, Any, Optional


def _get_app_dir() -> str:
    """获取应用目录（打包后为exe所在目录，开发时为Scripts目录）"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SettingsModel:
    """设置模型 - 管理应用设置"""
    
    DEFAULT_SETTINGS: Dict[str, Any] = {
        'interval': 500,
        'hotkey': 'F9',
        'is_dark': True,
        'button': 'left',
    }
    
    def __init__(self, settings_file: str = 'settings.json'):
        """初始化设置模型
        
        Args:
            settings_file: 设置文件路径（相对于应用目录）
        """
        app_dir = _get_app_dir()
        self.settings_file = os.path.join(app_dir, settings_file)
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.load_settings()
    
    def load_settings(self) -> None:
        """加载设置"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
        except Exception:
            pass
    
    def save_settings(self) -> None:
        """保存设置"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def get_setting(self, key: str) -> Any:
        """获取设置
        
        Args:
            key: 设置键名
            
        Returns:
            Any: 设置值
        """
        return self.settings.get(key)
    
    def set_setting(self, key: str, value: Any) -> None:
        """设置设置
        
        Args:
            key: 设置键名
            value: 设置值
        """
        self.settings[key] = value
        self.save_settings()
