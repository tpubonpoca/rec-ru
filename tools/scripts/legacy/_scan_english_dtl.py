import glob, sys, os, re
sys.stdout.reconfigure(encoding="utf-8")

dtl_files = sorted(glob.glob(r"C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res\dialogue\timelines\*.dtl"))

english_lines = []

for p in dtl_files:
    fname = os.path.basename(p)
    lines = open(p, encoding="utf-8").readlines()
    for idx, raw in enumerate(lines):
        line = raw.strip()
        # ignore pure godot/dialogic commands
        if not line: continue
        if line.startswith(("[", "set ", "jump ", "label ", "update ", "join ", "leave ", "if ", "elif ", "else:", "return")):
            # but check if there is English text inside [color=...] or [text_input text="..."]
            m_col = re.search(r'\[color=[^\]]+\](.*?)\[/color\]', line)
            if m_col:
                text_part = m_col.group(1)
                # check if english letters > 3
                if re.search(r'[A-Za-z]{4,}', text_part) and not any(k in text_part for k in ["GameVariables", "Items", "Cutscenes", "BattleVariables"]):
                    english_lines.append((fname, idx+1, "color_tag", line))
            continue
        if line.startswith("//"):
            continue

        # Check speaker lines or narration lines
        # Remove tags and variables
        clean = re.sub(r'\{[^\}]+\}', '', line)
        clean = re.sub(r'\[[^\]]+\]', '', clean)
        clean = re.sub(r'#id:[0-9a-f]+', '', clean).strip()
        if re.search(r'[a-zA-Z]{4,}', clean):
            # check if it's speaker name prefix like "roommate:"
            if ":" in clean:
                spk, rest = clean.split(":", 1)
                if not re.search(r'[a-zA-Z]{4,}', rest):
                    continue
            english_lines.append((fname, idx+1, "dialogue", line))

print(f"Total English occurrences in dtl: {len(english_lines)}")
for item in english_lines:
    print(f"{item[0]}:{item[1]} [{item[2]}] -> {item[3]}")
