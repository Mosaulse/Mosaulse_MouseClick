# 鼠标连点器 MVP 架构优化实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use compose:subagent (recommended) or compose:execute to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将鼠标连点器重构为 MVP 架构，优化性能和代码质量

**Architecture:** 采用 MVP（Model-View-Presenter）架构模式，将项目重构为清晰的三层结构，分离关注点，提高可维护性

**Tech Stack:** Python, PyQt5, pyautogui, keyboard

## Global Constraints

- Python 3.8+
- PyQt5 >= 5.15
- pyautogui >= 0.9.54
- keyboard >= 0.13.5
- 遵循 PEP8 规范
- 使用类型提示（Type Hints）
- 使用 Google 风格的文档格式

---

### Task 1: 创建项目结构

**Covers:** [S3]

**Files:**
- Create: `models/__init__.py`
- Create: `views/__init__.py`
- Create: `views/components/__init__.py`
- Create: `presenters/__init__.py`
- Create: `utils/__init__.py`
- Create: `tests/__init__.py`

**Interfaces:**
- Consumes: (none)
- Produces: (none)

- [ ] **Step 1: 创建目录结构**

```bash
mkdir -p models views/components presenters utils tests
```

- [ ] **Step 2: 创建 __init__.py 文件**

```bash
touch models/__init__.py views/__init__.py views/components/__init__.py presenters/__init__.py utils/__init__.py tests/__init__.py
```

- [ ] **Step 3: 验证目录结构**

```bash
ls -la
```

Expected: 输出显示新创建的目录

- [ ] **Step 4: 提交更改**

```bash
git add models views presenters utils tests
git commit -m "feat: create MVP project structure"
```

---

### Task 2: 提取 ThemeManager 到 utils 模块

**Covers:** [S3, S5]

**Files:**
- Create: `utils/theme_manager.py`
- Modify: `mouse_clicker.py` (移除 ThemeManager 类)

**Interfaces:**
- Consumes: (none)
- Produces: `ThemeManager.detect_system_theme()`, `ThemeManager.get_theme()`

- [ ] **Step 1: 创建 ThemeManager 类**

```python
# utils/theme_manager.py
# -*- coding: utf-8 -*-
"""
主题管理器模块 - 管理明暗两套主题
"""
import sys
from typing import Dict, Any

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
                r"Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize"
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
```

- [ ] **Step 2: 验证模块可导入**

```bash
python -c "from utils.theme_manager import ThemeManager; print('ThemeManager imported successfully')"
```

Expected: 输出 "ThemeManager imported successfully"

- [ ] **Step 3: 提交更改**

```bash
git add utils/theme_manager.py
git commit -m "feat: extract ThemeManager to utils module"
```

---

### Task 3: 提取 ClickThread 到 models 模块

**Covers:** [S3, S5]

**Files:**
- Create: `models/clicker_model.py`
- Modify: `mouse_clicker.py` (移除 ClickThread 类)

**Interfaces:**
- Consumes: (none)
- Produces: `ClickThread.run()`, `ClickThread.stop()`

- [ ] **Step 1: 创建 ClickerModel 类**

```python
# models/clicker_model.py
# -*- coding: utf-8 -*-
"""
点击器模型模块 - 管理点击器状态和业务逻辑
"""
import sys
import time
import threading
from typing import Optional


class ClickThread(threading.Thread):
    """后台点击线程"""
    
    def __init__(self, interval: int, button: str = 'left'):
        """初始化点击线程
        
        Args:
            interval: 点击间隔（毫秒）
            button: 鼠标按钮类型（'left' 或 'right'）
        """
        super().__init__()
        self.interval = interval / 1000.0
        self.button = button
        self.running = False
        self.daemon = False
    
    def run(self) -> None:
        """运行点击线程"""
        import pyautogui
        pyautogui.FAILSAFE = False
        self.running = True
        while self.running:
            try:
                pyautogui.click(button=self.button)
                time.sleep(self.interval)
            except Exception:
                pass
    
    def stop(self) -> None:
        """停止点击线程"""
        self.running = False


class ClickerModel:
    """点击器模型 - 管理点击器状态"""
    
    def __init__(self):
        """初始化点击器模型"""
        self.click_thread: Optional[ClickThread] = None
        self.is_running: bool = False
        self.interval: int = 500
        self.button: str = 'left'
    
    def start_clicking(self, interval: int, button: str = 'left') -> None:
        """开始点击
        
        Args:
            interval: 点击间隔（毫秒）
            button: 鼠标按钮类型
        """
        if self.is_running:
            return
        
        self.interval = interval
        self.button = button
        self.click_thread = ClickThread(interval, button)
        self.click_thread.start()
        self.is_running = True
    
    def stop_clicking(self) -> None:
        """停止点击"""
        self.is_running = False
        
        if self.click_thread:
            self.click_thread.stop()
            self.click_thread.join(timeout=1.0)
            self.click_thread = None
```

