import os
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res\dialogue\timelines'
fixes = {}
fixes['class.dtl'] = [('jump sounds/MOVE_OUTDOORS\n', 'jump sounds/MOVE_OUTDOORS_URBAN\n')]
fixes['event_relationship_80.dtl'] = [('jump sounds/VOICE_APOLOGIZE', 'jump sounds/VOICE_SIGH')]
for f, pairs in fixes.items():
    p = os.path.join(root, f)
    t = open(p, encoding='utf-8').read()
    o = t
    for a, b in pairs:
        t = t.replace(a, b)
    if t != o:
        open(p, 'w', encoding='utf-8', newline='').write(t)
        print('fixed', f)
print('done')