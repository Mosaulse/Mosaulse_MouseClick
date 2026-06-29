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