- [ ] **Step 2: 验证模块可导入**

```bash
python -c "from models.clicker_model import ClickerModel; print('ClickerModel imported successfully')"
```

Expected: 输出 "ClickerModel imported successfully"

- [ ] **Step 3: 提交更改**

```bash
git add models/clicker_model.py
git commit -m "feat: extract ClickThread and create ClickerModel"
```

---

### Task 4: 提取 SettingsModel 到 models 模块

**Covers:** [S3, S5]

**Files:**
- Create: `models/settings_model.py`

**Interfaces:**
- Consumes: `ThemeManager`
- Produces: `SettingsModel.get_setting()`, `SettingsModel.set_setting()`

- [ ] **Step 1: 创建 SettingsModel 类**

```python
# models/settings_model.py
# -*- coding: utf-8 -*-
"""
设置模型模块 - 管理应用设置
"""
import json
import os
from typing import Dict, Any, Optional


class SettingsModel:
    """设置模型 - 管理应用设置"""
    
    DEFAULT_SETTINGS: Dict[str, Any] = {
        'interval': 500,
        'hotkey': 'F9',
        'is_dark': False,
        'button': 'left',
    }
    
    def __init__(self, settings_file: str = 'settings.json'):
        """初始化设置模型
        
        Args:
            settings_file: 设置文件路径
        """
        self.settings_file = settings_file
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.load_settings()
    
    def load_settings(self) -> None:
        """加载设置"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
        except Exception:
            pass
    
    def save_settings(self) -> None:
        """保存设置"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def get_setting(self, key: str) -> Any:
        """获取设置
        
        Args:
            key: 设置键名
            
        Returns:
            Any: 设置值
        """
        return self.settings.get(key)
    
    def set_setting(self, key: str, value: Any) -> None:
        """设置设置
        
        Args:
            key: 设置键名
            value: 设置值
        """
        self.settings[key] = value
        self.save_settings()
```

- [ ] **Step 2: 验证模块可导入**

```bash
python -c "from models.settings_model import SettingsModel; print('SettingsModel imported successfully')"
```

Expected: 输出 "SettingsModel imported successfully"

- [ ] **Step 3: 提交更改**

```bash
git add models/settings_model.py
git commit -m "feat: create SettingsModel for application settings"
```

---

### Task 5: 提取 UI 组件到 views/components 模块

**Covers:** [S3, S5]

**Files:**
- Create: `views/components/styled_button.py`
- Create: `views/components/styled_input.py`
- Create: `views/components/card_frame.py`

**Interfaces:**
- Consumes: `ThemeManager`
- Produces: `StyledButton`, `StyledInput`, `CardFrame`

- [ ] **Step 1: 创建 StyledButton 组件**

```python
# views/components/styled_button.py
# -*- coding: utf-8 -*-
"""
样式按钮组件 - 自定义样式按钮
"""
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from typing import Dict, Any


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
```

- [ ] **Step 2: 创建 StyledInput 组件**

```python
# views/components/styled_input.py
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
```

- [ ] **Step 3: 创建 CardFrame 组件**

```python
# views/components/card_frame.py
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
```

- [ ] **Step 4: 验证组件可导入**

```bash
python -c "from views.components import StyledButton, StyledInput, CardFrame; print('Components imported successfully')"
```

Expected: 输出 "Components imported successfully"

- [ ] **Step 5: 提交更改**

```bash
git add views/components/
git commit -m "feat: extract UI components to views/components module"
```

---

### Task 6: 创建 MainView 视图

**Covers:** [S3, S5]

**Files:**
- Create: `views/main_view.py`

