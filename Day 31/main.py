BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
from tkinter import messagebox
import pandas
import random

try:
    records = pandas.DataFrame.to_dict(pandas.read_csv("Day 31/data/words_to_learn.csv"))
except FileNotFoundError:
    records = pandas.DataFrame.to_dict(pandas.read_csv("Day 31/data/it_en.csv"))
italian_words = records["Italian"]
english_words = records["English"]
new_word = {
        "it" : "word",
        "en" : "word"
    }
timer = None
timer_length = 3000
is_italian_on_display = True
new_word_index = 0

def save_words_to_file():
    to_save = pandas.DataFrame(records)
    to_save.to_csv("Day 31/data/words_to_learn.csv", index=False)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit and save words that you have learnt?"):
        save_words_to_file()
        window.destroy()

def new_word_dict():
    global new_word
    global new_word_index
    global records
    global italian_words
    global english_words

    try:
        new_word_index = random.randint(0, len(italian_words) - 1)
        italian = italian_words[new_word_index]
        english = english_words[new_word_index]
    except KeyError:
        new_word_index = random.choice(list(italian_words.keys()))
        italian = italian_words[new_word_index]
        english = english_words[new_word_index]
    except ValueError:
        messagebox.showinfo("Wow!", "You have learnt all popular italian words!\nNext tasks will occur among that you already know.")
        records = pandas.DataFrame.to_dict(pandas.read_csv("Day 31/data/it_en.csv"))
        italian_words = records["Italian"]
        english_words = records["English"]
        new_word_index = random.randint(0, len(italian_words) - 1)
        italian = italian_words[new_word_index]
        english = english_words[new_word_index]

    new_word = {
        "it" : italian,
        "en" : english
    }

def change_card_in_front():
    global timer
    global is_italian_on_display
    new_word_dict()
    canvas.itemconfig(bg_image, image=card_front_image)
    canvas.itemconfig(title, text="Italian", fill="#000000")
    canvas.itemconfig(word, text=new_word["it"], fill="#000000")
    timer = window.after(timer_length, timer_tick)
    is_italian_on_display = True

def wrong_click():
    if not is_italian_on_display:
        change_card_in_front()

def right_click():
    if not is_italian_on_display:
        print(records["Italian"][new_word_index])
        print(records["English"][new_word_index])
        del records["Italian"][new_word_index]
        del records["English"][new_word_index]

        change_card_in_front()

def timer_tick():
    global is_italian_on_display
    global timer
    window.after_cancel(timer)
    canvas.itemconfig(bg_image, image=card_back_image)
    canvas.itemconfig(title, text="English", fill="#FFFFFF")
    canvas.itemconfig(word, text=new_word["en"], fill="#FFFFFF")
    is_italian_on_display = False

window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
window.protocol("WM_DELETE_WINDOW", on_closing)

right_image = PhotoImage(file="Day 31/images/right.png")
wrong_image = PhotoImage(file="Day 31/images/wrong.png")
card_front_image = PhotoImage(file="Day 31/images/card_front.png")
card_back_image = PhotoImage(file="Day 31/images/card_back.png")

right_button = Button(width=100, height=100, highlightthickness=0, image=right_image, command=right_click)
right_button.grid(column=1,row=1)

wrong_button = Button(width=100, height=99, highlightthickness=0, image=wrong_image, command=wrong_click)
wrong_button.grid(column=0, row=1)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
bg_image = canvas.create_image(400, 263, image=card_front_image)
canvas.grid(column=0, row=0, columnspan=2)
title = canvas.create_text(400, 150, text="Italian", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))

change_card_in_front()

window.mainloop()