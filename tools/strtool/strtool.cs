// dump: выписать все ldstr сборки; patch: заменить строки по таблице (тип, метод, исходная строка -> новая)
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using dnlib.DotNet;
using dnlib.DotNet.Emit;

class StrTool
{
    const char BS = (char)92, TAB = (char)9, LF = (char)10, CR = (char)13;

    static string Esc(string s)
    {
        var sb = new StringBuilder();
        foreach (char c in s)
        {
            if (c == BS) sb.Append(BS).Append(BS);
            else if (c == TAB) sb.Append(BS).Append('t');
            else if (c == LF) sb.Append(BS).Append('n');
            else if (c == CR) sb.Append(BS).Append('r');
            else sb.Append(c);
        }
        return sb.ToString();
    }

    static string Unesc(string s)
    {
        var sb = new StringBuilder();
        for (int i = 0; i < s.Length; i++)
        {
            if (s[i] == BS && i + 1 < s.Length)
            {
                char c = s[++i];
                sb.Append(c == 't' ? TAB : c == 'n' ? LF : c == 'r' ? CR : c);
            }
            else sb.Append(s[i]);
        }
        return sb.ToString();
    }

    static void Main(string[] args)
    {
        var mod = ModuleDefMD.Load(args[1]);
        if (args[0] == "dump")
        {
            using (var w = new StreamWriter(args[2], false, new UTF8Encoding(false)))
                foreach (var t in mod.GetTypes())
                    foreach (var m in t.Methods)
                    {
                        if (!m.HasBody) continue;
                        foreach (var i in m.Body.Instructions)
                            if (i.OpCode == OpCodes.Ldstr) w.WriteLine(t.FullName + TAB + m.Name + TAB + Esc((string)i.Operand));
                    }
            return;
        }
        if (args[0] == "patch")
        {
            var map = new Dictionary<string, string>();
            foreach (var line in File.ReadAllLines(args[3], Encoding.UTF8))
            {
                var p = line.Split(TAB);
                if (p.Length == 4) map[p[0] + TAB + p[1] + TAB + Unesc(p[2])] = Unesc(p[3]);
            }
            int n = 0;
            var used = new HashSet<string>();
            foreach (var t in mod.GetTypes())
                foreach (var m in t.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var i in m.Body.Instructions)
                    {
                        if (i.OpCode != OpCodes.Ldstr) continue;
                        string k = t.FullName + TAB + m.Name + TAB + (string)i.Operand, v;
                        if (map.TryGetValue(k, out v)) { i.Operand = v; n++; used.Add(k); }
                    }
                }
            if (args.Length > 5) InjectTr(mod, args[4], args[5]);
            if (args.Length > 6) InjectFontSizes(mod, args[4], args[6]);
            mod.Write(args[2]);
            Console.WriteLine("replaced " + n + ", keys used " + used.Count + " of " + map.Count);
            foreach (var k in map.Keys) if (!used.Contains(k)) Console.WriteLine("unused: " + Esc(k));
        }
    }

    // spec: "Type.Method:field=size;field=size" добавляет в конец метода AddThemeFontSizeOverride("font_size", size) для полей-контролов
    static void InjectFontSizes(ModuleDefMD mod, string godotSharpPath, string specs)
    {
        var gs = ModuleDefMD.Load(godotSharpPath);
        IMethod toSn = null, addSize = null;
        foreach (var m in gs.Find("Godot.StringName", true).Methods)
            if (m.Name == "op_Implicit" && m.Parameters.Count == 1 && m.Parameters[0].Type.FullName == "System.String") toSn = mod.Import(m);
        foreach (var m in gs.Find("Godot.Control", true).Methods)
            if (m.Name == "AddThemeFontSizeOverride") addSize = mod.Import(m);
        foreach (var spec in specs.Split(','))
        {
            var p = spec.Split(':');
            int dot = p[0].LastIndexOf('.');
            var type = mod.Find(p[0].Substring(0, dot), true);
            MethodDef md = null;
            foreach (var m in type.Methods) if (m.Name == p[0].Substring(dot + 1) && m.HasBody) md = m;
            var body = md.Body.Instructions;
            int at = body.Count - 1;
            while (body[at].OpCode != OpCodes.Ret) at--;
            // вставка перед последним ret: старый ret становится первой новой инструкцией, чтобы ветки на него не обходили вставку
            var ret = body[at];
            var ins = new List<Instruction>();
            foreach (var fs in p[1].Split(';'))
            {
                var kv = fs.Split('=');
                FieldDef fd = null;
                foreach (var f in type.Fields) if (f.Name == kv[0]) fd = f;
                if (fd == null) throw new Exception("field not found: " + kv[0]);
                ins.Add(new Instruction(OpCodes.Ldarg_0));
                ins.Add(new Instruction(OpCodes.Ldfld, fd));
                ins.Add(new Instruction(OpCodes.Ldstr, "font_size"));
                ins.Add(new Instruction(OpCodes.Call, toSn));
                ins.Add(new Instruction(OpCodes.Ldc_I4, int.Parse(kv[1])));
                ins.Add(new Instruction(OpCodes.Callvirt, addSize));
            }
            ret.OpCode = ins[0].OpCode; ret.Operand = ins[0].Operand;
            for (int i = 1; i < ins.Count; i++) body.Insert(at + i, ins[i]);
            body.Insert(at + ins.Count, new Instruction(OpCodes.Ret));
            md.Body.SimplifyBranches(); md.Body.OptimizeBranches();
            Console.WriteLine("font sizes injected: " + spec);
        }
    }

    // spec: "Type.Method:argN" переводит строковый аргумент на входе, "Type.Method:ret" переводит возвращаемую строку
    static void InjectTr(ModuleDefMD mod, string godotSharpPath, string specs)
    {
        var gs = ModuleDefMD.Load(godotSharpPath);
        var sn = gs.Find("Godot.StringName", true);
        var ts = gs.Find("Godot.TranslationServer", true);
        IMethod toSn = null, toStr = null, translate = null;
        foreach (var m in sn.Methods)
        {
            if (m.Name != "op_Implicit" || m.Parameters.Count != 1) continue;
            if (m.Parameters[0].Type.FullName == "System.String") toSn = mod.Import(m);
            else if (m.ReturnType.FullName == "System.String") toStr = mod.Import(m);
        }
        foreach (var m in ts.Methods)
            if (m.Name == "Translate" && m.Parameters.Count == 2) translate = mod.Import(m);
        if (toSn == null || toStr == null || translate == null) throw new Exception("GodotSharp refs not found");
        foreach (var spec in specs.Split(','))
        {
            var p = spec.Split(':');
            int dot = p[0].LastIndexOf('.');
            var type = mod.Find(p[0].Substring(0, dot), true);
            MethodDef md = null;
            foreach (var m in type.Methods) if (m.Name == p[0].Substring(dot + 1) && m.HasBody) md = m;
            if (md == null) throw new Exception("method not found: " + p[0]);
            var body = md.Body.Instructions;
            if (p[1] == "ret")
            {
                for (int i = body.Count - 1; i >= 0; i--)
                {
                    if (body[i].OpCode != OpCodes.Ret) continue;
                    // ret остаётся на месте, чтобы ветки, прыгающие на него, тоже шли через перевод
                    var tail = new Instruction(OpCodes.Ret);
                    var old = body[i];
                    old.OpCode = OpCodes.Call; old.Operand = toSn;
                    body.Insert(i + 1, new Instruction(OpCodes.Ldnull));
                    body.Insert(i + 2, new Instruction(OpCodes.Call, translate));
                    body.Insert(i + 3, new Instruction(OpCodes.Call, toStr));
                    body.Insert(i + 4, tail);
                }
            }
            else
            {
                var param = md.Parameters[int.Parse(p[1].Substring(3))];
                body.Insert(0, new Instruction(OpCodes.Ldarg, param));
                body.Insert(1, new Instruction(OpCodes.Call, toSn));
                body.Insert(2, new Instruction(OpCodes.Ldnull));
                body.Insert(3, new Instruction(OpCodes.Call, translate));
                body.Insert(4, new Instruction(OpCodes.Call, toStr));
                body.Insert(5, new Instruction(OpCodes.Starg, param));
            }
            md.Body.SimplifyBranches(); md.Body.OptimizeBranches();
            Console.WriteLine("tr injected: " + spec);
        }
    }
}
