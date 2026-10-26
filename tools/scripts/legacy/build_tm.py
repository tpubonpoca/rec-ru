import json, os, glob
todo = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\todo.json', encoding='utf-8'))
ids = {}
idx = 0
for cat in ['scene','dialogue','txt']:
    for s in todo[cat]:
        ids[idx] = s; idx += 1
# but batches used different id spaces; build map from batch files
batch_map = {}
for bf in glob.glob(r'C:\Users\Asyncoder\Downloads\REC_extract\batches\*.txt'):
    for line in open(bf, encoding='utf-8'):
        if '\t' not in line: continue
        i, s = line.rstrip('\n').split('\t', 1)
        batch_map[i] = s.replace('\\n', '\n')
tm = {}
missing = 0
for tf in sorted(glob.glob(r'C:\Users\Asyncoder\Downloads\REC_extract\tm\*.txt')):
    for line in open(tf, encoding='utf-8'):
        if '\t' not in line: continue
        parts = line.rstrip('\n').split('\t', 1)
        if len(parts) != 2: continue
        i, v = parts
        src = batch_map.get(i)
        if src is None:
            missing += 1; continue
        v = v.replace('\\n', '\n')
        if v.strip(): tm[src] = v
try:
    w = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\words.json', encoding='utf-8'))
    tm.update(w['map'])
except Exception as e:
    print('words merge failed', e)
print('tm entries', len(tm), 'missing ids', missing)
json.dump(tm, open(r'C:\Users\Asyncoder\Downloads\REC_extract\tm.json','w',encoding='utf-8'), ensure_ascii=False, indent=0)
print('chars en', sum(len(k) for k in tm), 'chars ru', sum(len(v) for v in tm.values()))