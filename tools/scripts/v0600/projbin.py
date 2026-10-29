# Чтение/запись project.binary (ECFG): ключ -> закодированный Variant
import struct, sys
def read(path):
    d = open(path, 'rb').read(); assert d[:4] == b'ECFG'
    n = struct.unpack_from('<I', d, 4)[0]; o = 8; out = []
    for _ in range(n):
        kl = struct.unpack_from('<I', d, o)[0]; o += 4; k = d[o:o+kl].decode(); o += kl
        vl = struct.unpack_from('<I', d, o)[0]; o += 4; v = d[o:o+vl]; o += vl
        out.append((k, v))
    return out
def write(path, items):
    b = bytearray(b'ECFG' + struct.pack('<I', len(items)))
    for k, v in items:
        kb = k.encode(); b += struct.pack('<I', len(kb)) + kb + struct.pack('<I', len(v)) + v
    open(path, 'wb').write(b)
def vstr(s):
    sb = s.encode(); return struct.pack('<II', 4, len(sb)) + sb + b'\0' * ((-len(sb)) % 4)
if __name__ == '__main__':
    for k, v in read(sys.argv[1]):
        t = struct.unpack_from('<I', v)[0]
        print(k, t, v[8:8+struct.unpack_from('<I', v, 4)[0]].decode('utf-8', 'replace') if (t & 0xff) == 4 else v[:40].hex())
