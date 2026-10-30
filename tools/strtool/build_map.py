# Карта строк C#: оригинал 0.5.5.2 -> RU 21.10, перенос на 0.6
import collections, difflib, re, json, os
GEN = re.compile(r'^(GetGodot|InvokeGodot|HasGodot|SetGodot|GetGodotClass|SaveGodot|RestoreGodot)')
def load(p):
    d = collections.defaultdict(list)
    for l in open(p, encoding='utf-8'):
        t, m, s = l.rstrip('\n').split('\t', 2)
        d[(t, m)].append(s)
    return d
def skip(t, m): return GEN.match(m) or re.search(r'/(MethodName|PropertyName|SignalName)$', t)
o, r, n = load('orig.tsv'), load('ru.tsv'), load('new.tsv')
pairs = {}; glob = collections.defaultdict(collections.Counter)
for k in o:
    if skip(*k) or k not in r: continue
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, o[k], r[k], autojunk=False).get_opcodes():
        if tag == 'replace' and i2 - i1 == j2 - j1:
            for a, b in zip(o[k][i1:i2], r[k][j1:j2]):
                pairs[(k, a)] = b; glob[a][b] += 1
FIX = {('MailResource', 'SaveToDictionary', 'name'): None, ('Purchasable', 'SetPermanentlyPurchased', 'Purchased'): 'Куплено', ('Purchasable', 'SetPermanentlyPurchased', 'Purchase'): 'Купить', ('Purchasable', 'SetLimitReached', 'Purchase'): 'Купить'}
for (t, m, a), b in FIX.items():
    if b is None: pairs.pop(((t, m), a), None)
    else: pairs[((t, m), a)] = b
extra = {}
if os.path.exists('new_ru.tsv'):
    for l in open('new_ru.tsv', encoding='utf-8'):
        if '\t' in l:
            a, b = l.rstrip('\n').split('\t', 1); extra[a] = b
out = []; todo = collections.OrderedDict(); oldall = {s for v in o.values() for s in v}
for k, ss in n.items():
    if skip(*k): continue
    for s in set(ss):
        v = pairs.get((k, s))
        if v is None and s in extra: v = extra[s]
        if v is not None and v != s: out.append('\t'.join([k[0], k[1], s, v]))
        elif v is None and s not in oldall and re.search(r'[A-Za-z]{2}', s) and (' ' in s.strip() or re.match(r'^[A-Z][a-z]+[!.:]?$', s)):
            todo.setdefault(s, k)
open('map.tsv', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
open('todo.tsv', 'w', encoding='utf-8').write('\n'.join(s + '\t' + k[0] + '::' + k[1] for s, k in todo.items()) + '\n')
lost = [(k, a, b) for (k, a), b in pairs.items() if k in n and a not in n[k]]
open('lost.tsv', 'w', encoding='utf-8').write('\n'.join(f'{k[0]}::{k[1]}\t{a}\t{b}' for k, a, b in lost) + '\n')
print('pairs', len(pairs), 'mapped in new', len(out), 'todo', len(todo), 'lost (EN changed in same method)', len(lost))
