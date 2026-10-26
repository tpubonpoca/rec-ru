import os

content = """extends Node

const EXACT := {
	"NORMAL": "ОБЫЧНО", "Normal": "Обычно", "normal": "обычно",
	"SLOT": "СЛОТ", "Slot": "Слот", "slot": "слот",
	"LOADING": "ЗАГРУЗКА", "Loading": "Загрузка", "loading": "загрузка",
	"Accept": "Принять", "ACCEPT": "ПРИНЯТЬ",
	"Refuse": "Отклонить", "REFUSE": "ОТКЛОНИТЬ",
	"Empty": "Пусто", "EMPTY": "ПУСТО",
	"YOU\\'VE BEEN CAUGHT!": "ТЕБЯ ПОЙМАЛИ!",
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

	# UI Labels
	" days remaining.": " дн. осталось.",
	"1 days remaining.": "1 день остался.",
	"DAY#": "ДЕНЬ #",
	"Times Upgraded:": "Улучшено:",
	"Current Bonus:": "Текущий бонус:",
	" Rating": " Рейтинг",
	"stars": "звёзд",
	"request fulfilled!": "запрос выполнен!",

	# Rent timer
	"in 1 days": "через 1 день",
	"in 1 day": "через 1 день",
	"in 2 days": "через 2 дня",
	"in 3 days": "через 3 дня",
	"in 4 days": "через 4 дня",
	"in 5 days": "через 5 дней",
	"in 6 days": "через 6 дней",
	"in 7 days": "через 7 дней",

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
}

var _t := 0.0

func _ready() -> void:
	_repair_saves()

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
		var lim = float(data.get("Stamina Limit", 0.0))
		var st = float(data.get("Stamina", 0.0))
		if lim > 0.0 and st <= 0.0:
			data["Stamina"] = lim
			var w := FileAccess.open(path, FileAccess.WRITE)
			if w != null:
				w.store_string(JSON.stringify(data))
				w.close()

func _process(delta: float) -> void:
	_t += delta
	if _t < 0.25: return
	_t = 0.0
	var stack := [get_tree().root]
	var n := 0
	while stack.size() > 0 and n < 1500:
		var nd = stack.pop_back()
		n += 1
		if nd is CanvasItem and not nd.visible: continue
		var txt := ""
		if nd is Label: txt = str(nd.text)
		elif nd is RichTextLabel: txt = str(nd.text)
		elif nd is Button: txt = str(nd.text)
		if txt != "":
			var t := txt.strip_edges()
			if EXACT.has(t):
				nd.text = EXACT[t]
			else:
				var nt := txt
				for k in SUB.keys():
					if nt.contains(k): nt = nt.replace(k, SUB[k])
				if nt != txt: nd.text = nt
		if nd.get_child_count() > 0:
			for c in nd.get_children(): stack.push_back(c)
"""

p = r"C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res\label_fix.gd"
open(p, "w", encoding="utf-8", newline="\n").write(content)
print("label_fix.gd updated successfully!")
