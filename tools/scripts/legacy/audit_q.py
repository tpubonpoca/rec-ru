import json, sys, os
sys.path.insert(0, r'C:\Users\Asyncoder\Downloads\REC_extract')
from rsrc import RSRC
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
orig = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\_orig.json', encoding='utf-8'))
pck = open(r'C:\Users\Asyncoder\Downloads\REC_extract\REC.pck.orig','rb')
bad = 0; total = 0
for name, m in orig.items():
    if '/questions/' not in name and 'questions' not in name: continue
    if not name.endswith('.res'): continue
    total += 1
    pck.seek(m['base']+m['ofs']); d = pck.read(m['size'])
    try: r = RSRC(d)
    except Exception: continue
    vals = {}
    for (lp,ln,v,k,prop) in r.strings:
        if k == 'value': vals.setdefault(prop, []).append(v)
    q = vals.get('Question', [''])[0]
    ans = [vals.get('Answer%d' % i, [''])[0] for i in range(1,5)]
    empt = [i+1 for i,a in enumerate(ans) if not a.strip()]
    if empt or not q.strip():
        bad += 1
        print('BAD', os.path.basename(name), 'empty answers', empt, 'q:', repr(q[:40]))
print('questions', total, 'bad', bad)