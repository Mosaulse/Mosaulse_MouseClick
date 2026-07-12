# 常见问题

## Q1: PyInstaller 打包后模块导入失败

**现象**：`ModuleNotFoundError: No module named 'xxx'`

**原因**：`hiddenimports` 未包含所有 `Scripts/` 下的模块。

**解决**：在 `MouseClicker.spec` 的 `hiddenimports` 中添加缺失模块。

## Q2: 测试从非项目根目录运行失败

**现象**：`ModuleNotFoundError: No module named 'models'`

**原因**：测试文件使用 `sys.path.insert(0, ...)` 导入，依赖相对路径。

**解决**：从项目根目录运行 `python -m pytest Scripts/tests/ -v`。

## Q3: 全局热键无响应

**现象**：按下热键无反应。

**原因**：
1. `keyboard` 库需要管理员权限（部分 Windows 版本）
2. 热键被其他程序占用

**解决**：以管理员身份运行，或更换热键组合。

## Q4: 点击线程无法停止

**现象**：点击开始后无法停止。

**原因**：`ClickThread.running` 为 True 时线程持续循环。

**解决**：确保调用 `stop()` 后 `join(timeout=1.0)` 等待线程结束。

## Q5: 设置未保存

**现象**：修改设置后重启丢失。

**原因**：`_get_app_dir()` 路径不正确，或文件写入权限问题。

**解决**：检查 `settings.json` 是否在可执行文件同目录。

## Q6: GUI 冻结

**现象**：界面无响应，无法操作。

**原因**：主线程执行了阻塞操作（如 `time.sleep()`、网络请求）。

**解决**：将耗时操作移至线程，使用 Qt 信号更新 UI。
