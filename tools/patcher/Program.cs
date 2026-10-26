using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using dnlib.DotNet;
using dnlib.DotNet.Emit;

class Program
{
    static void Main(string[] args)
    {
        string mode = args[0];
        string inPath = args[1];

        if (mode == "patch_amogus_and_ui")
        {
            PatcherV2.Patch(args[1], args[2], args[3]);
            return;
        }

        if (mode == "printenum")
        {
            var mod = ModuleDefMD.Load(inPath);
            var t = mod.GetTypes().FirstOrDefault(x => x.Name == args[2]);
            if (t != null)
            {
                Console.WriteLine("Enum " + t.Name + " fields count: " + t.Fields.Count);
                foreach (var f in t.Fields)
                    Console.WriteLine("  " + f.Name + " = " + f.Constant?.Value);
            }
            return;
        }

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

        if (mode == "dump")
        {
            var mod = ModuleDefMD.Load(inPath);
            string targetClass = args.Length > 2 ? args[2] : null;
            foreach (var t in mod.GetTypes())
            {
                if (targetClass != null && !t.Name.Contains(targetClass)) continue;
                Console.WriteLine("CLASS: " + t.FullName);
                foreach (var m in t.Methods)
                {
                    Console.WriteLine("  METHOD: " + m.Name);
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        Console.WriteLine($"    {ins.OpCode} {ins.Operand}");
                    }
                }
            }
            return;
        }

        string outPath = args[2];
        var mod2 = ModuleDefMD.Load(inPath);

        if (mode == "fix_all")
        {
            int stringFixes = 0;
            int enumFixes = 0;

            // 1. Revert Days enum fields
            var daysType = mod2.GetTypes().FirstOrDefault(x => x.Name == "Days");
            if (daysType != null)
            {
                var dayMap = new Dictionary<string, string>
                {
                    { "ВС", "SUN" },
                    { "ПН", "MON" },
                    { "ВТ", "TUE" },
                    { "СР", "WED" },
                    { "ЧТ", "THU" },
                    { "ПТ", "FRI" },
                    { "СБ", "SAT" }
                };
                foreach (var f in daysType.Fields)
                {
                    if (dayMap.TryGetValue(f.Name, out var enName))
                    {
                        f.Name = enName;
                        enumFixes++;
                    }
                }
            }

            // 2. Fix StateVariables
            var stateVarsType = mod2.GetTypes().FirstOrDefault(x => x.Name == "StateVariables");
            if (stateVarsType != null)
            {
                foreach (var m in stateVarsType.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        if (ins.OpCode == OpCodes.Ldstr && ins.Operand is string s)
                        {
                            if (s == "выносливость") { ins.Operand = "stamina"; stringFixes++; }
                            else if (s == "похоть") { ins.Operand = "lust"; stringFixes++; }
                            else if (s == "подозрение") { ins.Operand = "suspicion"; stringFixes++; }
                            else if (s == "имя") { ins.Operand = "name"; stringFixes++; }
                        }
                    }
                }
            }

