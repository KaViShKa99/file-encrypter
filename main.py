import base64
import tkinter as tk
from tkinter import END, ttk
from tkinter import filedialog
import os
from tkinter import messagebox
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

file_path = ""
derectory_path = ""
last_file = ""
encryptPassword = ""


# Create the main window

root = tk.Tk()
root.title("File Encryption")

root.resizable(0, 0)

root.attributes('-fullscreen', False)


# add the styles
style = ttk.Style()

xscrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL)

style.configure("Encrypt.TButton",
                background="green",
                foreground="black",
                font=("Helvetica", 12),
                borderwidth=0,
                anchor="center",
                relief="solid")

style.configure("Decrypt.TButton",
                background="red",
                foreground="black",
                font=("Helvetica", 12),
                borderwidth=0,
                anchor="center",
                relief="solid")
# Create a tabbed interface
tab_control = ttk.Notebook(root)

# Create the tabs for encrypted and decrypted files
encrypted_tab = ttk.Frame(tab_control)
decrypted_tab = ttk.Frame(tab_control)
about_tab = ttk.Frame(tab_control)

# Add the tabs to the tab control
tab_control.add(encrypted_tab, text="Encrypted File")
tab_control.add(decrypted_tab, text="Decrypted File")
tab_control.add(about_tab, text="About")

# about file tab
title_lable = tk.Label(about_tab, text="File Encryption App",font=("Arial", 10, "bold"))
title_lable.grid(column=0, row=0, padx=20, pady=10)
version_lable = tk.Label(about_tab, text="Version 1.0")
version_lable.grid(column=0, row=1, padx=20, pady=10)
description_lable = tk.Label(about_tab, text="This application allows you to encrypt your files with a password.")
description_lable.grid(column=0, row=2, padx=40, pady=10)
developer_lable = tk.Label(about_tab, text="Developed by kavishka Ganewattha")
developer_lable.grid(column=0, row=3, padx=20, pady=10)

# encrypted file tab
encrypted_label = tk.Label(encrypted_tab, text="Choose a file to encrypt:")
encrypted_label.grid(column=0, row=0, padx=10, pady=10)


def on_tab_change(event):
    global file_path,last_file,derectory_path
    file_path = ""
    derectory_path = ""
    last_file = ""
    encrypted_entry.delete(0, END)
    Decrypted_entry.delete(0, END)
    selected_file.config(text=" None ")
    selected_file2.config(text=" None ")
   
def createFernetObj(key):

    password_bytes = key.encode()

    salt = b'secretpwd'
    iterations = 100000

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )

    encoded_key = kdf.derive(password_bytes)
    key_b64 = base64.urlsafe_b64encode(encoded_key)
    return key_b64

def choose_file():
    global file_path,last_file,derectory_path
    file_path = filedialog.askopenfilename()
    last_file = os.path.basename(file_path)
    derectory_path = os.path.dirname(file_path)

    tab_index = tab_control.index(tab_control.select())
    tab_text = tab_control.tab(tab_index, "text")
 

    if last_file != "" and tab_text == "Encrypted File" :
        selected_file.config(text=last_file)
    if last_file != "" and tab_text == "Decrypted File" :
        selected_file2.config(text=last_file)

# Function to handle the "Encrypted" button
def encrypted():
 
    try :
        fernet = Fernet(createFernetObj(encrypted_entry.get()))

        with open(f'{file_path}', 'rb') as file:
            original = file.read()

        encrypted = fernet.encrypt(original)

        with open(f'{derectory_path}/encrypted_{last_file}', 'wb') as file:
            file.write(encrypted)
        messagebox.showinfo("Encryption Result ","Encryption Complete")    
    except:
        messagebox.showinfo("Encryption Result", "Encryption Not Successfully, Tryagain !!!!!!")

    encrypted_entry.delete(0, END)
    selected_file.config(text=" None ")

# Function to handle the "Decrypted" button 
def Decrypted():

    try:
        with open(f'{file_path}', 'rb') as file:
            encrypted = file.read()
        fernet = Fernet(createFernetObj(Decrypted_entry.get()))
        decrypted = fernet.decrypt(encrypted)

        with open(f'{derectory_path}/decrypted_{last_file}', 'wb') as file:
            file.write(decrypted)
        messagebox.showinfo("Decryption Result ","Decryption Complete")
    except :
        messagebox.showinfo("Decryption Result", "Decryption Not Successfully, Tryagain !!!!!!")
    
    Decrypted_entry.delete(0, END)
    
tab_control.bind("<<NotebookTabChanged>>", on_tab_change)

file_button = tk.Button(encrypted_tab, text="Choose File", command=choose_file)
file_button.grid(column=1, row=0, padx=10)


format_label = tk.Label(encrypted_tab, text="Selected File:")
format_label.grid(column=0, row=1, padx=10, pady=10)

selected_file = tk.Label(encrypted_tab, text=" None ")
selected_file.grid(column=1, row=1)

password_label = tk.Label(encrypted_tab, text="Enter a password:")
password_label.grid(column=0, row=2, padx=10, pady=10)

encrypted_entry = tk.Entry(encrypted_tab, show="*")
encrypted_entry.grid(column=1, row=2)


Encrypted_button = ttk.Button(encrypted_tab, text="Encrypted", command=encrypted, style="Encrypt.TButton")
Encrypted_button.grid(column=1, row=3, padx=50, pady=10)


# the decrypted file tab
password_label = tk.Label(decrypted_tab, text="Enter the password:")
password_label.grid(column=0, row=0, padx=10, pady=10)

file_button = tk.Button(decrypted_tab, text="Choose File", command=choose_file)
file_button.grid(column=2, row=0, padx=10,pady=10)

Decrypted_entry = tk.Entry(decrypted_tab, show="*")
Decrypted_entry.grid(column=1, row=0)

format_label = tk.Label(decrypted_tab, text="Selected File:")
format_label.grid(column=0, row=1, padx=10, pady=10)

selected_file2 = tk.Label(decrypted_tab, text=" None ")
selected_file2.grid(column=1, row=1)


Decrypted_button = ttk.Button(decrypted_tab, text="Decrypted", command=Decrypted, style="Decrypt.TButton")
Decrypted_button.grid(column=1, row=3, padx=50, pady=10)

# the main window
tab_control.pack(expand=1, fill="both")

# Start the GUI loop
root.mainloop()
