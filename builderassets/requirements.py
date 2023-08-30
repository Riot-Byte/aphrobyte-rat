import subprocess, threading

installreq_button = None

def func():
    installreq_button.config(text="INSTALLING REQUIREMENTS")
    subprocess.call("pip install -r .buildmodules\\requirements.txt", shell=True)
    installreq_button.config(text="INSTALLED REQUIREMENTS")

def install():
    threading.Thread(target=func, daemon=True).start()