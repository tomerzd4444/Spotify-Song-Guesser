import time
from pygame import mixer
from tkinter import *
import random
import os

folder = os.getcwd()

# only if songs not download already
# playlist_id = "https://open.spotify.com/playlist/36qgBYI1oOFY46PF8bPDEZ?si=3e0bd06110cc466e"
# os.system(f"spotdl download {playlist_id}")
#
# for filename in os.listdir(folder):
#     file_path = os.path.join(folder, filename)
#     if 'Live' in file_path:
#         os.unlink(file_path)
#         continue
#     if 'System Of A Down - ' in file_path:
#         os.rename(file_path, file_path[len(folder) + 19:])
#         continue

root = Tk()
root.title('Spotify guessing songs')
root.geometry("700x800")
mixer.init()

mixer.music.set_volume(0.05)
buttons = []


def create_guess():
    files = list(os.listdir(folder))
    for file in files:
        if '.mp3' not in file:
            files.remove(file)
    d = {files.pop(files.index(random.choice(files))): 1}
    for _ in range(3):
        d[files.pop(files.index(random.choice(files)))] = 0
    return d


def play(song):
    mixer.music.load(song)
    mixer.music.play()
    time.sleep(5)
    mixer.music.pause()


def check(guess, correct):
    global buttons
    if guess == correct:
        print('Right!')
        label_right.pack(pady=20)
    else:
        print('Wrong!')
        label_wrong.text = f"Wrong! the correct answer was {correct}"
        label_wrong.pack(pady=20)
    root.update()
    for i in buttons:
        i.pack_forget()
    time.sleep(1)
    start()


def start():
    s = create_guess()
    keys = list(s.keys())
    correct = keys[0]
    random.shuffle(keys)
    for key in keys:
        buttons.append(Button(root, text=key[:-4], font=("Helvetica", 32),
                              relief=GROOVE, command=lambda j=key: check(j, correct)))
        buttons[-1].pack(pady=20)
    play_button.pack_forget()
    label_right.pack_forget()
    label_wrong.pack_forget()
    root.update()
    play(correct)


# title on the screen you can modify it
title = Label(root, text="Guess The Song!", bd=9, relief=GROOVE,
              font=("times new roman", 50, "bold"), bg="white", fg="green")
title.pack(side=TOP, fill=X)

# making a button which trigger the function so sound can be playeed
# play_button = Button(root, text="Play Song", font=("Helvetica", 32),
#                      relief=GROOVE, command=play)
play_button = Button(root, text="Start Game", font=("Helvetica", 32),
                     relief=GROOVE, command=start)
play_button.pack(pady=20)

label_right = Label(root, text="Correct!",
                    font=("times new roman", 32, "bold"))

label_wrong = Label(root, text="Wrong!",
                    font=("times new roman", 32, "bold"))
root.mainloop()
