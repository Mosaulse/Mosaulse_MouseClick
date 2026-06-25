# -*- coding: utf-8 -*-
"""
鼠标连点器 - 现代化UI版本
支持明暗主题切换、圆角设计、渐变效果
"""
import sys
import time
import threading
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QSystemTrayIcon, QMenu, QAction,
    QFrame, QDialog, QTextBrowser, QGraphicsDropShadowEffect, QComboBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QEvent, QPoint
from PyQt5.QtGui import QIcon, QColor, QPainter, QPolygon, QFont, QFontDatabase
# pyautogui & keyboard 延迟导入以加速启动，见各方法内的 lazy import

# win10toast 延迟导入以加速启动，见 send_notification()
from utils.theme_manager import ThemeManager
from models.clicker_model import ClickThread


class StyledButton(QPushButton):
    """自定义样式按钮"""
    
    def __init__(self, text, btn_type='primary', parent=None):
        super().__init__(text, parent)
        self.btn_type = btn_type
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(42)
    
    def apply_theme(self, theme):
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


class StyledInput(QLineEdit):
    """自定义样式输入框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(40)
        self.setAlignment(Qt.AlignCenter)
    
    def apply_theme(self, theme):
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


class CardFrame(QFrame):
    """卡片式容器"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
    
    def apply_theme(self, theme):
        self.setStyleSheet(f"""
            CardFrame {{
                background: {theme['bg_card']};
                border-radius: 16px;
                border: 1px solid {theme['border']};
            }}
        """)


class HelpDialog(QDialog):
    """帮助窗口 - 现代化样式"""
    
    def __init__(self, parent=None, is_dark=False):
        super().__init__(parent)
        self.is_dark = is_dark
        self.theme = ThemeManager.get_theme(is_dark)
        self.setup_ui()
    
    def setup_ui(self):
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


