# Перенос перевода в бинарные ресурсы 0.6: замена строк по карте EN->RU, отчёт о новых строках
import sys, os, json, struct, glob, re
sys.path.insert(0, os.path.dirname(__file__))
from rsrc import RSRC

def rewrite(data, fn):
    r = RSRC(data); edits = []
    for (lp, ln, val, kind, prop) in r.strings:
        if not kind.startswith('value'): continue
        new = fn(val, prop)
        if new is None or new == val: continue
        payload = new.encode('utf-8') + b'\x00'
        edits.append((lp, lp + 4 + ln, struct.pack('<I', len(payload)) + payload))
    if not edits: return data, 0
    edits.sort(); out = bytearray(); last = 0
    for s, e, nb in edits:
        out += data[last:s] + nb; last = e
    out += data[last:]
    def shift(old):
        d = 0
        for s, e, nb in edits:
            if s >= old: break
            d += len(nb) - (e - s)
        return old + d
    for (path, ofs, pos) in r.int_res: struct.pack_into('<Q', out, shift(pos), shift(ofs))
    if r.importmd_ofs: struct.pack_into('<Q', out, shift(r.importmd_ofs_pos), shift(r.importmd_ofs))
    RSRC(bytes(out))
    return bytes(out), len(edits)

if __name__ == '__main__':
    pairs = json.load(open('res_pairs.json', encoding='utf-8'))
    extra = json.load(open('res_new_ru.json', encoding='utf-8')) if os.path.exists('res_new_ru.json') else {}
    m = {(p, e): r for _, p, e, r in pairs}
    props = {p for _, p, _, _ in pairs}
    props0 = {p for _, p, _, _ in pairs} - {'variants', 'values'}
    for e, r in extra.items():
        for p in props0: m[(p, e)] = r
    # строки, существовавшие в 0.5.5.2 и оставленные без перевода
    old = set()
    for f in glob.glob('res_0552_ru/.godot/exported/**/*.*', recursive=True):
        try: old.update(s[2] for s in RSRC(open(f, 'rb').read()).strings if s[3].startswith('value'))
        except Exception: pass
    import shutil; shutil.rmtree('res_ru', ignore_errors=True)
    out = 'res_ru'; todo = {}; n = 0
    for f in glob.glob('res/.godot/exported/**/*.*', recursive=True):
        d = open(f, 'rb').read()
        if d[:4] != b'RSRC': continue
        rel = os.path.relpath(f, 'res').replace(os.sep, '/')
        def fn(v, p):
            if (p, v) in m: return m[(p, v)]
            if p in props and v not in old and re.search('[A-Za-z]{2}', v) and not re.fullmatch(r'[\w./:-]+\.(png|ogg|mp3|tscn|tres|gd|wav)', v):
                todo.setdefault(v, []).append((rel.rsplit('-', 1)[-1], p))
            return None
        nd, k = rewrite(d, fn)
        if k:
            fp = os.path.join(out, rel); os.makedirs(os.path.dirname(fp), exist_ok=True); open(fp, 'wb').write(nd); n += 1
    json.dump(todo, open('res_todo_left.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('rewritten files', n, 'todo strings', len(todo))
