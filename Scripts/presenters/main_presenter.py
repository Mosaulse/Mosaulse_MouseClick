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
        self.view.is_dark = True
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