class MouseClicker(QWidget):
    """鼠标连点器主窗口 - 现代化UI"""
    
    show_notification = pyqtSignal(str, str)
    toggle_clicking_signal = pyqtSignal()
    hotkey_pressed_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.click_thread = None
        self.is_running = False
        self.current_hotkey = None
        self.tray_icon = None
        # 启动时自动检测系统主题
        self.is_dark = ThemeManager.detect_system_theme()
        self.theme = ThemeManager.get_theme(self.is_dark)
        
        self.setup_ui()
        self.setup_tray()
        self.apply_theme()
        # 延迟初始化热键，让窗口先显示出来，提升启动体感速度
        QTimer.singleShot(50, self.setup_hotkey)
        self.show_notification.connect(self.send_notification)
        self.toggle_clicking_signal.connect(self.toggle_clicking)
        self.hotkey_pressed_signal.connect(self.handle_hotkey_pressed)
    
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("鼠标连点器")
        self.setFixedSize(420, 480)
        self.setWindowFlags(
            Qt.Window | 
            Qt.WindowCloseButtonHint | 
            Qt.WindowMinimizeButtonHint
        )
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)
        
        # 顶部栏 - 标题和主题切换
        header_layout = QHBoxLayout()
        
        # 标题带图标
        title_layout = QHBoxLayout()
        title_icon = QLabel("🖱️")
        title_icon.setStyleSheet("font-size: 28px;")
        self.title_label = QLabel("鼠标连点器")
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        title_layout.addWidget(title_icon)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        header_layout.addLayout(title_layout)
        
        header_layout.addStretch()
        
        # 主题切换按钮
        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setFixedSize(36, 36)
        self.theme_btn.setCursor(Qt.PointingHandCursor)
        self.theme_btn.setToolTip("切换主题")
        self.theme_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_btn)
        
        # 帮助按钮
        self.help_btn = QPushButton("?")
        self.help_btn.setFixedSize(36, 36)
        self.help_btn.setCursor(Qt.PointingHandCursor)
        self.help_btn.setToolTip("帮助")
        self.help_btn.clicked.connect(self.show_help)
        header_layout.addWidget(self.help_btn)
        
        main_layout.addLayout(header_layout)
        
        # 主卡片区域
        self.main_card = CardFrame()
        card_layout = QVBoxLayout(self.main_card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(20)
        
        # 状态指示器
        status_layout = QHBoxLayout()
        status_layout.addStretch()
        self.status_indicator = QLabel("●")
        self.status_indicator.setStyleSheet("font-size: 16px;")
        self.status_text = QLabel("已停止")
        self.status_text.setStyleSheet("font-size: 14px; font-weight: 500;")
        status_layout.addWidget(self.status_indicator)
        status_layout.addWidget(self.status_text)
        status_layout.addStretch()
        card_layout.addLayout(status_layout)
        
        # 间隔时间设置
        interval_container = QFrame()
        interval_layout = QVBoxLayout(interval_container)
        interval_layout.setContentsMargins(0, 0, 0, 0)
        interval_layout.setSpacing(8)
        
        interval_label = QLabel("⏱️ 点击间隔")
        interval_label.setStyleSheet("font-size: 13px; font-weight: 600;")
        interval_layout.addWidget(interval_label)
        
        interval_input_layout = QHBoxLayout()
        self.interval_input = StyledInput()
        self.interval_input.setText("500")
        self.interval_input.setPlaceholderText("100-10000")
        interval_input_layout.addWidget(self.interval_input)
        
        ms_label = QLabel("毫秒")
        ms_label.setStyleSheet("font-size: 13px;")
        interval_input_layout.addWidget(ms_label)
        interval_layout.addLayout(interval_input_layout)
        
        interval_hint = QLabel("建议设置在 100-1000 毫秒之间")
        interval_hint.setStyleSheet("font-size: 11px;")
        interval_layout.addWidget(interval_hint)
        
        card_layout.addWidget(interval_container)
        
        # 快捷键设置
        hotkey_container = QFrame()
        hotkey_layout = QVBoxLayout(hotkey_container)
        hotkey_layout.setContentsMargins(0, 0, 0, 0)
        hotkey_layout.setSpacing(8)
        
        hotkey_label = QLabel("⌨️ 快捷键")
        hotkey_label.setStyleSheet("font-size: 13px; font-weight: 600;")
        hotkey_layout.addWidget(hotkey_label)
        
        self.hotkey_input = StyledInput()
        self.hotkey_input.setText("F9")
        self.hotkey_input.setReadOnly(True)
        self.hotkey_input.installEventFilter(self)
        self.hotkey_input.mousePressEvent = lambda e: self.start_hotkey_capture()
        hotkey_layout.addWidget(self.hotkey_input)
        
        hotkey_hint = QLabel("点击输入框后按下快捷键组合")
        hotkey_hint.setStyleSheet("font-size: 11px;")
        hotkey_layout.addWidget(hotkey_hint)
        
        card_layout.addWidget(hotkey_container)
        
        # 开始/停止按钮
        self.start_stop_btn = StyledButton("▶ 开始连点", 'success')
        self.start_stop_btn.clicked.connect(self.toggle_clicking_signal.emit)
        self.start_stop_btn.setMinimumHeight(48)
        card_layout.addWidget(self.start_stop_btn)
        
        main_layout.addWidget(self.main_card)
        
        # 底部提示
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        self.tray_hint = QLabel("💡 点击最小化可隐藏到系统托盘")
        self.tray_hint.setStyleSheet("font-size: 11px;")
        bottom_layout.addWidget(self.tray_hint)
        
        bottom_layout.addStretch()
        main_layout.addLayout(bottom_layout)
        
        self.setLayout(main_layout)
        
        # 添加阴影效果
        self.setup_shadow()
    
    def setup_shadow(self):
        """设置窗口阴影"""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
    
    def apply_theme(self):
        """应用当前主题"""
        self.theme = ThemeManager.get_theme(self.is_dark)
        
        # 窗口背景 - 使用更具体的选择器确保背景色正确应用
        self.setStyleSheet(f"""
            MouseClicker {{
                background-color: {self.theme['bg_primary']};
                color: {self.theme['text_primary']};
                font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
            }}
            QWidget {{
                background-color: transparent;
                color: {self.theme['text_primary']};
            }}
        """)
        
        # 强制刷新窗口背景
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(self.theme['bg_primary']))
        self.setPalette(palette)
        
        # 标题
        self.title_label.setStyleSheet(f"""
            font-size: 22px; 
            font-weight: bold; 
            color: {self.theme['text_primary']};
        """)
        
        # 卡片
        self.main_card.apply_theme(self.theme)
        
        # 状态指示器
        if self.is_running:
            self.status_indicator.setStyleSheet(f"color: {self.theme['success']}; font-size: 16px;")
            self.status_text.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {self.theme['success']};")
        else:
            self.status_indicator.setStyleSheet(f"color: {self.theme['text_muted']}; font-size: 16px;")
            self.status_text.setStyleSheet(f"font-size: 14px; font-weight: 500; color: {self.theme['text_secondary']};")
        
        # 输入框
        self.interval_input.apply_theme(self.theme)
        self.hotkey_input.apply_theme(self.theme)
        
        # 标签
        for label in self.findChildren(QLabel):
            if label not in [self.status_indicator, self.status_text, self.title_label]:
                if "建议" in label.text() or "点击" in label.text():
                    label.setStyleSheet(f"font-size: 11px; color: {self.theme['text_muted']};")
                elif "毫秒" in label.text():
                    label.setStyleSheet(f"font-size: 13px; color: {self.theme['text_secondary']};")
                elif "⏱️" in label.text() or "⌨️" in label.text():
                    label.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {self.theme['text_primary']};")
                elif "💡" in label.text():
                    label.setStyleSheet(f"font-size: 11px; color: {self.theme['text_muted']};")
        
        # 按钮
        if self.is_running:
            self.start_stop_btn.btn_type = 'danger'
            self.start_stop_btn.setText("⏹ 停止连点")
        else:
            self.start_stop_btn.btn_type = 'success'
            self.start_stop_btn.setText("▶ 开始连点")
        self.start_stop_btn.apply_theme(self.theme)
        
        # 主题和帮助按钮
        self.theme_btn.setStyleSheet(f"""
            QPushButton {{
                background: {self.theme['bg_card']};
                color: {self.theme['text_primary']};
                border: 2px solid {self.theme['border']};
                border-radius: 10px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background: {self.theme['accent']};
                border-color: {self.theme['accent']};
            }}
        """)
        
        self.help_btn.setStyleSheet(f"""
            QPushButton {{
                background: {self.theme['bg_card']};
                color: {self.theme['text_secondary']};
                border: 2px solid {self.theme['border']};
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {self.theme['accent']};
                color: white;
                border-color: {self.theme['accent']};
            }}
        """)
        
        # 更新托盘图标
        if self.tray_icon:
            self.tray_icon.setIcon(self.create_tray_icon())
    
    def toggle_theme(self):
        """切换明暗主题"""
        self.is_dark = not self.is_dark
        self.theme_btn.setText("☀️" if self.is_dark else "🌙")
        self.apply_theme()
    
    def eventFilter(self, obj, event):
        """事件过滤器"""
        if obj == self.hotkey_input:
            if event.type() == QEvent.MouseButtonPress:
                self.start_hotkey_capture()
                return True
            elif event.type() == QEvent.KeyPress:
                self.set_hotkey(event)
                return True
        return super().eventFilter(obj, event)
    
    def start_hotkey_capture(self):
        """开始捕获快捷键"""
        self.hotkey_input.setPlaceholderText("按下快捷键...")
        self.hotkey_input.clear()
    
    def set_hotkey(self, event):
        """设置快捷键"""
        modifiers = []
        key = ""
        
        if event.modifiers() & Qt.ControlModifier:
            modifiers.append("ctrl")
        if event.modifiers() & Qt.AltModifier:
            modifiers.append("alt")
        if event.modifiers() & Qt.ShiftModifier:
            modifiers.append("shift")
        
        key_name = event.key()
        key_map = {
            Qt.Key_Space: "space",
            Qt.Key_Enter: "enter",
            Qt.Key_Return: "enter",
            Qt.Key_Tab: "tab",
            Qt.Key_Backspace: "backspace",
            Qt.Key_Delete: "delete",
            Qt.Key_Home: "home",
            Qt.Key_End: "end",
            Qt.Key_PageUp: "page up",
            Qt.Key_PageDown: "page down",
            Qt.Key_Left: "left",
            Qt.Key_Right: "right",
            Qt.Key_Up: "up",
            Qt.Key_Down: "down",
            Qt.Key_F1: "f1", Qt.Key_F2: "f2", Qt.Key_F3: "f3", Qt.Key_F4: "f4",
            Qt.Key_F5: "f5", Qt.Key_F6: "f6", Qt.Key_F7: "f7", Qt.Key_F8: "f8",
            Qt.Key_F9: "f9", Qt.Key_F10: "f10", Qt.Key_F11: "f11", Qt.Key_F12: "f12",
        }
        
        if key_name in key_map:
            key = key_map[key_name]
        elif Qt.Key_A <= key_name <= Qt.Key_Z:
            key = chr(key_name).lower()
        elif Qt.Key_0 <= key_name <= Qt.Key_9:
            key = chr(key_name)
        
        if key or modifiers:
            hotkey_str = "+".join(modifiers + [key]) if modifiers else key
            self.hotkey_input.setText(hotkey_str)
            self.hotkey_input.setPlaceholderText("")
            self.setup_hotkey()
    
    def setup_hotkey(self):
        """设置全局快捷键"""
        import keyboard
        hotkey = self.hotkey_input.text().strip()
        if not hotkey:
            return
        
        try:
            if self.current_hotkey:
                keyboard.remove_hotkey(self.current_hotkey)
            
            self.current_hotkey = keyboard.add_hotkey(hotkey, self.hotkey_pressed_signal.emit)
        except ValueError as e:
            QMessageBox.warning(self, "错误", f"无效的快捷键: {str(e)}")

    def handle_hotkey_pressed(self):
        """处理快捷键事件"""
        if self.is_running:
            self.stop_clicking()
        else:
            self.start_clicking()
    
    def setup_tray(self):
        """设置系统托盘"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.create_tray_icon())
        
        tray_menu = QMenu()
        tray_menu.setStyleSheet(f"""
            QMenu {{
                background: {self.theme['bg_card']};
                color: {self.theme['text_primary']};
                border: 1px solid {self.theme['border']};
                border-radius: 8px;
                padding: 8px;
            }}
            QMenu::item {{
                padding: 8px 24px;
                border-radius: 6px;
            }}
            QMenu::item:selected {{
                background: {self.theme['accent']};
                color: white;
            }}
        """)
        
        show_action = QAction("显示窗口", self)
        show_action.triggered.connect(self.show_from_tray)
        tray_menu.addAction(show_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()
    
    def create_tray_icon(self):
        """创建托盘图标"""
        from PyQt5.QtGui import QPixmap, QPainter, QColor, QPolygon
        
        accent_color = QColor(self.theme['accent'])
        
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setBrush(accent_color)
        painter.setPen(Qt.NoPen)
        
        points = QPolygon([
            QPoint(8, 2), QPoint(16, 2), QPoint(16, 14), QPoint(24, 14), 
            QPoint(24, 22), QPoint(16, 18), QPoint(16, 30), QPoint(8, 30),
            QPoint(8, 18), QPoint(2, 18), QPoint(2, 10), QPoint(8, 10)
        ])
        painter.drawPolygon(points)
        
        painter.end()
        
        return QIcon(pixmap)
    
    def tray_icon_activated(self, reason):
        """托盘图标被点击"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_from_tray()
    
    def show_from_tray(self):
        """从托盘显示窗口"""
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized)
        self.activateWindow()
    
    def toggle_clicking(self):
        """切换点击状态"""
        if self.is_running:
            self.stop_clicking()
        else:
            self.start_clicking()
    
    def start_clicking(self):
        """开始点击"""
        try:
            interval = int(self.interval_input.text())
            if interval < 10:
                QMessageBox.warning(self, "错误", "间隔时间不能小于10毫秒")
                return
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的数字")
            return
        
        self.is_running = True
        self.click_thread = ClickThread(interval)
        self.click_thread.start()
        
        self.status_indicator.setText("●")
        self.status_indicator.setStyleSheet(f"color: {self.theme['success']}; font-size: 16px;")
        self.status_text.setText("工作中...")
        self.status_text.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {self.theme['success']};")
        
        self.start_stop_btn.btn_type = 'danger'
        self.start_stop_btn.setText("⏹ 停止连点")
        self.start_stop_btn.apply_theme(self.theme)
        
        self.show_notification.emit("鼠标连点器", "✅ 已开启连点功能")
    
    def stop_clicking(self):
        """停止点击"""
        self.is_running = False
        
        if self.click_thread:
            self.click_thread.stop()
            # 等待线程安全结束，避免资源泄漏
            self.click_thread.join(timeout=1.0)
            self.click_thread = None
        
        self.status_indicator.setText("●")
        self.status_indicator.setStyleSheet(f"color: {self.theme['text_muted']}; font-size: 16px;")
        self.status_text.setText("已停止")
        self.status_text.setStyleSheet(f"font-size: 14px; font-weight: 500; color: {self.theme['text_secondary']};")
        
        self.start_stop_btn.btn_type = 'success'
        self.start_stop_btn.setText("▶ 开始连点")
        self.start_stop_btn.apply_theme(self.theme)
        
        # 使用try-except包裹通知，避免通知失败导致程序退出
        try:
            self.show_notification.emit("鼠标连点器", "⏹ 已停止连点功能")
        except Exception:
            pass
    
    def send_notification(self, title, message):
        """发送Windows通知"""
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            # 不使用threaded模式，避免线程冲突导致程序退出
            toaster.show_toast(title, message, duration=2, threaded=False)
        except Exception:
            pass
    
    def show_help(self):
        """显示帮助窗口"""
        dialog = HelpDialog(self, self.is_dark)
        dialog.exec_()
    
    def changeEvent(self, event):
        """窗口状态变化事件 - 最小化时隐藏到托盘"""
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                # 最小化时隐藏窗口到托盘
                self.hide()
                # 显示托盘提示气泡（首次最小化时）
                if self.tray_icon and self.tray_icon.supportsMessages():
                    self.tray_icon.showMessage(
                        "鼠标连点器",
                        "程序已最小化到系统托盘，双击托盘图标可恢复窗口",
                        QSystemTrayIcon.Information,
                        2000
                    )
                # 阻止默认最小化行为（不调用 super）
                return
        super().changeEvent(event)
    
    def closeEvent(self, event):
        """关闭事件"""
        # 先停止点击，确保线程安全结束
        if self.is_running:
            self.stop_clicking()
        
        # 移除热键监听
        if self.current_hotkey:
            try:
                import keyboard
                keyboard.remove_hotkey(self.current_hotkey)
            except Exception:
                pass
        
        # 隐藏托盘图标
        if self.tray_icon:
            self.tray_icon.hide()
        
        # 接受关闭事件
        event.accept()
    
    def quit_app(self):
        """退出应用"""
        # 先停止点击，确保线程安全结束
        if self.is_running:
            self.stop_clicking()
        
        # 移除热键监听
        if self.current_hotkey:
            try:
                import keyboard
                keyboard.remove_hotkey(self.current_hotkey)
            except Exception:
                pass
        
        # 隐藏托盘图标
        if self.tray_icon:
            self.tray_icon.hide()
        
        # 安全退出应用
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # 设置应用程序字体
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)
    
    window = MouseClicker()
    window.show()
    
    sys.exit(app.exec_())
