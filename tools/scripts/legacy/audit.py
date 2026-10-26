import json, os, re, sys
sys.path.insert(0, r'C:\Users\Asyncoder\Downloads\REC_extract')
from rsrc import RSRC
from rewriter import SAFE_PROPS
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
orig = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\_orig.json', encoding='utf-8'))
pck = open(r'C:\Users\Asyncoder\Downloads\REC_extract\REC.pck.orig','rb')
unsafe = []; changed = 0; files = 0; english_left = []
for name, m in orig.items():
    if not (name.endswith('.scn') or name.endswith('.res')): continue
    pck.seek(m['base']+m['ofs']); od = pck.read(m['size'])
    p = os.path.join(root, name)
    if not os.path.exists(p): continue
    nd = open(p,'rb').read()
    if nd[:4] != b'RSRC': continue
    try: ro = RSRC(od); rn = RSRC(nd)
    except Exception: continue
    if len(ro.strings) != len(rn.strings):
        unsafe.append((name, 'string count mismatch', len(ro.strings), len(rn.strings))); continue
    files += 1
    for a, b in zip(ro.strings, rn.strings):
        if a[2] == b[2]: continue
        changed += 1
        prop = a[4]
        if prop not in SAFE_PROPS and prop != 'variants':
            unsafe.append((name, prop, a[2][:50], b[2][:50]))
print('files', files, 'changed strings', changed, 'unsafe', len(unsafe))
for u in unsafe[:15]: print('  UNSAFE', u)