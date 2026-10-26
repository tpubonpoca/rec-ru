import json, os, hashlib
mb = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\_files.json'
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
files = json.load(open(mb, encoding='utf-8'))
n = 0
for f in files:
    p = os.path.join(root, f['name'])
    d = open(p,'rb').read()
    if len(d) != f['size'] or hashlib.md5(d).hexdigest() != f['md5']:
        f['size'] = len(d); f['md5'] = hashlib.md5(d).hexdigest(); n += 1
json.dump(files, open(mb,'w',encoding='utf-8'))
print('synced', n)