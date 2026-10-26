import struct, sys, json, os

V_NIL=1; V_BOOL=2; V_INT=3; V_FLOAT=4; V_STRING=5
V_VECTOR2=10; V_RECT2=11; V_VECTOR3=12; V_PLANE=13; V_QUATERNION=14; V_AABB=15; V_BASIS=16
V_TRANSFORM3D=17; V_TRANSFORM2D=18; V_COLOR=20; V_NODE_PATH=22; V_RID=23; V_OBJECT=24
V_INPUT_EVENT=25; V_DICTIONARY=26; V_ARRAY=30; V_PACKED_BYTE_ARRAY=31
V_PACKED_INT32_ARRAY=32; V_PACKED_FLOAT32_ARRAY=33; V_PACKED_STRING_ARRAY=34; V_PACKED_VECTOR3_ARRAY=35
V_PACKED_COLOR_ARRAY=36; V_PACKED_VECTOR2_ARRAY=37; V_INT64=40; V_DOUBLE=41; V_CALLABLE=42; V_SIGNAL=43
V_STRING_NAME=44; V_VECTOR2I=45; V_RECT2I=46; V_VECTOR3I=47; V_PACKED_INT64_ARRAY=48
V_PACKED_FLOAT64_ARRAY=49; V_VECTOR4=50; V_VECTOR4I=51; V_PROJECTION=52; V_PACKED_VECTOR4_ARRAY=53
OBJ_EMPTY=0; OBJ_EXT=1; OBJ_INT=2; OBJ_EXT_INDEX=3
F_NAMED_IDS=1; F_UIDS=2; F_REAL_DOUBLE=4; F_SCRIPT_CLASS=8
RESERVED_FIELDS=11

class Fault(Exception): pass

