# tests/test_utils.py
# -*- coding: utf-8 -*-
"""
工具模块单元测试
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.theme_manager import ThemeManager
from utils.hotkey_manager import HotkeyManager
from utils.notification import NotificationManager


class TestThemeManager:
    """主题管理器测试"""

    def test_get_theme_light(self):
        """测试获取浅色主题"""
        theme = ThemeManager.get_theme(is_dark=False)
        assert theme['name'] == 'light'
        assert theme['bg_primary'] == '#F5F7FA'

    def test_get_theme_dark(self):
        """测试获取深色主题"""
        theme = ThemeManager.get_theme(is_dark=True)
        assert theme['name'] == 'dark'
        assert theme['bg_primary'] == '#1A1A2E'


class TestHotkeyManager:
    """快捷键管理器测试"""

    def test_init(self):
        """测试初始化"""
        manager = HotkeyManager()
        assert manager.current_hotkey is None


class TestNotificationManager:
    """通知管理器测试"""

    def test_init(self):
        """测试初始化"""
        manager = NotificationManager()
        assert manager is not None
