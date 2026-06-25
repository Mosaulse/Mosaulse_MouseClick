# -*- coding: utf-8 -*-
"""
卡片容器组件 - 卡片式容器
"""
from PyQt5.QtWidgets import QFrame
from typing import Dict


class CardFrame(QFrame):
    """卡片式容器"""
    
    def __init__(self, parent=None):
        """初始化卡片容器
        
        Args:
            parent: 父组件
        """
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
    
    def apply_theme(self, theme: Dict[str, str]) -> None:
        """应用主题
        
        Args:
            theme: 主题配置字典
        """
        self.setStyleSheet(f"""
            CardFrame {{
                background: {theme['bg_card']};
                border-radius: 16px;
                border: 1px solid {theme['border']};
            }}
        """)
