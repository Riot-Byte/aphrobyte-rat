import subprocess, threading


def func():
    subprocess.call('PyInstaller --onefile --noconsole --icon=".buildmodules\\exeic.ico" --name="Client-built" .buildmodules\\main.py', shell=True)

def compile():
    threading.Thread(target=func, daemon=True).start()