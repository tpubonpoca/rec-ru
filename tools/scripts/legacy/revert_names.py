import os, sys, struct, json
sys.path.insert(0, r'C:\Users\Asyncoder\Downloads\REC_extract')
from rsrc import RSRC
tm = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\tm.json', encoding='utf-8'))
rev = {}
for k, v in tm.items():
    if isinstance(v, str) and v not in rev: rev[v] = k
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
changed = 0; n = 0
for dp, dn, fn in os.walk(root):
    if '.packer' in dp: continue
    for f in fn:
        if not f.endswith('.res'): continue
        p = os.path.join(dp, f)
        try: d = open(p,'rb').read(); r = RSRC(d)
        except Exception: continue
        edits = []
        for (lp, ln, val, kind, prop) in r.strings:
            if kind != 'value' or prop != 'Name': continue
            if val in rev:
                payload = rev[val].encode('utf-8') + b'\x00'
                edits.append((lp, lp + 4 + ln, struct.pack('<I', len(payload)) + payload))
        if not edits: continue
        edits.sort(); out = bytearray(); last = 0
        for (s,e,nb) in edits:
            if s < last: continue
            out += d[last:s]; out += nb; last = e
        out += d[last:]
        def shift(old):
            dd = 0
            for (s,e,nb) in edits:
                if s >= old: break
                dd += len(nb) - (e - s)
            return old + dd
        for (ipath, ofs, pos) in r.int_res: struct.pack_into('<Q', out, pos, shift(ofs))
        if r.importmd_ofs: struct.pack_into('<Q', out, r.importmd_ofs_pos, shift(r.importmd_ofs))
        open(p,'wb').write(bytes(out)); changed += 1; n += len(edits)
print('restored resources', changed, 'names', n)