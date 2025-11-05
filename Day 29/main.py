from tkinter import *
from tkinter import messagebox
import random
import pyperclip

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+']
FONT = ("Times New Roman", 14, "italic")
LOGO_PATH = "Day 29/logo.png"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    q_let = random.randint(8,10)
    q_num = random.randint(2,4)
    q_sym = random.randint(2,4)

    new_password = []
    for _ in range(q_let):
        new_password.append(random.choice(LETTERS))
    for _ in range(q_num):
        new_password.append(random.choice(NUMBERS))
    for _ in range(q_sym):
        new_password.append(random.choice(SYMBOLS))

    random.shuffle(new_password)
    new_password = "".join(new_password)

    password_entry.delete(0, END)
    password_entry.insert(0, new_password)

    pyperclip.copy(new_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    username = user_entry.get()
    password = password_entry.get()

    if website != "" and username != "" and password != "":
        if messagebox.askyesno(title=website, message=f"These are the details entered \nUsername: {username}\nPassword: {password}\nIs it ok to save?"):

            string_to_save = f"{website} | {username} | {password}\n"
            with open("Day 29/password_manager_data.txt", "a") as f:
                f.write(string_to_save)
                website_entry.delete(0, END)
                user_entry.delete(0, END)
                user_entry.insert(0, "username@gmail.com")
                password_entry.delete(0, END)
    else:
        messagebox.showinfo(title="Warning", message="Please don't leave fields empty!")

# ---------------------------- UI SETUP ------------------------------- #
screen = Tk()
screen.title("Password Manager")
screen.config(padx=50, pady=50)
screen.resizable(False, False)

logo = PhotoImage(file=LOGO_PATH)

# Logo Image
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Website Entry
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

website_entry = Entry(width=53)
website_entry.grid(column=1, row=1, columnspan=2)
website_entry.focus()

# Username Entry
user_label = Label(text="Email/Username:")
user_label.grid(column=0, row=2)

user_entry = Entry(width=53)
user_entry.grid(column=1, row=2, columnspan=2)
user_entry.insert(0, "username@gmail.com")

# Password
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

password_entry = Entry(width=34)
password_entry.grid(column=1, row=3)

password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=2, row=3)

# Add
add_button = Button(text="Add", command=save_password, width=45)
add_button.grid(column=1, row=4, columnspan=2)

screen.mainloop()