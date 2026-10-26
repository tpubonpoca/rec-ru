import os, sys
sys.stdout.reconfigure(encoding="utf-8")

fixes = {
    "adventure_checkpoint_level_4.dtl": [
        ("roommate: Я думал, мы застрянем там навсегда!", "roommate: Я думала, мы застрянем там навсегда!"),
    ],
    "adventure_functions.dtl": [
        ("<Фух. Отлично!/Хех. Я ни секунды в тебе не сомневался./Я устал просто смотреть!> #id:12a",
         "<Фух. Отлично!/Хех. Я ни секунды в тебе не сомневалась./Я устала просто смотреть!> #id:12a"),
    ],
    "event_relationship_100.dtl": [
        ("roommate: ...Похоже, мы засиделись дольше, чем я думал. #id:e71",
         "roommate: ...Похоже, мы засиделись дольше, чем я думала. #id:e71"),
    ],
    "event_relationship_40.dtl": [
        ("roommate: Я же сказал, это место довольно милое, разве нет? #id:221",
         "roommate: Я же говорила, это место довольно милое, разве нет? #id:221"),
    ],
    "event_relationship_80.dtl": [
        ("protagonist: [font_size=13]...ты уверен, что это хорошая идея?[/font_size] #id:eea",
         "protagonist: [font_size=13]...ты уверена, что это хорошая идея?[/font_size] #id:eea"),
        ("roommate: Хочешь, чтобы я остановился? #id:eeb",
         "roommate: Хочешь, чтобы я остановилась? #id:eeb"),
    ],
    "intro.dtl": [
        ("roommate: Я слышал, тебе пришлось ходить на коррективные занятия. #id:f81",
         "roommate: Я слышала, тебе пришлось ходить на дополнительные занятия. #id:f81"),
        ("roommate: Как бы то ни было, я думал, не помочь ли тебе с учёбой... #id:f84",
         "roommate: Как бы то ни было, я думала, не помочь ли тебе с учёбой... #id:f84"),
    ],
    "morning_jerk.dtl": [
        ("Прежде чем ты успеваешь убрать себя, в комнату входит {roommate_name}.",
         "Не успеваешь ты заправить стояк обратно в трусы, как в комнату входит {roommate_name}."),
        ("roommate: Правда?...", "roommate: Ты что... прямо сейчас?..."),
        ("protagonist: [pause=0.5].[pause=0.5].[pause=0.5].[pause=0.5]да. Это я.",
         "protagonist: [pause=0.5].[pause=0.5].[pause=0.5].[pause=0.5]ну да. Как видишь."),
        ("roommate: Хочешь, чтобы я остановился?", "roommate: Хочешь, чтобы я остановилась?"),
        ("- Держать\n\tjump HANDJOB_SLOW", "- Так же\n\tjump HANDJOB_SLOW"),
        ("roommate: Это хорошо?", "roommate: Так приятно?"),
        ("roommate: Это было... весьма.", "roommate: Ого... сколько выплеснулось."),
    ],
    "morning_shower.dtl": [
        ("roommate: Ладно, кажется, я понял, что ты имеешь в виду. #id:5ba",
         "roommate: Ладно, кажется, я поняла, о чём ты. #id:5ba"),
        ("protagonist: Да, ты прав. #id:5bd", "protagonist: Да, ты права. #id:5bd"),
        ("roommate: Ого... уже так тяжело, да? #id:5bf", "roommate: Ого... уже такой твёрдый, да? #id:5bf"),
        ("roommate: Наверное, так мыться проще. #id:5c0", "roommate: Ну, так мне будет даже проще. #id:5c0"),
        ("manager: Извини... ты прав. #id:5d2", "manager: Извини... ты права. #id:5d2"),
        ("roommate: Я думал, он никогда не уйдёт. #id:5d5", "roommate: Я думала, он никогда не уйдёт. #id:5d5"),
        ("roommate: Я сказал, что выйду через... несколько минут... #id:630",
         "roommate: Я же сказала, что выйду через... пару минут... #id:630"),
    ],
    "morning_study.dtl": [
        ("roommate: Кажется, теперь я понял. #id:4b0", "roommate: Кажется, теперь я поняла. #id:4b0"),
        ("- Держать\n\tjump SLOW", "- Так же\n\tjump SLOW"),
    ],
    "party_event_evening_strip_games.dtl": [
        ("friend: Я думал, мы подшучиваем над {roommate_name}? #id:fd3",
         "friend: Я думала, мы подшучиваем над {roommate_name}? #id:fd3"),
        ("roommate: Я видел достаточно. #id:7d5", "roommate: Я видела достаточно. #id:7d5"),
    ],
    "adventure_checkpoint_level_1.dtl": [
        ("protagonist: Ты уверен насчёт этого места? #id:1038",
         "protagonist: Ты уверена насчёт этого места? #id:1038"),
        ("- Держать #id:1047", "- Так же #id:1047"),
        ("roommate: Рад, что тебе понравилось... #id:f20",
         "roommate: Рада, что тебе понравилось... #id:f20"),
    ],
    "adventure_checkpoint_level_2.dtl": [
        ("- Держать #id:1069", "- Так же #id:1069"),
    ],
    "adventure_sex.dtl": [
        ("- Держать\n\tjump PSYCHO_SLOW", "- Так же\n\tjump PSYCHO_SLOW"),
    ],
    "night_living_room.dtl": [
        ("- Чат #id:d16", "- Поболтать #id:d16"),
    ],
    "party_event_afternoon_punch.dtl": [
        ("roommate: Это так... красное. #id:71d", "roommate: Он такой... красный. #id:71d"),
        ("- Анализировать удар #id:723", "- Проанализировать пунш #id:723"),
    ],
    "passout.dtl": [
        ("[color=e5be3e]{GameVariables.get_credit_loss()} Credits lost.[/color]",
         "[color=e5be3e]Потеряно {GameVariables.get_credit_loss()} кредитов.[/color]"),
        ("roommate: Мне пришлось самому тащить тебя сюда наверх. #id:bc2",
         "roommate: Мне пришлось самой тащить тебя сюда наверх. #id:bc2"),
    ],
    "morning_mini_avoidkan.dtl": [
        ("[color=e5be3e]Stamina[/color] lost. #id:3d1",
         "[color=e5be3e]Потеряна выносливость.[/color] #id:3d1"),
    ],
    "morning_nut.dtl": [
        ("[color=e5be3e]Тебе приснился мокрый сон![/color]",
         "[color=e5be3e]У тебя случилась ночная поллюция![/color]"),
    ],
    "event_rewind.dtl": [
        ("[color=e5be3e]Have fun![/color] #id:2df",
         "[color=e5be3e]Приятного отдыха![/color] #id:2df"),
    ],
    "stat_change.dtl": [
        ("[color=ff934d]{GameVariables.get_xp_gain()} Charisma XP Gained![/color] #id:1002",
         "[color=ff934d]Получено {GameVariables.get_xp_gain()} опыта Харизмы![/color] #id:1002"),
        ("[color=ff934d]{GameVariables.get_study_gains()} Charisma XP Gained![/color] #id:1004",
         "[color=ff934d]Получено {GameVariables.get_study_gains()} опыта Харизмы![/color] #id:1004"),
        ("[color=1cd5ff]{GameVariables.get_xp_gain()} Dexterity XP Gained![/color] #id:559",
         "[color=1cd5ff]Получено {GameVariables.get_xp_gain()} опыта Ловкости![/color] #id:559"),
        ("[color=1cd5ff]{GameVariables.get_study_gains()} Dexterity XP Gained![/color] #id:1006",
         "[color=1cd5ff]Получено {GameVariables.get_study_gains()} опыта Ловкости![/color] #id:1006"),
        ("[color=d3ff75]{GameVariables.get_xp_gain()} Intelligence XP Gained![/color] #id:55d",
         "[color=d3ff75]Получено {GameVariables.get_xp_gain()} опыта Интеллекта![/color] #id:55d"),
        ("[color=d3ff75]{GameVariables.get_study_gains()} Intelligence XP Gained![/color] #id:1008",
         "[color=d3ff75]Получено {GameVariables.get_study_gains()} опыта Интеллекта![/color] #id:1008"),
        ("[color=e5be3e]Lust[/color] Increased!",
         "[color=e5be3e]Похоть выросла![/color]"),
        ("[color=e5be3e]Lust[/color] Decreased!",
         "[color=e5be3e]Похоть снизилась![/color]"),
        ("[color=ff3f49]{GameVariables.decrease_relationship()} Relationship XP lost.[/color] #id:ba3",
         "[color=ff3f49]Потеряно {GameVariables.decrease_relationship()} опыта отношений.[/color] #id:ba3"),
        ("[color=e5be3e]{GameVariables.increase_relationship()} Relationship XP gained.[/color] #id:ba4",
         "[color=e5be3e]Получено {GameVariables.increase_relationship()} опыта отношений.[/color] #id:ba4"),
        ("[color=e5be3e]{GameVariables.increase_relationship_dog()} Relationship XP gained.[/color]",
         "[color=e5be3e]Получено {GameVariables.increase_relationship_dog()} опыта дружбы с Псом.[/color]"),
    ]
}

root = r"C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res\dialogue\timelines"

for fname, pairs in fixes.items():
    p = os.path.join(root, fname)
    raw = open(p, "rb").read()
    txt = raw.decode("utf-8").replace("\r\n", "\n")
    changed = 0
    for old, new in pairs:
        if old in txt:
            txt = txt.replace(old, new)
            changed += 1
        else:
            print(f"WARN: could not find in {fname}:\n  {repr(old)}")
    # write back with pure LF
    open(p, "w", encoding="utf-8", newline="\n").write(txt)
    print(f"OK: {fname} ({changed}/{len(pairs)} replaced)")