**Interfaces:**
- Consumes: `ThemeManager`, `StyledButton`, `StyledInput`, `CardFrame`
- Produces: `MainView.setup_ui()`, `MainView.apply_theme()`, `MainView.toggle_theme()`

- [ ] **Step 1: 创建 MainView 类**

```python
# views/main_view.py
# -*- coding: utf-8 -*-
"""
主窗口视图模块 - 主窗口界面
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QSystemTrayIcon, QMenu, QAction, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QTimer, QEvent, QPoint
from PyQt5.QtGui import QIcon, QColor, QPainter, QPolygon, QFont
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
```

- [ ] **Step 2: 验证模块可导入**

```bash
python -c "from views.main_view import MainView; print('MainView imported successfully')"
```

Expected: 输出 "MainView imported successfully"

- [ ] **Step 3: 提交更改**

```bash
git add views/main_view.py
git commit -m "feat: create MainView for user interface"
```

---

### Task 7: 创建 MainPresenter

**Covers:** [S3, S5]

**Files:**
- Create: `presenters/main_presenter.py`

**Interfaces:**
- Consumes: `ClickerModel`, `SettingsModel`, `MainView`
- Produces: `MainPresenter.start_clicking()`, `MainPresenter.stop_clicking()`, `MainPresenter.toggle_theme()`

- [ ] **Step 1: 创建 MainPresenter 类**

```python
# presenters/main_presenter.py
# -*- coding: utf-8 -*-
"""
主窗口展示者模块 - 协调模型和视图
"""
import sys
import threading
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox
from typing import Optional
from models.clicker_model import ClickerModel
from models.settings_model import SettingsModel
from views.main_view import MainView


class MainPresenter(QObject):
    """主窗口展示者"""
    
    show_notification = pyqtSignal(str, str)
    hotkey_pressed_signal = pyqtSignal()
    
    def __init__(self):
        """初始化主窗口展示者"""
        super().__init__()
        self.model = ClickerModel()
        self.settings = SettingsModel()
        self.view = MainView()
        
        self.current_hotkey: Optional[str] = None
        
        # 连接信号
        self.show_notification.connect(self.send_notification)
        self.hotkey_pressed_signal.connect(self.handle_hotkey_pressed)
        
        # 设置视图回调
        self.view.on_theme_toggle = self.toggle_theme
        self.view.on_help_show = self.show_help
        self.view.on_start_stop_click = self.toggle_clicking
        self.view.on_hotkey_capture_start = self.setup_hotkey
        
        # 初始化视图
        self.view.setup_ui()
        self.view.apply_theme()
        self.view.setup_tray()
        
        # 加载设置
        self.load_settings()
        
        # 延迟初始化热键
        QTimer.singleShot(50, self.setup_hotkey_from_settings)
    
    def load_settings(self) -> None:
        """加载设置"""
        self.view.interval_input.setText(str(self.settings.get_setting('interval')))
        self.view.set_hotkey(self.settings.get_setting('hotkey'))
        self.view.is_dark = self.settings.get_setting('is_dark')
        self.view.apply_theme()
    
    def save_settings(self) -> None:
        """保存设置"""
        self.settings.set_setting('interval', self.view.get_interval())
        self.settings.set_setting('hotkey', self.view.get_hotkey())
        self.settings.set_setting('is_dark', self.view.is_dark)
    
    def toggle_clicking(self) -> None:
        """切换点击状态"""
        if self.model.is_running:
            self.stop_clicking()
        else:
            self.start_clicking()
    
    def start_clicking(self) -> None:
        """开始点击"""
        interval = self.view.get_interval()
        
        try:
            if interval < 10:
                QMessageBox.warning(self.view, "错误", "间隔时间不能小于10毫秒")
                return
        except ValueError:
            QMessageBox.warning(self.view, "错误", "请输入有效的数字")
            return
        
        self.model.start_clicking(interval)
        self.view.update_status(True)
        self.show_notification.emit("鼠标连点器", "✅ 已开启连点功能")
    
    def stop_clicking(self) -> None:
        """停止点击"""
        self.model.stop_clicking()
        self.view.update_status(False)
        self.show_notification.emit("鼠标连点器", "⏹ 已停止连点功能")
    
    def toggle_theme(self, is_dark: bool) -> None:
        """切换主题
        
        Args:
            is_dark: 是否使用深色主题
        """
        self.settings.set_setting('is_dark', is_dark)
    
    def setup_hotkey(self, hotkey_str: str) -> None:
        """设置快捷键
        
        Args:
            hotkey_str: 快捷键字符串
        """
        import keyboard
        
        try:
            if self.current_hotkey:
                keyboard.remove_hotkey(self.current_hotkey)
            
            self.current_hotkey = keyboard.add_hotkey(hotkey_str, self.hotkey_pressed_signal.emit)
            self.settings.set_setting('hotkey', hotkey_str)
        except ValueError as e:
            QMessageBox.warning(self.view, "错误", f"无效的快捷键: {str(e)}")
    
    def setup_hotkey_from_settings(self) -> None:
        """从设置加载快捷键"""
        hotkey = self.settings.get_setting('hotkey')
        if hotkey:
            self.setup_hotkey(hotkey)
    
    def handle_hotkey_pressed(self) -> None:
        """处理快捷键事件"""
        if self.model.is_running:
            self.stop_clicking()
        else:
            self.start_clicking()
    
    def send_notification(self, title: str, message: str) -> None:
        """发送Windows通知
        
        Args:
            title: 通知标题
            message: 通知内容
        """
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=2, threaded=False)
        except Exception:
            pass
    
    def show_help(self) -> None:
        """显示帮助窗口"""
        from views.help_view import HelpView
        dialog = HelpView(self.view, self.view.is_dark)
        dialog.exec_()
    
    def show(self) -> None:
        """显示窗口"""
        self.view.show()
    
    def close(self) -> None:
        """关闭窗口"""
        # 停止点击
        if self.model.is_running:
            self.stop_clicking()
        
        # 移除热键监听
        if self.current_hotkey:
            try:
                import keyboard
                keyboard.remove_hotkey(self.current_hotkey)
            except Exception:
                pass
        
        # 隐藏托盘图标
        if self.view.tray_icon:
            self.view.tray_icon.hide()
    
    def quit_app(self) -> None:
        """退出应用"""
        self.close()
        from PyQt5.QtWidgets import QApplication
        QApplication.quit()
```

