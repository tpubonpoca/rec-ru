import json, os, sys
sys.path.insert(0, r'C:\Users\Asyncoder\Downloads\REC_extract')
from rsrc import RSRC
from fontTools.ttLib import TTFont
font = TTFont(r'C:\Users\Asyncoder\Downloads\REC_extract\fontproj\out\VCR_OSD_Mono.ttf-45fb8313e03f845b2bc3e59d42d2d129.fontdata.ttf')
cmap = font.getBestCmap(); hmtx = font['hmtx']
def width(s):
    w = 0
    for ch in s:
        g = cmap.get(ord(ch))
        w += hmtx[g][0] if g else 1200
    return w
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
orig = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\_orig.json', encoding='utf-8'))
pck = open(r'C:\Users\Asyncoder\Downloads\REC_extract\REC.pck.orig','rb')
rows = []
for name, m in orig.items():
    if not (name.endswith('.scn') or name.endswith('.res')): continue
    pck.seek(m['base']+m['ofs']); od = pck.read(m['size'])
    p = os.path.join(root, name)
    if not os.path.exists(p): continue
    nd = open(p,'rb').read()
    if nd[:4] != b'RSRC' or od[:4] != b'RSRC': continue
    try: ro = RSRC(od); rn = RSRC(nd)
    except Exception: continue
    if len(ro.strings) != len(rn.strings): continue
    for a,b in zip(ro.strings, rn.strings):
        if a[2] == b[2]: continue
        if a[4] not in ('text','placeholder_text','title','Name','label','name_label','text_label'): continue
        w0, w1 = width(a[2]), width(b[2])
        if w0 == 0: continue
        r = w1/w0
        if r > 1.35 and len(a[2]) < 30:
            rows.append((round(r,2), a[4], a[2][:30], b[2][:34], name.split('-')[-1]))
rows.sort(reverse=True)
print('flagged', len(rows))
for r in rows[:25]: print(r)