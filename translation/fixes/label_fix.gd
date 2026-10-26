extends Node

const EXACT := {
	"NORMAL": "ОБЫЧНО", "Normal": "Обычно", "normal": "обычно",
	"SLOT": "СЛОТ", "Slot": "Слот", "slot": "слот",
	"LOADING": "ЗАГРУЗКА", "Loading": "Загрузка", "loading": "загрузка",
	"Accept": "Принять", "ACCEPT": "ПРИНЯТЬ",
	"Refuse": "Отклонить", "REFUSE": "ОТКЛОНИТЬ",
	"Empty": "Пусто", "EMPTY": "ПУСТО",
	"YOU'VE BEEN CAUGHT!": "ТЕБЯ ПОЙМАЛИ!",
	"Purchase": "Купить", "PURCHASE": "КУПИТЬ",
	"Purchased": "Куплено", "PURCHASED": "КУПЛЕНО",
	"SUN.": "ВС.", "MON.": "ПН.", "TUE.": "ВТ.", "WED.": "СР.", "THU.": "ЧТ.", "FRI.": "ПТ.", "SAT.": "СБ.",
	"SUN": "ВС", "MON": "ПН", "TUE": "ВТ", "WED": "СР", "THU": "ЧТ", "FRI": "ПТ", "SAT": "СБ",
	"headpat": "поглаживание", "Headpat": "Поглаживание", "HEADPAT": "ПОГЛАЖИВАНИЕ",
	"grab": "схватить", "Grab": "Схватить",
	"kiss": "поцелуй", "Kiss": "Поцелуй",
	"remove": "снять", "Remove": "Снять",
	"shift": "поправить", "Shift": "Поправить",
	"unzip": "расстегнуть", "Unzip": "Расстегнуть",
	"spank_left": "шлёпнуть слева", "spank_right": "шлёпнуть справа",
	"doggystyle": "раком", "missionary": "миссионерская",
	"blowjob": "минет", "handjob": "дрочка",
	"titjob": "секс с грудью", "footjob": "футджоб", "assjob": "секс с попкой",
	"masturbate": "мастурбировать", "penetrate": "проникновение",
	# Kitchen stove & oven controls & heat
	"NONE": "НЕТ", "None": "Нет", "none": "нет",
	"LOW": "НИЗК", "Low": "Низк", "low": "низк",
	"MED": "СРЕД", "Med": "Сред", "med": "сред",
	"HIGH": "ВЫС", "High": "Выс", "high": "выс",
	"ON": "ВКЛ", "On": "Вкл", "on": "вкл",
	"OFF": "ВЫКЛ", "Off": "Выкл", "off": "выкл",
	# Dialog confirmations
	"Confirm": "Подтвердить", "CONFIRM": "ПОДТВЕРДИТЬ", "confirm": "подтвердить",
	"YES": "ДА", "Yes": "Да", "yes": "да",
	"NO": "НЕТ", "No": "Нет", "no": "нет",
	# PeepTube & UI buttons
	"upgrade": "улучшить", "UPGRADE": "УЛУЧШИТЬ", "Upgrade": "Улучшить",
	"cancel": "отмена", "CANCEL": "ОТМЕНА", "Cancel": "Отмена",
	"stream is offline": "стрим оффлайн",
	"recent comments": "последние комментарии",
	"request accepted": "запрос принят",
	"served nothing!": "Ничего не подано!",
	# Strings built in C#
	"shift over!": "Смена окончена!",
	"shift ended early!": "Смена завершена досрочно!",
	"I... can't... move...": "Я... не... могу... двигаться...",
	"Unlocked all cutscenes!": "Все сцены открыты!",
	"in 0 days": "сегодня",
}

