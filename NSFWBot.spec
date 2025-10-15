# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

block_cipher = None

try:
    project_root = Path(__file__).parent.resolve()
except NameError:
    project_root = Path.cwd()

datas = []

for relative in ("templates", "static", "languages"):
    src = project_root / relative
    if src.exists():
        datas.append((str(src), relative))

for file_name in ("config.py", "env_example.txt"):
    src = project_root / file_name
    if src.exists():
        datas.append((str(src), "."))

icon_path = project_root / "static" / "icons" / "bot.ico"
icon_file = str(icon_path) if icon_path.exists() else None

a = Analysis(
    ['start_bot.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NSFWBot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
)
