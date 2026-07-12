# 架构决策记录

## AD-001: MVP 架构

**决策**：采用 Model-View-Presenter（MVP）架构。

**背景**：需要分离 UI 逻辑与业务逻辑，便于测试和维护。

**影响**：
- `models/`：纯业务逻辑，无 PyQt5 依赖
- `views/`：纯 UI 展示，无业务逻辑
- `presenters/`：协调层，连接 Model 与 View

## AD-002: 线程模型

**决策**：使用 `threading.Thread` 而非 `QThread` 管理点击线程。

**背景**：`pyautogui.click()` 是阻塞调用，需要在独立线程中执行以避免冻结 GUI。

**影响**：
- 通过 Qt 信号（`hotkey_pressed_signal`）线程安全地传递热键事件
- `ClickThread.running` 使用普通 bool（良性数据竞争）

## AD-003: 延迟导入

**决策**：`keyboard`、`win10toast` 等库在方法内部导入。

**背景**：避免模块加载时自动执行系统钩子（如全局热键注册）。

**影响**：
- 新增系统级依赖时必须遵循此模式
- 首次调用会有微小延迟（可忽略）

## AD-004: 设置路径

**决策**：`_get_app_dir()` 返回 `sys.executable` 目录（打包后）或 `Scripts/` 的父目录（开发时）。

**背景**：PyInstaller 打包后 `sys.executable` 指向 EXE 所在目录，开发时需要指向项目根目录。

**影响**：`settings.json` 始终与可执行文件在同一目录。
