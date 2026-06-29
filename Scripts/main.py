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