- [ ] **Step 2: 验证模块可导入**

```bash
python -c "from presenters.main_presenter import MainPresenter; print('MainPresenter imported successfully')"
```

Expected: 输出 "MainPresenter imported successfully"

- [ ] **Step 3: 提交更改**

```bash
git add presenters/main_presenter.py
git commit -m "feat: create MainPresenter for business logic coordination"
```

---

### Task 8: 创建 HelpView 和 HelpPresenter

**Covers:** [S3, S5]

**Files:**
- Create: `views/help_view.py`
- Create: `presenters/help_presenter.py`

**Interfaces:**
- Consumes: `ThemeManager`, `StyledButton`
- Produces: `HelpView`, `HelpPresenter`

- [ ] **Step 1: 创建 HelpView 类**

```python
# views/help_view.py
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
```

- [ ] **Step 2: 创建 HelpPresenter 类**

```python
# presenters/help_presenter.py
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
```

- [ ] **Step 3: 验证模块可导入**

```bash
python -c "from views.help_view import HelpView; from presenters.help_presenter import HelpPresenter; print('Help modules imported successfully')"
```

Expected: 输出 "Help modules imported successfully"

- [ ] **Step 4: 提交更改**

```bash
git add views/help_view.py presenters/help_presenter.py
git commit -m "feat: create HelpView and HelpPresenter for help dialog"
```

---

### Task 9: 创建 utils 模块

**Covers:** [S3, S5]

**Files:**
- Create: `utils/hotkey_manager.py`
- Create: `utils/notification.py`

**Interfaces:**
- Consumes: (none)
- Produces: `HotkeyManager`, `NotificationManager`

- [ ] **Step 1: 创建 HotkeyManager 类**

