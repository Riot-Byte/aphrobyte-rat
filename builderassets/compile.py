import subprocess, threading, os, shutil

build_button = None

def func():
    build_button.config(text="BUILDING")
    subprocess.call('PyInstaller --onefile --noconsole --icon=".buildmodules\\exeic.ico" --name="Client-built" .buildmodules\\main.py', shell=True)
    build_button.config(text="BUILD COMPLETE")
    
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.copy("dist\\Client-built.exe", "Client-built.exe")
        shutil.rmtree("dist")
    if os.path.exists("Client-built.spec"):
        os.remove("Client-built.spec")
    if os.path.exists("builderassets\\__pycache__"):
        shutil.rmtree("builderassets\\__pycache__")

def compile():
    threading.Thread(target=func, daemon=True).start()