            // 3. Fix Calendar
            var calType = mod2.GetTypes().FirstOrDefault(x => x.Name == "Calendar");
            if (calType != null)
            {
                foreach (var m in calType.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        if (ins.OpCode == OpCodes.Ldstr && ins.Operand is string s)
                        {
                            if (s == "день") { ins.Operand = "day"; stringFixes++; }
                            else if (s == "подозрение") { ins.Operand = "suspicion"; stringFixes++; }
                        }
                    }
                }
            }

            // 4. Fix NightSequence
            var nightType = mod2.GetTypes().FirstOrDefault(x => x.Name == "NightSequence");
            if (nightType != null)
            {
                foreach (var m in nightType.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        if (ins.OpCode == OpCodes.Ldstr && ins.Operand is string s)
                        {
                            if (s == "выносливость") { ins.Operand = "stamina"; stringFixes++; }
                            else if (s == "похоть") { ins.Operand = "lust"; stringFixes++; }
                            else if (s == "имя") { ins.Operand = "name"; stringFixes++; }
                        }
                    }
                }
            }

            // 5. Fix Purchasable
            var purchType = mod2.GetTypes().FirstOrDefault(x => x.Name == "Purchasable");
            if (purchType != null)
            {
                foreach (var m in purchType.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        if (ins.OpCode == OpCodes.Ldstr && ins.Operand is string s)
                        {
                            if (s == "Purchase") { ins.Operand = "Купить"; stringFixes++; }
                            else if (s == "Purchased") { ins.Operand = "Куплено"; stringFixes++; }
                        }
                    }
                }
            }

            // 6. Fix UpgradeRegularResource & ItemResource requirement strings
            foreach (var typeName in new[] { "UpgradeRegularResource", "ItemResource" })
            {
                var tt = mod2.GetTypes().FirstOrDefault(x => x.Name == typeName);
                if (tt == null) continue;
                foreach (var m in tt.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        if (ins.OpCode == OpCodes.Ldstr && ins.Operand is string s)
                        {
                            if (s == "[color=#00ffa8](Requires: ") { ins.Operand = "[color=#00ffa8](Требуется: "; stringFixes++; }
                            else if (s == "[color=#96413d](Requires: ") { ins.Operand = "[color=#96413d](Требуется: "; stringFixes++; }
                            else if (s == " Access") { ins.Operand = " Доступ"; stringFixes++; }
                            else if (s == " Access[/color]") { ins.Operand = " Доступ[/color]"; stringFixes++; }
                            else if (s == "[color=#00ffa8]CHA ") { ins.Operand = "[color=#00ffa8]ХАР "; stringFixes++; }
                            else if (s == "[color=#00ffa8]DEX ") { ins.Operand = "[color=#00ffa8]ЛОВ "; stringFixes++; }
                            else if (s == "[color=#00ffa8]INT ") { ins.Operand = "[color=#00ffa8]ИНТ "; stringFixes++; }
                            else if (s == "[color=#00ffa8]STA ") { ins.Operand = "[color=#00ffa8]ВЫН "; stringFixes++; }
                        }
                    }
                }
            }

            // 7. Fix Statistics secondary stat labels so numbers are never clipped
            var statsType = mod2.GetTypes().FirstOrDefault(x => x.Name == "Statistics");
            if (statsType != null)
            {
                foreach (var m in statsType.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        if (ins.OpCode == OpCodes.Ldstr && ins.Operand is string s)
                        {
                            if (s == "предметов использовано") { ins.Operand = "предметы исп."; stringFixes++; }
                            else if (s == "осмотров у Кана") { ins.Operand = "осмотры Кана"; stringFixes++; }
                            else if (s == "головоломок решено") { ins.Operand = "загадок решено"; stringFixes++; }
                            else if (s == "головоломок провалено") { ins.Operand = "загадок сбито"; stringFixes++; }
                            else if (s == "событий просмотрено") { ins.Operand = "события просм."; stringFixes++; }
                            else if (s == "врагов побеждено") { ins.Operand = "враги разбиты"; stringFixes++; }
                            else if (s == "телефон отключён") { ins.Operand = "телефон выкл."; stringFixes++; }
                        }
                    }
                }
            }

            // 8. Fix Hint.SetDescription and NightSequence.AddScore to prevent flickering of shift, unzip, etc.
            var hintType = mod2.GetTypes().FirstOrDefault(x => x.Name == "Hint");
            if (hintType != null && !hintType.Methods.Any(x => x.Name == "Translate"))
            {
                var toLowerMethod = mod2.Import(typeof(string).GetMethod("ToLowerInvariant", Type.EmptyTypes));
                var opEqualityMethod = mod2.Import(typeof(string).GetMethod("op_Equality", new[] { typeof(string), typeof(string) }));

                var translateMethod = new MethodDefUser("Translate",
                    MethodSig.CreateStatic(mod2.CorLibTypes.String, mod2.CorLibTypes.String),
                    MethodImplAttributes.IL | MethodImplAttributes.Managed,
                    MethodAttributes.Public | MethodAttributes.Static);
                translateMethod.Parameters[0].CreateParamDef();
                var cil = new CilBody();
                translateMethod.Body = cil;

                var isNullLabel = new Instruction(OpCodes.Ldnull);
                cil.Instructions.Add(new Instruction(OpCodes.Ldarg_0));
                cil.Instructions.Add(new Instruction(OpCodes.Brfalse, isNullLabel));
                cil.Instructions.Add(new Instruction(OpCodes.Ldarg_0));
                cil.Instructions.Add(new Instruction(OpCodes.Callvirt, toLowerMethod));

                var pairs = new (string en, string ru)[]
                {
                    ("shift", "поправить"),
                    ("unzip", "расстегнуть"),
                    ("headpat", "поглаживание"),
                    ("grab", "схватить"),
                    ("kiss", "поцелуй"),
                    ("remove", "снять"),
                    ("spank_left", "шлёпнуть слева"),
                    ("spank_right", "шлёпнуть справа"),
                    ("doggystyle", "раком"),
                    ("missionary", "миссионерская"),
                    ("blowjob", "минет"),
                    ("handjob", "дрочка"),
                    ("titjob", "секс с грудью"),
                    ("footjob", "футджоб"),
                    ("assjob", "секс с попкой"),
                    ("masturbate", "мастурбировать"),
                    ("penetrate", "проникновение"),
                    ("unlock door", "открыть дверь"),
                    ("female climax", "женский оргазм"),
                    ("male climax", "мужской оргазм"),
                    ("exposed body", "нагота"),
                    ("sexual activity", "сексуальная активность"),
                    ("perfect temp", "идеальная темп."),
                    ("good temp", "хорошая темп."),
                    ("danger bonus", "бонус риска"),
                    ("mess bonus", "бонус грязи"),
                    ("evaded capture", "уклонение"),
                    ("killed fly", "муха убита"),
                    ("donation", "донат"),
                    ("silenced phone", "телефон заглушён"),
                    ("plush removed", "плюш убран"),
                    ("perfect timing", "идеальный тайминг"),
                    ("request fulfilled!", "запрос выполнен!"),
                    // Enemy names
                    ("deep-sea diver", "Глубоководник"),
                    ("buff bro", "Качок-братан"),
                    ("corrupt cop", "Продажный коп"),
                    ("cranky cop", "Ворчливый коп"),
                    ("healing hamster", "Целебный хомяк"),
                    ("iron maiden", "Железная дева"),
                    ("lumberjane", "Лесорубка"),
                    ("mad science student", "Студент безумной науки"),
                    ("menacing hobo", "Зловещий бродяга"),
                    ("perverted doctor", "Извращённый доктор"),
                    ("sexy psycho", "Секс-психопатка"),
                    ("silent hunter", "Тихий охотник"),
                    ("slime queen", "Королева слизи"),
                    ("unholy nun", "Нечестивая монашка"),
                    ("wandering ronin", "Странствующий ронин"),
                    ("assimilator", "Ассимилятор"),
                    // Battle button tooltips
                    ("reduces damage + effects", "Снижает урон и негативные эффекты"),
                    ("talk", "Поговорить"),
                    ("skills", "Навыки"),
                    ("flee from battle", "Сбежать из боя"),
                    ("run", "Сбежать из боя"),
                    ("stops enemy offensive moves", "Блокирует атаки врага"),
                    ("reduces enemy accuracy/dodge", "Снижает меткость и уклонение"),
                    ("prevents enemy skills + increases damage", "Блокирует навыки, повышает урон"),
                    ("stun all enemies.", "Оглушает всех врагов"),
                    ("back", "Назад"),
                };

                for (int pIdx = 0; pIdx < pairs.Length; pIdx++)
                {
                    var nextLabel = new Instruction(OpCodes.Nop);
                    cil.Instructions.Add(new Instruction(OpCodes.Dup));
                    cil.Instructions.Add(new Instruction(OpCodes.Ldstr, pairs[pIdx].en));
                    cil.Instructions.Add(new Instruction(OpCodes.Call, opEqualityMethod));
                    cil.Instructions.Add(new Instruction(OpCodes.Brfalse, nextLabel));
                    cil.Instructions.Add(new Instruction(OpCodes.Pop));
                    cil.Instructions.Add(new Instruction(OpCodes.Ldstr, pairs[pIdx].ru));
                    cil.Instructions.Add(new Instruction(OpCodes.Ret));
                    cil.Instructions.Add(nextLabel);
                }

                // Default return original arg
                cil.Instructions.Add(new Instruction(OpCodes.Pop));
                cil.Instructions.Add(new Instruction(OpCodes.Ldarg_0));
                cil.Instructions.Add(new Instruction(OpCodes.Ret));

                // isNullLabel
                cil.Instructions.Add(isNullLabel);
                cil.Instructions.Add(new Instruction(OpCodes.Ret));

                cil.OptimizeBranches();

                hintType.Methods.Add(translateMethod);

                // Inject call at start of Hint.SetDescription
                var setDesc = hintType.Methods.FirstOrDefault(x => x.Name == "SetDescription");
                if (setDesc != null && setDesc.HasBody)
                {
                    setDesc.Body.Instructions.Insert(0, new Instruction(OpCodes.Ldarg, setDesc.Parameters[0]));
                    setDesc.Body.Instructions.Insert(1, new Instruction(OpCodes.Call, translateMethod));
                    setDesc.Body.Instructions.Insert(2, new Instruction(OpCodes.Starg, setDesc.Parameters[0]));
                    Console.WriteLine("Injected Translate into Hint.SetDescription");
                }

                // Inject call into NightSequence.AddScore
                var nightSeqType = mod2.GetTypes().FirstOrDefault(x => x.Name == "NightSequence");
                if (nightSeqType != null)
                {
                    var addScore = nightSeqType.Methods.FirstOrDefault(x => x.Name == "AddScore" && x.Parameters.Count == 3);
                    if (addScore != null && addScore.HasBody)
                    {
                        addScore.Body.Instructions.Insert(0, new Instruction(OpCodes.Ldarg, addScore.Parameters[2]));
                        addScore.Body.Instructions.Insert(1, new Instruction(OpCodes.Call, translateMethod));
                        addScore.Body.Instructions.Insert(2, new Instruction(OpCodes.Starg, addScore.Parameters[2]));
                        Console.WriteLine("Injected Translate into NightSequence.AddScore");
                    }
                }

                // Inject call into EnemyResource.GetName
                var enemyType = mod2.GetTypes().FirstOrDefault(x => x.Name == "EnemyResource");
                if (enemyType != null)
                {
                    var getName = enemyType.Methods.FirstOrDefault(x => x.Name == "GetName");
                    if (getName != null && getName.HasBody)
                    {
                        getName.Body.Instructions.Insert(getName.Body.Instructions.Count - 1, new Instruction(OpCodes.Call, translateMethod));
                        Console.WriteLine("Injected Translate into EnemyResource.GetName");
                    }
                }
            }

            // 9. Fix Cooking, Recipes, and PortraitYuna
            var recipesType = mod2.GetTypes().FirstOrDefault(x => x.Name == "Recipes");
            if (recipesType != null)
            {
                foreach (var m in recipesType.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        if (ins.OpCode == OpCodes.Ldstr && ins.Operand is string s)
                        {
                            if (s == "Детали рецепта") { ins.Operand = "Recipe Details"; stringFixes++; }
                        }
                    }
                }
            }

            var portraitYunaType = mod2.GetTypes().FirstOrDefault(x => x.Name == "PortraitYuna");
            if (portraitYunaType != null)
            {
                foreach (var m in portraitYunaType.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        if (ins.OpCode == OpCodes.Ldstr && ins.Operand is string s)
                        {
                            if (s == "Секс-акты") { ins.Operand = "Sex Acts"; stringFixes++; }
                        }
                    }
                }
            }

            var recipeBoxType = mod2.GetTypes().FirstOrDefault(x => x.Name == "RecipeBox");
            if (recipeBoxType != null)
            {
                foreach (var m in recipeBoxType.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        if (ins.OpCode == OpCodes.Ldstr && ins.Operand is string s)
                        {
                            if (s == "What are you planning to make?") { ins.Operand = "Что ты планируешь приготовить?"; stringFixes++; }
                            else if (s == "What should I make today?") { ins.Operand = "Что бы мне сегодня приготовить?"; stringFixes++; }
                        }
                    }
                }
            }

            var ingredientType = mod2.GetTypes().FirstOrDefault(x => x.Name == "Ingredient");
            if (ingredientType != null)
            {
                foreach (var m in ingredientType.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        if (ins.OpCode == OpCodes.Ldstr && ins.Operand is string s)
                        {
                            if (s == "I can't blend this...") { ins.Operand = "Я не могу это взбить..."; stringFixes++; }
                            else if (s == "This ingredient needs preparing first...") { ins.Operand = "Этот ингредиент сначала нужно подготовить..."; stringFixes++; }
                            else if (s == "There's nothing to place this in...") { ins.Operand = "Здесь не во что это положить..."; stringFixes++; }
                            else if (s == "There's no water in there...") { ins.Operand = "Там нет воды..."; stringFixes++; }
                        }
                    }
                }
            }

            foreach (var t in mod2.GetTypes().Where(x => x.Name.StartsWith("Serving") || x.FullName.Contains("Serving")))
            {
                foreach (var m in t.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        if (ins.OpCode == OpCodes.Ldstr && ins.Operand is string s)
                        {
                            if (s == "There's nothing to serve here.") { ins.Operand = "Здесь нечего подавать."; stringFixes++; }
                            else if (s == "Am I ready to serve this?" || s == "\"Am I ready to serve this?\"") { ins.Operand = "Подать это блюдо?"; stringFixes++; }
                        }
                    }
                }
            }

            var settingsType = mod2.GetTypes().FirstOrDefault(x => x.Name == "Settings");
            if (settingsType != null)
            {
                foreach (var m in settingsType.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        if (ins.OpCode == OpCodes.Ldstr && ins.Operand is string s)
                        {
                            if (s == "подозрение") { ins.Operand = "suspicion"; stringFixes++; }
                            else if (s == "выносливость") { ins.Operand = "stamina"; stringFixes++; }
                        }
                    }
                }
            }

            // 10. Kitchen Stove & Oven controls
            foreach (var typeName in new[] { "Stove", "Oven" })
            {
                var tt = mod2.GetTypes().FirstOrDefault(x => x.Name == typeName);
                if (tt == null) continue;
                foreach (var m in tt.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        if (ins.OpCode == OpCodes.Ldstr && ins.Operand is string s)
                        {
                            if (s == "on") { ins.Operand = "вкл"; stringFixes++; }
                            else if (s == "off") { ins.Operand = "выкл"; stringFixes++; }
                        }
                    }
                }
            }

            // 11. SaveTape labels & time substring fix
            var saveTapeType = mod2.GetTypes().FirstOrDefault(x => x.Name == "SaveTape");
            if (saveTapeType != null)
            {
                foreach (var m in saveTapeType.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        if (ins.OpCode == OpCodes.Ldstr && ins.Operand is string s)
                        {
                            if (s == "Ночь  #") { ins.Operand = "Ночь #"; stringFixes++; }
                            else if (s == "Night #") { ins.Operand = "Ночь #"; stringFixes++; }
                            else if (s == "Empty") { ins.Operand = "Пусто"; stringFixes++; }
                        }
                    }
                }

                var updateLabels = saveTapeType.Methods.FirstOrDefault(x => x.Name == "UpdateLabels");
                if (updateLabels != null && updateLabels.HasBody)
                {
                    var instrs = updateLabels.Body.Instructions;
                    for (int i = 0; i < instrs.Count - 3; i++)
                    {
                        if (instrs[i].OpCode == OpCodes.Callvirt && instrs[i].Operand != null && instrs[i].Operand.ToString().Contains("get_Length")
                            && instrs[i + 1].OpCode == OpCodes.Ldc_I4_S && Convert.ToInt32(instrs[i + 1].Operand) == 11
                            && instrs[i + 2].OpCode == OpCodes.Sub)
                        {
                            var indexOfMethod = mod2.Import(typeof(string).GetMethod("IndexOf", new[] { typeof(char) }));
                            instrs[i].OpCode = OpCodes.Ldc_I4_S;
                            instrs[i].Operand = (sbyte)32; // ' '
                            instrs[i + 1].OpCode = OpCodes.Callvirt;
                            instrs[i + 1].Operand = indexOfMethod;
                            instrs[i + 2].OpCode = OpCodes.Ldc_I4_1;
                            instrs[i + 2].Operand = null;
                            instrs.Insert(i + 3, new Instruction(OpCodes.Add));
                            Console.WriteLine("Patched SaveTape.UpdateLabels time substring logic (space + 1)");
                            break;
                        }
                    }
                }
            }

            // 12. RequestGenerator email strings
            var reqGenType = mod2.GetTypes().FirstOrDefault(x => x.Name == "RequestGenerator");
            if (reqGenType != null)
            {
                foreach (var m in reqGenType.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        if (ins.OpCode == OpCodes.Ldstr && ins.Operand is string s)
                        {
                            if (s == "This is an automated message from the PeepTube system. Please do not reply to this message.")
                            {
                                ins.Operand = "Это автоматическое сообщение системы PeepTube. Пожалуйста, не отвечайте на него.";
                                stringFixes++;
                            }
                            else if (s == "-------------START OF MESSAGE-------------")
                            {
                                ins.Operand = "-------------НАЧАЛО СООБЩЕНИЯ-------------";
                                stringFixes++;
                            }
                            else if (s == "I was wondering if in the next stream you could [color=ffce65]")
                            {
                                ins.Operand = "Не мог(ла) бы ты на следующем стриме [color=ffce65]";
                                stringFixes++;
                            }
                            else if (s == "--------------END OF MESSAGE--------------")
                            {
                                ins.Operand = "--------------КОНЕЦ СООБЩЕНИЯ--------------";
                                stringFixes++;
                            }
                            else if (s == " is willing to send you the following in compensation:")
                            {
                                ins.Operand = " предлагает тебе следующую награду:";
                                stringFixes++;
                            }
                            else if (s == " Viewer score[/color]")
                            {
                                ins.Operand = " к рейтингу зрителей[/color]";
                                stringFixes++;
                            }
                            else if (s == "We hope you consider this request for your next stream.")
                            {
                                ins.Operand = "Надеемся, ты примешь этот заказ к исполнению на следующем стриме.";
                                stringFixes++;
                            }
                            else if (s == "Best,")
                            {
                                ins.Operand = "С наилучшими пожеланиями,";
                                stringFixes++;
                            }
                            else if (s == "STREAM REQUEST")
                            {
                                ins.Operand = "ЗАПРОС НА СТРИМ";
                                stringFixes++;
                            }
                        }
                    }
                }
            }

            // 13. Rating
            var ratingType = mod2.GetTypes().FirstOrDefault(x => x.Name == "Rating");
            if (ratingType != null)
            {
                foreach (var m in ratingType.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        if (ins.OpCode == OpCodes.Ldstr && ins.Operand is string s)
                        {
                            if (s == "served dish!") { ins.Operand = "Блюдо подано!"; stringFixes++; }
                            else if (s == "served ") { ins.Operand = "Подано: "; stringFixes++; }
                            else if (s == " Rating") { ins.Operand = " Рейтинг"; stringFixes++; }
                        }
                    }
                }
            }

            // 14. MailDisplay
            var mailDisplayType = mod2.GetTypes().FirstOrDefault(x => x.Name == "MailDisplay");
            if (mailDisplayType != null)
            {
                foreach (var m in mailDisplayType.Methods)
                {
                    if (!m.HasBody) continue;
                    foreach (var ins in m.Body.Instructions)
                    {
                        if (ins.OpCode == OpCodes.Ldstr && ins.Operand is string s)
                        {
                            if (s == "FROM: ") { ins.Operand = "ОТ: "; stringFixes++; }
                            else if (s == "SUBJECT: ") { ins.Operand = "ТЕМА: "; stringFixes++; }
                        }
                    }
                }
            }

            // 15. Fix MailResource.SaveToDictionary
            var mailResType = mod2.GetTypes().FirstOrDefault(x => x.Name == "MailResource");
            if (mailResType != null)
            {
                var saveMethod = mailResType.Methods.FirstOrDefault(x => x.Name == "SaveToDictionary");
                if (saveMethod != null)
                {
                    var dictCtor = mod2.GetMemberRefs().FirstOrDefault(r => r.DeclaringType.FullName == "Godot.Collections.Dictionary" && r.Name == ".ctor" && r.MethodSig.Params.Count == 0);
                    var dictAdd = mod2.GetMemberRefs().FirstOrDefault(r => r.DeclaringType.FullName == "Godot.Collections.Dictionary" && r.Name == "Add" && r.MethodSig.Params.Count == 2);
                    var strOpImp = mod2.GetMemberRefs().FirstOrDefault(r => r.DeclaringType.FullName == "Godot.StringName" && r.Name == "op_Implicit" && r.MethodSig.Params.Count == 1 && r.MethodSig.Params[0].FullName == "System.String");
                    var varOpImp = mod2.GetMemberRefs().FirstOrDefault(r => r.DeclaringType.FullName == "Godot.Variant" && r.Name == "op_Implicit" && r.MethodSig.Params.Count == 1 && r.MethodSig.Params[0].FullName == "System.String");
                    var godotGet = mod2.GetMemberRefs().FirstOrDefault(r => r.DeclaringType.FullName == "Godot.GodotObject" && r.Name == "Get" && r.MethodSig.Params.Count == 1 && r.MethodSig.Params[0].FullName == "Godot.StringName");

                    if (dictCtor != null && dictAdd != null && strOpImp != null && varOpImp != null && godotGet != null)
                    {
                        var props = new string[]
                        {
                            "Enabled", "From", "Subject", "Body", "IsRead",
                            "SendOnDay", "SentOnDay", "IsRequest", "IsRequestAccepted",
                            "IsRequestRejected", "IsRequestFulfilled", "ExpiresInDays",
                            "InteractionType", "Area", "Cursor", "Person", "Position",
                            "Points", "Score"
                        };

                        var cil = new CilBody();
                        saveMethod.Body = cil;
                        var dictVar = new Local(dictCtor.DeclaringType.ToTypeSig());
                        cil.Variables.Add(dictVar);

                        cil.Instructions.Add(new Instruction(OpCodes.Newobj, dictCtor));
                        cil.Instructions.Add(new Instruction(OpCodes.Stloc, dictVar));

                        foreach (var prop in props)
                        {
                            cil.Instructions.Add(new Instruction(OpCodes.Ldloc, dictVar));
                            cil.Instructions.Add(new Instruction(OpCodes.Ldstr, prop));
                            cil.Instructions.Add(new Instruction(OpCodes.Call, varOpImp));
                            cil.Instructions.Add(new Instruction(OpCodes.Ldarg_0));
                            cil.Instructions.Add(new Instruction(OpCodes.Ldstr, prop));
                            cil.Instructions.Add(new Instruction(OpCodes.Call, strOpImp));
                            cil.Instructions.Add(new Instruction(OpCodes.Callvirt, godotGet));
                            cil.Instructions.Add(new Instruction(OpCodes.Callvirt, dictAdd));
                        }

                        cil.Instructions.Add(new Instruction(OpCodes.Ldloc, dictVar));
                        cil.Instructions.Add(new Instruction(OpCodes.Ret));
                        Console.WriteLine("Rebuilt MailResource.SaveToDictionary with 19 properties");
                    }
                }
            }

            mod2.Write(outPath);
            Console.WriteLine($"fix_all complete: {enumFixes} enum fields, {stringFixes} strings patched.");
            return;
        }
    }
}
