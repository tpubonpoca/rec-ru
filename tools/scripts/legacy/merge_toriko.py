import sys
sys.path.insert(0, r'C:\Users\Asyncoder\Downloads\REC_extract')
from fontTools.ttLib import TTFont
try:
    from fontTools.ttLib.scaleUpem import scale_upem
except Exception as e:
    print('no scaleUpem', e); raise
from merge_font3 import merge
src = r'C:\Users\Asyncoder\Downloads\REC_extract\fontproj\out\Toriko.ttf-9d8a733741cf0a7e03818cd52a1c990b.fontdata.ttf'
up = r'C:\Users\Asyncoder\Downloads\REC_extract\fonts\Toriko_1024.ttf'
dst = r'C:\Users\Asyncoder\Downloads\REC_extract\fonts\Toriko_cyr2.ttf'
f = TTFont(src)
print('old upem', f['head'].unitsPerEm)
scale_upem(f, 1024)
f.save(up)
print('scaled upem', TTFont(up)['head'].unitsPerEm)
merge(up, r'C:\Users\Asyncoder\Downloads\REC_extract\fontproj\out\Joystix.ttf-b6d1179187941581768bf13fd88ecf93.fontdata.ttf', dst)