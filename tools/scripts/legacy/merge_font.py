import sys, copy
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

def capheight(f, ch='H'):
    gs = f.getGlyphSet(); pen = BoundsPen(gs)
    try:
        gs[ch].draw(pen)
        if pen.bounds: return pen.bounds[3]
    except Exception: pass
    os2 = f['OS/2']
    return getattr(os2, 'sCapHeight', f['head'].unitsPerEm * 0.7)

def merge(base_path, donor_path, out_path):
    base = TTFont(base_path)
    donor = TTFont(donor_path)
    bmap = base.getBestCmap(); dmap = donor.getBestCmap()
    cb, cd = capheight(base), capheight(donor)
    s = cb / cd
    gsD = donor.getGlyphSet()
    from collections import Counter
    adv = Counter(v[0] for v in base['hmtx'].metrics.values()).most_common(1)[0][0]
    glyf = base['glyf']
    order = list(base.getGlyphOrder())
    added = 0
    for cp, gname in sorted(dmap.items()):
        if not (0x400 <= cp <= 0x4FF): continue
        if cp in bmap: continue
        newname = 'cyr_%04X' % cp
        if newname in order: continue
        pen = TTGlyphPen(None)
        try:
            gsD[gname].draw(TransformPen(pen, (s, 0, 0, s, 0, 0)))
            g = pen.glyph()
        except Exception: continue
        glyphs = glyf.glyphs if hasattr(glyf,'glyphs') else glyf
        glyphs[newname] = g
        base['hmtx'].metrics[newname] = (adv, getattr(g, 'xMin', 0) or 0)
        order.append(newname)
        added += 1
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
    print('added', added, 'scale', round(s,4), '->', out_path)

if __name__ == '__main__':
    merge(sys.argv[1], sys.argv[2], sys.argv[3])