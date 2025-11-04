import math
from tkinter import *
from math import floor
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
IMAGE_PATH = "Day 28/tomato.png"
CHECKMARK = "  ✔️"
reps = 1
is_timer_on = False
timer = None
# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global timer
    global is_timer_on
    global reps
    reps = 1
    window.after_cancel(timer)
    is_timer_on = False
    canvas.itemconfig(timer_text, text="00:00")
    label_timer.config(text="Timer", fg = PINK)
    label_checkmark.config(text="")

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def button_reset_clicked():
    reset_timer()

def button_start_clicked():
    global reps
    global is_timer_on
    if not is_timer_on:
        time = 0
        is_timer_on = True
        if reps <=8:
            if reps%2 != 0:
                label_timer.config(text = "Work", fg=GREEN)
                time = WORK_MIN
            elif reps < 8:
                label_timer.config(text = "Break", fg=PINK)
                time = SHORT_BREAK_MIN
            elif reps == 8:
                label_timer.config(text = "Break", fg=RED)
                time = LONG_BREAK_MIN
            count_down(time*60)
            reps += 1
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    global is_timer_on
    global reps
    global timer
    display_count(count)
    if count > 0:
        timer = window.after(1000, count_down, count-1)
    else:
        is_timer_on = False
        if reps%2==0:
            mark = ""
            for _ in range(int(reps/2)):
                mark += CHECKMARK
            label_checkmark.config(text=mark)
        button_start_clicked()

def display_count(count):
    minutes_left = int(math.floor(count / 60))
    seconds_left = int(count % 60)
    if minutes_left < 10:
        minutes_left = f"0{minutes_left}"
    if seconds_left < 10:
        seconds_left = f"0{seconds_left}"
    canvas.itemconfig(timer_text, text=f"{minutes_left}:{seconds_left}")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro method")
window.config(padx=100, pady=50, bg=YELLOW)
window.resizable(False, False)

tomato_png = PhotoImage(file=IMAGE_PATH)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
canvas.create_image(100, 112, image=tomato_png)
timer_text = canvas.create_text(100, 112, text="00:00", font=(FONT_NAME, 20, "italic"), fill="white")
canvas.grid(column=1,row=1)

label_timer = Label(text="Timer", font=(FONT_NAME, 30, "bold"), bg=YELLOW, fg=PINK)
label_timer.grid(column=1, row=0)

label_checkmark = Label(text="", font=(FONT_NAME, 12, "bold"), bg=YELLOW, fg=GREEN)
label_checkmark.grid(column=1, row=3)

button_start = Button(text="Start", command=button_start_clicked)
button_start.grid(column=0,row=2)

button_reset = Button(text="Reset", command=button_reset_clicked)
button_reset.grid(column=2,row=2)

window.mainloop()