const SUB := {
	# Ranks with brackets
	"(REPULSIVE)": "(ОТТАЛКИВАЮЩИЙ)",
	"(PARALYZED)": "(ПАРАЛИЗОВАННЫЙ)",
	"(STUPID)": "(ТУПОЙ)",
	"(UGLY)": "(УРОДЛИВЫЙ)",
	"(PLAIN)": "(ОБЫЧНЫЙ)",
	"(CUTE)": "(МИЛЫЙ)",
	"(BEAUTIFUL)": "(КРАСИВЫЙ)",
	"(HANDSOME)": "(КРАСИВЫЙ)",
	"(IRRESISTIBLE)": "(НЕОТРАЗИМЫЙ)",
	"(FLABBY)": "(ДРЯБЛЫЙ)",
	"(WEAK)": "(СЛАБЫЙ)",
	"(FIT)": "(ПОДТЯНУТЫЙ)",
	"(ATHLETIC)": "(АТЛЕТИЧНЫЙ)",
	"(RIPPED)": "(РЕЛЬЕФНЫЙ)",
	"(DUMB)": "(ГЛУПЫЙ)",
	"(SMART)": "(УМНЫЙ)",
	"(GENIUS)": "(ГЕНИЙ)",

	# Ranks bare caps
	"REPULSIVE": "ОМЕРЗИТЕЛЬНЫЙ",
	"RIZZLORD": "ПОВЕЛИТЕЛЬ РИЗЗА",
	"MAGNETIC": "МАГНЕТИЧЕСКИЙ",
	"CHARMING": "ОБАЯТЕЛЬНЫЙ",
	"STIRRING": "ВОЛНУЮЩИЙ",
	"DULL": "СКУЧНЫЙ",
	"PARALYZED": "ПАРАЛИЗОВАННЫЙ",
	"CLUMSY": "НЕЛОВКИЙ",
	"AVERAGE": "СРЕДНИЙ",
	"GRACEFUL": "ГРАЦИОЗНЫЙ",
	"ACROBATIC": "АКРОБАТИЧЕСКИЙ",
	"NINJA": "НИНДЗЯ",
	"STUPID": "ТУПОЙ",
	"FORGETFUL": "ЗАБЫВЧИВЫЙ",
	"LOGICAL": "ЛОГИЧНЫЙ",
	"ACADEMIC": "АКАДЕМИЧЕСКИЙ",
	"PROFESSOR": "ПРОФЕССОР",
	"SAGE": "МУДРЕЦ",

	# UI & Calendar
	" days remaining.": " дн. осталось.",
	"1 days remaining.": "1 день остался.",
	"DAY#": "ДЕНЬ #",
	"Times Upgraded:": "Улучшено:",
	"Current Bonus:": "Текущий бонус:",
	" secs filmed": " сек. снято",
	" Rating": " Рейтинг",
	"stars": "звёзд",
	"request fulfilled!": "запрос выполнен!",
	"served dish!": "Блюдо подано!",
	"served ": "Подано: ",
	"overcooked": "пережарено",
	"undercooked": "недожарено",
	"Yuna ": "Юна ",
	"Yuna,": "Юна,",
	"Yuna.": "Юна.",
	"Yuna!": "Юна!",
	"Yuna?": "Юна?",
	# Relationship & stat grammar fixes
	"Внимание Юна": "Внимание Юны",
	"внимание юна": "внимание Юны",
	"ВНИМАНИЕ ЮНА": "ВНИМАНИЕ ЮНЫ",
	"Отношения (Юна)": "Отношения с Юной",
	"ОТНОШЕНИЯ (ЮНА)": "ОТНОШЕНИЯ С ЮНОЙ",
	"отношения (юна)": "отношения с Юной",
	"Yuna Attention": "Внимание Юны",
	"Yuna's Attention": "Внимание Юны",
	"Yuna's attention": "внимание Юны",

	# Rent timer
	"in 1 days": "через 1 день",
	"in 1 day": "через 1 день",
	"in 2 days": "через 2 дня",
	"in 3 days": "через 3 дня",
	"in 4 days": "через 4 дня",
	"in 5 days": "через 5 дней",
	"in 6 days": "через 6 дней",
	"in 7 days": "через 7 дней",
	"in 8 days": "через 8 дней",
	"in 9 days": "через 9 дней",
	"in 10 days": "через 10 дней",
	"in 11 days": "через 11 дней",
	"in 12 days": "через 12 дней",
	"in 13 days": "через 13 дней",
	"in 14 days": "через 14 дней",

	# Food buff description (StatusEffects.cs)
	"You ate a hearty meal with extra benefits.": "Ты плотно поел, и это даёт бонусы.",
	"% stamina recovered from sleeping.": "% к восстановлению выносливости во сне.",
	"% pleasure increase during sexual activities.": "% к удовольствию при сексе.",
	"% natural wakefulness decrease during night sequences.": "% к естественному снижению бодрости в ночных сценах.",
	" base damage increase.": " к базовому урону.",
	" stamina limit increase per jog cycle.": " к пределу выносливости за круг пробежки.",

	# Quiz texts that do not fit the dialogue window, and a category name
	"В это время солнечный свет проходит через большую толщу земной атмосферы, что делает его мягче и теплее.": "Свет идёт сквозь толстый слой атмосферы и становится мягче и теплее.",
	"Фотографы часто гоняются за «золотым часом», потому что качество света в это время естественно льстит...": "Фотографы обожают «золотой час»: свет в это время сам по себе льстит...",
	"Кино и Фотография": "Кино и фотография",

	# Upgrade requirements & skill names
	"(Requires: ": "(Требуется: ",
	"(REQUIRES: ": "(ТРЕБУЕТСЯ: ",
	"TACTILE LEARNING": "ТАКТИЛЬНОЕ ОБУЧЕНИЕ",
	"Tactile Learning": "Тактильное обучение",
	"PITY SPEECH": "РЕЧЬ С ЖАЛОСТЬЮ",
	"Pity Speech": "Речь с жалостью",
	"ART OF MOUTH": "ИСКУССТВО ОРАЛА",
	"Art of Mouth": "Искусство орала",
	"DEEP CLEANER": "ГЛУБОКАЯ ОЧИСТКА",
	"Deep Cleaner": "Глубокая очистка",
	"STRANGER DANGER": "ЧУЖАК В ДОМЕ",
	"Stranger Danger": "Чужак в доме",
	"GOLDEN REEL": "ЗОЛОТАЯ КАТУШКА",
	"Golden Reel": "Золотая катушка",
	"POOR LAD": "БЕДНЯК",
	"Poor Lad": "Бедняк",
	"PEACE OF MIND": "ДУШЕВНЫЙ ПОКОЙ",
	"Peace of Mind": "Душевный покой",
	"RELENTLESS": "НЕУМОЛИМЫЙ",
	"Relentless": "Неумолимый",
	"CONVENIENCE STORE": "МАГАЗИНЧИК",
	"Convenience Store": "Магазинчик",
	"LOCK WHISPERER": "ВЗЛОМЩИК",
	"Lock Whisperer": "Взломщик",

	# Request template
	"This is an automated message from the PeepTube system. Please do not reply to this message.": "Это автоматическое сообщение системы PeepTube. Пожалуйста, не отвечайте на него.",
	"-------------START OF MESSAGE-------------": "-------------НАЧАЛО СООБЩЕНИЯ-------------",
	"I was wondering if in the next stream you could": "Не мог бы ты на следующем стриме",
	"--------------END OF MESSAGE--------------": "--------------КОНЕЦ СООБЩЕНИЯ--------------",
	"is willing to send you the following in compensation:": "готов(а) перевести тебе следующую награду в качестве компенсации:",
	"Viewer score": "к рейтингу зрителей",
	"We hope you consider this request for your next stream.": "Надеемся, ты примешь этот заказ к исполнению на следующем стриме.",

	# Erotic touch requests
	"grope her ass": "потискать её за попку",
	"grope her chest": "пощупать её за грудь",
	"finger her from the front": "поласкать пальчиками спереди",
	"finger her from the back": "поласкать пальчиками сзади",
	"pat her head from the front": "погладить её по головке спереди",
	"pat her head from the back": "погладить её по головке сзади",
	"hold her hands": "подержать её за ручки",
	"pinch her left nipple": "ущипнуть её за левый сосочек",
	"grab her thighs": "схватить её за бёдра",
	"pinch her right nipple": "ущипнуть её за правый сосочек",
	"eat her ass": "вылизать её попку",
	"lick her back": "полизать ей спинку",
	"lick her belly button": "полизать ей пупок",
	"eat her out from the front": "сладко вылизать её киску спереди",
	"eat her out from the back": "вылизать её сочную киску сзади",
	"lick her left clavicle": "полизать её левую ключицу",
	"lick her left foot": "полизать её левую стопу",
	"suck her left nipple": "пососать её левый сосочек",
	"lick her left thigh": "полизать её левое бедро",
	"make out with her": "страстно засосать её в губы",
	"lick her right clavicle": "полизать её правую ключицу",
	"suck her right nipple": "пососать её правый сосочек",
	"lick her right foot": "полизать её правую стопу",
	"lick her right thigh": "полизать её правое бедро",
	"perform an assjob": "трахнуть её между аппетитных булок",
	"insert it anally": "войти ей в тугую попку",
	"perform a titjob": "потрахать её прямо между сисек",
	"insert it missionary-style": "трахнуть её в миссионерской позе",
	"insert it doggy-style": "смачно засадить ей раком",
	"perform a footjob": "подрочить о её гладкие ножки",
	"perform a blowjob": "дать ей глубоко взять в рот",
	"finish in assjob position": "кончить прямо между её ягодиц",
	"finish in her ass": "смачно залить спермой её тугую попку",
	"finish on her chest": "облить тёплой спермой её пышную грудь",
	"finish in her missionary-style": "глубоко кончить в неё в миссионерской позе",
	"finish in her doggy-style": "залить её киску спермой раком",
	"finish on her face": "красиво спустить прямо ей на личико",
	"finish using her feet": "кончить ей на пальчики ножек",
	"finish using her mouth": "щедро кончить ей прямо в ротик",
	"finish over her panties": "кончить прямо поверх её мокрых трусиков",
	"finish over her vagina": "обильно кончить на её сочную щёлочку",
	"headpat": "поглаживание",
	"Headpat": "Поглаживание",
	"HEADPAT": "ПОГЛАЖИВАНИЕ",
	"spank_left": "шлёпнуть слева",
	"spank_right": "шлёпнуть справа",
	"doggystyle": "раком",
	"missionary": "миссионерская",
	"blowjob": "минет",
	"handjob": "дрочка",
	"titjob": "секс с грудью",
	"footjob": "футджоб",
	"assjob": "секс с попкой",
	"masturbate": "мастурбировать",
	"penetrate": "проникновение",
	# Enemies
	"Deep-sea Diver": "Глубоководник",
	"Buff Bro": "Качок-братан",
	"Corrupt Cop": "Продажный коп",
	"Cranky Cop": "Ворчливый коп",
	"Healing Hamster": "Целебный хомяк",
	"Iron Maiden": "Железная дева",
	"Lumberjane": "Лесорубка",
	"Mad Science Student": "Студент безумной науки",
	"Menacing Hobo": "Зловещий бродяга",
	"Perverted Doctor": "Извращённый доктор",
	"Sexy Psycho": "Секс-психопатка",
	"Silent Hunter": "Тихий охотник",
	"Slime Queen": "Королева слизи",
	"Unholy Nun": "Нечестивая монашка",
	"Wandering Ronin": "Странствующий ронин",
	"Assimilator": "Ассимилятор",
	# Battle text fragments
	" hit you!": " наносит тебе удар!",
	" attacks again!": " атакует снова!",
	" attempts to ": " пытается ",
	" you!": " тебя!",
	" successfully ": " успешно ",
	" healed themselves!": " исцелил(а) себя!",
	" is now Stunned!": " теперь оглушён(а)!",
	" was empowered!": " усиливается!",
	"Charmed": "очаровал",
	"Charm": "очаровать",
	"Enraged": "разъярил",
	"Enrage": "разъярить",
	"Frightened": "напугал",
	"Frighten": "напугать",
}

