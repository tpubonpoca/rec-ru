import json, os, sys
sys.path.insert(0, r'C:\Users\Asyncoder\Downloads\REC_extract')
from rewriter import rewrite_bytes
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
tm = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\tm.json', encoding='utf-8'))
orig = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\_orig.json', encoding='utf-8'))
pck = open(r'C:\Users\Asyncoder\Downloads\REC_extract\REC.pck.orig','rb')
kinds = sys.argv[1].split(',')
n=0; edits=0; fails=0
for name, meta in orig.items():
    if not any(name.endswith(k) for k in kinds): continue
    pck.seek(meta['base'] + meta['ofs']); data = pck.read(meta['size'])
    try:
        out, c = rewrite_bytes(data, tm)
    except Exception as e:
        fails += 1
        print('FAIL', name, e)
        out, c = data, 0
    open(os.path.join(root, name),'wb').write(out)
    if c: n += 1; edits += c
print('rewritten files', n, 'edits', edits, 'fails', fails)