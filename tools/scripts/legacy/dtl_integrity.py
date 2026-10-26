import json, os
orig = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\_orig.json', encoding='utf-8'))
pck = open(r'C:\Users\Asyncoder\Downloads\REC_extract\REC.pck.orig','rb')
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
issues = 0
for name, m in orig.items():
    if not name.endswith('.dtl'): continue
    pck.seek(m['base']+m['ofs']); o = pck.read(m['size'])
    p = os.path.join(root, name)
    d = open(p,'rb').read()
    probs = []
    if d.startswith(b'\xef\xbb\xbf'): probs.append('BOM')
    if b'\r\n' in d and b'\n' in d.replace(b'\r\n', b''): probs.append('mixed EOL')
    if not d.endswith(b'\n'): probs.append('no final newline')
    if o.startswith(b'\xef\xbb\xbf'): probs.append('orig BOM')
    try: d.decode('utf-8')
    except Exception: probs.append('bad utf8')
    if probs:
        issues += 1
        print(name.split('/')[-1], probs)
print('files with issues:', issues)