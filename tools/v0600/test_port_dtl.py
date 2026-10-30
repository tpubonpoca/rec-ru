from pathlib import Path
import subprocess
import sys
import tempfile

source = Path(__file__).resolve().parent / 'port_dtl.py'
with tempfile.TemporaryDirectory(prefix='rec-port-') as temp:
    base = Path(temp)
    cwd = base / 'work/v0600'
    old = cwd / 'res_0552_en/dialogue/timelines'
    new = cwd / 'res/dialogue/timelines'
    ru = base / 'repo/translation/dialogue/timelines'
    for path in (old, new, ru):
        path.mkdir(parents=True)
    en = 'label PLAYER\n- Attack #id:7b\n\tDamage {value}\n- Run #id:9a\n- Paparazzi #id:165\n- Back #id:16a\n- Attack training #id:20\n'
    translated = 'label PLAYER\n- Атака #id:7b\n\tУрон {value}\n- Сбежать #id:9a\n- Папарацци #id:165\n- Назад #id:16a\n- Тренировка атак #id:20\n'
    for name in ('adventure_battle.dtl', 'adventure_skills.dtl', 'morning.dtl'):
        (old / name).write_text(en, encoding='utf-8')
        (new / name).write_text(en, encoding='utf-8')
        (ru / name).write_text(translated, encoding='utf-8')
    subprocess.run([sys.executable, '-I', '-X', 'utf8', str(source)], cwd=cwd, check=True, capture_output=True)
    expected = translated.replace('- Атака #', '- Attack #').replace('- Сбежать #', '- Run #').replace('- Папарацци #', '- Paparazzi #').replace('- Назад #', '- Back #')
    failures = []
    for name in ('adventure_battle.dtl', 'adventure_skills.dtl', 'morning.dtl'):
        result = (cwd / 'dtl_ru' / name).read_text(encoding='utf-8')
        if result != (translated if name == 'morning.dtl' else expected):
            failures.append(name)
    print('PORT guard failures=' + str(len(failures)) + ' ' + ', '.join(failures))
    sys.exit(bool(failures))
