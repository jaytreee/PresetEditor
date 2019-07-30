# -*- mode: python -*-
import glob

def get_files(files, path):
    filelist = glob.glob(files)
    ret = []
    for f in filelist:
        ret.append((f, path))
        print((f, path))
    return ret

block_cipher = None

import subprocess, re, sys

# Detect debugging mode to generate debug exe (not distributed)
DEBUG = False
if '--debug' in sys.argv:
    DEBUG = True

# Get version 
with open('version.txt','r') as f:
    VERSION = str(f.read()).strip()
    
# Get output
hgoutput = subprocess.run(['hg','id','-n'], stdout=subprocess.PIPE)
hgoutput = hgoutput.stdout.decode('utf-8').strip()
match = re.search('^([0-9]+)(\+)?$', hgoutput)

# Check that directory is clean
if match.group(2) and not DEBUG:
    print('Cannot build with modifications in working directory')
    sys.exit(1)
    
REVISION = match.group(1)
OUTNAME = 'PresetEditor_v' + VERSION 

with open('revision.txt','w') as f:
	f.write(REVISION)

if DEBUG:
    OUTNAME += '_DEBUG' + '-rev' + '{:04d}'.format(int(REVISION))

a = Analysis(['source\\preset_editor.py'],
             pathex=['source'],
             binaries=[],
             datas=[
                *get_files('schemata/*.xsd', 'schemata'),
			    ('version.txt', '.'),
			    ('revision.txt', '.')
            ],
            hiddenimports=[],
            hookspath=[],
            runtime_hooks=[],
            excludes=[],
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher
)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=OUTNAME,
          debug=DEBUG,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=DEBUG )
