import os, re
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res\dialogue\timelines'
labels = {}
jumps = []
for f in sorted(os.listdir(root)):
    if not f.endswith('.dtl'): continue
    tl = f[:-4]
    labels.setdefault(tl, set())
    for i, line in enumerate(open(os.path.join(root,f), encoding='utf-8'), 1):
        s = line.strip()
        m = re.match(r'label\s+(\S+)', s)
        if m: labels[tl].add(m.group(1))
        m = re.match(r'jump\s+(\S+)', s)
        if m:
            tgt = m.group(1)
            jumps.append((tl, i, tgt))
bad = []
for tl, i, tgt in jumps:
    if '/' in tgt:
        t2, lab = tgt.split('/', 1)
        if t2 not in labels:
            bad.append((tl, i, tgt, 'timeline missing'))
        elif lab not in labels[t2] and lab != '':
            bad.append((tl, i, tgt, 'label missing'))
print('jumps', len(jumps), 'bad', len(bad))
for b in bad[:40]: print(b)