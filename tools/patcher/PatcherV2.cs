using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using dnlib.DotNet;
using dnlib.DotNet.Emit;

class PatcherV2
{
    public static void Patch(string inPath, string outPath, string godotSharpPath)
    {
        var mod = ModuleDefMD.Load(inPath);
        var godotSharpMod = ModuleDefMD.Load(godotSharpPath);

        // 1. SettingsUI
        var settingsType = mod.GetTypes().FirstOrDefault(x => x.Name == "SettingsUI");
        var applyCheat = settingsType?.Methods.FirstOrDefault(x => x.Name == "ApplyCheat");
        var showNoticeMethod = settingsType?.Methods.FirstOrDefault(x => x.Name == "ShowNotice");
        var codeInputField = settingsType?.Fields.FirstOrDefault(x => x.Name == "code_input");

        // StateVariables
        var stateVarsType = mod.GetTypes().FirstOrDefault(x => x.Name == "StateVariables");
        var setVarMethod = stateVarsType?.Methods.FirstOrDefault(x => x.Name == "SetVariable" && x.Parameters.Count == 2);

        // Settings
        var settingsClass = mod.GetTypes().FirstOrDefault(x => x.Name == "Settings");
        var settingsInstanceField = settingsClass?.Fields.FirstOrDefault(x => x.Name == "Instance");
        var setSuspicionField = settingsClass?.Fields.FirstOrDefault(x => x.Name == "SET_SUSPICION");

        // External refs
        var lineEditType = godotSharpMod.Find("Godot.LineEdit", true);
        var getTextMethod = lineEditType.FindMethod("get_Text");
        var setTextMethod = lineEditType.FindMethod("set_Text");
        var getTextRef = mod.Import(getTextMethod);
        var setTextRef = mod.Import(setTextMethod);

        var strOpEq = mod.GetMemberRefs().FirstOrDefault(r => r.DeclaringType.FullName == "System.String" && r.Name == "op_Equality");
        var toUpperMethod = mod.GetMemberRefs().FirstOrDefault(r => r.DeclaringType.FullName == "System.String" && r.Name == "ToUpper");

        // Find Variant.op_Implicit(int)
        var varOpImpInt = mod.GetMemberRefs().FirstOrDefault(r => r.DeclaringType.FullName == "Godot.Variant" && r.Name == "op_Implicit" && r.MethodSig.Params.Count == 1 && r.MethodSig.Params[0].FullName == "System.Int32");
        if (varOpImpInt == null)
        {
            var variantType = godotSharpMod.Find("Godot.Variant", true);
            foreach (var m in variantType.Methods)
            {
                if (m.Name == "op_Implicit" && m.Parameters.Count == 1 && m.Parameters[0].Type.TypeName == "Int32")
                {
                    varOpImpInt = mod.Import(m);
                    break;
                }
            }
        }

        Console.WriteLine($"ApplyCheat patch refs: applyCheat={applyCheat != null}, codeInput={codeInputField != null}, setVar={setVarMethod != null}, varOpImpInt={varOpImpInt != null}");

        if (applyCheat != null && codeInputField != null && setVarMethod != null && varOpImpInt != null && showNoticeMethod != null)
        {
            var origFirst = applyCheat.Body.Instructions[0];
            var ins = new List<Instruction>();

            ins.Add(new Instruction(OpCodes.Ldarg_0));
            ins.Add(new Instruction(OpCodes.Ldfld, codeInputField));
            ins.Add(new Instruction(OpCodes.Callvirt, getTextRef));
            ins.Add(new Instruction(OpCodes.Callvirt, toUpperMethod));
            ins.Add(new Instruction(OpCodes.Ldstr, "AMOGUS"));
            ins.Add(new Instruction(OpCodes.Call, strOpEq));
            ins.Add(new Instruction(OpCodes.Brfalse_S, origFirst));

            // Set suspicion to 0
            ins.Add(new Instruction(OpCodes.Ldstr, "suspicion"));
            ins.Add(new Instruction(OpCodes.Ldc_I4_0));
            ins.Add(new Instruction(OpCodes.Call, varOpImpInt));
            ins.Add(new Instruction(OpCodes.Call, setVarMethod));

            // Set Settings.Instance.SET_SUSPICION = 0
            var skipSettings = new Instruction(OpCodes.Nop);
            if (settingsInstanceField != null && setSuspicionField != null)
            {
                ins.Add(new Instruction(OpCodes.Ldsfld, settingsInstanceField));
                ins.Add(new Instruction(OpCodes.Brfalse_S, skipSettings));
                ins.Add(new Instruction(OpCodes.Ldsfld, settingsInstanceField));
                ins.Add(new Instruction(OpCodes.Ldc_I4_0));
                ins.Add(new Instruction(OpCodes.Stfld, setSuspicionField));
            }
            ins.Add(skipSettings);

            // ShowNotice
            ins.Add(new Instruction(OpCodes.Ldarg_0));
            ins.Add(new Instruction(OpCodes.Ldstr, "Подозрение Юны сброшено до 0!"));
            ins.Add(new Instruction(OpCodes.Call, showNoticeMethod));

            // Clear text
            ins.Add(new Instruction(OpCodes.Ldarg_0));
            ins.Add(new Instruction(OpCodes.Ldfld, codeInputField));
            ins.Add(new Instruction(OpCodes.Ldstr, ""));
            ins.Add(new Instruction(OpCodes.Callvirt, setTextRef));

            ins.Add(new Instruction(OpCodes.Ret));

            for (int k = ins.Count - 1; k >= 0; k--)
            {
                applyCheat.Body.Instructions.Insert(0, ins[k]);
            }
            Console.WriteLine("Injected AMOGUS cheat into SettingsUI.ApplyCheat");
        }

        // 2. SaveUI font size override in _Ready
        var saveType = mod.GetTypes().FirstOrDefault(x => x.Name == "SaveUI");
        var saveReady = saveType?.Methods.FirstOrDefault(x => x.Name == "_Ready");
        var nightField = saveType?.Fields.FirstOrDefault(x => x.Name == "night");
        var leftBtnField = saveType?.Fields.FirstOrDefault(x => x.Name == "left_button");
        var rightBtnField = saveType?.Fields.FirstOrDefault(x => x.Name == "right_button");

        var controlType = godotSharpMod.Find("Godot.Control", true);
        var addFontSizeMethod = controlType.FindMethod("AddThemeFontSizeOverride");
        var addThemeFontSizeRef = mod.Import(addFontSizeMethod);
        var strNameOpImp = mod.GetMemberRefs().FirstOrDefault(r => r.DeclaringType.FullName == "Godot.StringName" && r.Name == "op_Implicit" && r.MethodSig.Params.Count == 1 && r.MethodSig.Params[0].FullName == "System.String");

        Console.WriteLine($"SaveUI patch refs: saveReady={saveReady != null}, night={nightField != null}, leftBtn={leftBtnField != null}, rightBtn={rightBtnField != null}, addThemeFontSizeRef={addThemeFontSizeRef != null}, strNameOpImp={strNameOpImp != null}");

        if (saveReady != null && nightField != null && leftBtnField != null && rightBtnField != null && addThemeFontSizeRef != null && strNameOpImp != null)
        {
            var lastRet = saveReady.Body.Instructions.Last(x => x.OpCode == OpCodes.Ret);
            int idx = saveReady.Body.Instructions.IndexOf(lastRet);

            var fontIns = new List<Instruction>();

            // night.AddThemeFontSizeOverride("font_size", 5)
            fontIns.Add(new Instruction(OpCodes.Ldarg_0));
            fontIns.Add(new Instruction(OpCodes.Ldfld, nightField));
            fontIns.Add(new Instruction(OpCodes.Ldstr, "font_size"));
            fontIns.Add(new Instruction(OpCodes.Call, strNameOpImp));
            fontIns.Add(new Instruction(OpCodes.Ldc_I4_5));
            fontIns.Add(new Instruction(OpCodes.Callvirt, addThemeFontSizeRef));

            // left_button.AddThemeFontSizeOverride("font_size", 4)
            fontIns.Add(new Instruction(OpCodes.Ldarg_0));
            fontIns.Add(new Instruction(OpCodes.Ldfld, leftBtnField));
            fontIns.Add(new Instruction(OpCodes.Ldstr, "font_size"));
            fontIns.Add(new Instruction(OpCodes.Call, strNameOpImp));
            fontIns.Add(new Instruction(OpCodes.Ldc_I4_4));
            fontIns.Add(new Instruction(OpCodes.Callvirt, addThemeFontSizeRef));

            // right_button.AddThemeFontSizeOverride("font_size", 4)
            fontIns.Add(new Instruction(OpCodes.Ldarg_0));
            fontIns.Add(new Instruction(OpCodes.Ldfld, rightBtnField));
            fontIns.Add(new Instruction(OpCodes.Ldstr, "font_size"));
            fontIns.Add(new Instruction(OpCodes.Call, strNameOpImp));
            fontIns.Add(new Instruction(OpCodes.Ldc_I4_4));
            fontIns.Add(new Instruction(OpCodes.Callvirt, addThemeFontSizeRef));

            foreach (var fi in fontIns)
            {
                saveReady.Body.Instructions.Insert(idx++, fi);
            }
            Console.WriteLine("Injected font size overrides into SaveUI._Ready");
        }

        mod.Write(outPath);
        Console.WriteLine($"Saved patched assembly to: {outPath}");
    }
}
