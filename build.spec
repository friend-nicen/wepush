# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

main_a = Analysis(
    ['main.py'],
    pathex=['D:\\python-project\\proxy\\weauto'],
    binaries=[],
    datas=[
        ('utils/*.png', 'utils'),
        ('wxauto/*.py', 'wxauto')
    ],
    hiddenimports=['uvicorn.logging', 'uvicorn.protocols', 'fastapi'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

main_pyz = PYZ(main_a.pure, main_a.zipped_data, cipher=block_cipher)

main_exe = EXE(
    main_pyz,
    main_a.scripts,
    main_a.binaries,
    main_a.zipfiles,
    main_a.datas,
    [],
    name='weauto_server',
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
)

mq_a = Analysis(
    ['mq.py'],
    pathex=['D:\\python-project\\proxy\\weauto'],
    binaries=[],
    datas=[
        ('utils/*.png', 'utils'),
        ('wxauto/*.py', 'wxauto')
    ],
    hiddenimports=['redis.asyncio'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

mq_pyz = PYZ(mq_a.pure, mq_a.zipped_data, cipher=block_cipher)

mq_exe = EXE(
    mq_pyz,
    mq_a.scripts,
    mq_a.binaries,
    mq_a.zipfiles,
    mq_a.datas,
    [],
    name='weauto_mq',
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
)