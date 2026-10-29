# Сбор пар EN->RU из бинарных ресурсов: ванильный 0.5.5.2 против нашего RU
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(__file__))
from rsrc import RSRC
EN, RU = 'res_0552_en', 'res_0552_ru'
files = [l.strip() for l in open('ru_changed.txt') if l.strip().endswith(('.res', '.scn')) ]
pairs = []; props = collections.Counter(); mism = []
for p in files:
    a = RSRC(open(os.path.join(EN, p), 'rb').read()); b = RSRC(open(os.path.join(RU, p), 'rb').read())
    sa = [s for s in a.strings if s[3].startswith('value')]; sb = [s for s in b.strings if s[3].startswith('value')]
    if len(sa) != len(sb): mism.append(p); continue
    for x, y in zip(sa, sb):
        if x[2] != y[2]:
            pairs.append((p, x[4], x[2], y[2])); props[x[4]] += 1
json.dump(pairs, open('res_pairs.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(pairs), 'mismatch', mism)
print(props.most_common())
# конфликты: один EN -> разные RU
m = collections.defaultdict(set)
for p, pr, e, r in pairs: m[e].add(r)
print('conflicts', sum(1 for e in m if len(m[e]) > 1))
