import subprocess, threading

def func():
    subprocess.call("pip install -r .buildmodules\\requirements.txt", shell=True)

def install():
    threading.Thread(target=func, daemon=True).start()