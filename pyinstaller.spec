# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

#hiddenimports = ['whitenoise', 'whitenoise.middleware']
hiddenimports = collect_submodules('consultorio')


a = Analysis(
    ['manage.py'],
    pathex=[],
    binaries=[],
    datas=[('historia\\templates', 'historia\\templates'), ('historia\\static', 'historia\\static'), ('.env.example', '.')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['db.sqlite3'],
    noarchive=False,
    optimize=0,
)

a.datas = [entry for entry in a.datas if 'db.sqlite3' not in entry[0] and 'db.sqlite3' not in entry[1]]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='manage',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['historia\\static\\eye.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='manage',
)
