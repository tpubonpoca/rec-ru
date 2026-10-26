import sys
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from collections import Counter

def top(f, ch):
    gs = f.getGlyphSet(); pen = BoundsPen(gs)
    try:
        gs[ch].draw(pen)
        if pen.bounds: return pen.bounds[3]
    except Exception: pass
    return f['head'].unitsPerEm * 0.7

def merge(base_path, donor_path, out_path):
    base = TTFont(base_path); donor = TTFont(donor_path)
    bcmap = base.getBestCmap(); dmap = donor.getBestCmap()
    bH, dH = top(base,'H'), top(donor,'H')
    bx = top(base,'x') if 'x' in bcmap else bH*0.7
    dxh = top(donor,'x') if 'x' in dmap else dH*0.7
    s_cap, s_x = bH/dH, bx/dxh
    print('cap scale', round(s_cap,4), 'x scale', round(s_x,4))
    gsD = donor.getGlyphSet()
    adv = Counter(v[0] for v in base['hmtx'].metrics.values()).most_common(1)[0][0]
    glyf = base['glyf']
    order = list(base.getGlyphOrder())
    added = 0
    for cp, gname in sorted(dmap.items()):
        if not (0x400 <= cp <= 0x4FF): continue
        if cp in bcmap: continue
        newname = 'cyr_%04X' % cp
        if newname in order or gname not in gsD: continue
        s = s_x if chr(cp).islower() else s_cap
        pen = BoundsPen(gsD)
        try:
            gsD[gname].draw(pen)
        except Exception:
            continue
        if pen.bounds is None: continue
        x0, y0, x1, y1 = pen.bounds
        w = (x1 - x0) * s
        dx = (adv - w) / 2.0 - x0 * s
        tpen = TTGlyphPen(None)
        try:
            gsD[gname].draw(TransformPen(tpen, (s, 0, 0, s, dx, 0)))
            g = tpen.glyph()
        except Exception: continue
        glyf.glyphs[newname] = g
        base['hmtx'].metrics[newname] = (adv, getattr(g, 'xMin', 0) or 0)
        order.append(newname); added += 1
    base.setGlyphOrder(order)
    try: glyf.glyphOrder = order
    except Exception: pass
    base['maxp'].numGlyphs = len(order)
    for table in base['cmap'].tables:
        if table.isUnicode():
            for cp in range(0x400, 0x500):
                nn = 'cyr_%04X' % cp
                if nn in order: table.cmap[cp] = nn
    base.save(out_path)
    print('added', added, '->', out_path)

if __name__ == '__main__':
    merge(sys.argv[1], sys.argv[2], sys.argv[3])