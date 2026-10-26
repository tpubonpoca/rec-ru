import os, re
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res\dialogue'
m = {'MON.':'ПН.','TUE.':'ВТ.','WED.':'СР.','THU.':'ЧТ.','FRI.':'ПТ.','SAT.':'СБ.','SUN.':'ВС.'}
n = 0
for dp,dn,fn in os.walk(root):
    for f in fn:
        if not f.endswith('.dtl'): continue
        p = os.path.join(dp,f)
        t = open(p, encoding='utf-8').read()
        orig = t
        for k,v in m.items():
            t = t.replace('"%s"' % k, '"%s"' % v)
        if t != orig:
            open(p,'w',encoding='utf-8').write(t); n += 1
print('files changed', n)