import os, re, json
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res\dialogue\timelines'
cmd_re = re.compile(r'^\s*(\[|#|\- |if |elif |else:|set |jump |label |goto |end|return|var |join |leave |update |do |wait )')
leftover = []
total_text = 0
for f in sorted(os.listdir(root)):
    if not f.endswith('.dtl'): continue
    for i, line in enumerate(open(os.path.join(root,f), encoding='utf-8'), 1):
        s = line.strip()
        if not s or cmd_re.match(line): continue
        body = re.sub(r'#[a-z0-9]{3,}\s*$', '', s).strip()
        if not body: continue
        total_text += 1
        lat = re.findall(r'[A-Za-z]{3,}', body)
        cyr = re.search(r'[А-Яа-я]', body)
        if lat and not cyr:
            leftover.append((f, i, body[:90]))
        elif not cyr and len(lat) >= 2:
            leftover.append((f, i, body[:90]))
print('text lines', total_text, 'leftover english', len(leftover))
for x in leftover[:30]: print(x[0], x[1], x[2])