const DAY_PREFIXES := {
	"SUN.": "ВС.",
	"MON.": "ПН.",
	"TUE.": "ВТ.",
	"WED.": "СР.",
	"THU.": "ЧТ.",
	"FRI.": "ПТ.",
	"SAT.": "СБ.",
}

var _t := 0.0
var _vt := 0.0
var _rx_rules: Array = []

func _build_rx() -> void:
	for r in [
		[r"(\d)\s*secs", "$1 сек."],
		[r"(\d)\s*Points", "$1 очк."],
		[r"(\+\d+)s$", "$1 с"],
		[r"^(\d\d:\d\d) [AP]M$", "$1"],
	]:
		var rx := RegEx.new()
		if rx.compile(r[0]) == OK:
			_rx_rules.append([rx, r[1]])

func _ready() -> void:
	_build_rx()
	_repair_saves()
	_init_dialogic_vars()
	_init_player_name()
	_disable_key_cheat()

# The AMOGUS cheat is applied from Settings only; GameVariables must not read it from raw key presses.
func _disable_key_cheat() -> void:
	var gv = get_node_or_null("/root/GameVariables")
	if gv != null and gv.is_processing_unhandled_input():
		gv.set_process_unhandled_input(false)

func _init_player_name() -> void:
	var gv = get_node_or_null("/root/GameVariables")
	if gv != null and "player_name" in gv and str(gv.player_name) == "Nita":
		gv.player_name = "Нита"

