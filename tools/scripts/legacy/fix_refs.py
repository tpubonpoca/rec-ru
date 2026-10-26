import os, json
root = r'C:\Users\Asyncoder\Downloads\REC_extract\unpacked\res\dialogue\timelines'
tl = {
 'class.dtl': [('res://audio/se/BusArriving.ogg', 'res://audio/se/BusArrival.ogg')],
 'morning_mini_avoidkan.dtl': [('res://audio/se/Movement.wav', 'res://audio/se/Movement.ogg')],
 'sounds.dtl': [('res://audio/se/Scratch.ogg', 'res://audio/se/rustle.ogg')],
 'event_relationship_80.dtl': [('res://audio/voice/ee2_surprise.ogg', 'res://audio/voice/ee2_surprise.wav')],
 'morning_mini_meetfriend.dtl': [('res://audio/voice/hajimemashite2_Pleasure_meeting_you.ogg', 'res://audio/voice/hajimemashite3_Pleasure_meeting_you.mp3')],
}
for f, pairs in tl.items():
    p = os.path.join(root, f)
    t = open(p, encoding='utf-8').read()
    o = t
    for a, b in pairs:
        t = t.replace(a, b)
    if t != o:
        open(p, 'w', encoding='utf-8', newline='').write(t)
        print('fixed', f)
print('done')