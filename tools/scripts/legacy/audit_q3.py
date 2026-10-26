import json, sys, os, re
sys.path.insert(0, r'C:\Users\Asyncoder\Downloads\REC_extract')
from rsrc import RSRC
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
orig = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\_orig.json', encoding='utf-8'))
pck = open(r'C:\Users\Asyncoder\Downloads\REC_extract\REC.pck.orig','rb')
pat = re.compile(r'-(film|science|history)_\d+\.res$')
total = 0
for name, m in orig.items():
    if not pat.search(name): continue
    total += 1
    pck.seek(m['base']+m['ofs']); od = pck.read(m['size'])
    p = os.path.join(root, name)
    nd = open(p,'rb').read() if os.path.exists(p) else od
    rn = RSRC(nd)
    v = {}
    for (lp,ln,val,k,prop) in rn.strings:
        if k=='value': v.setdefault(prop, []).append(val)
    c = (v.get('CorrectAnswer') or [''])[0]
    w = [(v.get('WrongAnswer%d'%i) or [''])[0] for i in range(1,4)]
    q = (v.get('Question') or [''])[0]
    empt = [i+1 for i,a in enumerate(w) if not a.strip()]
    if not c.strip() or empt:
        print('BAD', os.path.basename(name).split('-')[-1], '| q:', q[:45], '| correct:', repr(c[:25]), '| empty wrong:', empt)
print('total', total)