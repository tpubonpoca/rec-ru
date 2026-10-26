import json, os, sys
sys.path.insert(0, r'C:\Users\Asyncoder\Downloads\REC_extract')
from rsrc import RSRC
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
orig = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\_orig.json', encoding='utf-8'))
have = set(orig.keys())
def exists(p):
    rel = p[len('res://'):]
    return rel in have or (rel + '.import') in have or (rel + '.remap') in have
missing = {}
for name in list(orig.keys()):
    if not (name.endswith('.scn') or name.endswith('.res')): continue
    p = os.path.join(root, name)
    if not os.path.exists(p): continue
    d = open(p,'rb').read()
    if d[:4] != b'RSRC': continue
    try: r = RSRC(d)
    except Exception: continue
    for t, path in r.ext:
        if path.startswith('res://') and not exists(path):
            missing.setdefault(path, []).append(name.split('-')[-1])
print('missing ext refs:', len(missing))
for p, w in sorted(missing.items())[:30]:
    print(p, '|', w[:2])