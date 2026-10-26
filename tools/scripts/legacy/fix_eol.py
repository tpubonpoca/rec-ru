import os
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res\dialogue'
crlf = 0
fixed = 0
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.endswith('.dtl'): continue
        p = os.path.join(dp, f)
        b = open(p,'rb').read()
        if b'\r\n' in b:
            crlf += 1
            b = b.replace(b'\r\n', b'\n')
            open(p,'wb').write(b)
            fixed += 1
print('files with CRLF:', crlf, 'fixed:', fixed)