```python
# utils/hotkey_manager.py
# -*- coding: utf-8 -*-
"""
快捷键管理器模块 - 管理全局快捷键
"""
from PyQt5.QtCore import pyqtSignal, QObject
from typing import Optional, Callable


class HotkeyManager(QObject):
    """快捷键管理器"""
    
    hotkey_pressed = pyqtSignal()
    
    def __init__(self):
        """初始化快捷键管理器"""
        super().__init__()
        self.current_hotkey: Optional[str] = None
    
    def set_hotkey(self, hotkey_str: str) -> bool:
        """设置快捷键
        
        Args:
            hotkey_str: 快捷键字符串
            
        Returns:
            bool: 是否设置成功
        """
        import keyboard
        
        try:
            if self.current_hotkey:
                keyboard.remove_hotkey(self.current_hotkey)
            
            self.current_hotkey = keyboard.add_hotkey(hotkey_str, self.hotkey_pressed.emit)
            return True
        except ValueError:
            return False
    
    def remove_hotkey(self) -> None:
        """移除快捷键"""
        if self.current_hotkey:
            try:
                import keyboard
                keyboard.remove_hotkey(self.current_hotkey)
                self.current_hotkey = None
            except Exception:
                pass
```

- [ ] **Step 2: 创建 NotificationManager 类**

```python
# utils/notification.py
# -*- coding: utf-8 -*-
"""
通知管理器模块 - 管理系统通知
"""
from typing import Optional


class NotificationManager:
    """通知管理器"""
    
    def __init__(self):
        """初始化通知管理器"""
        pass
    
    def send_notification(self, title: str, message: str) -> bool:
        """发送Windows通知
        
        Args:
            title: 通知标题
            message: 通知内容
            
        Returns:
            bool: 是否发送成功
        """
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=2, threaded=False)
            return True
        except Exception:
            return False
```

- [ ] **Step 3: 验证模块可导入**

```bash
python -c "from utils.hotkey_manager import HotkeyManager; from utils.notification import NotificationManager; print('Utils modules imported successfully')"
```

Expected: 输出 "Utils modules imported successfully"

- [ ] **Step 4: 提交更改**

```bash
git add utils/hotkey_manager.py utils/notification.py
git commit -m "feat: create HotkeyManager and NotificationManager utilities"
```

---

### Task 10: 创建新的程序入口

**Covers:** [S3, S5]

**Files:**
- Create: `main.py`

**Interfaces:**
- Consumes: `MainPresenter`
- Produces: (none)

- [ ] **Step 1: 创建 main.py**

```python
# main.py
# -*- coding: utf-8 -*-
"""
鼠标连点器 - 程序入口
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from presenters.main_presenter import MainPresenter


def main() -> None:
    """主函数"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # 设置应用程序字体
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)
    
    # 创建主展示者
    presenter = MainPresenter()
    presenter.show()
    
    # 连接退出信号
    app.aboutToQuit.connect(presenter.close)
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 验证程序可运行**

```bash
python main.py
```

Expected: 程序窗口正常显示

- [ ] **Step 3: 提交更改**

```bash
git add main.py
git commit -m "feat: create new program entry point"
```

---

### Task 11: 添加单元测试

**Covers:** [S5]

**Files:**
- Create: `tests/test_models.py`
- Create: `tests/test_presenters.py`
- Create: `tests/test_utils.py`

**Interfaces:**
- Consumes: `ClickerModel`, `SettingsModel`, `HotkeyManager`, `NotificationManager`
- Produces: (none)

- [ ] **Step 1: 创建 test_models.py**

```python
# tests/test_models.py
# -*- coding: utf-8 -*-
"""
模型单元测试
"""
import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.clicker_model import ClickerModel, ClickThread
from models.settings_model import SettingsModel


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
        model = SettingsModel()
        assert model.settings == SettingsModel.DEFAULT_SETTINGS
    
    def test_get_setting(self):
        """测试获取设置"""
        model = SettingsModel()
        assert model.get_setting('interval') == 500
        assert model.get_setting('hotkey') == 'F9'
    
    def test_set_setting(self):
        """测试设置设置"""
        model = SettingsModel()
        model.set_setting('interval', 1000)
        assert model.get_setting('interval') == 1000
```

- [ ] **Step 2: 创建 test_utils.py**

```python
# tests/test_utils.py
# -*- coding: utf-8 -*-
"""
工具模块单元测试
"""
import pytest
import sys
import os

