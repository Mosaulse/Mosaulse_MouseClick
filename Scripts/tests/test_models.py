# tests/test_models.py
# -*- coding: utf-8 -*-
"""
模型单元测试
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.clicker_model import ClickerModel, ClickThread
from models.settings_model import SettingsModel

TEMP_SETTINGS = '_test_settings_temp.json'


class TestClickerModel:
    """点击器模型测试"""

    def test_init(self):
        """测试初始化"""
        model = ClickerModel()
        assert model.is_running is False
        assert model.interval == 500
        assert model.button == 'left'
        assert model.click_thread is None

    def test_start_clicking(self):
        """测试开始点击"""
        model = ClickerModel()
        model.start_clicking(1000)
        assert model.is_running is True
        assert model.click_thread is not None
        model.stop_clicking()

    def test_stop_clicking(self):
        """测试停止点击"""
        model = ClickerModel()
        model.start_clicking(1000)
        model.stop_clicking()
        assert model.is_running is False
        assert model.click_thread is None


class TestSettingsModel:
    """设置模型测试"""

    def test_init(self):
        """测试初始化"""
        model = SettingsModel(TEMP_SETTINGS)
        assert model.settings == SettingsModel.DEFAULT_SETTINGS

    def test_get_setting(self):
        """测试获取设置"""
        model = SettingsModel(TEMP_SETTINGS)
        assert model.get_setting('interval') == 500
        assert model.get_setting('hotkey') == 'F9'

    def test_set_setting(self):
        """测试设置设置"""
        model = SettingsModel(TEMP_SETTINGS)
        model.set_setting('interval', 1000)
        assert model.get_setting('interval') == 1000
