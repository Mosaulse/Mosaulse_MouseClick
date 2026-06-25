# -*- coding: utf-8 -*-
"""
帮助窗口视图模块 - 帮助窗口界面
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QTextBrowser
)
from PyQt5.QtCore import Qt
from typing import Dict
from utils.theme_manager import ThemeManager
from views.components import StyledButton


class HelpView(QDialog):
    """帮助窗口视图"""
    
    def __init__(self, parent=None, is_dark: bool = False):
        """初始化帮助窗口视图
        
        Args:
            parent: 父组件
            is_dark: 是否使用深色主题
        """
        super().__init__(parent)
        self.is_dark = is_dark
        self.theme = ThemeManager.get_theme(is_dark)
        self.setup_ui()
    
    def setup_ui(self) -> None:
        """设置用户界面"""
        self.setWindowTitle("使用帮助")
        self.setMinimumSize(550, 450)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 容器
        container = QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background: {self.theme['bg_primary']};
                border-radius: 12px;
            }}
        """)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # 标题
        title = QLabel("📖 使用帮助")
        title.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {self.theme['text_primary']};
            padding-bottom: 8px;
        """)
        layout.addWidget(title)
        
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"background: {self.theme['border']}; max-height: 1px;")
        layout.addWidget(line)
        
        # 内容区域
        content = QTextBrowser()
        content.setOpenExternalLinks(True)
        content.setStyleSheet(f"""
            QTextBrowser {{
                background: {self.theme['bg_card']};
                color: {self.theme['text_primary']};
                border: 1px solid {self.theme['border']};
                border-radius: 12px;
                padding: 16px;
                font-size: 13px;
                line-height: 1.6;
            }}
            QTextBrowser QScrollBar:vertical {{
                background: {self.theme['bg_secondary']};
                width: 8px;
                border-radius: 4px;
            }}
            QTextBrowser QScrollBar::handle:vertical {{
                background: {self.theme['accent']};
                border-radius: 4px;
            }}
        """)
        
        accent_color = self.theme['accent']
        success_color = self.theme['success']
        text_secondary = self.theme['text_secondary']
        
        content.setHtml(f"""
        <style>
            body {{ font-family: 'Microsoft YaHei', sans-serif; line-height: 1.8; color: {self.theme['text_primary']}; }}
            h2 {{ color: {accent_color}; margin-top: 20px; margin-bottom: 12px; font-size: 18px; }}
            h3 {{ color: {success_color}; margin-top: 16px; margin-bottom: 8px; font-size: 15px; }}
            p {{ margin: 8px 0; color: {text_secondary}; }}
            ol, ul {{ margin: 8px 0; padding-left: 24px; }}
            li {{ margin: 6px 0; color: {text_secondary}; }}
            .highlight {{ background: {self.theme['bg_secondary']}; padding: 2px 8px; border-radius: 4px; font-weight: bold; color: {accent_color}; }}
            .tip {{ background: {self.theme['bg_card']}; border-left: 4px solid {success_color}; padding: 12px; margin: 12px 0; border-radius: 0 8px 8px 0; }}
        </style>
        
        <h2>🎯 功能介绍</h2>
        <p>本软件可以模拟鼠标自动点击，支持设置点击间隔和快捷键控制，适用于需要重复点击的场景。</p>
        
        <h2>🚀 快速开始</h2>
        <ol>
            <li><b>设置间隔时间</b>：在输入框中设置两次点击之间的间隔（建议 100-1000 毫秒）</li>
            <li><b>设置快捷键</b>：点击快捷键输入框，按下您想使用的快捷键组合</li>
            <li><b>启动连点</b>：按下设置的快捷键即可开始自动点击</li>
            <li><b>停止连点</b>：再次按下快捷键即可停止</li>
        </ol>
        
        <div class="tip">
            <b>💡 提示：</b>快捷键是全局的，即使窗口最小化到托盘也能生效！
        </div>
        
        <h2>⌨️ 快捷键说明</h2>
        <p>支持各种组合键：</p>
        <ul>
            <li>单键：<span class="highlight">F1-F12</span>、<span class="highlight">Space</span>、<span class="highlight">Enter</span></li>
            <li>组合键：<span class="highlight">Ctrl+F1</span>、<span class="highlight">Alt+Space</span>、<span class="highlight">Ctrl+Shift+C</span></li>
        </ul>
        
        <h2>⚠️ 注意事项</h2>
        <ul>
            <li>间隔时间建议设置在 <b>100毫秒以上</b>，过快可能导致系统卡顿</li>
            <li>点击"最小化"按钮可以将窗口隐藏到系统托盘</li>
            <li>托盘图标上右键可以恢复窗口或退出程序</li>
            <li>关闭窗口将真正退出程序，连点功能会自动停止</li>
        </ul>
        
        <p style="color: {self.theme['text_muted']}; margin-top: 24px; text-align: center;">
            版本 2.0.0 | 鼠标连点器
        </p>
        """)
        
        layout.addWidget(content)
        
        # 关闭按钮
        close_btn = StyledButton("知道了", 'primary', self)
        close_btn.clicked.connect(self.close)
        close_btn.setMinimumWidth(120)
        close_btn.setMaximumWidth(120)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        main_layout.addWidget(container)
        self.setLayout(main_layout)
