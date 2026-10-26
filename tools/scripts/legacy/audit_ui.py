import json, sys, re, os
sys.path.insert(0, r'C:\Users\Asyncoder\Downloads\REC_extract')
from rsrc import RSRC
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
orig = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\_orig.json', encoding='utf-8'))
pck = open(r'C:\Users\Asyncoder\Downloads\REC_extract\REC.pck.orig','rb')
UI_PROPS = {'text','label','title','placeholder_text','tooltip_text','text_label','name_label','description','Name','Description' }
found = []
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
    for a,b in zip(ro.strings, rn.strings):
        if b[3] != 'value': continue
        s = b[2].strip()
        if not s or len(s) < 3: continue
        if re.search(r'[А-Яа-я]', s): continue
        if not re.search(r'[A-Za-z]{2,}', s): continue
        if a[4] in UI_PROPS and a[4] != 'variants':
            found.append((a[4], s, name.split('-')[-1]))
uniq = {}
for prop, s, f in found: uniq.setdefault(s, set()).add(prop)
print('untranslated UI texts:', len(uniq))
for s in sorted(uniq):
    print(repr(s), '|', ','.join(sorted(uniq[s])))