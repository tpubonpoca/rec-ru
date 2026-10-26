import json, os
orig = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\_orig.json', encoding='utf-8'))
pck = open(r'C:\Users\Asyncoder\Downloads\REC_extract\REC.pck.orig','rb')
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
n=0
for name, m in orig.items():
    if not name.endswith('.fontdata'): continue
    pck.seek(m['base'] + m['ofs']); d = pck.read(m['size'])
    p = os.path.join(root, name)
    open(p,'wb').write(d)
    print(name, m['size'], d[:4])
    n+=1
print('restored', n)