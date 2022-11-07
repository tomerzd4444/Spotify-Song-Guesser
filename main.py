import time
import threading
from pygame import mixer
from tkinter import *
import random
import os

# get current directory
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
#         os.rename(file_path, file_path[len(folder) + 20:])
#         continue
# remember to remove the system of a down from the shame song (this hack doesn't work on it)

# create root and initialize mixer
SECONDS = 5
root = Tk()
root.title('Spotify guessing songs')
root.geometry("1000x800")
mixer.init()

# sets the volume (not sure if it really works)
mixer.music.set_volume(0.05)
buttons = []


def create_guess():
    files = list(os.listdir(folder))  # get all files in directory
    for file in files:
        if '.mp3' not in file:  # if file is not mp3 then discard it
            files.remove(file)
    d = {files.pop(files.index(random.choice(files))): 1}  # choose the correct song while removing it from the list
    for _ in range(3):
        d[files.pop(files.index(random.choice(files)))] = 0  # choose 3 incorrect songs
    return d


def play(song):  # play the song for 5 seconds
    mixer.music.load(song)
    mixer.music.play()
    time.sleep(SECONDS)
    mixer.music.pause()


def threaded_replay():
    t = threading.Thread(target=replay)
    t.start()


def replay():
    mixer.music.rewind()
    mixer.music.play()
    time.sleep(SECONDS)
    mixer.music.pause()


def check(guess, correct):
    #mixer.music.pause()
    global label_wrong
    if guess == correct:
        print('Right!')
        label_right.pack(pady=20)
    else:
        print('Wrong!')
        label_wrong.config(text=f"Wrong! the correct answer was {correct[:-4]}")
        label_wrong.pack(pady=20)
    root.update()  # update the root (show correct/incorrect label)
    for i in buttons:
        i.pack_forget()
    time.sleep(1)
    start()


def start():
    s = create_guess()
    keys = list(s.keys())
    correct = keys[0]
    random.shuffle(keys)
    replay_button.pack(pady=20)
    for key in keys:
        buttons.append(Button(root, text=key[:-4], font=("Helvetica", 32),
                              relief=GROOVE, command=lambda j=key: check(j, correct)))
        buttons[-1].pack(pady=20)
    play_button.pack_forget()
    label_right.pack_forget()
    label_wrong.pack_forget()
    root.update()
    t = threading.Thread(target=play, args=[correct])
    t.start()


# title on the screen you can modify it
title = Label(root, text="Guess The Song!", bd=9, relief=GROOVE,
              font=("times new roman", 50, "bold"), bg="white", fg="green")
title.pack(side=TOP, fill=X)

# making a button which trigger the function so sound can be playeed
play_button = Button(root, text="Start Game", font=("Helvetica", 32),
                     relief=GROOVE, command=start)
play_button.pack(pady=20)

replay_button = Button(root, text="Replay Song", font=("Helvetica", 20),
                     relief=GROOVE, command=threaded_replay)


label_right = Label(root, text="Correct!",
                    font=("times new roman", 32, "bold"))

label_wrong = Label(root, text="Wrong!",
                    font=("times new roman", 32, "bold"))
root.mainloop()
