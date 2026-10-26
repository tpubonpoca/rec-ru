import json, os, re, sys
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
tm = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\tm.json', encoding='utf-8'))
CMD = re.compile(r'^(if|elif|else|set|jump|label|goto|end|return|var|call|do|while|for|match|break|continue|signal|emit|await|join|leave|update|show|hide|background|music|sound|voice|portrait|style)\b')
ID = re.compile(r'\s*#id:([0-9a-fA-F]+)\s*$')
SPK = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*):\s*')
changed = 0; total = 0; missed = []
def tr_line(raw):
    global changed
    if raw.strip() == '' : return raw
    stripped = raw.strip()
    if stripped.startswith('//') or stripped.startswith('#'): return raw
    if stripped.startswith('[') or stripped.startswith('{'): return raw
    if CMD.match(stripped): return raw
    lead = raw[:len(raw) - len(raw.lstrip())]
    body = stripped
    choice = ''
    if body.startswith('- '):
        choice = '- '; body = body[2:]
    ident = ''
    m = ID.search(body)
    if m:
        ident = ' #id:' + m.group(1)
        body = body[:m.start()].rstrip()
    spk = ''
    m = SPK.match(body)
    if m:
        spk = m.group(1) + ': '
        body = body[m.end():]
    if body in tm:
        changed += 1
        body = tm[body]
    elif body and re.search(r'[A-Za-z]{3}', body) and len(body) > 8:
        missed.append(body)
    return lead + choice + spk + body + ident
nfiles = 0
for dp, dn, fn in os.walk(os.path.join(root, 'dialogue')):
    for f in fn:
        if not f.endswith('.dtl'): continue
        p = os.path.join(dp, f)
        lines = open(p, encoding='utf-8').read().split('\n')
        out = [tr_line(l) for l in lines]
        open(p, 'w', encoding='utf-8').write('\n'.join(out))
        nfiles += 1
print('dtl files', nfiles, 'lines translated', changed)
open(r'C:\Users\Asyncoder\Downloads\REC_extract\missed_dtl.txt','w',encoding='utf-8').write('\n'.join(sorted(set(missed))))
print('untranslated lines', len(set(missed)))