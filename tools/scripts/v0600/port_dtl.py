# Перенос русских таймлайнов на 0.6: diff старого и нового EN, совпадающие строки берём из RU
import os, re, sys, difflib, json, collections
OLD_EN = 'res_0552_en/dialogue/timelines'; RU = '../../repo/translation/dialogue/timelines'
NEW_EN = 'res/dialogue/timelines'; OUT = 'dtl_ru'; os.makedirs(OUT, exist_ok=True)
STRUCT = re.compile(r'^\s*(audio |label |jump |return|set |if |elif |else|join |leave |update |do |\[(?!text_input)[a-z_]+[ \]]|\[/|#|$)')
# названия предметов и рецептов в репликах приходят из ресурсов на английском: переводим через tr() в выражении Dialogic
NAMEVAR = re.compile(r'\{((?:GameVariables|Items|BattleVariables)[^{}]*\.Name|BattleVariables\.get_item_reward\(\)|GameVariables\.recipe_name)\}')
def wrap_names(line):
    s = line.strip()
    if re.match(r'(if|elif|set|jump|label|join|update|leave|do|audio) ', s): return line
    head, sep, tail = line.partition(' | [if ')
    return NAMEVAR.sub(lambda m: '{tr(' + m.group(1) + ')}', head) + sep + tail
def L(p): return open(p, encoding='utf-8').read().split('\n')
glob_map = collections.defaultdict(collections.Counter)
for n in os.listdir(OLD_EN):
    if n.endswith('.dtl') and os.path.exists(os.path.join(RU, n)):
        for e, r in zip(L(os.path.join(OLD_EN, n)), L(os.path.join(RU, n))): glob_map[e][r] += 1
extra = json.load(open('dtl_new_ru.json', encoding='utf-8')) if os.path.exists('dtl_new_ru.json') else {}
todo = []; stat = collections.Counter()
for n in sorted(os.listdir(NEW_EN)):
    if not n.endswith('.dtl'): continue
    new = L(os.path.join(NEW_EN, n))
    if os.path.exists(os.path.join(OLD_EN, n)):
        oe, ru = L(os.path.join(OLD_EN, n)), L(os.path.join(RU, n))
    else: oe, ru = [], []
    out = []
    sm = difflib.SequenceMatcher(None, oe, new, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal': out += ru[i1:i2]; stat['eq'] += i2 - i1; continue
        for j in range(j1, j2):
            ln = new[j]; key = n + ':' + str(j + 1)
            ind = ln[:len(ln) - len(ln.lstrip())]
            if ln.strip() in extra: out.append(ind + extra[ln.strip()]); stat['extra'] += 1
            elif ln in glob_map: out.append(glob_map[ln].most_common(1)[0][0]); stat['moved'] += 1
            elif STRUCT.match(ln) and not re.search(r'text="|placeholder="|\[text_input', ln): out.append(ln); stat['struct'] += 1
            else: out.append(ln); todo.append((n, j + 1, ln)); stat['todo'] += 1
    out = [wrap_names(x) for x in out]
    open(os.path.join(OUT, n), 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
json.dump(todo, open('dtl_todo.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(stat)
