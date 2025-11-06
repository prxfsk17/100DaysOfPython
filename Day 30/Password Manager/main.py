import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+']
FONT = ("Times New Roman", 14, "italic")
LOGO_PATH = "Day 30/Password Manager/logo.png"

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
def search_for_website():
    website = website_entry.get()
    if website == "":
        messagebox.showinfo(title="Oops", message="Enter the field 'Website' for search.")
    else:
        try:
            with open("Day 30/Password Manager/password_manager_data.json", "r") as f:
                data = json.load(f)
                login = data[f"{website}"]["login"]
                password = data[f"{website}"]["password"]
        except FileNotFoundError:
            messagebox.showinfo(title="Oops", message="There are no any account data yet.")
        except KeyError:
            messagebox.showinfo(title="Oops", message = f"There is no {website} account data yet.")
        else:
            messagebox.showinfo(title=website, message=f"Login: {login}\nPassword: {password}.")

def save_password():
    website = website_entry.get()
    username = user_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure uou have not left any fields empty")
    else:
        new_data = {
            f"{website}": {
                "login": f"{username}",
                "password": f"{password}",
            },
        }

        try:
            with open("Day 30/Password Manager/password_manager_data.json", "r") as f:
                data = json.load(f)

        except FileNotFoundError:
            f = open("Day 30/Password Manager/password_manager_data.json", "w")
            data = new_data
            f.close()

        else:
            data.update(new_data)

        finally:
            with open("Day 30/Password Manager/password_manager_data.json", "w") as f:
                json.dump(data, f, indent=4)
            website_entry.delete(0, END)
            user_entry.delete(0, END)
            user_entry.insert(0, "username@gmail.com")
            password_entry.delete(0, END)


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

website_entry = Entry(width=34)
website_entry.grid(column=1, row=1)
website_entry.focus()

website_button = Button(text="Search", command=search_for_website, width = 15)
website_button.grid(column=2, row=1)

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