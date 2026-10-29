# Строки таблицы перевода для 0.6: keys2.json + ключи разработчика + подсказки и имена, переводимые через TranslationServer
import json, re, sys, glob, os
sys.path.insert(0, os.path.dirname(__file__))
from rsrc import RSRC
sys.path.insert(0, '../build'); from fix_keys_for_build import fix
k2 = json.load(open('../../repo/translation/tables/keys2.json', encoding='utf-8'))['ru']
base = {fix(k): (fix(v) if isinstance(v, str) else v) for k, v in k2.items()}
add = {}
for l in open('tr/table_add.tsv', encoding='utf-8'):
    l = l.rstrip('\n')
    if '\t' in l and not l.startswith('#'):
        a, b = l.split('\t', 1); add[a] = b
hint = dict(re.findall(r'"([^"]+)" => "([^"]+)"', open('../dll_2110/src/Hint.cs', encoding='utf-8').read()))
hint.update({k.lower(): v for k, v in add.items() if k.islower()})
def variants(k):
    return {k, k.lower(), k.capitalize(), k.title(), k.upper()}
rows = dict(base)
for k, v in hint.items():
    for x in variants(k):
        rows.setdefault(x, v)
rows.update(add)
# имена врагов, навыков и предметов из ресурсов 0.6 (Name не трогаем в файлах: это идентификатор)
names = {}
for f in glob.glob('res/.godot/exported/**/*.res', recursive=True):
    try: st = RSRC(open(f, 'rb').read()).strings
    except Exception: continue
    props = {s[4]: s[2] for s in st if s[3].startswith('value')}
    for key in ('Name', 'NameWhileWeakened'):
        n = props.get(key)
        if n and re.search('[A-Za-z]', n):
            ru = rows.get(n) or hint.get(n.lower())
            names[n] = ru
            if ru:
                rows.setdefault(n, ru)
                rows.setdefault(n.lower().replace(' ', '_'), ru)
                rows.setdefault(n.lower(), ru)
missing = sorted(n for n, r in names.items() if not r)
open('table_missing_names.txt', 'w', encoding='utf-8').write('\n'.join(missing) + '\n')
CTX = ['', 'Label', 'Button', 'Checkbox', 'LineEdit', 'LinkButton']
out = []
for k, v in rows.items():
    if not isinstance(v, str): continue
    if re.fullmatch(r'[A-Z][A-Z0-9_]+', k) and '_' in k or k in ('NIGHT', 'LOOP', 'VERSION', 'CHEATS', 'SETTINGS', 'EXIT', 'BACK', 'CONTINUE', 'VISUAL'):
        out += [[k, c, v] for c in CTX]
    else:
        out.append([k, '', v])
for k in ('On', 'At'):
    if k in rows: out.append([k, 'Time', rows[k]])
json.dump(out, open('runner/rows.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('rows', len(out), 'keys', len(rows), 'names missing', len(missing))
