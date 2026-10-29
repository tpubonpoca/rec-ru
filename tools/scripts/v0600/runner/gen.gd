extends Node

func _ready():
	var args = OS.get_cmdline_user_args()
	var job = args[0]
	if job == "dump":
		_dump(args[1], args[2], args[3])
	elif job == "expr":
		_expr(args[1])
	elif job == "make":
		_make(args[1], args[2], args[3])
	get_tree().quit()

func _dump(tables_dir, keys_file, out_file):
	var keys = JSON.parse_string(FileAccess.get_file_as_string(keys_file))
	var res = {}
	for f in DirAccess.get_files_at(tables_dir):
		if not f.ends_with(".translation"):
			continue
		var t = ResourceLoader.load(tables_dir + "/" + f)
		var d = {"class": t.get_class(), "locale": t.locale, "values": t.get_translated_message_list(), "found": {}}
		for k in keys:
			for ctx in ["", "Label", "Button", "Checkbox", "LineEdit", "LinkButton", "Time"]:
				var m = t.get_message(k, ctx)
				if m != StringName("") and String(m) != k:
					d["found"][k + "|" + ctx] = String(m)
		res[f] = d
	var fa = FileAccess.open(out_file, FileAccess.WRITE)
	fa.store_string(JSON.stringify(res, " "))
	fa.close()
	print("dump ok ", Engine.get_version_info().string)

func _make(in_json, locale, out_file):
	var rows = JSON.parse_string(FileAccess.get_file_as_string(in_json))
	var t = Translation.new()
	t.locale = locale
	for r in rows:
		t.add_message(r[0], r[2], r[1])
	var err = ResourceSaver.save(t, out_file)
	print("make ", err, " ", rows.size())

func _expr(table):
	TranslationServer.add_translation(ResourceLoader.load(table))
	TranslationServer.set_locale("ru")
	var holder = Node.new()
	holder.name = "GameVariables"
	holder.set_meta("x", 1)
	var e := Expression.new()
	print("parse ", e.parse("tr(\"Candy\") + \"|\" + tr(GameVariables.name)", ["GameVariables"]))
	print("result ", e.execute([holder], self), " failed ", e.has_execute_failed(), " ", e.get_error_text())