func _init_dialogic_vars() -> void:
	var dlg = get_node_or_null("/root/Dialogic")
	if dlg != null and "VAR" in dlg and dlg.VAR != null:
		if dlg.VAR.has_method("set_variable"):
			dlg.VAR.set_variable("roommate_name", "Юна")
			dlg.VAR.set_variable("manager_name", "Кан")

func _repair_saves() -> void:
	for i in range(12):
		var path := "user://savegame%d.save" % i
		if not FileAccess.file_exists(path): continue
		var f := FileAccess.open(path, FileAccess.READ)
		if f == null: continue
		var raw := f.get_as_text()
		f.close()
		var data = JSON.parse_string(raw)
		if typeof(data) != TYPE_DICTIONARY: continue
		var changed := false
		if data.has("Предел выносливости") and not data.has("Stamina Limit"):
			data["Stamina Limit"] = data["Предел выносливости"]
			changed = true
		if data.has("Выносливость") and not data.has("Stamina"):
			data["Stamina"] = data["Выносливость"]
			changed = true
		if data.has("Похоть") and not data.has("Lust"):
			data["Lust"] = data["Похоть"]
			changed = true
		if data.has("Подозрение") and not data.has("Suspicion"):
			data["Suspicion"] = data["Подозрение"]
			changed = true

		var lim = float(data.get("Stamina Limit", 0.0))
		var st = float(data.get("Stamina", 0.0))
		if lim > 0.0 and st <= 0.0:
			data["Stamina"] = lim
			changed = true

		if changed:
			var w := FileAccess.open(path, FileAccess.WRITE)
			if w != null:
				w.store_string(JSON.stringify(data))
				w.close()

