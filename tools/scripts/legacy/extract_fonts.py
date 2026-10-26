import sys, os, struct
sys.path.insert(0, r'C:\Users\Asyncoder\Downloads\REC_extract')
import rsrc
# patch parser to record byte arrays
orig = rsrc.RSRC.parse_variant
def patched(self, depth=0):
    t = self.u32()
    if t == 31:
        ln = self.u32(); start = self.p; self.skip(ln); self.pad(ln)
        self.blobs.append((start, ln))
        return
    self.p -= 4
    return orig(self, depth)
rsrc.RSRC.parse_variant = patched
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res\.godot\imported'
out = r'C:\Users\Asyncoder\Downloads\REC_extract\fonts'
os.makedirs(out, exist_ok=True)
for f in os.listdir(root):
    if not f.endswith('.fontdata'): continue
    d = open(os.path.join(root,f),'rb').read()
    r = rsrc.RSRC.__new__(rsrc.RSRC)
    r.d = d; r.p = 0; r.strings = []; r.int_res = []; r.cur_prop = None; r.blobs = []
    try: r.parse()
    except Exception as e:
        print('parse issue', f, e)
    best = max(r.blobs, key=lambda b: b[1]) if r.blobs else None
    if not best: print('no blob', f); continue
    start, ln = best
    data = d[start:start+ln]
    name = f.split('.ttf')[0].split('.otf')[0].replace(' ', '_')
    p = os.path.join(out, name + '.ttf')
    open(p,'wb').write(data)
    print(name, ln, data[:4].hex())