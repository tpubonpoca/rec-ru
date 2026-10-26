import json, os
mb = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\_files.json'
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
files = json.load(open(mb, encoding='utf-8'))
keep = [f for f in files if os.path.exists(os.path.join(root, f['name']))]
names = {f['name'] for f in keep}
import hashlib
for dp, dn, fn in os.walk(root):
    for f in fn:
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, root).replace('\\','/')
        if rel in names: continue
        d = open(p,'rb').read()
        keep.append({'name': rel, 'ofs': 0, 'size': len(d), 'md5': hashlib.md5(d).hexdigest(), 'flags': 0})
json.dump(keep, open(mb,'w',encoding='utf-8'))
print('entries', len(keep))