func _fix_dialogic_vars() -> void:
	var dlg = get_node_or_null("/root/Dialogic")
	if dlg != null and "VAR" in dlg and dlg.VAR != null:
		if dlg.VAR.has_method("get_variable") and dlg.VAR.has_method("set_variable"):
			if dlg.VAR.get_variable("roommate_name") == "Yuna":
				dlg.VAR.set_variable("roommate_name", "Юна")
			if dlg.VAR.get_variable("manager_name") == "Kan":
				dlg.VAR.set_variable("manager_name", "Кан")

func _process(delta: float) -> void:
	_t += delta
	if _t < 0.05: return
	_t = 0.0

	_vt += 0.05
	if _vt >= 1.0:
		_vt = 0.0
		_fix_dialogic_vars()
		_disable_key_cheat()

	var stack := [get_tree().root]
	var n := 0
	while stack.size() > 0 and n < 1500:
		var nd = stack.pop_back()
		n += 1
		if nd is CanvasItem and not nd.visible: continue

		if nd is Label and nd.name == "Name":
			nd.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
			nd.clip_text = false

		if nd is Label and (nd.name == "Label (Left Side)" or nd.name == "Label (Right Side)"):
			nd.clip_text = false

		# Skip Hint tooltip to let C# Hint.SetDescription handle it with zero flicker
		if nd.name == "Label" and nd.get_parent() != null and nd.get_parent().name == "MarginContainer":
			var p2 = nd.get_parent().get_parent()
			if p2 != null and p2.name == "Hint":
				continue

		# Skip choice buttons with battle icons to preserve clean icon display
		if nd is Button and nd.is_in_group("dialogic_choice_button") and nd.icon != null:
			if nd.text != "": nd.text = ""
			continue

		var txt := ""
		if nd is Label: txt = str(nd.text)
		elif nd is RichTextLabel: txt = str(nd.text)
		elif nd is Button: txt = str(nd.text)

		if "{PLAYERNAME}" in txt:
			var pname := ""
			var gv = get_node_or_null("/root/GameVariables")
			if gv != null and "player_name" in gv:
				pname = str(gv.player_name)
			if pname == "" or pname == "{PLAYERNAME}":
				pname = "Нита"
			nd.text = nd.text.replace("{PLAYERNAME}", pname)
			txt = str(nd.text)

		if txt != "":
			var t := txt.strip_edges()
			if EXACT.has(t):
				nd.text = EXACT[t]
			else:
				var nt := txt
				for dp in DAY_PREFIXES.keys():
					if nt.begins_with(dp):
						nt = DAY_PREFIXES[dp] + nt.substr(dp.length())
						break
				for k in SUB.keys():
					if nt.contains(k): nt = nt.replace(k, SUB[k])
				for r in _rx_rules:
					nt = r[0].sub(nt, r[1], true)
				if nt != txt: nd.text = nt

		if nd.get_child_count() > 0:
			for c in nd.get_children(): stack.push_back(c)
