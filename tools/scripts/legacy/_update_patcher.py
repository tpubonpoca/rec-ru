import sys, io

content = '''using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using dnlib.DotNet;
using dnlib.DotNet.Emit;

class Program
{
    static void Main(string[] args)
    {
        string mode = args[0];
        string inPath = args[1];

        if (mode == "audit")
        {
            var mod = ModuleDefMD.Load(inPath);
            string targetClass = args.Length > 2 ? args[2] : null;
            foreach (var t in mod.GetTypes())
            {
                if (targetClass != null && t.Name != targetClass) continue;
                foreach (var m in t.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var i in m.Body.Instructions)
                    {
                        if (i.OpCode == OpCodes.Ldstr && i.Operand is string s)
                        {
                            Console.WriteLine($"{t.Name}::{m.Name} -> \"{s}\"");
                        }
                    }
                }
            }
            return;
        }

        string outPath = args[2];
        var mod2 = ModuleDefMD.Load(inPath);

        if (mode == "il")
        {
            var t0 = mod2.GetTypes().First(x => x.Name == args[3]);
            var m0 = t0.Methods.First(x => x.Name == args[4]);
            var sb = new System.Text.StringBuilder();
            foreach (var i in m0.Body.Instructions) sb.AppendLine(i.Offset.ToString("X4") + "  " + i.OpCode + " " + i.Operand);
            File.WriteAllText(outPath, sb.ToString());
            Console.WriteLine("dumped " + m0.Body.Instructions.Count);
            return;
        }

        if (mode == "reverttype")
        {
            var mapBack = JsonSerializer.Deserialize<Dictionary<string, string>>(File.ReadAllText(args[3]));
            var tt = mod2.GetTypes().First(x => x.Name == args[4]);
            int cnt = 0;
            foreach (var mm in tt.Methods)
            {
                if (!mm.HasBody) continue;
                foreach (var instr in mm.Body.Instructions)
                    if (instr.OpCode == OpCodes.Ldstr && instr.Operand is string s && mapBack.TryGetValue(s, out var en))
                    {
                        instr.Operand = en;
                        cnt++;
                    }
            }
            mod2.Write(outPath);
            Console.WriteLine("reverted strings in " + args[4] + ": " + cnt);
            return;
        }

        if (mode == "patchmethod")
        {
            // args: patchmethod <inPath> <outPath> <ClassName> <MethodName> <OldStr> <NewStr>
            string cls = args[3];
            string meth = args[4];
            string oldS = args[5];
            string newS = args[6];
            var tt = mod2.GetTypes().First(x => x.Name == cls);
            var mm = tt.Methods.First(x => x.Name == meth);
            int cnt = 0;
            foreach (var instr in mm.Body.Instructions)
            {
                if (instr.OpCode == OpCodes.Ldstr && instr.Operand is string s && s == oldS)
                {
                    instr.Operand = newS;
                    cnt++;
                }
            }
            mod2.Write(outPath);
            Console.WriteLine($"patched {cnt} occurrences in {cls}::{meth}");
            return;
        }

        string typeFilter = args.Length > 4 && args[4] != "*" ? args[4] : null;
        var types = mod2.GetTypes().Where(t => typeFilter == null || t.Name == typeFilter).ToList();

        if (mode == "dump")
        {
            var seen = new List<string>();
            foreach (var type in types)
                foreach (var m in type.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var instr in m.Body.Instructions)
                        if (instr.OpCode == OpCodes.Ldstr && instr.Operand is string s && !seen.Contains(s))
                            seen.Add(s);
                }
            File.WriteAllText(outPath, JsonSerializer.Serialize(seen, new JsonSerializerOptions { WriteIndented = true }));
            Console.WriteLine("strings: " + seen.Count);
            return;
        }

        var map = JsonSerializer.Deserialize<Dictionary<string, string>>(File.ReadAllText(args[3]));
        int n = 0;
        foreach (var type in types)
            foreach (var m in type.Methods)
            {
                if (!m.HasBody) continue;
                foreach (var instr in m.Body.Instructions)
                    if (instr.OpCode == OpCodes.Ldstr && instr.Operand is string s && map.TryGetValue(s, out var repl))
                    {
                        instr.Operand = repl;
                        n++;
                    }
            }
        mod2.Write(outPath);
        Console.WriteLine("patched strings: " + n);
    }
}
'''

with open(r'C:\Users\Asyncoder\Downloads\REC_extract\patcher\Program.cs', 'w', encoding='utf-8') as f:
    f.write(content)
