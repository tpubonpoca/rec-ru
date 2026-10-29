# Сборка REC.pck 0.6 с переводом: все записи исходного пака + замены
import sys, os, glob, struct
sys.path.insert(0, os.path.dirname(__file__))
import pck4, projbin
key = bytes.fromhex(open('key.hex').read().strip())
pk = pck4.read_pck('zip/REC.pck', key)
names = {e['path'] for e in pk['ents']}
repl = {}
def put(path, data):
    repl[path] = data
for f in glob.glob('dtl_ru/*.dtl'):
    put('dialogue/timelines/' + os.path.basename(f), open(f, 'rb').read())
for f in glob.glob('dch_ru/*.dch'):
    put('dialogue/characters/' + os.path.basename(f), open(f, 'rb').read())
for f in [x for x in glob.glob('res_ru/**/*', recursive=True, include_hidden=True) if os.path.isfile(x)]:
    put(os.path.relpath(f, 'res_ru').replace(os.sep, '/'), open(f, 'rb').read())
for name in ('comments', 'comments_special'):
    if os.path.exists('tr/%s_ru.txt' % name):
        put('resources/comments/%s.txt' % name, open('tr/%s_ru.txt' % name, 'rb').read())
for loc in ('ru', 'en'):
    put('translations/rec_translations.%s.translation' % loc, open('tables/rec_translations.%s.translation' % loc, 'rb').read())
FONTS = {'Toriko.ttf': 'Toriko.ttf-9d8a733741cf0a7e03818cd52a1c990b.fontdata', 'VCR_OSD_Mono.ttf': 'VCR_OSD_Mono.ttf-45fb8313e03f845b2bc3e59d42d2d129.fontdata'}
for font, old in FONTS.items():
    new = [p for p in names if p.startswith('.godot/imported/' + font + '-') and p.endswith('.fontdata')]
    assert len(new) == 1, new
    put(new[0], open('res_0552_ru/.godot/imported/' + old, 'rb').read())
items = projbin.read('res/project.binary')
items = [i for i in items if i[0] != 'autoload/ZFix'] + [('autoload/ZFix', projbin.vstr('*res://label_fix.gd'))]
projbin.write('build_project.binary', items)
put('project.binary', open('build_project.binary', 'rb').read())
put('label_fix.gd', open('fix/label_fix.gd', 'rb').read())
unknown = [p for p in repl if p not in names and p != 'label_fix.gd']
assert not unknown, unknown[:5]
os.makedirs('build', exist_ok=True)
pck4.write_pck(pk, 'build/REC.pck', repl)
print('replaced', len(repl), 'size', os.path.getsize('build/REC.pck'))