class RSRC:
    def __init__(self, data):
        self.d = data
        self.p = 0
        self.strings = []
        self.int_res = []
        self.cur_prop = None
        self.parse()

    def u32(self):
        v = struct.unpack_from('<I', self.d, self.p)[0]; self.p += 4; return v
    def u16(self):
        v = struct.unpack_from('<H', self.d, self.p)[0]; self.p += 2; return v
    def u64(self):
        v = struct.unpack_from('<Q', self.d, self.p)[0]; self.p += 8; return v
    def real(self):
        if self.real64:
            v = struct.unpack_from('<d', self.d, self.p)[0]; self.p += 8
        else:
            v = struct.unpack_from('<f', self.d, self.p)[0]; self.p += 4
        return v
    def skip(self, n):
        self.p += n
        if self.p > len(self.d): raise Fault('eof')
    def pad(self, n):
        extra = 4 - (n % 4)
        if extra < 4: self.skip(extra)

    def ustring(self, kind='name'):
        lp = self.p
        ln = self.u32()
        if ln > len(self.d): raise Fault('bad strlen')
        raw = self.d[self.p:self.p+ln]; self.p += ln
        if self.p > len(self.d): raise Fault('eof str')
        txt = raw.split(b'\x00', 1)[0].decode('utf-8', 'replace')
        self.strings.append((lp, ln, txt, kind, self.cur_prop))
        return txt

    def get_string_idx(self):
        sid = self.u32()
        if sid & 0x80000000:
            ln = sid & 0x7FFFFFFF
            raw = self.d[self.p:self.p+ln]; self.p += ln
            return raw.split(b'\x00',1)[0].decode('utf-8','replace')
        if sid >= len(self.string_map): raise Fault('bad string idx')
        return self.string_map[sid]

    def parse(self):
        d = self.d
        if d[:4] != b'RSRC': raise Fault('not RSRC')
        self.p = 4
        big_endian = self.u32()
        if big_endian: raise Fault('big endian unsupported')
        use_real64 = self.u32()
        ver_major = self.u32(); ver_minor = self.u32(); self.ver_fmt = self.u32()
        self.type_str = self.ustring('meta')
        self.importmd_ofs_pos = self.p
        self.importmd_ofs = self.u64()
        self.flags = self.u32()
        self.uid = self.u64()
        self.real64 = bool(self.flags & F_REAL_DOUBLE) or bool(use_real64)
        self.script_class = self.ustring('meta') if (self.flags & F_SCRIPT_CLASS) else None
        for i in range(RESERVED_FIELDS): self.u32()
        n = self.u32()
        self.string_map = []
        for i in range(n): self.string_map.append(self.ustring('name'))
        next_ = self.u32()
        self.ext = []
        for i in range(next_):
            t = self.ustring('meta'); path = self.ustring('meta')
            if self.flags & F_UIDS: self.u64()
            self.ext.append((t, path))
        ni = self.u32()
        self.int_res = []
        for i in range(ni):
            path = self.ustring('meta')
            pos = self.p
            ofs = self.u64()
            self.int_res.append([path, ofs, pos])
        for idx in range(len(self.int_res)):
            path, ofs, pos = self.int_res[idx]
            try:
                self.p = ofs
                cls = self.ustring('meta')
                pc = self.u32()
                for j in range(pc):
                    self.cur_prop = self.get_string_idx()
                    self.parse_variant(0)
            except Exception as e:
                raise Fault('resource %d (%s) parse error: %s' % (idx, path, e))

    def parse_variant(self, depth=0):
        if depth > 64: raise Fault('deep')
        t = self.u32()
        rs = 8 if self.real64 else 4
        if t == V_NIL: return
        if t == V_BOOL: self.skip(4); return
        if t == V_INT: self.skip(4); return
        if t == V_INT64: self.skip(8); return
        if t == V_FLOAT: self.skip(rs); return
        if t == V_DOUBLE: self.skip(8); return
        if t == V_STRING: self.ustring('value'); return
        if t == V_STRING_NAME or t == V_STRING_NAME: self.ustring('value_name'); return
        if t == V_VECTOR2: self.skip(2*rs); return
        if t == V_VECTOR2I or t == V_VECTOR2I: self.skip(8); return
        if t == V_RECT2: self.skip(4*rs); return
        if t == V_RECT2I or t == V_RECT2I: self.skip(16); return
        if t == V_VECTOR3: self.skip(3*rs); return
        if t == V_VECTOR3I or t == V_VECTOR3I: self.skip(12); return
        if t == V_VECTOR4 or t == V_VECTOR4: self.skip(4*rs); return
        if t == V_VECTOR4I or t == V_VECTOR4I: self.skip(16); return
        if t == V_PLANE: self.skip(4*rs); return
        if t == V_QUATERNION: self.skip(4*rs); return
        if t == V_AABB: self.skip(6*rs); return
        if t == V_BASIS: self.skip(9*rs); return
        if t == V_TRANSFORM2D: self.skip(6*rs); return
        if t == V_TRANSFORM3D: self.skip(12*rs); return
        if t == V_PROJECTION or t == V_PROJECTION: self.skip(16*rs); return
        if t == V_COLOR: self.skip(16); return
        if t == V_NODE_PATH:
            names = self.u16(); subs = self.u16()
            subs = subs & 0x7FFF
            if self.ver_fmt < 3: subs += 1
            for i in range(names): self.get_string_idx()
            for i in range(subs): self.get_string_idx()
            return
        if t == V_RID: self.skip(4); return
        if t == V_CALLABLE: return
        if t == V_SIGNAL: return
        if t == V_OBJECT:
            ot = self.u32()
            if ot == OBJ_EMPTY: return
            if ot == OBJ_INT: self.skip(4); return
            if ot == OBJ_EXT: self.ustring('meta'); self.ustring('meta'); return
            if ot == OBJ_EXT_INDEX: self.skip(4); return
            raise Fault('bad obj type %d' % ot)
        if t == V_DICTIONARY:
            ln = self.u32() & 0x7FFFFFFF
            for i in range(ln):
                n0 = len(self.strings)
                self.parse_variant(depth+1)
                key = None
                if len(self.strings) > n0:
                    lastrec = self.strings[-1]
                    if lastrec[3] == 'value': key = lastrec[2]
                prev = self.cur_prop
                if key is not None: self.cur_prop = key
                self.parse_variant(depth+1)
                self.cur_prop = prev
            return
        if t == V_ARRAY:
            ln = self.u32() & 0x7FFFFFFF
            for i in range(ln): self.parse_variant(depth+1)
            return
        if t == V_PACKED_BYTE_ARRAY:
            ln = self.u32(); self.skip(ln); self.pad(ln); return
        if t == V_PACKED_INT32_ARRAY:
            ln = self.u32(); self.skip(4*ln); return
        if t == V_PACKED_INT64_ARRAY:
            ln = self.u32(); self.skip(8*ln); return
        if t == V_PACKED_FLOAT32_ARRAY:
            ln = self.u32(); self.skip(4*ln); return
        if t == V_PACKED_FLOAT64_ARRAY:
            ln = self.u32(); self.skip(8*ln); return
        if t == V_PACKED_STRING_ARRAY:
            ln = self.u32()
            for i in range(ln): self.ustring('value')
            return
        if t == V_PACKED_VECTOR2_ARRAY:
            ln = self.u32(); self.skip(2*rs*ln); return
        if t == V_PACKED_VECTOR3_ARRAY:
            ln = self.u32(); self.skip(3*rs*ln); return
        if t == V_PACKED_VECTOR4_ARRAY:
            ln = self.u32(); self.skip(4*rs*ln); return
        if t == V_PACKED_COLOR_ARRAY:
            ln = self.u32(); self.skip(16*ln); return
        raise Fault('unknown variant type %d at %d' % (t, self.p-4))