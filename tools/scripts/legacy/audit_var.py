import json, sys, re, os
sys.path.insert(0, r'C:\Users\Asyncoder\Downloads\REC_extract')
from rsrc import RSRC
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
orig = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\_orig.json', encoding='utf-8'))
pck = open(r'C:\Users\Asyncoder\Downloads\REC_extract\REC.pck.orig','rb')
found = {}
for name, m in orig.items():
    if not (name.endswith('.scn') or name.endswith('.res')): continue
    pck.seek(m['base']+m['ofs']); od = pck.read(m['size'])
    p = os.path.join(root, name)
    if not os.path.exists(p): continue
    nd = open(p,'rb').read()
    if od[:4] != b'RSRC' or nd[:4] != b'RSRC': continue
    try: ro = RSRC(od); rn = RSRC(nd)
    except Exception: continue
    if len(ro.strings) != len(rn.strings): continue
    names = set(v for (lp,ln,v,k,prop) in rn.strings if prop=='names')
    for a,b in zip(ro.strings, rn.strings):
        if b[3] != 'value': continue
        s = b[2].strip()
        if not s or s in names: continue
        if re.search(r'[А-Яа-я]', s): continue
        if not re.search(r'[A-Za-z]{3,}', s): continue
        if len(s) < 4 or len(s) > 80: continue
        if not re.search(r'[a-z] [a-z]', s.lower()): continue
        if re.match(r'^(res|uid)://', s): continue
        found.setdefault(s, 0)
        found[s] += 1
print('english phrases left in variants:', len(found))
for s in sorted(found):
    print(repr(s))