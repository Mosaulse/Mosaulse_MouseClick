# -*- coding: utf-8 -*-
"""
主窗口视图模块 - 主窗口界面
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QSystemTrayIcon, QMenu, QAction, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QTimer, QEvent, QPoint
from PyQt5.QtGui import QIcon, QColor, QPainter, QPolygon, QFont, QPixmap
from typing import Dict, Any, Optional
from utils.theme_manager import ThemeManager
from views.components import StyledButton, StyledInput, CardFrame


class MainView(QWidget):
    """主窗口视图"""
    
    def __init__(self):
        """初始化主窗口视图"""
        super().__init__()
        self.is_dark = ThemeManager.detect_system_theme()
        self.theme = ThemeManager.get_theme(self.is_dark)
        self.tray_icon: Optional[QSystemTrayIcon] = None
        
        # UI组件
        self.title_label: Optional[QLabel] = None
        self.theme_btn: Optional[QPushButton] = None
        self.help_btn: Optional[QPushButton] = None
        self.main_card: Optional[CardFrame] = None
        self.status_indicator: Optional[QLabel] = None
        self.status_text: Optional[QLabel] = None
        self.interval_input: Optional[StyledInput] = None
        self.hotkey_input: Optional[StyledInput] = None
        self.start_stop_btn: Optional[StyledButton] = None
        self.tray_hint: Optional[QLabel] = None
        
        # 回调函数
        self.on_theme_toggle = None
        self.on_help_show = None
        self.on_start_stop_click = None
        self.on_hotkey_capture_start = None
        self.on_quit = None
    
    def setup_ui(self) -> None:
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
        self.start_stop_btn.clicked.connect(self.toggle_clicking)
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
    
    def setup_shadow(self) -> None:
        """设置窗口阴影"""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
    
    def apply_theme(self) -> None:
        """应用当前主题"""
        self.theme = ThemeManager.get_theme(self.is_dark)
        
        # 窗口背景
        self.setStyleSheet(f"""
            MainView {{
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
        self.update_status()
        
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
    
    def update_status(self, is_running: bool = False) -> None:
        """更新状态显示
        
        Args:
            is_running: 是否正在运行
        """
        if is_running:
            self.status_indicator.setStyleSheet(f"color: {self.theme['success']}; font-size: 16px;")
            self.status_text.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {self.theme['success']};")
            self.start_stop_btn.btn_type = 'danger'
            self.start_stop_btn.setText("⏹ 停止连点")
        else:
            self.status_indicator.setStyleSheet(f"color: {self.theme['text_muted']}; font-size: 16px;")
            self.status_text.setStyleSheet(f"font-size: 14px; font-weight: 500; color: {self.theme['text_secondary']};")
            self.start_stop_btn.btn_type = 'success'
            self.start_stop_btn.setText("▶ 开始连点")
    
    def toggle_theme(self) -> None:
        """切换主题"""
        self.is_dark = not self.is_dark
        self.theme_btn.setText("☀️" if self.is_dark else "🌙")
        self.apply_theme()
        if self.on_theme_toggle:
            self.on_theme_toggle(self.is_dark)
    
    def show_help(self) -> None:
        """显示帮助窗口"""
        if self.on_help_show:
            self.on_help_show()
    
    def toggle_clicking(self) -> None:
        """切换点击状态"""
        if self.on_start_stop_click:
            self.on_start_stop_click()
    
    def start_hotkey_capture(self) -> None:
        """开始捕获快捷键"""
        self.hotkey_input.setPlaceholderText("按下快捷键...")
        self.hotkey_input.clear()
    
    def set_hotkey(self, hotkey_str: str) -> None:
        """设置快捷键
        
        Args:
            hotkey_str: 快捷键字符串
        """
        self.hotkey_input.setText(hotkey_str)
        self.hotkey_input.setPlaceholderText("")
    
    def get_interval(self) -> int:
        """获取间隔时间
        
        Returns:
            int: 间隔时间（毫秒）
        """
        try:
            return int(self.interval_input.text())
        except ValueError:
            return 500
    
    def get_hotkey(self) -> str:
        """获取快捷键
        
        Returns:
            str: 快捷键字符串
        """
        return self.hotkey_input.text().strip()
    
    def eventFilter(self, obj, event) -> bool:
        """事件过滤器
        
        Args:
            obj: 事件对象
            event: 事件
            
        Returns:
            bool: 是否处理事件
        """
        if obj == self.hotkey_input:
            if event.type() == QEvent.MouseButtonPress:
                self.start_hotkey_capture()
                return True
            elif event.type() == QEvent.KeyPress:
                self.handle_key_press(event)
                return True
        return super().eventFilter(obj, event)
    
    def handle_key_press(self, event) -> None:
        """处理按键事件
        
        Args:
            event: 按键事件
        """
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
            self.set_hotkey(hotkey_str)
            if self.on_hotkey_capture_start:
                self.on_hotkey_capture_start(hotkey_str)
    
    def setup_tray(self) -> None:
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
    
    def create_tray_icon(self) -> QIcon:
        """创建托盘图标
        
        Returns:
            QIcon: 托盘图标
        """
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
    
    def tray_icon_activated(self, reason) -> None:
        """托盘图标被点击
        
        Args:
            reason: 激活原因
        """
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_from_tray()
    
    def show_from_tray(self) -> None:
        """从托盘显示窗口"""
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized)
        self.activateWindow()
    
    def quit_app(self) -> None:
        """退出应用"""
        if self.on_quit:
            self.on_quit()
