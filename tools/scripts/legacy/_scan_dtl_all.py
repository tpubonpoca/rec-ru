import glob, sys, os, re
sys.stdout.reconfigure(encoding="utf-8")

dtl_files = sorted(glob.glob(r"C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res\dialogue\timelines\*.dtl"))

issues = []

for p in dtl_files:
    fname = os.path.basename(p)
    lines = open(p, encoding="utf-8").readlines()
    for idx, raw in enumerate(lines):
        line = raw.rstrip("\r\n")
        l = line.strip()

        # Check choices
        if l.startswith("- Держать"):
            issues.append((fname, idx+1, "choice_hold", line, "- Так же"))
        if l.startswith("- Чат"):
            issues.append((fname, idx+1, "choice_chat", line, "- Поболтать"))
        if l.startswith("- Анализировать удар"):
            issues.append((fname, idx+1, "choice_punch", line, "- Проанализировать пунш"))

        # Check specific bad phrases
        if "убрать себя" in l:
            issues.append((fname, idx+1, "bad_phrase", line, "заправить стояк в трусы"))
        if "Правда?..." in l and "roommate" in fname or "roommate:" in l:
            issues.append((fname, idx+1, "bad_phrase", line, "Ты что... дрочишь?..."))
        if "да. Это я." in l:
            issues.append((fname, idx+1, "bad_phrase", line, "ну да. Как видишь."))
        if "Это так... красное." in l:
            issues.append((fname, idx+1, "bad_phrase", line, "Он такой... красный."))
        if "уже так тяжело, да?" in l:
            issues.append((fname, idx+1, "bad_phrase", line, "уже такой твёрдый, да?"))
        if "мокрый сон" in l:
            issues.append((fname, idx+1, "bad_phrase", line, "ночная поллюция"))

print(f"Total specific issues found: {len(issues)}")
for item in issues:
    print(f"{item[0]}:{item[1]} [{item[2]}]")
    print(f"  OLD: {item[3]}")
    print(f"  SUG: {item[4]}")