# 添加项目根目录到路径
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
```

- [ ] **Step 3: 运行测试**

```bash
python -m pytest tests/ -v
```

Expected: 所有测试通过

- [ ] **Step 4: 提交更改**

```bash
git add tests/
git commit -m "test: add unit tests for models and utils"
```

---

### Task 12: 更新 requirements.txt 和 README.md

**Covers:** [S5]

**Files:**
- Modify: `requirements.txt`
- Modify: `README.md`

**Interfaces:**
- Consumes: (none)
- Produces: (none)

- [ ] **Step 1: 更新 requirements.txt**

```txt
PyQt5>=5.15
pyautogui>=0.9.54
keyboard>=0.13.5
win10toast>=0.9
pytest>=7.0
```

- [ ] **Step 2: 更新 README.md**

```markdown
# 🖱️ 鼠标连点器 (Mouse Clicker)

一款现代化的 Windows 鼠标自动连点工具，基于 PyQt5 构建，支持全局快捷键、明暗主题、系统托盘等功能。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-3.0.0-orange.svg)

## ✨ 功能特性

- **自动连点** — 模拟鼠标自动点击，支持自定义间隔时间（10ms ~ 自定义）
- **全局快捷键** — 默认 F11，支持自定义任意单键或组合键（Ctrl/Alt/Shift + 键）
- **系统托盘** — 最小化自动隐藏到托盘，双击恢复，右键菜单退出
- **明暗主题** — 自动检测 Windows 系统主题，也可手动切换
- **现代化 UI** — 圆角卡片、渐变按钮、阴影效果
- **桌面通知** — 通过系统托盘气泡提示连点开启/停止状态

## 📦 安装

### 从源码运行

1. 克隆仓库：
   ```bash
   git clone https://github.com/your-username/Mosaulse_MouseClick.git
   cd Mosaulse_MouseClick
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行程序：
   ```bash
   python main.py
   ```

### 直接使用

下载 `dist/MouseClicker.exe` 并直接运行，无需安装 Python 环境。

## 🚀 使用方法

1. **设置间隔** — 在"点击间隔"输入框中输入毫秒数（建议 100-1000ms）
2. **设置快捷键** — 点击"快捷键"输入框，按下你想用的快捷键组合
3. **开始/停止** — 按下快捷键或点击按钮即可切换连点状态

### 支持的快捷键

| 类型 | 示例 |
|------|------|
| 单键 | F1-F12、Space、Enter、Tab |
| 组合键 | Ctrl+F1、Alt+Space、Ctrl+Shift+C |

## 🏗️ 架构设计

本项目采用 MVP（Model-View-Presenter）架构：

- **Model**：数据模型和业务逻辑
- **View**：用户界面组件
- **Presenter**：协调模型和视图

### 目录结构

```
Mosaulse_MouseClick/
├── main.py                    # 程序入口
├── models/                    # 数据模型
├── views/                     # 用户界面
├── presenters/                # 展示者
├── utils/                     # 工具类
└── tests/                     # 单元测试
```

## ⚙️ 构建 EXE

使用 PyInstaller 打包：

```bash
pip install pyinstaller
pyinstaller MouseClicker.spec
```

生成的 EXE 文件位于 `dist/MouseClicker.exe`。

## 📋 依赖

| 包名 | 用途 |
|------|------|
| PyQt5 | GUI 框架 |
| pyautogui | 模拟鼠标点击 |
| keyboard | 全局快捷键注册 |
| win10toast | 系统通知 |
| pytest | 单元测试 |

## 🧪 运行测试

```bash
python -m pytest tests/ -v
```

## 📄 许可证

[MIT License](LICENSE) © 2026 Mosaulse
```

- [ ] **Step 3: 提交更改**

```bash
git add requirements.txt README.md
git commit -m "docs: update requirements and README for MVP architecture"
```

---

### Task 13: 验证和清理

**Covers:** [S7]

**Files:**
- Verify: All files
- Delete: `mouse_clicker.py` (旧文件)

**Interfaces:**
- Consumes: (none)
- Produces: (none)

- [ ] **Step 1: 验证程序功能**

```bash
python main.py
```

Expected: 程序正常运行，所有功能正常

- [ ] **Step 2: 运行所有测试**

```bash
python -m pytest tests/ -v
```

Expected: 所有测试通过

- [ ] **Step 3: 代码风格检查**

```bash
python -m flake8 main.py models/ views/ presenters/ utils/
```

Expected: 无严重风格问题

- [ ] **Step 4: 删除旧文件**

```bash
git rm mouse_clicker.py
```

- [ ] **Step 5: 最终提交**

```bash
git add .
git commit -m "refactor: complete MVP architecture migration"
```
