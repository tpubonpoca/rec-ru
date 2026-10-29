# tr/*.tsv (EN<TAB>RU, \n как перевод строки) -> json-словари для port_dtl.py и port_res.py
import json
NL = chr(92) + 'n'
for src, dst in [('tr/dtl_new.tsv', 'dtl_new_ru.json'), ('tr/res_new.tsv', 'res_new_ru.json')]:
    d = {}
    for l in open(src, encoding='utf-8'):
        l = l.rstrip('\n')
        if '\t' in l:
            a, b = l.split('\t', 1)
            d[a.replace(NL, '\n')] = b.replace(NL, '\n')
    json.dump(d, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(dst, len(d))
