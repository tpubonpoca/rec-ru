# Чтение и пересборка pck Godot 4.7 (формат 3/4, каталог может быть зашифрован AES-256-CFB)
import sys, struct, hashlib, os
from cryptography.hazmat.decrepit.ciphers.modes import CFB
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

PACK_DIR_ENCRYPTED = 1
PACK_REL_FILEBASE = 2
PACK_FILE_ENCRYPTED = 1

def read_pck(path, key=None):
    f = open(path, 'rb')
    h = f.read(0x70)
    assert h[:4] == b'GDPC'
    ver, maj, mi, pa, flags, base, diroff = struct.unpack_from('<IIIIIQQ', h, 4)
    if ver < 3: diroff = 0x60
    f.seek(diroff)
    count = struct.unpack('<I', f.read(4))[0]
    if flags & PACK_DIR_ENCRYPTED:
        md5 = f.read(16); ln = struct.unpack('<Q', f.read(8))[0]; iv = f.read(16)
        enc = f.read((ln + 15) // 16 * 16)
        d = Cipher(algorithms.AES(key), CFB(iv)).decryptor().update(enc)[:ln]
        assert hashlib.md5(d).digest() == md5, 'bad key'
    else:
        d = f.read()
    ents = []; o = 0
    for _ in range(count):
        pl = struct.unpack_from('<I', d, o)[0]; o += 4
        p = d[o:o+pl].rstrip(b'\0').decode(); o += pl
        off, size = struct.unpack_from('<QQ', d, o); o += 16
        md5 = d[o:o+16]; o += 16
        fl = struct.unpack_from('<I', d, o)[0]; o += 4
        ents.append(dict(path=p, off=off + (base if (flags & PACK_REL_FILEBASE or ver < 3) else 0), size=size, md5=md5, flags=fl))
    return dict(ver=ver, engine=(maj, mi, pa), flags=flags, ents=ents, f=f)

def data(pk, e):
    # у зашифрованного файла в каталоге записан размер открытых данных; на диске: md5, длина, iv и блоки по 16 байт
    n = e['size'] if not e['flags'] & PACK_FILE_ENCRYPTED else 40 + (e['size'] + 15) // 16 * 16
    pk['f'].seek(e['off']); return pk['f'].read(n)

def write_pck(pk, out, repl):
    # repl: путь -> bytes (замена или новый файл); каталог пишется без шифрования
    ents = list(pk['ents']); names = {e['path'] for e in ents}
    for p in repl:
        if p not in names: ents.append(dict(path=p, flags=0))
    o = open(out, 'wb')
    maj, mi, pa = pk['engine']
    o.write(b'GDPC' + struct.pack('<IIIIIQQ', pk['ver'], maj, mi, pa, PACK_REL_FILEBASE, 0x70, 0))
    o.write(b'\0' * (0x70 - o.tell()))
    rows = []
    for e in ents:
        b = repl[e['path']] if e['path'] in repl else data(pk, e)
        fl = 0 if e['path'] in repl else e['flags']
        md5 = hashlib.md5(b).digest() if e['path'] in repl else e['md5']
        off = o.tell() - 0x70
        o.write(b); pad = (-o.tell()) % 32; o.write(b'\0' * pad)
        rows.append((e['path'], off, len(b) if not fl & PACK_FILE_ENCRYPTED else e['size'], md5, fl))
    diroff = o.tell()
    o.write(struct.pack('<I', len(rows)))
    for p, off, size, md5, fl in rows:
        pb = p.encode(); pb += b'\0' * ((-len(pb)) % 4)
        o.write(struct.pack('<I', len(pb)) + pb + struct.pack('<QQ', off, size) + md5 + struct.pack('<I', fl))
    o.seek(0x20); o.write(struct.pack('<Q', diroff)); o.close()

if __name__ == '__main__':
    cmd, pck = sys.argv[1], sys.argv[2]
    key = bytes.fromhex(open(sys.argv[3]).read().strip()) if len(sys.argv) > 3 and os.path.isfile(sys.argv[3]) else None
    pk = read_pck(pck, key)
    if cmd == 'list':
        print(pk['ver'], pk['engine'], pk['flags'], len(pk['ents']))
        for e in pk['ents']: print(e['path'], e['size'], e['flags'])
    elif cmd == 'extract':
        dst = sys.argv[4]; bad = 0
        for e in pk['ents']:
            b = data(pk, e)
            if not e['flags'] & PACK_FILE_ENCRYPTED and hashlib.md5(b).digest() != e['md5']: bad += 1
            fp = os.path.join(dst, e['path']); os.makedirs(os.path.dirname(fp), exist_ok=True)
            open(fp, 'wb').write(b)
        print('extracted', len(pk['ents']), 'md5 bad', bad)
