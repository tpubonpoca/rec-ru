import struct, json, os
from rsrc import RSRC
_W = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'words.json'), encoding='utf-8'))
WORDS = _W['map']

SAFE_PROPS = set('''
text tooltip_text title placeholder label message text_label name_label
Name Description YunaComment PowerUpDescription ActionName Subject Instructions IngredientList
Question Answer1 Answer2 Answer3 Answer4 CorrectAnswer WrongAnswer1 WrongAnswer2 WrongAnswer3
Explanation1 Explanation2 Explanation3 Explanation4 Explanation5 Explanation6
NameWhileWeakened WeakenedText IntroText AttackText Attack1 Attack2 Attack3
Charm1 CharmFail CharmSuccessful CharmAttemptText
Fear1 Fear2 FearFail FearSuccessful FearAttemptText
Enrage1 EnrageFail EnrageSuccessful EnrageAttemptText
StunDialogue BrickDialogue UsageQuote PrepQuote PaparazziResponse GalleryTitle display_name
'''.split())

def rewrite_bytes(data, mapping, safe_only=True, path=''):
    r = RSRC(data)
    if not path and r.int_res:
        path = r.int_res[0][0]
    edits = []
    for (lp, ln, val, kind, prop) in r.strings:
        if kind != 'value':
            continue
        if safe_only:
            if prop == 'names':
                continue
            if prop == 'variants':
                if os.environ.get('SKIP_VARIANTS') == '1' and not val.strip().endswith(':'):
                    continue
                if ' ' not in val:
                    if val not in WORDS:
                        continue
                elif len(val) <= 3:
                    continue
            elif prop not in SAFE_PROPS:
                continue
        import os as _os
        if prop in _os.environ.get('EXCL_PROPS', '').split(','):
            continue
        nf = _os.environ.get('NAME_FOLDERS', '')
        if prop == 'Name' and nf and not any(x in path for x in nf.split(',')):
            continue
        if val in mapping:
            new = mapping[val]
            if not isinstance(new, str): continue
            payload = new.encode('utf-8') + b'\x00'
            edits.append((lp, lp + 4 + ln, struct.pack('<I', len(payload)) + payload))
    if not edits: return data, 0
    edits.sort()
    out = bytearray()
    last = 0
    for (s, e, nb) in edits:
        if s < last: continue
        out += data[last:s]
        out += nb
        last = e
    out += data[last:]
    def shift(old):
        d = 0
        for (s, e, nb) in edits:
            if s >= old: break
            d += len(nb) - (e - s)
        return old + d
    for (path, ofs, pos) in r.int_res:
        struct.pack_into('<Q', out, pos, shift(ofs))
    if r.importmd_ofs:
        struct.pack_into('<Q', out, r.importmd_ofs_pos, shift(r.importmd_ofs))
    return bytes(out), len(edits)