import json, os
items = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\scn_missing.json', encoding='utf-8'))
budget = 6000
chunks=[]; cur=[]; size=0
for s in items:
    L=len(s)+2
    if cur and size+L>budget: chunks.append(cur); cur=[]; size=0
    cur.append(s); size+=L
if cur: chunks.append(cur)
for i,ch in enumerate(chunks):
    with open(r'C:\Users\Asyncoder\Downloads\REC_extract\batches\scn_%02d.txt' % i, 'w', encoding='utf-8') as f:
        for j,s in enumerate(ch):
            f.write('%d\t%s\n' % (300000 + i*1000 + j, s.replace(chr(10), '\\n')))
print('chunks', len(chunks))