extends Node

func _ready():
	var src = ResourceLoader.load("res://imported/Toriko.ttf-9d8a733741cf0a7e03818cd52a1c990b.fontdata")
	var bytes = FileAccess.get_file_as_bytes("res://out/Toriko_cyr2.ttf")
	var f = FontFile.new()
	f.data = bytes
	f.antialiasing = src.antialiasing
	f.multichannel_signed_distance_field = src.multichannel_signed_distance_field
	f.msdf_pixel_range = src.msdf_pixel_range
	f.msdf_size = src.msdf_size
	f.subpixel_positioning = src.subpixel_positioning
	f.oversampling = src.oversampling
	f.hinting = src.hinting
	f.allow_system_fallback = src.allow_system_fallback
	f.force_autohinter = src.force_autohinter
	f.embolden = src.embolden
	f.fixed_size = src.fixed_size
	f.generate_mipmaps = src.generate_mipmaps
	f.transform = src.transform
	var err = ResourceSaver.save(f, "res://out/Toriko_new2.fontdata")
	print("saved err=", err, " cyr=", f.has_char(0x0410))
	get_tree().quit()
