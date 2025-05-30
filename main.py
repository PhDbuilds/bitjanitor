import json
import os
from random import choice, randint, shuffle
from tkinter import *
from tkinter import messagebox
import decrypt_password

import pyperclip
from cryptography.fernet import Fernet

FONT_NAME = "Courier"
GREEN = "#008000"
RED = "#FF0000"

# ---------------------------- GENERATE OR LOAD KEY ------------------------------- #
key_file_path = "encryption_key.key"
# key_file_path =  ".secrets/encryption_key.key"

if os.path.exists(key_file_path):
    with open(key_file_path, "rb") as key_file:
        key = key_file.read()
else:
    key = Fernet.generate_key()
    with open(key_file_path, "wb") as key_file:
        key_file.write(key)

cipher_suite = Fernet(key)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_pw():
    letters = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i",
        "j", "k", "l", "m", "n", "o", "p", "q", "r",
        "s", "t", "u", "v", "w", "x", "y", "z", "A",
        "B", "C", "D", "E", "F", "G", "H", "I", "J",
        "K", "L", "M", "N", "O", "P", "Q", "R", "S",
        "T", "U", "V", "W", "X", "Y", "Z", ]

    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols

    shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    """Save the inputs to a file named data.json"""
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(
            title="Oops", message="Please don't leave any fields empty!"
        )
        return

    encrypted_password = cipher_suite.encrypt(password.encode())
    new_data = {
        website: {
            "email": email,
            "password": encrypted_password.decode(),
        }
    }
    try:
        with open("data.json", "r") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                data = {}
    except FileNotFoundError:
        data = {}

    data.update(new_data)
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

    website_input.delete(0, "end")
    password_input.delete(0, "end")


# ---------------------------- SEARCH SETUP ------------------------------- #


def find_password():
    website = website_input.get()
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
        if website in data:
            website_details = data[website]
            password = decrypt_password.decrypt_password(
                website_details["password"])
            details_message = (
                f"Website: {website}\n"
                f"Email: {website_details['email']}\n"
                f"Password: {password}"
            )
            messagebox.showinfo("Website Details", details_message)
        else:
            messagebox.showerror("Error", f"Website '{website}' not found in the file.")

    except FileNotFoundError:
        messagebox.showerror("Error", "The file was not found.")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Failed to decode JSON from the file.")


# ---------------------------- PWNed SETUP ------------------------------- #


def pwned():
    password = password_input.get()
    with open("pwnedlist.txt") as p:
        if password in p.read():
            password_input.configure(bg=RED)
        else:
            password_input.configure(bg=GREEN)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Assistant Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=500, height=400)
logo_img = PhotoImage(file="images/logo.png")
canvas.create_image(250, 200, image=logo_img)
canvas.grid(column=0, row=0, columnspan=3)

website_label = Label(text="W3bs1te:", font=(FONT_NAME, 20, "normal"))
website_label.grid(column=0, row=1)

website_input = Entry()
website_input.grid(column=1, row=1, columnspan=1)
website_input.configure(width=28)
website_input.focus()

email_label = Label(text="Ema1l/Us3rname3", font=(FONT_NAME, 20, "normal"))
email_label.grid(column=0, row=2)

email_input = Entry()
email_input.grid(column=1, row=2, columnspan=2)
email_input.configure(width=38)
email_input.insert(0, "logan@phdbuilds.tech")

password_label = Label(text="P4ssw0rd:", font=(FONT_NAME, 20, "normal"))
password_label.grid(column=0, row=3)

password_input = Entry()
password_input.grid(column=1, row=3, columnspan=1)
password_input.configure(width=28)

generate_pw_button = Button(text="G3ner4te", command=generate_pw)
generate_pw_button.grid(column=2, row=3)

pwned_button = Button(text="Am I pwn3d?", command=pwned)
pwned_button.grid(column=0, row=4)

add_button = Button(text="N-crypt & S4v3", command=save)
add_button.grid(column=1, row=4, columnspan=2)
add_button.config(width=36)

search_button = Button(text="Se4rch👀", command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
