import mido

training_dir = "./training_data/Aghostofachance.mid"

msg = mido.MidiFile(training_dir, clip=True)
print(msg)

msg.save('new_version.mid')

print("hello world")