import sys
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from collections import Counter

def top(f, ch):
    gs = f.getGlyphSet(); cm = f.getBestCmap()
    if ord(ch) not in cm: return f['head'].unitsPerEm * 0.7
    rec = DecomposingRecordingPen(gs); gs[cm[ord(ch)]].draw(rec)
    bp = BoundsPen(None); rec.replay(bp)
    return bp.bounds[3] if bp.bounds else f['head'].unitsPerEm * 0.7

def merge(base_path, donor_path, out_path):
    base = TTFont(base_path); donor = TTFont(donor_path)
    bcmap = base.getBestCmap(); dmap = donor.getBestCmap()
    s_cap = top(base,'H') / top(donor,'H')
    s_x = top(base,'x') / top(donor,'x')
    print('cap', round(s_cap,4), 'x', round(s_x,4))
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
        rec = DecomposingRecordingPen(gsD)
        try: gsD[gname].draw(rec)
        except Exception: continue
        bp = BoundsPen(None); rec.replay(bp)
        if not bp.bounds: continue
        x0, y0, x1, y1 = bp.bounds
        dx = (adv - (x1 - x0) * s) / 2.0 - x0 * s
        pen = TTGlyphPen(None)
        try: rec.replay(TransformPen(pen, (s, 0, 0, s, dx, 0)))
        except Exception: continue
        g = pen.glyph()
        try: g.recalcBounds(glyf)
        except Exception: pass
        glyf.glyphs[newname] = g
        base['hmtx'].metrics[newname] = (adv, getattr(g, 'xMin', 0) or 0)
        order.append(newname); added += 1
    base.setGlyphOrder(order)
    try: glyf.glyphOrder = order
    except Exception: pass
    base['maxp'].numGlyphs = len(order)
    for t in base['cmap'].tables:
        if t.isUnicode():
            for cp in range(0x400, 0x500):
                nn = 'cyr_%04X' % cp
                if nn in order: t.cmap[cp] = nn
    base.save(out_path)
    print('added', added, '->', out_path)

if __name__ == '__main__':
    merge(sys.argv[1], sys.argv[2], sys.argv[3])