# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import copy_metadata
import toga_winforms
import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Below imports are not necessary. These are automatically imported by pyinstaller. But I added to avoid error message in editor.
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.api import PYZ, EXE, COLLECT


os.environ["TOGA_BACKEND"] = "winforms"
sys.path.insert(0, os.getcwd())

datas = []
datas += copy_metadata("toga-core")
datas += collect_data_files("toga") + collect_data_files("toga_winforms") + copy_metadata("toga-winforms")

hidden_imports = ["toga", "toga_winforms"] + collect_submodules("toga") + collect_submodules("toga_winforms")

packages = {
    "ai_video_generators": ["pixverse_ai", "haiper_ai"],
    "ai_image_generators": ["ideogram_ai", "pixlr_ai"],
    "ai_content_generators": ["wordhero_ai"],
}
all_submodules = []


for package, sub_packages in packages.items():
    datas += collect_data_files(package)
    for sub_package in sub_packages:
        all_submodules.append(f"{package}.{sub_package}")
        print(collect_submodules(f"{package}.{sub_package}"))
        datas += collect_data_files(sub_package)
        all_submodules.extend(collect_submodules(f"{package}.{sub_package}"))

hidden_imports = hidden_imports + list(packages.keys()) + all_submodules
print(hidden_imports)

a = Analysis(
    ["app.py"],
    pathex=[f"{os.getcwd()}\\appenv"],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=["."],  # Add this line to include the current directory
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
    # a.binaries,
    # a.datas,
    [],
    name="AI Generators",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=f"{os.getcwd()}\\temp\\testing_exe",  # Only for standalone EXE
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.scripts,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="ai_generator",
)
