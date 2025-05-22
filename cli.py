import os
import librosa
import soundfile as sf
from meowifylib.run import meowify_song

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

sample_choices = [
    {"name": "samples/a3.wav", "pitch": librosa.note_to_midi("A3")},
    {"name": "samples/a4.wav", "pitch": librosa.note_to_midi("A4")},
    {"name": "samples/b3.wav", "pitch": librosa.note_to_midi("B3")},
    {"name": "samples/b4.wav", "pitch": librosa.note_to_midi("B4")},
    {"name": "samples/c4.wav", "pitch": librosa.note_to_midi("C4")},
    {"name": "samples/c5.wav", "pitch": librosa.note_to_midi("C5")},
    {"name": "samples/d4.wav", "pitch": librosa.note_to_midi("D4")},
    {"name": "samples/d5.wav", "pitch": librosa.note_to_midi("D5")},
    {"name": "samples/e4.wav", "pitch": librosa.note_to_midi("E4")},
    {"name": "samples/e5.wav", "pitch": librosa.note_to_midi("E5")},
    {"name": "samples/f4.wav", "pitch": librosa.note_to_midi("F4")},
]

# Get the songs
songs = os.listdir("input")
songs = list(set(songs))
song_names = []
for i in range(0, len(songs)):
    if songs[i] != "split":
        song_names.append(songs[i][:-4])

choice = 0

while True:
    print("### Choices: ###")
    for i in range(0, len(song_names)):
        print(i, song_names[i])

    print("\n")

    choice = int(input("Enter choice num or -1 to quit:   "))

    if choice == -1:
        break

    print("\n")

    output = meowify_song("input/" + song_names[choice], sample_choices,
                          "checkpoint/trained.ckpt")

    # Save the final mix and midi
    sf.write(f"output/{song_names[choice]}_gen.wav", output, 22050)
