# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ["Scripts/main.py"],
    pathex=["Scripts"],
    binaries=[],
    datas=[("Resources/mouse_click_icon.png", ".")],
    hiddenimports=[
        "models.clicker_model",
        "models.settings_model",
        "views.main_view",
        "views.help_view",
        "views.components.styled_button",
        "views.components.styled_input",
        "views.components.card_frame",
        "presenters.main_presenter",
        "presenters.help_presenter",
        "utils.theme_manager",
        "utils.hotkey_manager",
        "utils.notification",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="MouseClicker",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="Resources/mouse_click_icon.png",
)
