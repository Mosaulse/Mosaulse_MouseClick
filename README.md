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
