# -*- coding: utf-8 -*-
"""
样式输入框组件 - 自定义样式输入框
"""
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt
from typing import Dict


class StyledInput(QLineEdit):
    """自定义样式输入框"""
    
    def __init__(self, parent=None):
        """初始化输入框
        
        Args:
            parent: 父组件
        """
        super().__init__(parent)
        self.setMinimumHeight(40)
        self.setAlignment(Qt.AlignCenter)
    
    def apply_theme(self, theme: Dict[str, str]) -> None:
        """应用主题
        
        Args:
            theme: 主题配置字典
        """
        self.setStyleSheet(f"""
            QLineEdit {{
                background: {theme['input_bg']};
                color: {theme['text_primary']};
                border: 2px solid {theme['input_border']};
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: 500;
            }}
            QLineEdit:focus {{
                border-color: {theme['input_focus']};
            }}
            QLineEdit::placeholder {{
                color: {theme['text_muted']};
            }}
        """)
