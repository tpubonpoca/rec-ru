import json, os, re
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
orig = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\_orig.json', encoding='utf-8'))
have = set(orig.keys())
def exists(p):
    rel = p[len('res://'):]
    return rel in have or (rel + '.import') in have or (rel + '.remap') in have or (rel + '.uid') in have
refpat = re.compile(r'(?:path|arg)="(res://[^"]+)"')
missing = {}
tl = os.path.join(root, 'dialogue', 'timelines')
for f in sorted(os.listdir(tl)):
    if not f.endswith('.dtl'): continue
    for i, line in enumerate(open(os.path.join(tl, f), encoding='utf-8'), 1):
        for p in refpat.findall(line):
            if not exists(p):
                missing.setdefault(p, []).append(f + ':' + str(i))
print('missing refs:', len(missing))
for p, where in sorted(missing.items()):
    print(p, '|', where[:3])