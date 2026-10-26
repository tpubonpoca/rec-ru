import json, sys, os, struct, re
sys.path.insert(0, r'C:\Users\Asyncoder\Downloads\REC_extract')
from rsrc import RSRC
# read final pck
p = r'C:\Users\Asyncoder\Downloads\NOT FOR local local DONT TOUCH\REC.pck'
f = open(p,'rb'); h = f.read(100)
cnt = struct.unpack_from('<I', h, 96)[0]; fb = struct.unpack_from('<Q', h, 24)[0]
pos = 100; ent = {}
for i in range(cnt):
    f.seek(pos); sl = struct.unpack('<I', f.read(4))[0]
    name = f.read(sl).split(b'\x00')[0].decode(); ofs, size = struct.unpack('<QQ', f.read(16)); f.read(20)
    ent[name] = (ofs,size); pos += 4 + sl + 36
dll = open(r'C:\Users\Asyncoder\Downloads\NOT FOR local local DONT TOUCH\data_REC_windows_x86_64\REC.dll','rb').read()
checks = ['sleepover','thermostat_unlock','decoration_sweater','peace_of_mind','freeze_frame']
for k in checks:
    nm = [x for x in ent if k in x][0]
    o,s = ent[nm]; f.seek(fb+o); r = RSRC(f.read(s))
    names = [v for (lp,ln,v,kk,prop) in r.strings if kk=='value' and prop=='Name']
    desc = [v for (lp,ln,v,kk,prop) in r.strings if kk=='value' and prop=='Description']
    print(k, '=>', [repr(x) for x in names], '| dll has:', [dll.count(x.encode('utf-16-le')) for x in names])
    if desc: print('    desc:', desc[0][:60])