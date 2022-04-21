# -*- mode: python ; coding: utf-8 -*-


block_cipher = None
from sys import platform

if platform.startswith("win"):
    # Windows
    from kivy_deps import sdl2, glew
    sdl2_dep_bins = sdl2.dep_bins
    glew_dep_bins = glew.dep_bins
    hidden = ['win32timezone', 'websockets.legacy.client']
else:
    # on Linux
    sdl2_dep_bins = []
    glew_dep_bins = []
    hidden = ['websockets.legacy.client']

from kivymd import hooks_path as kivymd_hooks_path

a = Analysis(['src/main.py'],
             pathex=[],
             binaries=[],
             datas=[('./data', './data')],
             hiddenimports=hidden,
             hookspath=[kivymd_hooks_path],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz, Tree('src/'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          *[Tree(p) for p in (sdl2_dep_bins + glew_dep_bins)],
          name='webfpga-gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
