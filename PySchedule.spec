# -*- mode: python -*-

block_cipher = None


a = Analysis(['PySchedule.py'],
             pathex=['D:\\GitHub\\PySchedule'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break
a.datas += [('Icon.ico','D:\\GitHub\\PySchedule\\Icon.ico', 'Data')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='PySchedule',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='D:\\GitHub\\PySchedule\\Icon.ico')
