# -*- coding: utf-8 -*-
"""
样式按钮组件 - 自定义样式按钮
"""
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from typing import Dict


class StyledButton(QPushButton):
    """自定义样式按钮"""
    
    def __init__(self, text: str, btn_type: str = 'primary', parent=None):
        """初始化按钮
        
        Args:
            text: 按钮文本
            btn_type: 按钮类型（'primary', 'success', 'danger', 'icon'）
            parent: 父组件
        """
        super().__init__(text, parent)
        self.btn_type = btn_type
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(42)
    
    def apply_theme(self, theme: Dict[str, str]) -> None:
        """应用主题
        
        Args:
            theme: 主题配置字典
        """
        if self.btn_type == 'primary':
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {theme['accent']}, stop:1 {theme['accent_hover']});
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 10px 24px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {theme['accent_hover']}, stop:1 {theme['accent']});
                }}
                QPushButton:pressed {{
                    background: {theme['accent']};
                }}
            """)
        elif self.btn_type == 'success':
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {theme['success']}, stop:1 {theme['success_hover']});
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 10px 24px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {theme['success_hover']}, stop:1 {theme['success']});
                }}
            """)
        elif self.btn_type == 'danger':
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {theme['danger']}, stop:1 {theme['danger_hover']});
                    color: white;
                    border: none;
                    border-radius: 10px;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 10px 24px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {theme['danger_hover']}, stop:1 {theme['danger']});
                }}
            """)
        elif self.btn_type == 'icon':
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {theme['bg_card']};
                    color: {theme['text_secondary']};
                    border: 2px solid {theme['border']};
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                    min-width: 42px;
                    max-width: 42px;
                }}
                QPushButton:hover {{
                    background: {theme['accent']};
                    color: white;
                    border-color: {theme['accent']};
                }}
            """)
