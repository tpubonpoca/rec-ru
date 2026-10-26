import subprocess, re, sys
sys.stdout.reconfigure(encoding='utf-8')

out = subprocess.check_output([r'C:\Users\Asyncoder\dotnet\dotnet.exe', 'run', '--project', r'C:\Users\Asyncoder\Downloads\REC_extract\patcher', 'dump', r'C:\Users\Asyncoder\Desktop\REC_v0.5.5.2\data_REC_windows_x86_64\REC.dll'])
orig = subprocess.check_output([r'C:\Users\Asyncoder\dotnet\dotnet.exe', 'run', '--project', r'C:\Users\Asyncoder\Downloads\REC_extract\patcher', 'dump', r'C:\Users\Asyncoder\Downloads\REC_v0.5.5.2\data_REC_windows_x86_64\REC.dll'])

lines_patched = out.decode('utf-8', errors='ignore').splitlines()
lines_orig = orig.decode('utf-8', errors='ignore').splitlines()

ru_re = re.compile(r'[\u0400-\u04FF]')

# For each method, compare instructions
curr_class = ''
curr_method = ''
for i, l in enumerate(lines_patched):
    if l.startswith('CLASS: '):
        curr_class = l.strip()
    elif 'METHOD: ' in l:
        curr_method = l.strip()
    if 'ldstr ' in l and ru_re.search(l):
        # check if this is an API call
        for j in range(i+1, min(i+6, len(lines_patched))):
            target = lines_patched[j]
            if any(k in target for k in ['GetNode', 'GetVariable', 'SetVariable', 'NodePath', 'Play', 'StringName::op_Implicit', 'Dictionary', 'Action']):
                print(f'{curr_class} -> {curr_method}:')
                print(f'   {l.strip()}')
                print(f'   next: {target.strip()}')
                break
