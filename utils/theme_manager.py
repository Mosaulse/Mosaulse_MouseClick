# -*- coding: utf-8 -*-
"""
主题管理器模块 - 管理明暗两套主题
"""
from typing import Dict

# Windows系统主题检测
try:
    import winreg
except ImportError:
    import _winreg as winreg


class ThemeManager:
    """主题管理器 - 管理明暗两套主题"""
    
    LIGHT_THEME: Dict[str, str] = {
        'name': 'light',
        'bg_primary': '#F5F7FA',
        'bg_secondary': '#FFFFFF',
        'bg_card': '#FFFFFF',
        'text_primary': '#2C3E50',
        'text_secondary': '#5D6D7E',
        'text_muted': '#95A5A6',
        'accent': '#3498DB',
        'accent_hover': '#2980B9',
        'success': '#2ECC71',
        'success_hover': '#27AE60',
        'danger': '#E74C3C',
        'danger_hover': '#C0392B',
        'warning': '#F39C12',
        'border': '#E8E8E8',
        'shadow': 'rgba(0, 0, 0, 0.1)',
        'input_bg': '#FFFFFF',
        'input_border': '#D5D8DC',
        'input_focus': '#3498DB',
    }
    
    DARK_THEME: Dict[str, str] = {
        'name': 'dark',
        'bg_primary': '#1A1A2E',
        'bg_secondary': '#16213E',
        'bg_card': '#1E293B',
        'text_primary': '#E8E8E8',
        'text_secondary': '#B8B8B8',
        'text_muted': '#6B7280',
        'accent': '#60A5FA',
        'accent_hover': '#3B82F6',
        'success': '#10B981',
        'success_hover': '#059669',
        'danger': '#EF4444',
        'danger_hover': '#DC2626',
        'warning': '#F59E0B',
        'border': '#374151',
        'shadow': 'rgba(0, 0, 0, 0.3)',
        'input_bg': '#0F172A',
        'input_border': '#374151',
        'input_focus': '#60A5FA',
    }
    
    @staticmethod
    def detect_system_theme() -> bool:
        """检测Windows系统当前主题
        
        Returns:
            bool: True表示深色主题，False表示浅色主题
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, 
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return value == 0
        except (FileNotFoundError, OSError):
            return False
    
    @classmethod
    def get_theme(cls, is_dark: bool = False) -> Dict[str, str]:
        """获取主题配置
        
        Args:
            is_dark: 是否使用深色主题
            
        Returns:
            Dict[str, str]: 主题配置字典
        """
        return cls.DARK_THEME if is_dark else cls.LIGHT_THEME
