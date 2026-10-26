import os, re
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res\dialogue\characters'
names = {
  'Alice': 'Элис', 'Camera': 'Камера', 'chest': 'сундук', 'crowd': 'толпа',
  'item': 'предмет', 'Kaede': 'Каэда', 'Kan': 'Кан', 'Dog': 'Пёс', 'Yuna': 'Юна', 'scene': 'сцена'
}
n=0
for f in sorted(os.listdir(root)):
    if not f.endswith('.dch'): continue
    p = os.path.join(root,f)
    t = open(p, encoding='utf-8').read()
    def repl(m):
        global n
        v = m.group(1)
        if v in names:
            n += 1
            return '"display_name": "' + names[v] + '"'
        return m.group(0)
    t2 = re.sub(r'"display_name":\s*"([^"]*)"', repl, t)
    if t2 != t: open(p,'w',encoding='utf-8').write(t2)
print('names translated', n)