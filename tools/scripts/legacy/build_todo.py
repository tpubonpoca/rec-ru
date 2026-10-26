import json, os, re, collections
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res'
EXCLUDE_PROPS = {'_bundled','animations','overrides','_data','data','name','resource_name','bus/8/name','bus/3/name','bus/6/name','bus/5/name','bus/7/name','bus/4/name','bus/8/send','bus/7/send','bus/6/send','bus/5/send','bus/4/send','metadata/_latest_layer','metadata/timeline_not_saved','LineEditWithIcon/base_type','node_count','nodes','conn_count','conns','node_paths','editable_instances','version'}
def bad_prop(p):
    if p is None: return True
    if p in EXCLUDE_PROPS: return True
    if p.startswith('tracks/') or p.startswith('metadata/') or p.startswith('bus/'): return True
    return False
rows = json.load(open(r'C:\Users\Asyncoder\Downloads\REC_extract\scene_strings.json', encoding='utf-8'))
def proseish(v):
    if '://' in v: return False
    if not re.search(r'[A-Za-z]', v): return False
    return (' ' in v.strip()) or (v[:1].isupper() and len(v) > 3) or v.endswith('!') or v.endswith('?') or v.endswith(':')
scene = {}
for r in rows:
    if bad_prop(r['prop']): continue
    v = r['val']
    if not proseish(v): continue
    if re.fullmatch(r'[A-Za-z0-9_./ -]+', v) and ' ' not in v and not v[0].isupper(): continue
    scene[v] = scene.get(v,0)+1
# dialogue
dial = {}
for dp,dn,fn in os.walk(os.path.join(root,'dialogue')):
    for f in sorted(fn):
        if not f.endswith('.dtl'): continue
        for line in open(os.path.join(dp,f), encoding='utf-8', errors='replace'):
            s = line.rstrip('\n')
            st = s.strip()
            if not st: continue
            if st[0] in '[{': continue
            if re.match(r'^(if|elif|else|set|jump|label|goto|end|return|var|call|do|while|for|match|break|continue|signal|emit|await)\b', st): continue
            body = st
            if body.startswith('- '): body = body[2:].strip()
            body = re.sub(r'\s*#id:[0-9a-fA-F]+$', '', body).strip()
            m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$', body)
            if m: body = m.group(2).strip()
            if not body: continue
            if not re.search(r'[A-Za-z]', body): continue
            if body.startswith('#'): continue
            dial[body] = dial.get(body,0)+1
txt = {}
for dp,dn,fn in os.walk(os.path.join(root,'resources')):
    for f in fn:
        if f.endswith('.txt'):
            p = os.path.join(dp,f)
            for line in open(p, encoding='utf-8', errors='replace'):
                line=line.rstrip('\n')
                if line.strip(): txt[line]=txt.get(line,0)+1
dch = {}
for dp,dn,fn in os.walk(os.path.join(root,'dialogue')):
    for f in fn:
        if f.endswith('.dch'):
            try: j=json.load(open(os.path.join(dp,f), encoding='utf-8'))
            except Exception: continue
            def walk(o):
                if isinstance(o, dict):
                    for k,v in o.items():
                        if k in ('name','nickname','description','display_name') and isinstance(v,str) and v.strip(): dch[v]=dch.get(v,0)+1
                        walk(v)
                elif isinstance(o, list):
                    for x in o: walk(x)
            walk(j)
print('scene uniq', len(scene), 'chars', sum(len(k) for k in scene))
print('dialogue uniq', len(dial), 'chars', sum(len(k) for k in dial))
print('txt uniq', len(txt), 'chars', sum(len(k) for k in txt))
print('dch uniq', len(dch), 'chars', sum(len(k) for k in dch))
allv = list(scene.keys()) + list(dial.keys())
dup = len(set(allv))
print('combined unique', dup, 'chars', sum(len(k) for k in set(allv)))
json.dump({'scene':sorted(scene), 'dialogue':sorted(dial), 'txt':sorted(txt), 'dch':sorted(dch)}, open(r'C:\Users\Asyncoder\Downloads\REC_extract\todo.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)