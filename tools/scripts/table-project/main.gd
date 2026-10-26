extends Node

func _ready():
	var f = FileAccess.open("res://keys2.json", FileAccess.READ)
	var data = JSON.parse_string(f.get_as_text())
	for loc in ["en", "ru"]:
		var t = Translation.new()
		t.locale = loc
		for k in data[loc].keys():
			t.add_message(k, data[loc][k])
		var err = ResourceSaver.save(t, "res://gen_%s.translation" % loc)
		print("SAVED ", loc, " ", err, " n=", t.get_message_list().size())
	get_tree().quit()
