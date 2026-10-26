import json, sys, os, re
sys.path.insert(0, r'C:\Users\Asyncoder\Downloads\REC_extract')
from rsrc import RSRC
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
orig = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\_orig.json', encoding='utf-8'))
pck = open(r'C:\Users\Asyncoder\Downloads\REC_extract\REC.pck.orig','rb')
pat = re.compile(r'-(film|science|history)_\d+\.res$')
total = 0; bad = 0
for name, m in orig.items():
    if not pat.search(name): continue
    total += 1
    pck.seek(m['base']+m['ofs']); od = pck.read(m['size'])
    p = os.path.join(root, name)
    nd = open(p,'rb').read() if os.path.exists(p) else od
    ro = RSRC(od); rn = RSRC(nd)
    vo = {}; vn = {}
    for (lp,ln,v,k,prop) in ro.strings:
        if k=='value': vo.setdefault(prop, []).append(v)
    for (lp,ln,v,k,prop) in rn.strings:
        if k=='value': vn.setdefault(prop, []).append(v)
    ans = [vn.get('Answer%d'%i,[''])[0] for i in range(1,5)]
    empt = [i+1 for i,a in enumerate(ans) if not a.strip()]
    q = vn.get('Question',[''])[0]
    if empt or not q.strip():
        bad += 1
        print('BAD', os.path.basename(name), 'empty', empt, repr(q[:50]))
    if total <= 3:
        print(os.path.basename(name), '|', q[:50], '|', [a[:25] for a in ans])
print('total', total, 'bad', bad)