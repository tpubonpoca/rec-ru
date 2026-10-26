import os, sys
sys.stdout.reconfigure(encoding="utf-8")
root = r"C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res\dialogue\timelines"

fixes = [
    ("adventure_checkpoint_level_1.dtl", "Ты получил особый навык: ", "Ты получил особый навык\\: "),
    ("adventure_checkpoint_level_3.dtl", "гласит: ", "гласит\\: "),
    ("class.dtl", "И самое главное: #id:188", "И самое главное\\: #id:188"),
    ("class.dtl", "из учебника: #id:cec", "из учебника\\: #id:cec"),
    ("event_rent.dtl", "Ты получил особый навык: ", "Ты получил особый навык\\: "),
    ("event_rent.dtl", "Ты потерял особый навык: ", "Ты потерял особый навык\\: "),
    ("event_rewind.dtl", "И главное:[/color]", "И главное\\:[/color]"),
    ("event_rewind_final.dtl", "(Примечание: ", "(Примечание\\: "),
    ("night_yosuke.dtl", "Так скажи мне: ", "Так скажи мне\\: "),
    ("night_yosuke.dtl", "Ты получил особый навык: [color=e5be3e]Метаболизатор[/color]!", "Ты получил особый навык\\: [color=e5be3e]Метаболизатор[/color]!"),
    ("night_yosuke.dtl", "Ты получил особый навык: [color=e5be3e]Опасность: незнакомец[/color]!", "Ты получил особый навык\\: [color=e5be3e]Опасность\\: незнакомец[/color]!"),
    ("party_ending.dtl", "Ты получил особый навык: ", "Ты получил особый навык\\: "),
    ("party_ending.dtl", "не по важности: #id:908", "не по важности\\: #id:908"),
    ("party_event_evening_strip_games.dtl", "значит, правила: #id:776", "значит, правила\\: #id:776"),
    ("party_intro.dtl", "три основных качества: #id:874", "три основных качества\\: #id:874"),
    ("party_intro.dtl", "Итак, подытожим: #id:87a", "Итак, подытожим\\: #id:87a"),
]

for fname, old, new in fixes:
    p = os.path.join(root, fname)
    raw = open(p, "rb").read()
    txt = raw.decode("utf-8").replace("\r\n", "\n")
    if old in txt:
        txt = txt.replace(old, new)
        open(p, "w", encoding="utf-8", newline="\n").write(txt)
        print(f"Fixed colon in {fname}: {repr(old)}")
    else:
        print(f"NOT FOUND in {fname}: {repr(old)}")
