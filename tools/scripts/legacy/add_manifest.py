import json, os, hashlib, sys
mb = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\_files.json'
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
files = json.load(open(mb, encoding='utf-8'))
names = {f['name'] for f in files}
added = 0
for dp, dn, fn in os.walk(root):
    for f in fn:
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, root).replace('\\','/')
        if rel in names: continue
        d = open(p,'rb').read()
        files.append({'name': rel, 'ofs': 0, 'size': len(d), 'md5': hashlib.md5(d).hexdigest(), 'flags': 0})
        added += 1
json.dump(files, open(mb,'w',encoding='utf-8'))
print('added', added, 'total', len(files))