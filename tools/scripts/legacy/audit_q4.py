import json, sys, os, re
sys.path.insert(0, r'C:\Users\Asyncoder\Downloads\REC_extract')
from rsrc import RSRC
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
orig = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\_orig.json', encoding='utf-8'))
pck = open(r'C:\Users\Asyncoder\Downloads\REC_extract\REC.pck.orig','rb')
pat = re.compile(r'-(film|science|history)_\d+\.res$')
for name, m in orig.items():
    if not pat.search(name): continue
    pck.seek(m['base']+m['ofs']); od = pck.read(m['size'])
    p = os.path.join(root, name)
    nd = open(p,'rb').read() if os.path.exists(p) else od
    rn = RSRC(nd)
    for (lp,ln,val,k,prop) in rn.strings:
        if k != 'value': continue
        if val.count('[') != val.count(']'):
            print('BRACKET', os.path.basename(name).split('-')[-1], prop, repr(val[:70]))
        if '%' in val:
            print('PERCENT', os.path.basename(name).split('-')[-1], prop, repr(val[:70]))
        if '\\' in val:
            print('BACKSLASH', os.path.basename(name).split('-')[-1], prop, repr(val[:70]))