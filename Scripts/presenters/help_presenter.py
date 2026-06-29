# -*- coding: utf-8 -*-
"""
帮助窗口展示者模块 - 协调帮助窗口视图
"""
from PyQt5.QtWidgets import QDialog
from views.help_view import HelpView


class HelpPresenter:
    """帮助窗口展示者"""
    
    def __init__(self, parent=None, is_dark: bool = False):
        """初始化帮助窗口展示者
        
        Args:
            parent: 父组件
            is_dark: 是否使用深色主题
        """
        self.view = HelpView(parent, is_dark)
    
    def show(self) -> None:
        """显示帮助窗口"""
        self.view.exec_()
